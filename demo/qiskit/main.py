import json
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

# Initialize IBM Quantum account using your IBMQ token
service = QiskitRuntimeService()

# Define the quantum entanglement swapping circuit
def quantum_entanglement_swapping():
    # Create a quantum circuit with 4 qubits and 2 classical bits
    circuit = QuantumCircuit(4, 2)

    # Step 1: Create Bell state (entanglement) between qubits 0 and 1
    circuit.h(0)
    circuit.cx(0, 1)

    # Step 2: Create Bell state (entanglement) between qubits 2 and 3
    circuit.h(2)
    circuit.cx(2, 3)

    # Step 3: Perform the entanglement swapping
    circuit.cx(1, 2)
    circuit.h(1)
    circuit.measure([1, 2], [0, 1])  # Measure qubits 1 and 2

    # Step 4: Apply corrections to qubit 3 based on the measurement results
    circuit.cx(0, 3)
    circuit.cz(1, 3)

    return circuit

# Generate the quantum circuit
circuit = quantum_entanglement_swapping()

# Visualize the quantum circuit
print("Quantum Circuit for Entanglement Swapping:")
print(circuit)
circuit.draw("mpl")
plt.show()

# Run on a real IBM Quantum computer
try:
    # Get the least busy operational backend (not a simulator)
    backend = service.least_busy(operational=True, simulator=False)

    # Transpile the circuit to match the backend's gate set and topology
    transpiled_circuit = transpile(circuit, backend)

    # Create a sampler instance with the transpiled backend
    sampler = Sampler(backend)
    
    # Submit the job to the backend
    job = sampler.run([transpiled_circuit])
    print(f"Job id: {job.job_id()}")
    
    # Get the results once the job is complete



    result = job.result()

    # Access the raw data from the result (correct way to access it)
    # Navigate through the PrimitiveResult -> SamplerPubResult -> DataBin -> BitArray
    data_bin = result.results[0].data
    counts = data_bin.c

    # Convert BitArray to dictionary-style counts (if needed)
    counts_dict = {}
    for measurement in counts:
        if measurement not in counts_dict:
            counts_dict[measurement] = 0
        counts_dict[measurement] += 1

    # Print the counts
    print("Measurement Counts:")
    print(counts_dict)

    # Save the data as a JSON file
    with open("quantum_result.json", "w") as f:
        json.dump(counts_dict, f)
    print("Data saved to quantum_result.json")

    # Plot the histogram of the results (counts)
    if counts_dict:
        plot_histogram(counts_dict)
        plt.show()




except Exception as e:
    print("Could not execute on IBM Quantum hardware. Error:", e)

