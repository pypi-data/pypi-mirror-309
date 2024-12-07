import abc
import warnings
from flair_visual.simulation import schema
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Generic,
    Union,
    Hashable,
    Callable,
    Set,
)
from dataclasses import dataclass as python_dataclass, field as python_field

import numpy as np


CircuitType = TypeVar("CircuitType")
InputType = TypeVar("InputType", bound=Hashable)


@python_dataclass
class CZResults(Generic[CircuitType]):
    storage: CircuitType
    entangled: CircuitType
    single: CircuitType


@python_dataclass(frozen=True)
class OperatorEmitter(Generic[InputType, CircuitType]):

    _callable: Callable[["CircuitConstructorABC", InputType], CircuitType]
    _cache: Dict[InputType, CircuitType] = python_field(default_factory=dict)

    def __call__(
        self, backend: "CircuitConstructorABC", input: InputType
    ) -> CircuitType:
        if input not in self._cache:
            self._cache[input] = self._callable(backend, input)
        return self._cache[input]


@python_dataclass
class CircuitDispatcher(Generic[CircuitType]):
    GATE_TABLE: ClassVar[
        Dict[
            Type[schema.Operation],
            Callable[["CircuitConstructorABC", InputType], CircuitType],
        ]
    ]

    ERROR_TABLE: ClassVar[
        Dict[
            Type[schema.ErrorModel],
            Callable[["CircuitConstructorABC", InputType], CircuitType],
        ]
    ]

    gate_table: Dict[
        Type[schema.Operation], OperatorEmitter[schema.Operation, CircuitType]
    ] = python_field(init=False, default_factory=dict)
    error_table: Dict[
        Type[schema.ErrorModel], OperatorEmitter[schema.ErrorModel, CircuitType]
    ] = python_field(init=False, default_factory=dict)

    def __init_subclass__(cls):
        cls.GATE_TABLE = {}
        cls.ERROR_TABLE = {}

    def __post_init__(self):
        self.gate_table.update(
            {
                gate_type: OperatorEmitter(func)
                for gate_type, func in self.GATE_TABLE.items()
            }
        )
        self.error_table.update(
            {
                error_type: OperatorEmitter(func)
                for error_type, func in self.ERROR_TABLE.items()
            }
        )

    @classmethod
    def register(cls, input_type: Type[InputType]) -> Type[InputType]:
        def _decorator(
            constructor: Callable[[InputType], CircuitType],
        ) -> Type[OperatorEmitter[InputType, CircuitType]]:

            if issubclass(input_type, schema.Operation):
                assert (
                    input_type not in cls.GATE_TABLE
                ), f"{input_type} already registered"
                cls.GATE_TABLE[input_type] = constructor
            elif issubclass(input_type, schema.ErrorModel):
                assert (
                    input_type not in cls.ERROR_TABLE
                ), f"{input_type} already registered"
                cls.ERROR_TABLE[input_type] = constructor
            else:
                raise ValueError(f"Cannot register {input_type}")

            return constructor

        return _decorator


