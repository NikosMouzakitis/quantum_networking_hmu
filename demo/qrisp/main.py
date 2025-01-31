from qrisp import QuantumSession, QuantumCircuit, Qubit, h, cx, measure

# Create a QuantumSession to manage qubits
qs = QuantumSession()

# Allocate qubits for each node
# Bob (central node) has 3 qubits: one for Alice, Charlie, and David
alice_qubit = Qubit(qs, name="alice")
bob_qubit_1 = Qubit(qs, name="bob_1")  # For Alice
bob_qubit_2 = Qubit(qs, name="bob_2")  # For Charlie
bob_qubit_3 = Qubit(qs, name="bob_3")  # For David
charlie_qubit = Qubit(qs, name="charlie")
david_qubit = Qubit(qs, name="david")

# Create a QuantumCircuit
qc = QuantumCircuit(qs)

# Step 1: Create entanglement between Alice and Bob
h(qc, alice_qubit)  # Hadamard gate on Alice's qubit
cx(qc, alice_qubit, bob_qubit_1)  # Entangle Alice and Bob

# Step 2: Create entanglement between Charlie and Bob
h(qc, charlie_qubit)  # Hadamard gate on Charlie's qubit
cx(qc, charlie_qubit, bob_qubit_2)  # Entangle Charlie and Bob

# Step 3: Create entanglement between David and Bob
h(qc, david_qubit)  # Hadamard gate on David's qubit
cx(qc, david_qubit, bob_qubit_3)  # Entangle David and Bob

# Step 4: Perform Bell State Measurement (BSM) at Bob to entangle Alice-Charlie
cx(qc, bob_qubit_1, bob_qubit_2)  # CNOT for BSM
h(qc, bob_qubit_1)  # Hadamard for BSM
measure(qc, bob_qubit_1)  # Measure Bob's qubit for Alice
measure(qc, bob_qubit_2)  # Measure Bob's qubit for Charlie

# Step 5: Perform BSM at Bob to entangle Alice-David
cx(qc, bob_qubit_1, bob_qubit_3)  # CNOT for BSM
h(qc, bob_qubit_1)  # Hadamard for BSM
measure(qc, bob_qubit_1)  # Measure Bob's qubit for Alice
measure(qc, bob_qubit_3)  # Measure Bob's qubit for David

# Step 6: Perform BSM at Bob to entangle Charlie-David
cx(qc, bob_qubit_2, bob_qubit_3)  # CNOT for BSM
h(qc, bob_qubit_2)  # Hadamard for BSM
measure(qc, bob_qubit_2)  # Measure Bob's qubit for Charlie
measure(qc, bob_qubit_3)  # Measure Bob's qubit for David

# Step 7: Measure all peripheral qubits to verify entanglement
measure(qc, alice_qubit)
measure(qc, charlie_qubit)
measure(qc, david_qubit)

# Simulate the circuit
result = qc.run(shots=1024)
print("Measurement results:", result)

# Verify entanglement between nodes
def verify_entanglement(result, node1, node2):
    correlated = 0
    total_shots = 1024
    for outcome in result.keys():
        bits = outcome.split()  # Format: "alice bob_1 bob_2 ..."
        bit1 = int(bits[node1])
        bit2 = int(bits[node2])
        if bit1 == bit2:
            correlated += result[outcome]
    correlation_rate = correlated / total_shots
    print(f"Correlation rate between {node1} and {node2}: {correlation_rate:.4f}")

# Example verification (adjust indices based on measurement order)
verify_entanglement(result, 0, 1)  # Alice-Charlie
verify_entanglement(result, 0, 2)  # Alice-David
verify_entanglement(result, 1, 2)  # Charlie-David
