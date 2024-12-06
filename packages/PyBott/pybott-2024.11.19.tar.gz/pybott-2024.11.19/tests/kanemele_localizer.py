#!/usr/bin/env python

"""This module implements a finite 2D Kane-Mele model to compute the
density of states (DOS) and visualize a topologically protected edge
state. The Kane-Mele model is designed to capture quantum spin Hall
states and includes spin-orbit coupling and Rashba interactions. 

Key Functions:
- `get_finite_kane_mele`: Builds a finite Kane-Mele model with a specified number of supercells.
- `plot_edge_state`: Visualizes the spatial density of a selected edge state.

"""
import sys

sys.path.append("../src/pybott/")

import spin_bott

from dos import plot_dos

from pythtb import *
import numpy as np
import matplotlib.pyplot as plt


from rich import traceback
traceback.install()

sys.path.append("../src/pybott/")
import spin_bott


def kane_mele_model(nx=6, ny=6, t1=1, esite=0, t2=0, rashba=0.25, pbc=True):
    """
    Returns a finite Kane-Mele model with nx sites along the x-axis and ny sites along the y-axis.

    Args:
        nx (int): Number of sites along the x-axis.
        ny (int): Number of sites along the y-axis.
        esite (float): On-site energy for the Kane-Mele model.
        t2 (float): Strength of the spin-orbit coupling (second neighbor hopping).
        rashba (float): Strength of the Rashba coupling.

    Returns:
        tb_model: A finite tight-binding model representing the Kane-Mele system.
    """

    # Define lattice vectors and atomic site coordinates
    lat = [[1.0, 0.0], [0.5, np.sqrt(3.0) / 2.0]]
    orb = [[1.0 / 3.0, 1.0 / 3.0], [2.0 / 3.0, 2.0 / 3.0]]

    # Create the 2D Kane-Mele model with nx * ny supercells
    model = tb_model(2, 2, lat, orb, nspin=2)

    spin_orb = np.imag(t2)  # imag for coherence with Haldane model

    # Set on-site energies
    model.set_onsite([esite, -esite])

    # Useful definitions for spin matrices
    sigma_x = np.array([0.0, 1.0, 0.0, 0])
    sigma_y = np.array([0.0, 0.0, 1.0, 0])
    sigma_z = np.array([0.0, 0.0, 0.0, 1])

    # First-neighbor hopping (without spin)
    model.set_hop(t1, 0, 1, [0, 0])
    model.set_hop(t1, 0, 1, [0, -1])
    model.set_hop(t1, 0, 1, [-1, 0])

    # Second-neighbor hopping with spin-orbit interaction (s_z)
    model.set_hop(-1.0j * spin_orb * sigma_z, 0, 0, [0, 1])
    model.set_hop(1.0j * spin_orb * sigma_z, 0, 0, [1, 0])
    model.set_hop(-1.0j * spin_orb * sigma_z, 0, 0, [1, -1])
    model.set_hop(1.0j * spin_orb * sigma_z, 1, 1, [0, 1])
    model.set_hop(-1.0j * spin_orb * sigma_z, 1, 1, [1, 0])
    model.set_hop(1.0j * spin_orb * sigma_z, 1, 1, [1, -1])

    # Rashba (first-neighbor hopping with spin)
    r3h = np.sqrt(3.0) / 2.0
    model.set_hop(
        1.0j * rashba * (0.5 * sigma_x - r3h * sigma_y), 0, 1, [0, 0], mode="add"
    )
    model.set_hop(1.0j * rashba * (-1.0 * sigma_x), 0, 1, [0, -1], mode="add")
    model.set_hop(
        1.0j * rashba * (0.5 * sigma_x + r3h * sigma_y), 0, 1, [-1, 0], mode="add"
    )

    # Create a finite model (e.g., a ribbon of size nx * ny)
    tmp_model = model.cut_piece(nx, 0, glue_edgs=pbc)
    fin_model = tmp_model.cut_piece(ny, 1, glue_edgs=pbc)

    # What follows is to get rid of the spinor formalism
    ham = fin_model._gen_ham()
    ham = ham.reshape(2 * fin_model._norb, 2 * fin_model._norb)
    evals, evects = np.linalg.eigh(ham)
    n_sites = evals.shape[0]
    evects = evects.reshape(n_sites // 2, n_sites * 2)
    evects = np.concatenate((evects[:, :n_sites].T, evects[:, n_sites:].T), axis=1)

    return fin_model, evects


def plot_edge_state(model, evals, vecs, state_index, nx, ny):
    """
    Visualize the density of a localized edge state.

    Args:
        model (tb_model): The tight-binding model.
        evals (array): Array of eigenvalues of the system.
        vecs (array): Array of eigenvectors of the system.
        state_index (int): Index of the edge state to visualize.
        nx (int): Number of sites along the x-axis.
        ny (int): Number of sites along the y-axis.

    Returns:
        None: Displays and saves a plot of the edge state's spatial density.
    """
    (fig, ax) = model.visualize(
        0, 1, eig_dr=vecs[state_index, :, 1], draw_hoppings=False
    )
    ax.set_title("Edge state for finite model without periodic direction")
    ax.set_xlabel("x coordinate")
    ax.set_ylabel("y coordinate")
    fig.tight_layout()
    fig.savefig("edge_state.pdf")
    plt.show()


def convert_hamiltonian_to_2d(hamiltonian):
    """
    Convert a Hamiltonian of shape (N, 2, N, 2) into a flat 2D matrix (2N, 2N)
    while preserving eigenvector consistency.
    """
    N = hamiltonian.shape[0]  # Number of sites/orbitals per dimension
    hamiltonian_2d = np.zeros((2 * N, 2 * N), dtype=complex)

    for i in range(N):       # Iterate over site indices
        for j in range(N):   # Iterate over target site indices
            for s1 in range(2):  # Internal degrees of freedom
                for s2 in range(2):
                    hamiltonian_2d[2 * i + s1, 2 * j + s2] = hamiltonian[i, s1, j, s2]

    return hamiltonian_2d

if __name__ == "__main__":
    fin_model, evects_perso_old = kane_mele_model(nx=6, ny=6, t1=1, esite=0, t2=0.2j, rashba=0., pbc=False)
    lattice = fin_model.get_orb()
    ham = fin_model._gen_ham()


    ham_perso = np.block([[ham[:,0,:,0],ham[:,1,:,0]],
                          [ham[:,0,:,1],ham[:,1,:,1]]])


    # fig, axs = plt.subplots(2, 2)
    # axs[0, 0].imshow(np.real(ham_perso))
    # axs[0, 1].imshow(np.imag(ham_perso))
    # axs[1, 0].imshow(np.abs(ham_perso - np.conj(ham_perso.T)))
    # axs[1, 1].imshow(np.abs(ham_perso - ham_perso.T))
    # plt.tight_layout()
    # plt.show()

    evals, evects = np.linalg.eigh(ham_perso)
    
    n_sites = evals.shape[0]
    
    def get_sigma_bott(N):
        """Return the σ_z spin operator for Bott index calculation."""
        return np.kron(np.array([[1, 0], [0, -1]]), np.eye(N))


    sigma = get_sigma_bott(n_sites // 2)

    lattice_x2 = np.concatenate((lattice, lattice))

    # ham_rebuilt = evects.T @ np.diag(evals) @ np.linalg.inv(evects.T)
    ham_rebuilt = evects.T @ np.diag(evals) @ np.conj(evects)

    evals, evects = np.linalg.eigh(ham_rebuilt)

    c_sb = spin_bott.spin_bott(
        lattice_x2,
        evals,
        evects,
        sigma,
        fermi_energy=0.8,
        threshold_bott=-0.05,
        plot_psp=False,
    )

    print({c_sb})

    from localizer import localizer_index, calculate_line_li

    fig, axs = plt.subplots(2, 2)
    axs[0, 0].imshow(np.real(ham_rebuilt))
    axs[0, 1].imshow(np.imag(ham_rebuilt))
    axs[1, 0].imshow(np.abs(ham_rebuilt - np.conj(ham_rebuilt.T)))
    axs[1, 1].imshow(np.abs(ham_rebuilt - np.conj(ham_rebuilt)))
    plt.tight_layout()
    plt.show()

    lambda_param = np.array([0.1,0.1,0])
    kappa = 1
    print(np.max(ham_perso-np.conj(ham_rebuilt.T)))
    li = localizer_index(lattice, ham_rebuilt, 'AII2D', lambda_param, kappa)

    print(f"{li=}")




    params = {
        "lattice" : lattice,
        "ham" : ham_rebuilt,
        "class_az" : "AII2D",
        "lambda_param" : lambda_param,
        "kappa" : kappa
    }

    # evals, evects = np.linalg.eigh(ham_rebuilt)

    x0_values, li_values = calculate_line_li(params, x0_min=-1, x0_max=1, x0_ndots=40, which_param=2)
    plt.scatter(x0_values, li_values, color="black")
    plt.show()

    exit()

    # Optionally, diagonalize the Hamiltonian to check eigenvalues
    eigvals = np.linalg.eigvalsh(ham)
    plt.figure(figsize=(6, 4))
    plt.plot(np.sort(eigvals), 'o', label='Eigenvalues')
    plt.title(f"Eigenvalues for a {size_x}x{size_y} finite Kane-Mele system")
    plt.xlabel("Index")
    plt.ylabel("Energy")
    plt.grid()
    plt.legend()
    plt.show()