@python_dataclass
class CircuitConstructorABC(Generic[CircuitType], abc.ABC):
    all_qubits: Tuple[int, ...]
    circuit_dispatcher: CircuitDispatcher[CircuitType] = python_field(init=False)
    CIRCUIT_DISPATCHER: ClassVar[CircuitDispatcher[CircuitType]] = None

    def __init_subclass__(cls):
        assert cls.CIRCUIT_DISPATCHER is not None and issubclass(
            cls.CIRCUIT_DISPATCHER, CircuitDispatcher
        ), "CIRCUIT_DISPATCHER must be a CircuitDispatcher"

        for gate_type in schema.Operation.__subclasses__():
            assert (
                gate_type in cls.CIRCUIT_DISPATCHER.GATE_TABLE
            ), f"{gate_type} not registered"

        for error_model_type in schema.ErrorModel.__subclasses__():
            if error_model_type not in cls.CIRCUIT_DISPATCHER.ERROR_TABLE:
                warnings.warn(f"{error_model_type} not registered")

    def __post_init__(self):
        self.circuit_dispatcher = self.CIRCUIT_DISPATCHER()

    def mask_index(self, qubit_id_or_list: Union[int, Sequence[int]]) -> np.ndarray:
        return np.searchsorted(self.all_qubits, qubit_id_or_list)

    def _cz_participation_masks(
        self, participants, active_qubits
    ) -> CZResults[np.ndarray[Any, bool]]:
        non_participants_ids = set(self.all_qubits) - set(sum(participants, ()))
        non_participants_ids = list(non_participants_ids)

        non_participants = self.mask_index(non_participants_ids)

        # get participants that are single qubits or a pair of qubits with at least one inactive qubit
        single_qubit_participants_ids = (
            participant
            for participant in participants
            if len(participant) == 1
            or not active_qubits[participant[0]]
            or not active_qubits[participant[1]]
        )
        # get participants that are pairs of active qubits
        entangled_qubit_participants_ids = (
            participant
            for participant in participants
            if len(participant) == 2
            and active_qubits[participant[0]]
            and active_qubits[participant[1]]
        )

        # flatten the generator
        single_qubit_participants_ids = list(sum(single_qubit_participants_ids, ()))
        entangled_qubit_participants_ids = list(
            sum(entangled_qubit_participants_ids, ())
        )

        single_qubit_participants = self.mask_index(single_qubit_participants_ids)
        entangled_qubit_participants = self.mask_index(entangled_qubit_participants_ids)

        # create a copy of the active qubits
        active_single_qubit = active_qubits.copy()
        active_entangled_qubit = active_qubits.copy()
        active_storage_qubit = active_qubits.copy()
        # remove qubits that are not participating in the CZ gate
        active_entangled_qubit[non_participants] = False
        active_single_qubit[non_participants] = False
        # remove qubits that are in gate zone and are not paired up
        active_entangled_qubit[single_qubit_participants] = False
        # remove qubits that are in active zone and are not paired up
        active_single_qubit[entangled_qubit_participants] = False

        # remove qubits that are not either entangled or single qubit
        active_storage_qubit[single_qubit_participants] = False
        active_storage_qubit[entangled_qubit_participants] = False

        return CZResults(
            active_storage_qubit, active_entangled_qubit, active_single_qubit
        )

    def _apply_cz_loss(
        self,
        no_loss_results: CZResults[CircuitType],
        active_qubits: CZResults[np.ndarray[Any, bool]],
    ) -> CircuitType:

        storage_error = self.remove_lost_qubits(
            no_loss_results.storage, active_qubits.storage
        )
        entangled_error = self.remove_lost_qubits(
            no_loss_results.entangled, active_qubits.entangled
        )
        single_error = self.remove_lost_qubits(
            no_loss_results.single, active_qubits.single
        )

        return self.join([storage_error, entangled_error, single_error])

    @staticmethod
    @abc.abstractmethod
    def join(circuits: List[CircuitType]) -> CircuitType: ...

    @abc.abstractmethod
    def remove_lost_qubits(
        self, circuit: CircuitType, active_qubits: np.ndarray[Any, bool]
    ) -> CircuitType: ...

    @abc.abstractmethod
    def apply_measurement_loss_flips(
        self, operation: schema.Measurement, active_qubits
    ): ...

    def emit_error_model(self, error: schema.ErrorModelType) -> CircuitType:
        return self.circuit_dispatcher.error_table[type(error)](self, error)

    def emit_operation(self, operation: schema.OperationType) -> CircuitType:
        func = self.circuit_dispatcher.gate_table[type(operation)]
        return func(self, operation)

    def emit_error_operation(
        self, error_operation: schema.ErrorOperation[schema.ErrorModelType]
    ) -> Union[CZResults[CircuitType], CircuitType]:
        assert isinstance(
            error_operation, schema.ErrorOperation
        ), f"Cannot emit {type(error_operation)}"

        if isinstance(error_operation, schema.CZError):
            storage = error_operation.storage_error
            entangled = error_operation.entangled_error
            single = error_operation.single_error

            return CZResults(
                storage=self.emit_error_model(storage),
                entangled=self.emit_error_model(entangled),
                single=self.emit_error_model(single),
            )
        elif isinstance(error_operation, schema.SingleQubitError):
            return self.emit_error_model(error_operation.operator_error)
        else:
            raise ValueError(
                f"missing error operation for {type(error_operation).__name__}"
            )

    def emit(
        self, gate_event: schema.GateEvent, active_qubits: np.ndarray[Any, bool]
    ) -> CircuitType:
        operation = self.emit_operation(gate_event.operation)
        error = self.emit_error_operation(gate_event.error)

        if isinstance(gate_event.operation, schema.CZ):
            masks = self._cz_participation_masks(
                gate_event.operation.participants, active_qubits
            )
            return self.join(
                [
                    self._apply_cz_loss(error, masks),
                    self.remove_lost_qubits(operation, active_qubits),
                ]
            )

        elif isinstance(gate_event.operation, schema.Measurement):
            return self.join(
                [
                    self.remove_lost_qubits(error, active_qubits),
                    self.apply_measurement_loss_flips(
                        gate_event.operation, active_qubits
                    ),
                    operation,
                ]
            )

        else:
            return self.join(
                [
                    self.remove_lost_qubits(error, active_qubits),
                    self.remove_lost_qubits(operation, active_qubits),
                ]
            )

    @abc.abstractmethod
    def run(self, circuit: CircuitType, measure_tag: Set[str]) -> Dict[str, str]: ...


BackendType = TypeVar("BackendType", bound=CircuitConstructorABC)


class CircuitBackendRegistry:
    _registry: ClassVar[Dict[str, Type[CircuitConstructorABC[CircuitType]]]] = {}

    @classmethod
    def register(cls, backend: str) -> Callable[[Type[BackendType]], Type[BackendType]]:
        def _decorator(
            backend_type: Type[BackendType],
        ) -> Type[BackendType]:
            assert backend not in cls._registry, f"{backend} already registered"
            assert issubclass(
                backend_type, CircuitConstructorABC
            ), f"{backend_type} is not a CircuitConstructorABC"
            cls._registry[backend] = backend_type
            return backend_type

        return _decorator

    @classmethod
    def get(cls, backend: str) -> Type[CircuitConstructorABC[CircuitType]]:
        if backend not in cls._registry:
            raise ValueError(f"{backend} not registered")

        return cls._registry[backend]
