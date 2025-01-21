from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit_aer import Aer
from qiskit import transpile
from qiskit.visualization import plot_state_city
from qiskit.quantum_info import Statevector, DensityMatrix, partial_trace
import matplotlib.pyplot as plt
import numpy as np

qreg_q = QuantumRegister(4, 'q')
creg_c0 = ClassicalRegister(1, 'c0')
creg_c1 = ClassicalRegister(1, 'c1')
creg_c = ClassicalRegister(2, 'c')
circuit = QuantumCircuit(qreg_q, creg_c0, creg_c1, creg_c)

# Your quantum operations
circuit.h(qreg_q[0])  # Create superposition on q[0]
circuit.h(qreg_q[3])  # Create superposition on q[3]

# Apply a CNOT gate between q[0] and q[3] to entangle them
circuit.cx(qreg_q[0], qreg_q[3])

# Measure qubits 0 and 3
circuit.measure(qreg_q[0], creg_c[0])
circuit.measure(qreg_q[3], creg_c[1])

# Simulate the circuit using qasm_simulator
simulator = Aer.get_backend('qasm_simulator')
compiled_circuit = transpile(circuit, simulator)
job = simulator.run(compiled_circuit, shots=1024)
result = job.result()

# Get and print the measurement results
counts = result.get_counts()
print("Measurement Results (Counts):", counts)

# Simulate the circuit using statevector_simulator
statevector_simulator = Aer.get_backend('statevector_simulator')
job_statevector = statevector_simulator.run(circuit)
statevector_result = job_statevector.result()

# Get the statevector
final_state = statevector_result.get_statevector()
print("\nFinal Statevector:")
print(final_state)

# Analyze the reduced density matrix for qubits [0, 3]
density_matrix = DensityMatrix(final_state)
reduced_dm = partial_trace(density_matrix, [1, 2])  # Keep qubits 0 and 3

print("\nReduced Density Matrix (q[0] and q[3]):")
print(reduced_dm)

# Check for entanglement (optional - look for a mixed state)
eigenvalues = np.linalg.eigvals(reduced_dm.data)
print("\nEigenvalues of the Reduced Density Matrix:")
print(eigenvalues)

# Save the circuit diagram for visualization
circuit.draw('mpl')
plt.show()
