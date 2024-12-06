from functools import cached_property
import cirq.circuits
from flair_visual.simulation import constructor, schema
from typing import Any, Dict, List, Set, Tuple
import numpy as np
import math
import cirq


@cirq.value_equality
class W(cirq.Gate):
    def __init__(self, theta, phi):
        super(W, self)
        self.theta = theta
        self.phi = phi

    def _value_equality_values_(self):
        return self.theta, self.phi

    def __eq__(self, other):
        return other.theta == self.theta and other.phi == self.phi

    def _num_qubits_(self):
        return 1

    def _unitary_(self):
        return np.array(
            [
                [
                    np.cos(self.theta / 2),
                    -1j * np.exp(-1j * self.phi) * np.sin(self.theta / 2),
                ],
                [
                    -1j * np.exp(1j * self.phi) * np.sin(self.theta / 2),
                    np.cos(self.theta / 2),
                ],
            ]
        )

    def _circuit_diagram_info_(self, args):
        return f"R(θ = {self.theta}, φ = {self.phi})"


class CirqCircuitDispatcher(constructor.CircuitDispatcher[cirq.Circuit]):
    pass


@constructor.CircuitBackendRegistry.register("cirq")
class CirqCircuitConstructor(constructor.CircuitConstructorABC[cirq.Circuit]):

    CIRCUIT_DISPATCHER = CirqCircuitDispatcher
    PAULI = tuple(map(cirq.unitary, [cirq.I, cirq.X, cirq.Y, cirq.Z]))

    @cached_property
    def line_qubits(self) -> Tuple[cirq.LineQubit, ...]:
        return tuple(map(cirq.LineQubit, self.all_qubits))

    def remove_lost_qubits(
        self, circuit: cirq.Circuit, active_qubits: np.ndarray[Any, bool]
    ):
        assert isinstance(
            circuit, cirq.Circuit
        ), f"Circuit must be a cirq.Circuit, got {type(circuit)}"
        if np.all(active_qubits):
            return circuit

        lost_qubits = set(
            cirq.LineQubit(qubit_id)
            for qubit_id, is_active in zip(self.all_qubits, active_qubits)
            if not is_active
        )
        new_moments = []
        for moment in circuit:
            new_moments.append(
                cirq.Moment((op for op in moment if lost_qubits.isdisjoint(op.qubits)))
            )

        return cirq.Circuit(new_moments)

    @staticmethod
    def join(circuits: List[cirq.Circuit]):
        # want to avoid using the `+` operator due to performance degradation
        # so we get the moments out of each circuit and then put them into
        # one bigger circuit
        total_moments = []

        for circuit in circuits:
            total_moments += circuit.moments
        return cirq.Circuit(total_moments)

    def apply_measurement_loss_flips(
        self, operation: schema.Measurement, active_qubits
    ):
        # apply Reset, X, then M for lost qubits
        # the M has already been applied, you just need to prepend the R and X moments
        active_participants = active_qubits[self.mask_index(operation.participants)]
        if np.all(active_participants):
            return cirq.Circuit()

        lost_qubits = [
            cirq.LineQubit(qubit_id)
            for qubit_id, is_active in zip(operation.participants, active_participants)
            if not is_active
        ]

        reset_moment = cirq.Moment(list(map(cirq.reset, lost_qubits)))
        x_gate_moment = cirq.Moment(list(map(cirq.X, lost_qubits)))

        return cirq.Circuit([reset_moment, x_gate_moment])

    def run(self, noise_model: cirq.Circuit, measure_tag: Set[str]) -> Dict[str, str]:
        result = cirq.Simulator().run(noise_model, repetitions=1)

        out = {}
        for tag in measure_tag:
            result_histogram = result.histogram(key=tag)

            result_dict = dict(result_histogram)
            assert len(result_dict) == 1

            ((k, v),) = result_dict.items()
            assert v == 1

            out[tag] = k

        return out

    @CirqCircuitDispatcher.register(schema.CZ)
    def emit_cz(self, operation: schema.CZ):
        cz_gates = [
            cirq.CZ(cirq.LineQubit(pairs[0]), cirq.LineQubit(pairs[1]))
            for pairs in operation.participants
            if len(pairs) == 2
        ]
        return cirq.Circuit(cz_gates)

    @CirqCircuitDispatcher.register(schema.GlobalRz)
    def emit_global_rz(self, operation: schema.GlobalRz):
        rz_gates = [
            cirq.Rz(rads=operation.phi * math.tau)(qubit) for qubit in self.line_qubits
        ]
        return cirq.Circuit(rz_gates)

    @CirqCircuitDispatcher.register(schema.LocalRz)
    def emit_local_rz(self, operation: schema.LocalRz):
        rz_gates = [
            cirq.Rz(rads=operation.phi * math.tau)(cirq.LineQubit(qubit_id))
            for qubit_id in operation.participants
        ]
        return cirq.Circuit(rz_gates)

    @CirqCircuitDispatcher.register(schema.GlobalW)
    def emit_global_w(self, operation: schema.GlobalW):
        rotation_gates = [
            W(operation.theta * math.tau, operation.phi * math.tau)(qubit)
            for qubit in self.line_qubits
        ]
        return cirq.Circuit(rotation_gates)

    @CirqCircuitDispatcher.register(schema.LocalW)
    def emit_local_w(self, operation: schema.LocalW):
        rotation_gates = [
            W(operation.theta * math.tau, operation.phi * math.tau)(
                cirq.LineQubit(qubit_id)
            )
            for qubit_id in operation.participants
        ]
        return cirq.Circuit(rotation_gates)

    @CirqCircuitDispatcher.register(schema.Measurement)
    def emit_measurement(self, operation: schema.Measurement):
        qubits = tuple(map(cirq.LineQubit, sorted(operation.participants)))
        circuit = cirq.Circuit()

        circuit.append(cirq.measure(qubits, key=operation.measure_tag))
        return circuit

    @CirqCircuitDispatcher.register(schema.PauliErrorModel)
    def simple_pauli_channel(self, noise: schema.PauliErrorModel) -> cirq.Circuit:
        ops: Dict[Tuple[float, float, float], List[cirq.LineQubit]] = {}
        for qubit_id, prob in noise.errors:
            if prob == (0, 0, 0):
                continue

            ops.setdefault(prob, []).append(cirq.LineQubit(qubit_id))

        return cirq.Circuit(
            cirq.Moment(
                [
                    cirq.MixedUnitaryChannel(
                        zip([1 - px - py - pz, px, py, pz], self.PAULI)
                    ).on_each(qubits)
                    for (px, py, pz), qubits in ops.items()
                ]
            )
        )
