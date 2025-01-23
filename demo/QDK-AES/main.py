from qutip import basis, ket2dm
import numpy as np
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

# Define basis states of computational basis and Hadamard basis
zero = basis(2, 0)  # |0>
one = basis(2, 1)   # |1>
plus = (zero + one).unit()  # |+>
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

# Generate shared key
def generate_shared_key(num_qubits):
    alice_states, alice_bases = generate_bb84_states(num_qubits)
    bob_bases = np.random.choice(['z', 'x'], num_qubits)

    # Bob measures Alice's qubits
    bob_results = [measure_state(state, bob_bases[i]) for i, state in enumerate(alice_states)]
    matching_bases = [alice_bases[i] == bob_bases[i] for i in range(num_qubits)]
    shared_key = [bob_results[i] for i in range(num_qubits) if matching_bases[i]]

    # Success rate
    success_rate = len(shared_key) / num_qubits
    print(f"Key Exchange Success Rate: {success_rate:.2f}")

    # Ensure we have a sufficiently long key for AES (128 bits = 16 bytes)
    if len(shared_key) >= 16:
        shared_key = shared_key[:16]
        return bytes(shared_key), success_rate
    else:
        print("Not enough key bits generated. Increase number of qubits.")
        return None, success_rate

# Encrypt and decrypt messages using AES
def encrypt_message(message, key):
    cipher = AES.new(key, AES.MODE_CBC)  # Use AES in CBC mode
    iv = cipher.iv
    encrypted_message = cipher.encrypt(pad(message.encode(), AES.block_size))
    return iv, encrypted_message

def decrypt_message(iv, encrypted_message, key):
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    decrypted_message = unpad(cipher.decrypt(encrypted_message), AES.block_size)
    return decrypted_message.decode()

# Main simulation
num_qubits = 256
success_rate = 0
RATE = 0.57
while(success_rate <= RATE):
    key, success_rate = generate_shared_key(num_qubits)
    if(success_rate < RATE):
        print("retry key generation")

if key and success_rate > RATE:  # Use the key if success rate is high enough
    print("Shared key established:", key)

    # Alice sends a message to Bob
    alice_message = "Hello Bob!"
    iv, encrypted_message = encrypt_message(alice_message, key)
    print(f"Alice's encrypted message: {encrypted_message}")

    # Bob decrypts the message
    bob_message = decrypt_message(iv, encrypted_message, key)
    print(f"Bob's decrypted message: {bob_message}")

    # Bob sends a message to Alice
    bob_message = "Hello Alice!"
    iv, encrypted_message = encrypt_message(bob_message, key)
    print(f"Bob's encrypted message: {encrypted_message}")

    # Alice decrypts the message
    alice_message = decrypt_message(iv, encrypted_message, key)
    print(f"Alice's decrypted message: {alice_message}")
else:
    print("Failed to generate a secure shared key.")

