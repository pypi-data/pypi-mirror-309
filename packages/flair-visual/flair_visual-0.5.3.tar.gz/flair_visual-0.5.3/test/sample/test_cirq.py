from cirq.testing import assert_same_circuits
import math
from flair_visual.simulation.cirq_backend import CirqCircuitConstructor, W
from flair_visual.simulation import constructor, schema
import cirq
import numpy as np
import pytest


def test_cirq_rotation_gate():
    theta = 0.1023901
    phi = 0.123123

    gate_1 = W(theta=theta, phi=phi)
    gate_2 = W(theta=theta, phi=phi)

    assert gate_1 == gate_2

    assert np.array_equal(
        gate_1._unitary_(),
        np.array(
            [
                [
                    np.cos(theta / 2),
                    -1j * np.exp(-1j * phi) * np.sin(theta / 2),
                ],
                [
                    -1j * np.exp(1j * phi) * np.sin(theta / 2),
                    np.cos(theta / 2),
                ],
            ]
        ),
    )


def test_remove_qubits():

    circuit = cirq.Circuit(
        [
            cirq.CNOT(cirq.LineQubit(0), cirq.LineQubit(1)),
            cirq.H(cirq.LineQubit(0)),
        ]
    )
    cons = CirqCircuitConstructor((0, 1))
    result = cons.remove_lost_qubits(circuit, np.array([True, False]))

    expected_circuit = cirq.Circuit(
        [cirq.Moment(), cirq.Moment([cirq.H(cirq.LineQubit(0))])]
    )

    assert_same_circuits(result, expected_circuit)


def test_remove_qubits_2():

    active_qubits = np.array([True, True, False, True])

    circuit = cirq.Circuit(
        [
            cirq.CZ(cirq.LineQubit(0), cirq.LineQubit(1)),
            cirq.CZ(cirq.LineQubit(2), cirq.LineQubit(3)),
        ]
    )

    expected_circuit = cirq.Circuit(
        [
            cirq.CZ(cirq.LineQubit(0), cirq.LineQubit(1)),
        ]
    )

    cons = CirqCircuitConstructor((0, 1, 2, 3))

    result = cons.remove_lost_qubits(circuit, active_qubits)

    assert_same_circuits(result, expected_circuit)


def test_mixing_remove_qubits_3():

    active_qubits = np.array([True, True, True, True])

    circuit = cirq.Circuit(
        [
            cirq.CZ(cirq.LineQubit(0), cirq.LineQubit(1)),
            cirq.CZ(cirq.LineQubit(2), cirq.LineQubit(3)),
        ]
    )

    cons = CirqCircuitConstructor((0, 1, 2, 3))

    result = cons.remove_lost_qubits(circuit, active_qubits)

    assert_same_circuits(result, circuit)


def test_join_circuit():
    circuit1 = cirq.Circuit(
        [cirq.CNOT(cirq.LineQubit(0), cirq.LineQubit(1)), cirq.H(cirq.LineQubit(0))]
    )

    circuit2 = cirq.Circuit(
        [cirq.H(cirq.LineQubit(1)), cirq.CNOT(cirq.LineQubit(1), cirq.LineQubit(2))]
    )

    cons = CirqCircuitConstructor((0, 1, 2, 3))

    result = cons.join([circuit1, circuit2])

    expected_circuit = cirq.Circuit(
        [
            cirq.Moment([cirq.CNOT(cirq.LineQubit(0), cirq.LineQubit(1))]),
            cirq.Moment([cirq.H(cirq.LineQubit(0))]),
            cirq.Moment([cirq.H(cirq.LineQubit(1))]),
            cirq.Moment([cirq.CNOT(cirq.LineQubit(1), cirq.LineQubit(2))]),
        ]
    )

    assert_same_circuits(result, expected_circuit)


def test_clean_cz():
    participants = ((0, 1), (2, 3))
    cz_event = schema.CZ(participants=participants)
    cons = CirqCircuitConstructor(all_qubits=(0, 1, 2, 3))

    expected_circuit = cirq.Circuit(
        [
            cirq.CZ(cirq.LineQubit(0), cirq.LineQubit(1)),
            cirq.CZ(cirq.LineQubit(2), cirq.LineQubit(3)),
        ]
    )

    expected_cz_result = cons.emit_cz(cz_event)
    assert_same_circuits(expected_cz_result, expected_circuit)


