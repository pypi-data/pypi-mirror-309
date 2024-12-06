"""Code to compute the Bott index following the definition given by
T. A. Loring and M. B. Hastings in
https://iopscience.iop.org/article/10.1209/0295-5075/92/67004/meta

The **Bott index** measures the commutativity of projected position operators, 
providing a topological invariant that helps distinguish topological insulators 
from trivial insulators.
"""

import csv
from tqdm import tqdm

import numpy as np
import scipy

import matplotlib.pyplot as plt
import pandas as pd


def is_pair_of_ordered_reals(variable):
    return (
        isinstance(variable, (tuple, list))
        and len(variable) == 2
        and all(isinstance(i, (float, int)) for i in variable)
        and variable[0] < variable[1]
    )


def get_nearest_value(dictionary, key):
    if key in dictionary:
        return dictionary[key]

    nearest_key = min(dictionary.keys(), key=lambda k: abs(k - key))
    return dictionary[nearest_key]


def compute_uv(lattice, eigenvectors, pos_omega, orb, lx=None, ly=None):
    """
    Compute U and V matrices, which are the projected position operators.

    This function computes the U and V matrices (projected position operators) based
    on the given lattice coordinates and eigenvectors.

    :param lattice: Array of shape ``(N_sites, 2)`` containing the coordinates
        of the lattice sites.
    :type lattice: ndarray

    :param eigenvectors: Array of shape ``(orb * N_sites, orb * N_sites)``
        containing the eigenvectors.
    :type eigenvectors: ndarray

    :param pos_omega: Position of the frequency in the ordered list of frequencies.
    :type pos_omega: int

    :param orb: Number of orbitals.
    :type orb: int

    :param lx: Size of the sample along the x-axis. If ``None``, the function will
        determine it automatically.
    :type lx: float, optional

    :param ly: Size of the sample along the y-axis. If ``None``, the function will
        determine it automatically.
    :type ly: float, optional

    :return: ``u_proj`` and ``v_proj``, which are the projected position operators
        on the x and y coordinates, respectively.
    :rtype: tuple of (ndarray, ndarray)
    """
    n_sites = lattice.shape[0]
    x_lattice = lattice[:n_sites, 0]
    y_lattice = lattice[:n_sites, 1]
    if lx is None:
        lx = np.max(x_lattice) - np.min(x_lattice)
    if ly is None:
        ly = np.max(y_lattice) - np.min(y_lattice)
    u_proj = np.zeros((orb * n_sites, orb * n_sites), dtype=complex)
    v_proj = np.zeros((orb * n_sites, orb * n_sites), dtype=complex)

    x_lattice = np.repeat(x_lattice, orb)
    y_lattice = np.repeat(y_lattice, orb)

    w_stack = eigenvectors[:, :pos_omega]

    phase_x = np.diag(np.exp(2 * np.pi * 1j * x_lattice / lx))
    phase_y = np.diag(np.exp(2 * np.pi * 1j * y_lattice / ly))
    u_proj = np.conj(w_stack.T) @ phase_x @ w_stack
    v_proj = np.conj(w_stack.T) @ phase_y @ w_stack

    return u_proj, v_proj


def sorting_eigenvalues(evals, evects, rev=False):
    """This function sorts the eigenvalues and eigenvectors in
    ascending or descending order depending on the `rev` flag. Useful
    when the energy are not exactly the eigenvalues, typically in
    photonics systems or non Hermitian systems in general.

    :param evals: Array containing the eigenvalues to be sorted.
    :type evals: ndarray

    :param evects: Array containing the corresponding eigenvectors.
    :type evects: ndarray

    :param rev: If ``True``, the eigenvalues and eigenvectors are sorted in descending
        order; otherwise, they are sorted in ascending order. Default is ``False``.
    :type rev: bool, optional

    :return: A tuple containing the sorted eigenvalues and the corresponding
        sorted eigenvectors.
    :rtype: tuple of (ndarray, ndarray)

    """
    indices = np.argsort(evals)[::-1] if rev else np.argsort(evals)
    return evals[indices], evects[:, indices]


