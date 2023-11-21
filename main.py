from qiskit import QuantumCircuit

for input in {0b00, 0b01, 0b10, 0b11}:
    entangle_circuit = QuantumCircuit(2)
    entangle_circuit.h(0)
    entangle_circuit.cx(0, 1)
    entangle_circuit.barrier(range(2))

    a_circuit = QuantumCircuit(2)
    if input & 0b10 == 0b10:
        a_circuit.z(0)
    if input & 0b01 == 0b01:
        a_circuit.x(0)
    a_circuit.barrier(range(2))

    b_circuit = QuantumCircuit(2, 2)
    b_circuit.cx(0, 1)
    b_circuit.h(0)
    b_circuit.measure(range(2), reversed(range(2)))

    circuit = entangle_circuit.compose(a_circuit).compose(b_circuit)

    from qiskit_aer import AerSimulator
    from qiskit import transpile

    backend = AerSimulator()
    compiled_circuit = transpile(circuit, backend)
    job_simulation = backend.run(compiled_circuit, shots=1024)
    job_result = job_simulation.result()
    counts = job_result.get_counts()

    assert len(counts) == 1
    result = int(next(iter(counts.keys())), base=2)

    print(circuit)
    print(f"input = {(input & 2) >> 1}{input & 1}, result = {(result & 2) >> 1}{result & 1}", '\n')
