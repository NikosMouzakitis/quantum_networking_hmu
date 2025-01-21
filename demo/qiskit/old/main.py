
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
from qiskit_ibm_runtime import QiskitRuntimeService, Session, Sampler
import matplotlib.pyplot as plt

# Initialize IBM Quantum account
service = QiskitRuntimeService()

print("Successfully connected to IBM Quantum for service.")

# Define a function for quantum teleportation
def quantum_teleportation():
    # Create a quantum circuit with 3 qubits and 2 classical bits
    circuit = QuantumCircuit(3, 2)

    # Step 1: Create a Bell state (entanglement) between qubits 1 and 2
    circuit.h(1)
    circuit.cx(1, 2)

    # Step 2: Prepare the state to teleport on qubit 0 (e.g., |+> state)
    circuit.h(0)

    # Step 3: Bell measurement between qubit 0 and qubit 1
    circuit.cx(0, 1)
    circuit.h(0)
    circuit.measure([0, 1], [0, 1])

    # Step 4: Apply corrections to qubit 2 based on measurement results
    circuit.cx(1, 2)
    circuit.cz(0, 2)

    return circuit

# Generate the circuit
circuit = quantum_teleportation()

# Visualize the quantum circuit
print("Quantum Circuit for Teleportation:")
print(circuit)
circuit.draw("mpl")
plt.show()

# Simulate on a local simulator
simulator = Aer.get_backend('aer_simulator')
compiled_circuit = transpile(circuit, simulator)
result = execute(compiled_circuit, simulator, shots=1024).result()
counts = result.get_counts()

# Visualize the simulation results
print("Simulation Results:", counts)
plot_histogram(counts)
plt.show()

# OPTIONAL: Run on a real IBM Quantum computer
try:
    backend_name = "ibmq_quito"  # Change this to your preferred backend
    with Session(service=service, backend=backend_name) as session:
        sampler = Sampler(session=session)
        job = sampler.run(circuit)
        result = job.result()

    print(f"Results from {backend_name}:")
    print(result)
except Exception as e:
    print("Could not execute on IBM Quantum hardware. Error:", e)