def bott(lattice, ham, fermi_energy=0, gap=None, orb=1, dagger=False):
    """
    Calculate the Bott index of a system described by a given Hamiltonian and lattice.

    This function calculates the Bott index, which is a topological invariant used to
    distinguish topological phases in a system described by the Hamiltonian. If the
    Hamiltonian is not Hermitian, you must compute the eigenvalues and eigenvectors
    independently and use `bott_vect` instead. If the theoretical width of the gap is
    provided and the Hamiltonian is large, eigenvalues and eigenvectors will be computed
    in a restricted Hilbert space to save computation time.

    :param lattice: Array of shape ``(N_sites, 2)`` containing the coordinates of the
        lattice sites.
    :type lattice: ndarray

    :param ham: Hamiltonian matrix of shape ``(orb * N_sites, orb * N_sites)``.
        Must be Hermitian.
    :type ham: ndarray

    :param fermi_energy: Value of energy for which the Bott index is computed, must
        be in the bulk gap to match the Chern number. Not defined outside of the bulk
        gap but usually gives 0. Optional.
    :type fermi_energy: float, optional

    :param gap: Energy gap used for filtering eigenvalues when calculating the Bott
        index. Must be a tuple of two ordered real numbers. If ``None``, the entire
        spectrum is computed. Optional.
    :type gap: tuple of float, optional

    :param orb: Number of orbitals considered per lattice site. Default is ``1``.
    :type orb: int, optional

    :param dagger: Specifies the method to compute the Bott index. If ``True``,
        uses the dagger of the projected position operator; otherwise, it computes
        the inverse of the operator.
    :type dagger: bool

    :return: The computed Bott index.
    :rtype: float

    :raises ValueError: If the Hamiltonian is not Hermitian, or if `gap` is not a
        valid tuple of floats.
    """

    if not np.allclose(ham, ham.conj().T):
        raise ValueError(
            "Hamiltonian must be Hermitian. Use 'bott_vect' for non-Hermitian matrices."
        )

    n_ham = ham.shape[0]

    # Compute eigenvalues and eigenvectors for the entire spectrum if
    # Hamiltonian size is small or no gap provided.
    if n_ham < 512 or gap is None:
        evals, evects = np.linalg.eigh(ham)
        return bott_vect(
            lattice, evects, evals, fermi_energy=fermi_energy, orb=orb, dagger=dagger
        )

    if not is_pair_of_ordered_reals(gap):
        raise ValueError("Gap must be a tuple of two ordered real numbers.")

    # For bigger Hamiltonian, if the gap is provided, we can compute a
    # subset of the spectrum.
    if gap[0] <= fermi_energy <= gap[1]:
        evals, evects = scipy.linalg.eigh(
            ham, subset_by_value=(gap[0], fermi_energy), driver="evr"
        )
    elif fermi_energy < gap[0]:
        evals, evects = scipy.linalg.eigh(
            ham, subset_by_value=(-np.inf, fermi_energy), driver="evr"
        )
    else:
        evals, evects = scipy.linalg.eigh(
            ham, subset_by_value=(gap[0], fermi_energy), driver="evr"
        )

    return bott_vect(lattice, evects, evals, fermi_energy, gap, orb, dagger)


def bott_vect(
    lattice,
    evects,
    energies,
    fermi_energy=0,
    orb=1,
    dagger=False,
):
    """
    Compute the Bott index for a given set of eigenvectors and energies.

    This function computes the Bott index, which is useful when the Hamiltonian is
    not Hermitian, and there is a need for additional preparation of the eigenvalues
    and eigenvectors before sending them to the Bott routine. This can be particularly
    useful in systems beyond tight-binding models. See the example on topological
    photonic systems provided in the documentation.

    :param lattice: Array of shape ``(N_sites, 2)`` containing the coordinates
        of the lattice sites.
    :type lattice: ndarray

    :param evects: Array of shape ``(orb * N_sites, orb * N_sites)`` containing
        the eigenvectors.
    :type evects: ndarray

    :param energies: Array of shape ``(orb * N_sites,)`` containing the energies.
        These energies may differ from the eigenvalues of the Hamiltonian in more
        complex systems beyond tight-binding models.
    :type energies: ndarray

    :param fermi_energy: Energy value at which the Bott index is computed. It must
        be within the bulk gap to match the Chern number. Outside of the bulk gap,
        it usually returns 0. Default is ``0``.
    :type fermi_energy: float, optional

    :param orb: Number of orbitals considered per lattice site. Default is ``1``.
    :type orb: int, optional

    :param dagger: Specifies which method to use for computing the Bott index.
        If ``True``, the method uses the dagger of the projected position operator;
        otherwise, it computes the inverse of the operator. Default is ``False``.
    :type dagger: bool, optional

    :return: The Bott index value.
    :rtype: float
    """

    k = np.searchsorted(energies, fermi_energy)
    if k == 0:
        print(
            "Warning: no eigenstate included in the calculation of the Bott index. Something might have gone wrong."
        )
        return 0

    u_proj, v_proj = compute_uv(lattice, evects, k, orb)

    return bott_matrix(u_proj, v_proj, dagger)


