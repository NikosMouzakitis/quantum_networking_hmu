from qutip import basis, ket2dm
import numpy as np

# Define basis states of computational basis and Hadamart basis
zero = basis(2, 0)  # |0>
one = basis(2, 1)   # |1>
plus = (zero + one).unit()  # |+>   (normalization of addition to get the plus state)
minus = (zero - one).unit()  # |->

# Alice's qubits
def generate_bb84_states(num_qubits):
    states = []
    bases = []
    for _ in range(num_qubits):
        basis_choice = np.random.choice(['z', 'x'])
        bit = np.random.choice([0, 1])
        if basis_choice == 'z':
            states.append(zero if bit == 0 else one)
        else:
            states.append(plus if bit == 0 else minus)
        bases.append(basis_choice)
    return states, bases

# Measurement
def measure_state(state, basis):
    if basis == 'z':
        projection = [zero, one]
    else:  # 'x'
        projection = [plus, minus]
    probabilities = [abs(proj.overlap(state))**2 for proj in projection]
    return np.random.choice([0, 1], p=probabilities)

# Simulation
num_qubits = 100
alice_states, alice_bases = generate_bb84_states(num_qubits)
bob_bases = np.random.choice(['z', 'x'], num_qubits)

# Measure and compare
bob_results = [measure_state(state, bob_bases[i]) for i, state in enumerate(alice_states)]
matching_bases = [alice_bases[i] == bob_bases[i] for i in range(num_qubits)]
shared_key = [bob_results[i] for i in range(num_qubits) if matching_bases[i]]

# Calculate success rate
success_rate = len(shared_key) / num_qubits
print(f"Key Exchange Success Rate: {success_rate:.2f}")



import matplotlib.pyplot as plt
# Visualization 1: Basis Matching (Bar Chart)
matched = sum(matching_bases)
mismatched = num_qubits - matched

plt.figure(figsize=(8, 6))
plt.bar(['Matched', 'Mismatched'], [matched, mismatched], color=['green', 'red'])
plt.title('Basis Matching in BB84 Protocol')
plt.xlabel('Basis Match')
plt.ylabel('Number of Qubits')
plt.savefig('Basis Matching in BB84 Protocol.png')


# Visualization 2: Success Rate vs. Number of Qubits (Line Chart)
num_qubits_list = [10, 50, 100, 200, 500, 1000, 2000, 3000, 4000, 5000, 8000, 10000]
success_rates = []

for nq in num_qubits_list:
    alice_states, alice_bases = generate_bb84_states(nq)
    bob_bases = np.random.choice(['z', 'x'], nq)
    bob_results = [measure_state(state, bob_bases[i]) for i, state in enumerate(alice_states)]
    matching_bases = [alice_bases[i] == bob_bases[i] for i in range(nq)]
    shared_key = [bob_results[i] for i in range(nq) if matching_bases[i]]
    success_rate = len(shared_key) / nq
    success_rates.append(success_rate)

plt.figure(figsize=(8, 6))
plt.plot(num_qubits_list, success_rates, marker='o', color='b')
plt.title('Success Rate vs. Number of Qubits')
plt.xlabel('Number of Qubits')
plt.ylabel('Success Rate')
plt.grid(True)
plt.savefig("Success Rate vs Number of Qubits.png")

# Visualization 3: Key Distribution (Histogram)
key_bits = [bob_results[i] for i in range(num_qubits) if matching_bases[i]]
plt.figure(figsize=(8, 6))
plt.hist(key_bits, bins=2, color='purple', edgecolor='black', rwidth=0.85)
plt.title('Distribution of Key Bits')
plt.xlabel('Key Bit')
plt.ylabel('Frequency')
plt.xticks([0, 1])
plt.savefig("Distribution of Key Bits.png")