def test_clean_global_z_rotation():
    global_z_rot_event = schema.GlobalRz(phi=0.25)
    cons = CirqCircuitConstructor(all_qubits=(0, 1, 2, 3))

    expected_circuit = cirq.Circuit()
    qubits = cirq.LineQubit.range(4)
    op = cirq.Rz(rads=0.25 * math.tau)
    expected_circuit.append(op.on_each(qubits))

    assert_same_circuits(cons.emit_global_rz(global_z_rot_event), expected_circuit)

    active_qubits = np.array([False, True, False, True])

    expected_circuit_loss = cirq.Circuit()

    expected_circuit_loss.append(op.on_each([qubits[1], qubits[3]]))

    generated_circuit_loss = cons.remove_lost_qubits(
        expected_circuit, active_qubits=active_qubits
    )

    assert_same_circuits(
        generated_circuit_loss,
        expected_circuit_loss,
    )


def test_clean_global_rotation():
    global_rot_event = schema.GlobalW(phi=0.25, theta=0.5)

    cons = CirqCircuitConstructor(all_qubits=(0, 1, 2, 3))

    expected_circuit = cirq.Circuit()
    qubits = cirq.LineQubit.range(4)
    op = W(theta=0.5 * math.tau, phi=0.25 * math.tau)
    expected_circuit.append(op.on_each(qubits))

    assert_same_circuits(cons.emit_global_w(global_rot_event), expected_circuit)

    active_qubits = np.array([False, True, False, True])

    expected_circuit_loss = cirq.Circuit()
    expected_circuit_loss.append(op.on_each([qubits[1], qubits[3]]))

    generated_circuit_loss = cons.remove_lost_qubits(
        expected_circuit, active_qubits=active_qubits
    )
    assert_same_circuits(
        generated_circuit_loss,
        expected_circuit_loss,
    )


def test_clean_local_z_rotation():
    local_rot_z_event = schema.LocalRz(
        phi=0.25,
        participants=(1, 3),
    )

    cons = CirqCircuitConstructor(all_qubits=(0, 1, 2, 3))

    expected_circuit = cirq.Circuit()
    qubits = cirq.LineQubit.range(4)

    op = cirq.Rz(rads=0.25 * math.tau)
    expected_circuit.append(op.on_each([qubits[1], qubits[3]]))

    assert_same_circuits(cons.emit_local_rz(local_rot_z_event), expected_circuit)

    active_qubits = np.array([False, True, False, False])

    expected_circuit_loss = cirq.Circuit()
    expected_circuit_loss.append(op.on(qubits[1]))

    generated_circuit_loss = cons.remove_lost_qubits(
        expected_circuit, active_qubits=active_qubits
    )

    assert_same_circuits(generated_circuit_loss, expected_circuit_loss)


def test_clean_local_rotation():
    local_rot_event = schema.LocalW(
        phi=0.43,
        theta=0.123,
        participants=(1, 3),
    )

    cons = CirqCircuitConstructor((0, 1, 2, 3))
    op = W(theta=0.123 * math.tau, phi=0.43 * math.tau)
    expected_circuit = cirq.Circuit()
    qubits = cirq.LineQubit.range(4)
    expected_circuit.append(op.on_each([qubits[1], qubits[3]]))

    assert_same_circuits(cons.emit_local_w(local_rot_event), expected_circuit)

    active_qubits = np.array([False, True, False, False])

    expected_circuit_loss = cirq.Circuit()
    expected_circuit_loss.append(op.on(qubits[1]))

    generated_circuit_loss = cons.remove_lost_qubits(
        expected_circuit, active_qubits=active_qubits
    )

    assert_same_circuits(generated_circuit_loss, expected_circuit_loss)