def bott_matrix(u_mat, v_mat, dagger=False):
    """
    This function computes the Bott index for two invertible matrices, `U` and `V`.
    The Bott index is a topological invariant used to distinguish different topological
    phases. The function either computes the standard Bott index or uses the dagger
    of the projected position operator depending on the value of the `dagger` parameter.

    The Bott index is mathematically defined as:

    .. math::
        \\text{Bott}(U, V) = \\frac{1}{2 \pi i} \\text{Tr} \log (UVU^{- 1} V^{- 1})

    :param u_mat: The matrix ``U``.
    :type u_mat: ndarray

    :param v_mat: The matrix ``V``.
    :type v_mat: ndarray

    :param dagger: If ``True``, the method uses the conjugate transpose (dagger)
        of the matrices in the Bott index computation. Default is ``False``, in which
        case the inverse matrices are used.
    :type dagger: bool, optional

    :return: The computed Bott index.
    :rtype: float

    :raises np.linalg.LinAlgError: If either of the matrices ``U`` or ``V`` is
        not invertible.
    """
    if not dagger:
        try:
            u_inv = np.linalg.inv(u_mat)
            v_inv = np.linalg.inv(v_mat)
        except Exception as exc:
            raise np.linalg.LinAlgError(
                "U or V not invertible, can't compute Bott index."
            ) from exc
        ebott = np.linalg.eigvals(u_mat @ v_mat @ u_inv @ v_inv)

    else:
        ebott = np.linalg.eigvals(u_mat @ v_mat @ np.conj(u_mat.T) @ np.conj(v_mat.T))

    cbott = np.sum(np.log(ebott)) / (2 * np.pi)

    return np.imag(cbott)


def all_bott(
    lattice,
    ham,
    orb=1,
    dagger=False,
    energy_max=0,
):

    """
    Compute the Bott index for a given Hamiltonian and lattice for all energy levels
    or up to a specified limit.

    This function calculates the Bott index for each energy state in the system,
    from the lowest to the highest energy state, unless a stopping point is specified
    via the `energy_max` parameter.

    The Bott index is computed for each eigenstate, and its evolution can be tracked
    across the energy spectrum of the system.

    :param lattice: Array of shape ``(N_sites, 2)`` containing the coordinates
        of the lattice sites.
    :type lattice: ndarray

    :param ham: Hamiltonian matrix of shape ``(orb * N_sites, orb * N_sites)``.
        The Hamiltonian must be Hermitian.
    :type ham: ndarray

    :param orb: Number of orbitals considered per lattice site. Default is ``1``.
    :type orb: int, optional

    :param dagger: If ``True``, computes the Bott index using the Hermitian conjugate
        (dagger) of the projected position operators. If ``False``, computes using
        the inverse of the position operators. Default is ``False``.
    :type dagger: bool, optional

    :param energy_max: The maximum energy to consider. If not ``0``, the function
        will compute the Bott index only for eigenstates with energy less than
        ``energy_max``. Default is ``0``, meaning the function computes the Bott
        index for all energy levels.
    :type energy_max: float, optional

    :return: A dictionary where the keys are the energy values and the values
        are the corresponding Bott index calculated for each energy level.
    :rtype: dict

    :raises ValueError: If the Hamiltonian is not Hermitian.

    .. note::
        The function iterates over all the eigenstates (or up to the specified limit)
        and computes the Bott index for each state. This allows one to track the
        evolution of the topological properties of the system across its entire energy
        spectrum. This is particularly useful in systems with energy-dependent
        topological transitions.
    """
    if not np.allclose(ham, ham.conj().T):
        raise ValueError(
            "Hamiltonian must be Hermitian. Use 'bott_vect' for non-Hermitian matrices."
        )

    n_sites = np.size(lattice, 0)

    evals, evects = np.linalg.eigh(ham)

    u_proj, v_proj = compute_uv(lattice, evects, n_sites, orb)

    botts = {}

    if energy_max != 0:
        n_sites = np.searchsorted(evals, energy_max)

    with tqdm(
        total=n_sites, desc="Calculating BI for multiple energy levels"
    ) as progress_bar:
        for k in range(n_sites):
            uk, vk = u_proj[0:k, 0:k], v_proj[0:k, 0:k]
            if dagger:
                ebott, _ = np.linalg.eig(uk @ vk @ np.conj(uk.T) @ np.conj(vk.T))
            else:
                ebott, _ = np.linalg.eig(
                    uk @ vk @ np.linalg.inv(uk) @ np.linalg.inv(vk)
                )
            bott_value = np.imag(np.sum(np.log(ebott))) / (2 * np.pi)
            botts[evals[k]] = bott_value
            progress_bar.update(1)

    return botts


