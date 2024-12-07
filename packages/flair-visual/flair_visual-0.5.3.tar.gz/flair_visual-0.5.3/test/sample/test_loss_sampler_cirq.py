import cirq
from flair_visual.simulation import schema
import pytest
from .test_noise_model import get_noise_model
import numpy as np


def test_active_qubit_states():

    class DummyGenerator:
        def random(self, size):
            return np.ones(size)

    circuit = get_noise_model()

    sim_obj = circuit.get_sampler("cirq")

    generator = DummyGenerator()

    state = sim_obj.active_qubit_states(generator)

    gate_events = [gate.operation for gate in circuit.gate_events]

    expected_state = np.ones((len(gate_events), len(circuit.all_qubits)), dtype=bool)

    assert np.array_equal(state, expected_state)


def test_clean_circuit():

    circuit = get_noise_model()

    sim_obj = circuit.get_sampler("cirq")

    expected_circuit = cirq.Circuit()

    gate_operations = [gate.operation for gate in circuit.gate_events]

    for i, gate in enumerate(gate_operations):
        expected_circuit.append(sim_obj.circuit_generator.emit_operation(gate))

    assert expected_circuit == sim_obj.clean_circuit


def test_clean_empty_circuit():
    circuit = schema.NoiseModel(all_qubits=(), gate_events=[])

    sim_obj = circuit.get_sampler("cirq")

    assert sim_obj.clean_circuit == cirq.Circuit()
    assert sim_obj.run(10) == {}


def test_incorrect_backend_raises_error():
    circuit = get_noise_model()

    with pytest.raises(ValueError):
        circuit.get_sampler("invalid_backend")
