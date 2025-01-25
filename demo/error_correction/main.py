from qiskit import QuantumCircuit, transpile, QuantumRegister, ClassicalRegister
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator
from matplotlib import pyplot as plt
# Create quantum registers
qr = QuantumRegister(5, 'qubit')  # 3 data qubits, 2 ancilla
cr = ClassicalRegister(2, 'syndrome')  # Stores error information
result_reg = ClassicalRegister(1, 'result')  # Final measurement
qc = QuantumCircuit(qr, cr, result_reg)

# Encode logical state (|1> in this example)
qc.x(qr[0])  # Prepare |1>
qc.cx(qr[0], qr[1])  # Create entanglement
qc.cx(qr[0], qr[2])  # Now |111>

# Introduce artificial error (flip qubit 1)
qc.x(qr[1])  # Comment/uncomment to toggle error

# Syndrome measurement
qc.barrier()
qc.cx(qr[0], qr[3])  # Compare qubit 0 & 1
qc.cx(qr[1], qr[3])
qc.cx(qr[1], qr[4])  # Compare qubit 1 & 2
qc.cx(qr[2], qr[4])

# Measure ancilla qubits
qc.measure(qr[3], cr[0])
qc.measure(qr[4], cr[1])

# Error correction based on syndrome
qc.barrier()
qc.x(qr[0]).c_if(cr, 2)  # 10 -> fix qubit 0
qc.x(qr[1]).c_if(cr, 3)  # 11 -> fix qubit 1
qc.x(qr[2]).c_if(cr, 1)  # 01 -> fix qubit 2

# Final measurement
qc.measure(qr[0], result_reg[0])

# Draw the circuit
qc.draw('mpl', style='iqp')
plt.show()