def all_bott_vect(lattice, evects, energies, orb=1, dagger=False, energy_max=np.inf):
    """
    Compute the Bott index for all energy levels or up to a specified limit.

    This function calculates the Bott index for each energy state in the system,
    sequentially from the lowest to the highest energy state, unless a stopping
    point is specified via the `energy_max` parameter.

    :param lattice: Array of shape ``(N_sites, 2)`` containing the coordinates
        of the lattice sites.
    :type lattice: ndarray

    :param evects: Array of shape ``(orb * N_sites, orb * N_sites)`` containing
        the eigenvectors of the system.
    :type evects: ndarray

    :param energies: Array of shape ``(orb * N_sites,)`` containing the energy
        values corresponding to the eigenstates. These energies may differ
        from the eigenvalues of the Hamiltonian for more complex systems.
    :type energies: ndarray

    :param orb: Number of orbitals considered per lattice site. Default is ``1``.
    :type orb: int, optional

    :param dagger: If ``True``, computes the Bott index using the Hermitian conjugate
        (dagger) of the projected position operators. If ``False``, computes using
        the inverse of the position operators. Default is ``False``.
    :type dagger: bool, optional

    :param energy_max: The maximum energy to consider. If not ``np.inf``, the
        calculation will only be performed for eigenstates with energy less than
        ``energy_max``. Default is ``np.inf``, meaning the function computes the
        Bott index for all energy levels.
    :type energy_max: float, optional

    :return: A dictionary where the keys are the energy values and the values
        are the corresponding Bott index calculated for each energy level.
    :rtype: dict

    :raises ValueError: If the Hamiltonian is not Hermitian.

    .. note::
        The function iterates over all the eigenstates (or up to the specified limit)
        and computes the Bott index for each state. This allows one to track the
        evolution of the topological properties of the system across its entire energy
        spectrum. This is particularly useful in systems with energy-dependent
        topological transitions.
    """
    n_sites = np.size(lattice, 0)

    u_proj, v_proj = compute_uv(lattice, evects, n_sites, orb)

    botts = {}

    if energy_max != np.inf:
        n_sites = np.searchsorted(energies, energy_max)

    with tqdm(
        total=n_sites, desc="Calculating BI for multiple energy levels"
    ) as progress_bar:
        for k in range(n_sites):
            uk, vk = u_proj[0:k, 0:k], v_proj[0:k, 0:k]
            if dagger:
                ebott, _ = np.linalg.eig(uk @ vk @ np.conj(uk.T) @ np.conj(vk.T))
            else:
                ebott, _ = np.linalg.eig(
                    uk @ vk @ np.linalg.inv(uk) @ np.linalg.inv(vk)
                )
            bott_value = np.imag(np.sum(np.log(ebott))) / (2 * np.pi)
            botts[energies[k]] = bott_value
            progress_bar.update(1)

    return botts


