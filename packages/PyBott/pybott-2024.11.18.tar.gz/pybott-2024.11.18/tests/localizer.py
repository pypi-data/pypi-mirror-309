import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

from pythtb import *

from pybott import bott, spin_bott
from dos import plot_dos

import haldane
import kanemele as km

import sys

plt.rc("text", usetex=True)
plt.rc("font", family="serif", serif="Computer Modern")

import pfaffian as pff

# from pfapack import pfaffian as pf
import numpy.matlib

def localized_dirac_operator(lambda_param, x_op, y_op, ham):
    """
    Generates the localized dirac operator based on https://arxiv.org/abs/1907.11791 eq. (2.3)

    L_lambda(X0, Y0, H) = [[ H - lambda_3,  (X0 - lambda_1) - i*(Y0 - lambda_2) ],
                           [ (X0 - lambda_1) + i*(Y0 - lambda_2), -H + lambda_3 ]]

    Args:
    - x_op (numpy.ndarray): The matrix corresponding to X0 in the formula.
    - y_op (numpy.ndarray): The matrix corresponding to Y0 in the formula.
    - ham (numpy.ndarray): The matrix corresponding to H in the formula.
    - lambda_param (numpy.ndarray): A vector of three elements [lambda_1, lambda_2, lambda_3].

    Returns:
    - result (numpy.ndarray): The resulting matrix from the given formula, with complex entries.
    """
    dim_orb = (ham.shape[0] - x_op.shape[0])//x_op.shape[0]
    if dim_orb != 0:
        x_op = np.diag(np.repeat(np.diag(x_op), dim_orb+1))
        y_op = np.diag(np.repeat(np.diag(y_op), dim_orb+1))
        
    n_size = x_op.shape[0]

    lambda_1 = lambda_param[0]
    lambda_2 = lambda_param[1]
    lambda_3 = lambda_param[2]

    top_left = ham - lambda_3 * np.eye(n_size)
    top_right = (x_op - lambda_1 * np.eye(n_size)) - 1j * (
        y_op - lambda_2 * np.eye(n_size)
    )
    bottom_left = (x_op - lambda_1 * np.eye(n_size)) + 1j * (
        y_op - lambda_2 * np.eye(n_size)
    )
    bottom_right = -ham + lambda_3 * np.eye(n_size)

    result = np.block([[top_left, top_right], [bottom_left, bottom_right]])

    return result

def localizer_index_spectrum(lambda_param, x_op, y_op, ham):
    ldo = localized_dirac_operator(lambda_param, x_op, y_op, ham)
    return np.linalg.eigvalsh(ldo)

