
# Import necessary libraries
import streamlit as st
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

# Function to simulate BB84 protocol
def bb84_protocol(num_bits, eavesdrop=False):
    # Alice's random bits and bases
    alice_bits = np.random.randint(2, size=num_bits)
    alice_bases = np.random.choice(['Z', 'X'], size=num_bits)

    # Bob's random bases
    bob_bases = np.random.choice(['Z', 'X'], size=num_bits)

    # Eve's interception (if eavesdropping)
    if eavesdrop:
        eve_bases = np.random.choice(['Z', 'X'], size=num_bits)
    else:
        eve_bases = None

    # Create the quantum circuit
    qc = QuantumCircuit(num_bits)
    for i in range(num_bits):
        if alice_bits[i] == 1:
            qc.x(i)  # Apply X gate for bit 1
        if alice_bases[i] == 'X':
            qc.h(i)  # Apply Hadamard gate for X basis
    qc.barrier()

    # Eve's measurement (if eavesdropping)
    if eavesdrop:
        for i in range(num_bits):
            if eve_bases[i] == 'X':
                qc.h(i)
        # Simulate Eve's measurement using Statevector
        state = Statevector.from_instruction(qc)
        eve_measurement = list(state.sample_counts(shots=1).keys())[0]
        eve_measurement = [int(bit) for bit in eve_measurement]
        qc.reset(range(num_bits))
        for i in range(num_bits):
            if eve_measurement[i] == 1:
                qc.x(i)
            if eve_bases[i] == 'X':
                qc.h(i)
        qc.barrier()

    # Bob's measurement
    for i in range(num_bits):
        if bob_bases[i] == 'X':
            qc.h(i)

    # Simulate Bob's measurement using Statevector
    state = Statevector.from_instruction(qc)
    bob_measurement = list(state.sample_counts(shots=1).keys())[0]
    bob_measurement = [int(bit) for bit in bob_measurement]

    # Compare bases to generate the shared key
    shared_key = []
    for i in range(num_bits):
        if alice_bases[i] == bob_bases[i]:
            shared_key.append(bob_measurement[i])

    # Check for eavesdropping
    eavesdrop_detected = False
    if eavesdrop:
        for i in range(num_bits):
            if alice_bases[i] != eve_bases[i] and alice_bases[i] == bob_bases[i]:
                if alice_bits[i] != bob_measurement[i]:
                    eavesdrop_detected = True
                    break

    return alice_bits, alice_bases, bob_bases, bob_measurement, shared_key, eavesdrop_detected

# Streamlit app
st.title("Quantum Networking Demo: BB84 Protocol")
st.write("Simulate quantum key distribution with Alice, Bob, and Eve!")

# User inputs
num_bits = st.slider("Number of qubits to send:", min_value=4, max_value=20, value=8)
eavesdrop = st.checkbox("Enable eavesdropping (Eve)")

# Run the simulation
if st.button("Run Simulation"):
    alice_bits, alice_bases, bob_bases, bob_measurement, shared_key, eavesdrop_detected = bb84_protocol(num_bits, eavesdrop)

    # Display results
    st.write("### Alice's Bits:")
    st.write(alice_bits)
    st.write("### Alice's Bases:")
    st.write(alice_bases)
    st.write("### Bob's Bases:")
    st.write(bob_bases)
    st.write("### Bob's Measurement:")
    st.write(bob_measurement)
    st.write("### Shared Key:")
    st.write(shared_key)
    if eavesdrop:
        if eavesdrop_detected:
            st.error("Eavesdropping detected!")
        else:
            st.success("No eavesdropping detected.")
