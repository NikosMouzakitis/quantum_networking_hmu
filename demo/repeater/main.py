from qutip import *
import numpy as np
import matplotlib.pyplot as plt

# Define Bell state (|Φ⁺⟩)
def create_bell_state():
    zero = basis(2, 0)  # |0⟩, shape: (2, 1)
    one = basis(2, 1)   # |1⟩, shape: (2, 1)
    bell_state = (tensor(zero, zero) + tensor(one, one)).unit()  # |Φ⁺⟩, shape: (4, 1)
    bell_dm = ket2dm(bell_state)  # Convert to density matrix, shape: (4, 4)
    return bell_dm

# Apply noise to a quantum state (Depolarizing channel)
def apply_depolarizing_noise(state, p):
    """
    Depolarizing noise: ρ' = (1-p)ρ + (p/dim)I
    Parameters:
    - state: density matrix (shape: (dim, dim))
    - p: depolarizing noise probability (scalar)
    Returns:
    - noisy_state: noisy density matrix (shape: (dim, dim))
    """
    dim = np.prod(state.dims[0])  # Total dimension of the system
    identity = qeye(dim)  # Identity operator, shape: (dim, dim)
    identity.dims = state.dims
    n1=(1-p)*state
    n2 = (p/dim)*identity
    noisy_state = (1 - p) * state + (p / dim) * identity  # Combine components
    return noisy_state

# Entanglement swapping simulation
def entanglement_swapping(bell1, bell2):
    """
    Perform entanglement swapping between two Bell states:
    bell1: A-B (shape: (4, 4)), bell2: B-C (shape: (4, 4))
    Returns:
    - swapped_state: final entangled state between A and C (shape: (4, 4))
    """
    # Bell measurement on qubits 2 and 3 (middle qubits)
    bell_meas = (tensor(basis(2, 0), basis(2, 0)).proj() + 
                 tensor(basis(2, 1), basis(2, 1)).proj())  # Bell basis, shape: (4, 4)
    projection = tensor(qeye(2), bell_meas, qeye(2))  # Operate on qubits 2 and 3, shape: (16, 16)
    
    # Combine the two input states into a joint density matrix
    joint_state = tensor(bell1, bell2)  # Combined state, shape: (16, 16)
    
    # Apply projection for entanglement swapping
    swapped_state = (projection * joint_state * projection.dag()).unit()  # Shape: (16, 16)
    
    # Partial trace over qubits 2 and 3 to get A-C state
    final_state = swapped_state.ptrace([0, 3])  # Shape: (4, 4)
    return final_state

# Network Simulation
def simulate_network():
    """
    Simulates a basic quantum repeater network with entanglement swapping.
    Returns:
    - fidelity_value: fidelity of the final entangled state with an ideal Bell state
    """
    noise_levels = np.linspace(0, 1, 20)  # Noise levels from 0 to 1
    fidelities = []


    # Step 1: Create initial entanglement between nodes
    bell1 = create_bell_state()  # Between nodes A and B
    print(bell1)

    bell2 = create_bell_state()  # Between nodes B and C
    print(bell2)
    
    # Step 2: Calculate fidelity for different noise levels 
    for p in noise_levels:
        bell1_noisy = apply_depolarizing_noise(bell1, p)
        bell2_noisy = apply_depolarizing_noise(bell2, p)
        final_state = entanglement_swapping(bell1_noisy, bell2_noisy)
        ideal_bell = create_bell_state()
        print(ideal_bell)
        fidelity_value = fidelity(final_state, ideal_bell)
        fidelities.append(fidelity_value)
    
    # Step 3: Plot fidelity vs noise level
    plt.plot(noise_levels, fidelities)
    plt.xlabel("Noise Level (p)")
    plt.ylabel("Fidelity")
    plt.title("Fidelity vs. Noise Level in Entanglement Swapping")
    plt.grid(True)
    plt.savefig("Fidelity vs Noise Level in Entanglement Swapping.png")   

# Main Execution
if __name__ == "__main__":
    simulate_network()