def phase_diagram(
    lattice, ham_function, p1, p2, fermi_energy=0, name_of_file="phase_diagram.csv"
):
    """
    Generate a phase diagram by calculating the Bott index for each pair of parameters in p1 and p2.

    This function calculates the Bott index for each pair of parameter values from `p1` and `p2`
    and generates a phase diagram. The results are saved in a CSV file, with columns for `p1`,
    `p2`, and the corresponding Bott index.

    :param lattice: Array of shape ``(N_sites, 2)`` containing the coordinates of the lattice sites.
    :type lattice: ndarray

    :param ham_function: Callable function that generates the Hamiltonian matrix given the parameters.
        It should have the signature ``ham_function(param1, param2)`` and return the Hamiltonian matrix.
    :type ham_function: callable

    :param p1: List of values for the first parameter to vary in the phase diagram.
    :type p1: list

    :param p2: List of values for the second parameter to vary in the phase diagram.
    :type p2: list

    :param fermi_energy: The Fermi energy at which to calculate the Bott index. Default is ``0``.
    :type fermi_energy: float, optional

    :param name_of_file: Name of the output CSV file where the phase diagram will be saved.
        Default is ``"phase_diagram.csv"``.
    :type name_of_file: str, optional

    :return: None
    :rtype: None

    :output: A CSV file containing the phase diagram with columns for `p1`, `p2`, and the corresponding Bott index.

    .. note::
        This function iterates over each combination of values from `p1` and `p2`, calculates the Bott
        index for each pair, and writes the results to the specified CSV file. The resulting file can
        be used to visualize the topological phases as a function of the two parameters.
    """
    with open(name_of_file, mode="w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["p1", "p2", "Bott Index"])

        total_iterations = len(p1) * len(p2)

        with tqdm(
            total=total_iterations, desc="Calculating Phase Diagram"
        ) as progress_bar:
            for param1 in p1:
                for param2 in p2:
                    hamiltonian = ham_function(param1, param2)
                    try:
                        bott_index = bott(lattice, hamiltonian, fermi_energy)
                    except Exception as e:
                        print(
                            f"Error computing Bott index for p1={param1}, p2={param2}: {e}"
                        )
                        bott_index = np.nan

                    writer.writerow([param1, param2, bott_index])
                    progress_bar.update(1)

    print(f"Phase diagram saved as '{name_of_file}'.")


def phase_diagram_disorder(
    ham_lattice_function,
    disorder,
    energies,
    name_of_file="phase_diagram_disorder.csv",
    n_realisations=1,
):
    """
    Generate a phase diagram by calculating the averaged Bott index over multiple disorder realizations
    for a range of energy levels.

    This function computes the Bott index for a series of energy levels and disorder strengths,
    averaging the results over multiple disorder realizations. The phase diagram is saved to a CSV file.

    :param ham_lattice_function: Callable function that generates the lattice and Hamiltonian matrix
        given a disorder parameter. It should have the signature ``ham_lattice_function(disorder_value)``
        and return a tuple ``(lattice, hamiltonian)``.
    :type ham_lattice_function: callable

    :param disorder: A list of disorder strength values to use in generating the Hamiltonian.
    :type disorder: list

    :param energies: A list of energy levels at which the Bott index will be calculated.
    :type energies: list

    :param name_of_file: The name of the output CSV file where the phase diagram will be saved.
        Default is ``"phase_diagram_disorder.csv"``.
    :type name_of_file: str, optional

    :param n_realisations: Number of disorder realizations to compute for each pair of
        (disorder, energy) values. The average Bott index over all realizations will be saved in
        the CSV file. Default is 1.
    :type n_realisations: int, optional

    :return: None
    :rtype: None

    :output: Writes a CSV file with columns "energy", "disorder", and the averaged Bott index
        over all realizations for each combination of disorder and energy.

    .. note::
        The function outputs a progress bar showing the progress of the calculations across disorder values.
    """
    with open(name_of_file, mode="w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["energy", "disorder", "Bott Index"])

        total_iterations = len(disorder) * n_realisations

        with tqdm(
            total=total_iterations, desc="Calculating Phase Diagram"
        ) as progress_bar:
            bott_averages = {
                energy: {r_disorder: [] for r_disorder in disorder}
                for energy in energies
            }

            for _ in range(n_realisations):
                for r_disorder in disorder:
                    # Generate lattice and Hamiltonian for the current disorder realization
                    lattice, hamiltonian = ham_lattice_function(r_disorder)

                    try:
                        # Calculate Bott indices for all energy levels up to the maximum specified
                        all_bott_index = all_bott(
                            lattice, hamiltonian, energy_max=np.max(energies)
                        )
                    except Exception as e:
                        print(
                            f"Error computing Bott index for disorder={r_disorder}, max_energy={np.max(energies)}: {e}"
                        )
                        for energy in energies:
                            bott_averages[energy][r_disorder].append(np.nan)
                        continue

                    for energy in energies:
                        bott_index = get_nearest_value(all_bott_index, energy)
                        bott_averages[energy][r_disorder].append(bott_index)

                    progress_bar.update(1)

            # Calculate and save the average Bott index over all realizations for each (energy, disorder) pair
            for energy in energies:
                for r_disorder in disorder:
                    average_bott_index = np.nanmean(bott_averages[energy][r_disorder])
                    writer.writerow([energy, r_disorder, average_bott_index])

    print(f"Phase diagram saved as '{name_of_file}'.")


def plot_phase_diagram(
    filename="phase_diagram.csv",
    title_fig="Phase Diagram",
    save_fig="phase_diagram.pdf",
    xkey="p2",
    ykey="p1",
    xlabel="p2",
    ylabel="p1",
    colorbar_label="Bott Index",
    fontsize=20,
    cmap="coolwarm",
):
    """
    Plot a phase diagram from a CSV file generated by the `phase_diagram` function.

    This function reads a CSV file containing the phase diagram data (with columns 'p1', 'p2', and 'Bott Index')
    and generates a heatmap plot. The phase diagram can be saved as a figure in PDF format.

    :param filename: The name of the CSV file to read, which contains columns 'p1', 'p2', and 'Bott Index'.
        Default is ``"phase_diagram.csv"``.
    :type filename: str, optional

    :param title_fig: The title of the plot. Default is ``"Phase Diagram"``.
    :type title_fig: str, optional

    :param save_fig: The name of the file to save the plot. Default is ``"phase_diagram.pdf"``.
    :type save_fig: str, optional

    :param xkey: The key for the x-axis data in the CSV file. Default is ``"p2"``.
    :type xkey: str, optional

    :param ykey: The key for the y-axis data in the CSV file. Default is ``"p1"``.
    :type ykey: str, optional

    :param xlabel: Label for the x-axis. Default is ``"p2"``.
    :type xlabel: str, optional

    :param ylabel: Label for the y-axis. Default is ``"p1"``.
    :type ylabel: str, optional

    :param colorbar_label: Label for the colorbar. Default is ``"Bott Index"``.
    :type colorbar_label: str, optional

    :param fontsize: Size of all the fonts in the plot. Default is 20.
    :type fontsize: int, optional

    :param cmap: The colormap to use for the heatmap. Default is ``"coolwarm"``.
    :type cmap: str, optional

    :return: None
    :rtype: None

    :output: Displays a heatmap plot of the phase diagram, with an option to save the plot as a PDF file.

    .. note::
        The function assumes that the input CSV file contains the following columns: 'p1', 'p2', and 'Bott Index'.
    """
    data = pd.read_csv(filename)
    phase_data = data.pivot(index=ykey, columns=xkey, values="Bott Index")

    plt.figure(figsize=(8, 6))

    aspect_ratio = (data[xkey].max() - data[xkey].min()) / (
        data[ykey].max() - data[ykey].min()
    )
    plt.imshow(
        phase_data,
        origin="lower",
        extent=[data[xkey].min(), data[xkey].max(), data[ykey].min(), data[ykey].max()],
        aspect=str(aspect_ratio),
        cmap=cmap,
    )

    cbar = plt.colorbar()
    cbar.set_label(colorbar_label, size=fontsize)
    cbar.ax.tick_params(labelsize=fontsize)
    plt.xlabel(xlabel, fontsize=fontsize)
    plt.ylabel(ylabel, fontsize=fontsize)
    plt.title(title, fontsize=fontsize)
    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    plt.savefig(save_fig, format="pdf", bbox_inches="tight")
    plt.show()
