from pydantic import Field, BaseModel
from typing import Generic, Literal, TypeVar, Union
from typing import List, Tuple


class Operation(BaseModel, frozen=True, extra="forbid"):
    op_type: str = Field(init=False)


class CZ(Operation):
    op_type: Literal["CZ"] = Field(init=False, default="CZ")
    participants: Tuple[Union[Tuple[int], Tuple[int, int]], ...]


class GlobalRz(Operation):
    op_type: Literal["GlobalRz"] = Field(init=False, default="GlobalRz")
    phi: float


class GlobalW(Operation):
    op_type: Literal["GlobalW"] = Field(init=False, default="GlobalW")
    theta: float
    phi: float


class LocalRz(Operation):
    op_type: Literal["LocalRz"] = Field(init=False, default="LocalRz")
    participants: Tuple[int, ...]
    phi: float


class LocalW(Operation):
    op_type: Literal["LocalW"] = Field(init=False, default="LocalW")
    participants: Tuple[int, ...]
    theta: float
    phi: float


class Measurement(Operation):
    op_type: Literal["Measurement"] = Field(init=False, default="Measurement")
    measure_tag: str = Field(default="m")
    participants: Tuple[int, ...]


OperationType = TypeVar(
    "OperationType", bound=Union[CZ, GlobalRz, GlobalW, LocalRz, LocalW, Measurement]
)


class ErrorModel(BaseModel, frozen=True, extra="forbid"):
    error_model_type: str = Field(init=False)


class PauliErrorModel(ErrorModel):
    error_model_type: Literal["PauliNoise"] = Field(default="PauliNoise", init=False)
    errors: Tuple[Tuple[int, Tuple[float, float, float]], ...] = Field(
        default_factory=tuple
    )


ErrorModelType = TypeVar("ErrorModelType", bound=PauliErrorModel)


class ErrorOperation(BaseModel, Generic[ErrorModelType], frozen=True, extra="forbid"):
    error_type: str = Field(init=False)
    survival_prob: Tuple[float, ...]


class CZError(ErrorOperation[ErrorModelType]):
    error_type: Literal["CZError"] = Field(default="CZError", init=False)
    storage_error: ErrorModelType
    entangled_error: ErrorModelType
    single_error: ErrorModelType


class SingleQubitError(ErrorOperation[ErrorModelType]):
    error_type: Literal["SingleQubitError"] = Field(
        default="SingleQubitError", init=False
    )
    operator_error: ErrorModelType


class GateEvent(BaseModel, Generic[ErrorModelType], frozen=True, extra="forbid"):
    error: Union[SingleQubitError[ErrorModelType], CZError[ErrorModelType]] = Field(
        union_mode="left_to_right", discriminator="error_type"
    )
    operation: OperationType = Field(
        union_mode="left_to_right", discriminator="op_type"
    )

    def __pydantic_post_init__(self):
        assert (isinstance(self.operation, CZ) and isinstance(self.error, CZError)) or (
            not isinstance(self.operation, CZ)
            and isinstance(self.error, SingleQubitError)
        ), "Operation and error must be of the same type"


class NoiseModel(BaseModel, Generic[ErrorModelType], extra="forbid"):
    all_qubits: Tuple[int, ...] = Field(default_factory=tuple)
    gate_events: List[GateEvent[ErrorModelType]] = Field(default_factory=list)

    @property
    def num_qubits(self) -> int:
        return len(self.all_qubits)

    def __add__(self, other: "NoiseModel") -> "NoiseModel":
        if not isinstance(other, NoiseModel):
            raise ValueError(f"Cannot add {type(other)} to Circuit")

        if self.all_qubits != other.all_qubits:
            raise ValueError("Circuits must have the same number of qubits")

        return NoiseModel(
            all_qubits=self.all_qubits,
            gate_events=self.gate_events + other.gate_events,
        )

    def get_sampler(self, circuit_backend: str, *args, **kwargs):
        from flair_visual.simulation.sample import AtomLossCircuitSampler
        from flair_visual.simulation.constructor import CircuitBackendRegistry

        backend_type = CircuitBackendRegistry().get(circuit_backend, *args, **kwargs)
        return AtomLossCircuitSampler(
            circuit=self,
            circuit_generator=backend_type(self.all_qubits, *args, **kwargs),
        )