def gen_q(n_sites):
    id_op = np.eye(1)
    zeros = np.zeros((1,1))
    q_op = 1/np.sqrt(2)*np.block([[id_op, zeros, zeros, -1j*id_op],
                                  [zeros, id_op, 1j*id_op, zeros],
                                  [zeros, 1j*id_op, id_op, zeros],
                                  [-1j*id_op, zeros, zeros, id_op]]
                                 )
    return np.kron(np.eye(n_sites // 2), q_op)


def localizer_index(lattice, ham, class_az='A2D', lambda_param=np.array([0, 0, 0]), kappa=1):
    """Computes the localizer index for specified symmetry classes of the Altland-Zirnbauer classification in 
    condensed matter physics. This index helps identify topological phases based on the spectral properties 
    of the system's Hamiltonian and position operators.

    Parameters:
    -----------
    lattice : np.ndarray
        An N x 2 array representing the lattice coordinates in two dimensions, with each row [x, y] specifying
        the position of a lattice site.
        
    ham : np.ndarray
        The Hamiltonian matrix (Hermitian), representing the system's energy states.
        
    class_az : str, optional
        The Altland-Zirnbauer class, specifying the symmetry type. Supported classes are 'A2D' for class A in 
        2D and 'AII2D' for class AII in 2D.
        
    lambda_param : np.ndarray, optional
        A length-3 array specifying the localization parameters for the spectral localizer in 2D.

    kappa : float, optional
        Scaling factor for the position operators; used to adjust the localization strength in the Dirac operator.

    Returns:
    --------
    float or int
        The localizer index of the system: 
        - For 'A2D' class, the index is a half-integer based on the spectral signature.
        - For 'AII2D' class, the index is an integer calculated via the Pfaffian sign.

    Raises:
    -------
    ValueError:
        If an unsupported symmetry class is specified or operators do not match required conditions.
    """
    x_lat, y_lat = lattice.T
    x_op, y_op = np.diag(x_lat), np.diag(y_lat)

    if class_az == 'A2D':
        evals = localizer_index_spectrum(lambda_param, kappa * x_op, kappa * y_op, ham)
        return 0.5 * np.sum(np.sign(evals))

    elif class_az == 'AII2D':
        ldo = localized_dirac_operator(lambda_param, kappa * x_op, kappa * y_op, ham)
        if not np.allclose(ldo, dual(dual(ldo)), atol=1e-14):
            raise ValueError("Dual symmetry condition not met: H ≈ H^#⊗ # (See Section 5.4)")
        
        n_sites = ham.shape[0]
        q_op = gen_q(n_sites)
        qhq = 1j * np.conj(q_op) @ ldo @ q_op

        # if np.max(qhq+qhq.T)>1e-14 :#not np.allclose(qhq, -qhq.T, atol=1e-14):
        #     qhq = qhq-qhq.T ## investigate why sometimes necessary
        
        pfaff_sign = pff.pfaffian(qhq, sign_only=True)
        return np.sign(np.real(pfaff_sign))

    else:
        raise ValueError(f"Unsupported class {class_az}. Choose 'A2D' or 'AII2D'.")

        

def plot_heatmap(params, grid_size, sample_size):
    data_matrix = np.zeros((grid_size, grid_size))
    sample = np.linspace(-sample_size, sample_size, grid_size)
    for idx, x in tqdm(enumerate(sample), desc="Computing heatmap LI"):
        for idy, y in enumerate(sample):
            lambda_param = params["lambda_param"]
            lambda_param[0] = x
            lambda_param[1] = y
            li = localizer_index(params['lattice'], params['ham'], params['class_az'], lambda_param, params["kappa"])
            data_matrix[idx, idy] = li

    # plt.imshow(data_matrix, extent=(-side_length, side_length, -side_length, side_length), origin='lower', cmap='hot', interpolation='nearest')
    plt.imshow(
        data_matrix,
        extent=(0, sample_size, 0, sample_size),
        origin="lower",
        cmap="hot",
        interpolation="nearest",
    )
    plt.colorbar(label="Localizer Index")
    plt.title(
        f"Heatmap of Localizer Index $\\kappa={np.round(params['kappa'],2)}$ and $\\lambda_3={np.round(lambda_param[2],2)}$"
    )
    plt.xlabel("X")
    plt.ylabel("Y")

    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.savefig(
        f"localizer/kappa_{np.round(params['kappa'],2)}_l3_{np.round(lambda_param[2],2)}.png",
        format="png",
        bbox_inches="tight",
    )
    plt.savefig(
        f"localizer/kappa_{np.round(params['kappa'],2)}_l3_{np.round(lambda_param[2],2)}.pdf",
        format="pdf",
        bbox_inches="tight",
    )
    plt.clf()
    plt.cla()


def calculate_localizer_index(
    kappa=0.05,
    y0_min=0,
    y0_max=0.5,
    num_points=500,
    n=4,
    color="black",
    s=0.2,
    x_op=None,
    y_op=None,
    ham=None,
    title_fig="",
    save_fig="loc_index",
    ord_inf=-0.5,
    ord_sup=1.25,
    x0=0,
):
    y0_values = np.linspace(y0_min, y0_max, num_points)
    eigenvalues_list = []
    li_values = []
    scatter_x = []
    scatter_y = []
    for y0 in y0_values:
        lambda_param = np.array([x0, y0, 0.0])
        lis = localizer_index_spectrum(kappa, lambda_param, x_op, y_op, ham)
        li = localizer_index(kappa, lambda_param, x_op, y_op, ham)
        index = np.argsort(np.abs(lis))
        scatter_x.extend([y0] * n)
        scatter_y.extend(lis[index[:n]])
        li_values.append(li)

    plt.scatter(scatter_x, scatter_y, color=color, s=s)

    li_values = np.array(li_values)
    if np.max(li_values) - np.min(li_values) == 0:
        li_values = np.zeros_like(li_values)
    else:
        li_values = (li_values - np.min(li_values)) / (
            np.max(li_values) - np.min(li_values)
        )
    if np.abs(np.sum(li_values)) > 1e-3:
        print("ok")
    print(f"{x0=},{kappa=},{np.sum(li_values)}")
    plt.plot(y0_values, li_values, color="blue", ls="--")

    plt.axhline(y=0, color="red")
    plt.axis((y0_min, y0_max, ord_inf, ord_sup))
    plt.xlabel(r"$y_0$", fontsize=20)
    plt.ylabel(r"$\sigma[\mathcal{L}]$", fontsize=20)
    plt.title(title_fig, fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.savefig(save_fig, format="pdf", bbox_inches="tight")
    plt.show()

def dual(matrix):
    """
    Computes the dual of a 2x2 block matrix.

    Parameters:
    matrix (np.ndarray): A 2n x 2n NumPy array representing a block matrix.
                         Assumes the block structure [[A, B], [C, D]].

    Returns:
    np.ndarray: The dual matrix, given by [[D.T, -B.T], [-C.T, A.T]].
    """
    n = matrix.shape[0]
    assert n % 2 == 0, "Matrix should have even dimensions for 2x2 block structure"
    half_n = n // 2

    A = matrix[:half_n, :half_n]
    B = matrix[:half_n, half_n:]
    C = matrix[half_n:, :half_n]
    D = matrix[half_n:, half_n:]

    dual_matrix = np.block([
        [D.T, -B.T],
        [-C.T, A.T]
    ])
    
    return dual_matrix



def calculate_line_li(params, x0_min=-1, x0_max=1, x0_ndots=20, which_param=0):
    x0_values = np.linspace(x0_min, x0_max, x0_ndots)
    li_values = []
    
    # Utilisation de tqdm pour afficher la barre de progression
    for x0 in tqdm(x0_values, desc="Calculating LI values"):
        lambda_param = params["lambda_param"]
        lambda_param[which_param] = x0
        li = localizer_index(params["lattice"], params["ham"], params["class_az"], lambda_param, params["kappa"])
        li_values.append(li)
    
    return x0_values, li_values

if __name__ == "__main__":
    n_side = 12
    t1 = 1
    t2 = 0.1j
    delta = 1
    a = 1
    rashba = 0.

    kappa = 0.05
    lambda_param = np.array([0.2, 0.2, 0.5])

    lattice, ham = haldane.haldane_ham(n_side=n_side, t1=t1, t2=0.2j,
                                       delta=0.2, pbc=False)
    class_az = 'A2D'
    params = {
        "lattice" : lattice,
        "ham" : ham,
        "class_az" : class_az,
        "lambda_param" : lambda_param,
        "kappa" : kappa
    }

    # x0_values, li_values = calculate_line_li(params, x0_min=-2, x0_max=2, which_param=2)
    # plt.scatter(x0_values, li_values, color="black")
    # plt.show()

    # from pybott import bott
    # print(bott(lattice, ham))
    # li = localizer_index(lattice, ham, kappa=kappa)
    # print(f"{li}") 
    # exit()

    n_sites = lattice.shape[0]


    t2_values = np.linspace(-1.5,1.5,24)
    delta_values = np.linspace(-8,8,24)
    li_values = np.zeros((len(t2_values), len(delta_values)))

    for i, t2 in enumerate(t2_values):
        for j, delta in enumerate(delta_values):
            lattice, ham = haldane.haldane_ham(n_side=n_side, t1=t1, t2=t2*1j,
                                               delta=delta, pbc=False)
            from pybott import bott
            print(bott(lattice, ham))
            li = localizer_index(lattice, ham, lambda_param=lambda_param, kappa=kappa)
            li_values[i, j] = li
            print(f"{t2=},{delta=},{li=}")

    # plt.figure(figsize=(8, 6))
    plt.imshow(li_values, extent=(delta_values[0], delta_values[-1], t2_values[0], t2_values[-1]), 
               origin='lower', aspect='auto', cmap='coolwarm')
    # plt.colorbar(label="Localizer Index (li)",fontsize=20)
    plt.xlabel(r"$\delta$",fontsize=20)
    plt.ylabel(r"$t_2$",fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.title(f"$N={n_sites}\\quad \\kappa={kappa}\\quad \\lambda \\ne 0$",fontsize=20)
    plt.savefig(f"haldane_li_pd_{kappa}.pdf",format="pdf",bbox_inches='tight')
    plt.show()
    exit()
    

    t2_values = np.linspace(0,0.6,20)
    li_values = []
    for t2 in t2_values:
        lattice, ham = haldane.haldane_ham(n_side=n_side, t1=t1, t2=t2*1j,
                                           delta=delta, pbc=False)

        n_sites = ham.shape[0]
        zeros = np.zeros((n_sites, n_sites))
        ham_kane_mele = np.block([[ham,zeros],
                                  [zeros,np.conj(ham)]])
        li = localizer_index(lattice, ham_kane_mele, 'AII2D', lambda_param, kappa)
        li_values.append(li)
        print(f"{t2=},{li=}")


    plt.scatter(t2_values, li_values, color="black")
    plt.xlabel(r"$t_2$",fontsize=20)
    plt.ylabel(r"Localizer index AII2D",fontsize=20)
    plt.title(f"$N={n_sites}\\quad \\kappa={kappa} \\quad \\delta={delta}$",fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.savefig(f"li_kanemele_{kappa}_{n_sites}.pdf",format="pdf",bbox_inches='tight')
    plt.show()
    exit()
    
    n_sites_spin = ham_kane_mele.shape[0]
    # n_sites_spin = evals.shape[0]
    # n_sites = 2 * n_sites_spin
    
    # ham = ham.reshape(n_sites,n_sites)
    # evals, evects = np.linalg.eigh(ham)
    def get_sigma_bott(N):
        """Return the σ_z spin operator for Bott index calculation."""
        return np.kron(np.array([[1, 0], [0, -1]]), np.eye(N))

    sigma = get_sigma_bott(n_sites_spin // 2)

    evals, evects = np.linalg.eigh(ham_kane_mele)
    lattice_x2 = np.concatenate((lattice, lattice))
    sb = spin_bott(
        lattice_x2, evals, evects.T, sigma, fermi_energy=-0.1, threshold_bott=-0.1,
    )
    print(f"{sb=}")

    # print(evals)

    
    ham = evects@np.diag(evals)@np.linalg.inv(evects)
    ham = evects@np.diag(evals)@np.conj(evects.T)

    evals_bis, evects_bis = np.linalg.eigh(ham)


    

    exit()
    # print(evals_bis)

    # fig, axs = plt.subplots(2, 2)
    # axs[0, 0].imshow(np.abs(evects.T))
    # axs[0, 0].set_title("Figure 1")
    # axs[0, 1].imshow(np.abs(evects_bis)) # TR
    # axs[0, 1].set_title("Figure 2")

    # plt.tight_layout()
    # plt.show()

    sb = spin_bott.spin_bott(
        lattice_x2, evals_bis, evects_bis, sigma, fermi_energy=0, threshold_bott=-0.1, 
    )
    print(f"{sb=}")

    exit()
    

    psp = spin_bott.get_p_sigma_p_bott(evals, evects, evects, sigma, 0)

    print(lattice.shape)
    print(ham.shape)
    # plot_dos(evals)

    x_grid, y_grid = lattice.T

    x_grid = np.concatenate((x_grid, x_grid))
    y_grid = np.concatenate((y_grid, y_grid))

    n_sites = ham.shape[0]

    x_op = np.diag(x_grid)
    y_op = np.diag(y_grid)

    grid_size = 10
    side_length = 12
    # sample = np.linspace(-side_length,side_length,grid_size)
    sample = np.linspace(0, side_length, grid_size)
    # x0 = 0.15
    # kappa = 0.0478

    x0 = 0.05
    kappa = 0.05

    title_fig = f"$N={n_sites}\\quad t_2={np.imag(t2)}i\\quad\\delta={delta}\\quad\\kappa={kappa}$\n$ x_0={x0}\\quad \\lambda_R = {rashba}$"
    save_fig = f"N={n_sites}_{t2=}_{delta=}_{kappa=}_{rashba=}.pdf"
    calculate_localizer_index(
        kappa=kappa,
        y0_min=0,
        y0_max=0.35,
        num_points=400,
        n=4,
        color="black",
        s=0.2,
        x_op=x_op,
        y_op=y_op,
        ham=psp,
        title_fig=title_fig,
        save_fig=save_fig,
        ord_inf=-0.05,
        ord_sup=0.05,
        x0=x0,
    )
    exit()

    for kappa in np.linspace(0.01, 0.1, 20):
        for x0 in np.linspace(0, 0.2, 10):
            calculate_localizer_index(
                kappa=kappa,
                y0_min=-0.3,
                y0_max=1,
                num_points=100,
                n=4,
                color="black",
                s=0.2,
                x_op=x_op,
                y_op=y_op,
                ham=psp,
                ord_inf=-0.1,
                ord_sup=0.1,
                x0=x0,
            )
    exit()