def test_clean_measurement():
    # only qubits 1 and 3 have measurement applied
    measurement_event = schema.Measurement(participants=(1, 3))

    cons = CirqCircuitConstructor(all_qubits=(0, 1, 2, 3))

    expected_circuit = cirq.Circuit()
    qubits = cirq.LineQubit.range(4)
    expected_circuit.append(cirq.measure([qubits[1], qubits[3]], key="m"))

    assert_same_circuits(cons.emit_measurement(measurement_event), expected_circuit)

    # All qubits have been lost except qubit 1
    active_qubits = np.array([False, True, False, False])

    # loss should happen RIGHT BEFORE the measurement
    ## qubits 0 and 2 are lost but have no measurements applied to them so no flips are applied
    ## qubit 1 has a measurement but no loss so nothing gets generated for it
    ## qubit 3 is lost AND has measurement so loss is applied

    expected_circuit_loss = cirq.Circuit()
    expected_circuit_loss.append(cirq.R(qubits[3]))
    expected_circuit_loss.append(cirq.X(qubits[3]))

    generated_circuit_loss = cons.apply_measurement_loss_flips(
        measurement_event, active_qubits=active_qubits
    )

    assert_same_circuits(
        generated_circuit_loss,
        expected_circuit_loss,
    )


# Test OperatorEmitter
## Create dummy callable, pass in hashable obj.
def test_cache():

    def dummy_func(circuit_constructor, input):
        return 1

    op_emitter = constructor.OperatorEmitter(_callable=dummy_func)
    dummy_backend = CirqCircuitConstructor(all_qubits=(0,))

    op_emitter(dummy_backend, input=2)

    # ensure cache stores the input and the output from the prior call
    assert op_emitter._cache == {2: 1}


def pauli_error_and_circuit():

    pauli_error = schema.PauliErrorModel(
        errors=((0, (0.1, 0.2, 0.3)), (1, (0.4, 0.5, 0.0)), (2, (0, 0, 0)))
    )

    op_0 = cirq.MixedUnitaryChannel(
        zip((0.4, 0.1, 0.2, 0.3), CirqCircuitConstructor.PAULI)
    )
    op_1 = cirq.MixedUnitaryChannel(
        zip((0.1, 0.4, 0.5, 0.0), CirqCircuitConstructor.PAULI)
    )

    expected_result = cirq.Circuit(
        cirq.Moment(
            [
                op_0.on(cirq.LineQubit(0)),
                op_1.on(cirq.LineQubit(1)),
            ]
        )
    )

    cons = CirqCircuitConstructor(all_qubits=(0, 1, 3))

    yield (cons, pauli_error, expected_result)


@pytest.mark.parametrize(
    "cons, pauli_error, expected_result", pauli_error_and_circuit()
)
def test_pauli_error_generation(
    cons: CirqCircuitConstructor,
    pauli_error: schema.PauliErrorModel,
    expected_result: cirq.Circuit,
):
    assert_same_circuits(cons.emit_error_model(pauli_error), expected_result)


@pytest.mark.parametrize(
    "cons, pauli_error, expected_result", pauli_error_and_circuit()
)
def test_error_single_operation_generation(
    cons: CirqCircuitConstructor,
    pauli_error: schema.PauliErrorModel,
    expected_result: cirq.Circuit,
):
    error_operation = schema.SingleQubitError(
        survival_prob=(0.9, 0.8, 0.1), operator_error=pauli_error
    )
    assert_same_circuits(cons.emit_error_operation(error_operation), expected_result)


@pytest.mark.parametrize(
    "cons, pauli_error, expected_result", pauli_error_and_circuit()
)
def test_error_cz_operation_generation(
    cons: CirqCircuitConstructor,
    pauli_error: schema.PauliErrorModel,
    expected_result: cirq.Circuit,
):

    error_operation = schema.CZError(
        survival_prob=(0.9, 0.8, 0.1),
        storage_error=pauli_error,
        single_error=pauli_error,
        entangled_error=pauli_error,
    )

    assert cons.emit_error_operation(error_operation) == constructor.CZResults(
        storage=expected_result, single=expected_result, entangled=expected_result
    )


