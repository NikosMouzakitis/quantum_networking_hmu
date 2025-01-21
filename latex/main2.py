from qiskit_aer import Aer
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, transpile
from qiskit.visualization import plot_state_city
from qiskit.quantum_info import Statevector, DensityMatrix, partial_trace
import matplotlib.pyplot as plt

# Define the quantum circuit
qreg_q = QuantumRegister(4, 'q')
creg_c0 = ClassicalRegister(1, 'c0')
creg_c1 = ClassicalRegister(1, 'c1')
creg_c = ClassicalRegister(2, 'c')
circuit = QuantumCircuit(qreg_q, creg_c0, creg_c1, creg_c)

# Your quantum operations
circuit.h(qreg_q[0])
circuit.h(qreg_q[2])
circuit.cx(qreg_q[0], qreg_q[1])
circuit.cx(qreg_q[2], qreg_q[3])
circuit.cx(qreg_q[1], qreg_q[2])
circuit.h(qreg_q[1])
circuit.measure(qreg_q[2], creg_c1[0])
circuit.measure(qreg_q[1], creg_c0[0])
circuit.x(qreg_q[3]).c_if(creg_c1, 1)
circuit.z(qreg_q[3]).c_if(creg_c0, 1)
circuit.cx(qreg_q[0], qreg_q[3])
circuit.h(qreg_q[0])
circuit.measure(qreg_q[3], creg_c[1])
circuit.measure(qreg_q[0], creg_c[0])


# Simulate the circuit using qasm_simulator
simulator = Aer.get_backend('qasm_simulator')
compiled_circuit = transpile(circuit, simulator)
job = simulator.run(compiled_circuit, shots=1024)
result = job.result()

# Get and print only the values from the 'creg_c' register (q0 and q3)
counts = result.get_counts()
print("Measurement Results (Values of qubits 0 and 3):")
for measurement, count in counts.items():
    # Print only the first and last bit (corresponding to qubits 0 and 3)
    print(f"{measurement[0]}{measurement[3]}: {count}")

# Simulate the circuit using statevector_simulator
statevector_simulator = Aer.get_backend('statevector_simulator')
job_statevector = statevector_simulator.run(circuit)
statevector_result = job_statevector.result()

# Get the statevector
final_state = statevector_result.get_statevector()
print("\nFinal Statevector:")
print(final_state)

# Visualize the statevector
#plot_state_city(final_state)
#plt.show()

# Analyze the reduced density matrix for qubits [0, 3]
density_matrix = DensityMatrix(final_state)
reduced_dm = partial_trace(density_matrix, [1, 2])  # Keep qubits 0 and 3

print("\nReduced Density Matrix (q[0] and q[3]):")
print(reduced_dm)

# Check for entanglement (optional - look for a mixed state)
#eigenvalues = reduced_dm.eigenvalues()
#print("\nEigenvalues of the Reduced Density Matrix:")
#print(eigenvalues)

# Save the circuit diagram for visualization
circuit.draw('mpl')
plt.show()

