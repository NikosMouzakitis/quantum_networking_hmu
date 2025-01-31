import numpy as np
from qutip import *
import random

# Step 1: Create entangled state (Bell state)
bell_state = (tensor(basis(2, 0), basis(2, 0)) + tensor(basis(2, 1), basis(2, 1))).unit()  # |00⟩ + |11⟩
bell_state = bell_state / np.sqrt(2)

# Step 2: Define Pauli matrices
X = sigmax()  # Pauli-X (bit-flip)
Z = sigmaz()  # Pauli-Z (phase-flip)

# Step 3: Simulate measurements for Alice and Bob

# Number of rounds of measurement
rounds = 1000

# Lists to store the measurement outcomes
alice_results = []
bob_results = []
common_bases = []  # Stores whether they used the same basis

# Run the simulation for a number of rounds
for _ in range(rounds):
    # Alice and Bob choose random measurement bases (Z or X)
    alice_basis_choice = random.choice([X, Z])
    bob_basis_choice = random.choice([X, Z])
    
    # Alice and Bob measure their respective qubits from the Bell state
    # Correct extraction of Alice's and Bob's qubits
    alice_state = bell_state.ptrace(0)  # Alice's qubit (first qubit)
    bob_state = bell_state.ptrace(1)  # Bob's qubit (second qubit)
    
    # Apply the measurements to the states of Alice and Bob
    alice_result = expect(alice_basis_choice, alice_state)
    bob_result = expect(bob_basis_choice, bob_state)
    
    # Record measurement results (randomly assign 0 or 1 based on the measurement outcome)
    alice_result = 0 if np.random.rand() > 0.5 else 1
    bob_result = 0 if np.random.rand() > 0.5 else 1
    
    # Store results and the basis choice
    alice_results.append(alice_result)
    bob_results.append(bob_result)
    common_bases.append(alice_basis_choice == bob_basis_choice)

# Step 4: Key generation from matching bases
key_alice = []
key_bob = []

for i in range(rounds):
    if common_bases[i]:  # If Alice and Bob used the same basis
        key_alice.append(alice_results[i])
        key_bob.append(bob_results[i])

# Step 5: Output the generated keys
generated_key = np.array(key_alice)

print("Generated Key (Alice):", generated_key)
print("Generated Key (Bob):", np.array(key_bob))
print("Key match: ", np.array_equal(key_alice, key_bob))

# Optionally, compute a simple Bell's inequality check
bell_value = np.abs(np.mean(np.array(alice_results) - np.array(bob_results)))
print("Bell's Inequality Value:", bell_value)