@pytest.mark.parametrize(
    "cons, pauli_error, expected_result", pauli_error_and_circuit()
)
def test_cz_gate_event(
    cons: CirqCircuitConstructor,
    pauli_error: schema.PauliErrorModel,
    expected_result: cirq.Circuit,
):

    error_operation = schema.CZError(
        survival_prob=(0.9, 0.8, 0.1),
        storage_error=pauli_error,
        single_error=pauli_error,
        entangled_error=pauli_error,
    )
    cz = schema.CZ(participants=((0, 1),))
    active_qubits = np.array([True, False, True])

    cz_circuit = cons.emit_operation(cz)

    cz_errors = cons.emit_error_operation(error_operation)
    cz_active_qubits = cons._cz_participation_masks(cz.participants, active_qubits)

    expected_result = cons.join(
        [
            cons._apply_cz_loss(cz_errors, cz_active_qubits),
            cons.remove_lost_qubits(cz_circuit, active_qubits),
        ]
    )

    gate_event = schema.GateEvent(error=error_operation, operation=cz)

    assert_same_circuits(cons.emit(gate_event, active_qubits), expected_result)


@pytest.mark.parametrize(
    "cons, pauli_error, expected_result", pauli_error_and_circuit()
)
def test_single_qubit_gate_event(
    cons: CirqCircuitConstructor,
    pauli_error: schema.PauliErrorModel,
    expected_result: cirq.Circuit,
):

    error_operation = schema.SingleQubitError(
        survival_prob=(0.9, 0.8, 0.1), operator_error=pauli_error
    )
    gate = schema.LocalRz(participants=(0, 1), phi=0.1)
    active_qubits = np.array([True, False, True])

    circuit = cons.emit_operation(gate)

    errors = cons.emit_error_operation(error_operation)

    expected_result = cons.join(
        [
            cons.remove_lost_qubits(errors, active_qubits),
            cons.remove_lost_qubits(circuit, active_qubits),
        ]
    )

    gate_event = schema.GateEvent(error=error_operation, operation=gate)

    assert_same_circuits(cons.emit(gate_event, active_qubits), expected_result)


@pytest.mark.parametrize(
    "cons, pauli_error, expected_result", pauli_error_and_circuit()
)
def test_measurement_event(
    cons: CirqCircuitConstructor,
    pauli_error: schema.PauliErrorModel,
    expected_result: cirq.Circuit,
):

    error_operation = schema.SingleQubitError(
        survival_prob=(0.9, 0.8, 0.1), operator_error=pauli_error
    )
    gate = schema.Measurement(participants=(0, 1))
    active_qubits = np.array([True, False, True])

    circuit = cons.emit_operation(gate)

    errors = cons.emit_error_operation(error_operation)

    expected_result = cons.join(
        [
            cons.remove_lost_qubits(errors, active_qubits),
            cons.apply_measurement_loss_flips(gate, active_qubits),
            circuit,
        ]
    )

    gate_event = schema.GateEvent(error=error_operation, operation=gate)

    assert_same_circuits(cons.emit(gate_event, active_qubits), expected_result)


def test_cz_participation_and_loss():
    participants = ((0, 1), (2, 3), (4,))
    cirq_noise_model_constructor = CirqCircuitConstructor(all_qubits=(0, 1, 2, 3, 4, 5))
    active_qubits = np.array([True, False, True, True, False, True])

    # check masks
    active_qubits = cirq_noise_model_constructor._cz_participation_masks(
        participants, active_qubits
    )

    assert np.array_equal(
        active_qubits.single, np.array([True, False, False, False, False, False])
    )
    assert np.array_equal(
        active_qubits.entangled, np.array([False, False, True, True, False, False])
    )
    assert np.array_equal(
        active_qubits.storage, np.array([False, False, False, False, False, True])
    )

    random_state = np.random.RandomState(0)

    # check loss
    circuits = constructor.CZResults(
        storage=cirq.testing.random_circuit(6, 2, 0.5, random_state=random_state),
        single=cirq.testing.random_circuit(6, 2, 0.5, random_state=random_state),
        entangled=cirq.testing.random_circuit(6, 2, 0.5, random_state=random_state),
    )

    result = cirq_noise_model_constructor._apply_cz_loss(circuits, active_qubits)

    expected_result = cirq_noise_model_constructor.join(
        [
            cirq_noise_model_constructor.remove_lost_qubits(
                circuits.storage, active_qubits.storage
            ),
            cirq_noise_model_constructor.remove_lost_qubits(
                circuits.entangled, active_qubits.entangled
            ),
            cirq_noise_model_constructor.remove_lost_qubits(
                circuits.single, active_qubits.single
            ),
        ]
    )

    assert_same_circuits(result, expected_result)
