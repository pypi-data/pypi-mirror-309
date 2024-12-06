from pythtb import *
import numpy as np
import matplotlib.pyplot as plt

from localizer import localizer_index, dual, calculate_line_li

import sys
sys.path.append("../../chapter-2-thesis/code")
import lattice_r as lr
sys.path.append("../../chapter-5-thesis/code")
import kekule_tb_real as ktbr

from rich import traceback
traceback.install()

plt.rc("text", usetex=True)
plt.rc("font", family="serif", serif="Computer Modern")

def kekule_model(t1=1, t2=1.5, n_side=10, pbc=True):
    lat = [[3*np.sqrt(3), 0], [0, 3]]

    orb = [
        [2/np.sqrt(3), 0.0],       # Site 0
        [1/np.sqrt(3), 1.0],       # Site 1
        [-1/np.sqrt(3), 1],        # Site 2
        [-2/np.sqrt(3), 0.0],       # Site 3    
        [-1/np.sqrt(3), -1.0],     # Site 4
        [1/np.sqrt(3), -1.0]      # Site 5
    ]

    model = tb_model(2, 2, lat, orb)

    intra_hoppings = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0)
    ]

    for (i, j) in intra_hoppings:
        model.set_hop(t1, i, j, [0, 0])

    b = 2*np.sqrt(3)
    inter_hoppings = [(0,3,[b,0]), (1,4,[b/2,b]), (2,5,[-b/2,b])]

    for (i, j, R) in inter_hoppings:
        model.set_hop(t2, i, j, R)

    # cutout finite model first along direction x
    tmp_model = model.cut_piece(n_side, 0, glue_edgs=pbc)
    # cutout also along y direction
    fin_model = tmp_model.cut_piece(n_side, 1, glue_edgs=pbc)

    return fin_model.get_orb(), fin_model._gen_ham()

        
# Optionnel : Calcul et visualisation de la structure de bande
# nk = 100
# path = [[0.0, 0.0], [0, 1/b/2], [0.25/b, 0.25/b],  [0.0, 0.0]]
# label = (r"$\Gamma$", r"$M$", r"$K$", r"$\Gamma$")
# (k_vec, k_dist, k_node) = model.k_path(path, nk)

# Calcul des énergies pour chaque vecteur k
# evals = model.solve_all(k_vec)

# Tracé des bandes d'énergie


# # for i in range(len(evals[0])):
# #     plt.plot(k_dist, [evals[k][i] for k in range(nk)], color='b')

# for i in range(len(evals[0])):
#     plt.plot(k_dist, [eval[i] for eval in evals], color='b')

# (fig,ax)=model.visualize(0,1)
# ax.set_title("Graphene, bulk")
# ax.set_xlabel("x coordinate")
# ax.set_ylabel("y coordinate")
# fig.tight_layout()
# plt.show()
# exit()

# plt.figure(figsize=(8, 6))
# for i in range(6):
#     plt.plot(k_dist, evals[i,:])
    
# for n in range(len(k_node)):
#     plt.axvline(x=k_node[n], color='k', linestyle='--')
# plt.xticks(k_node, label)
# plt.xlabel("Chemin dans l'espace réciproque")
# plt.ylabel("Energie (eV)")
# plt.title("Structure de bande du modèle de Kekulé")
# plt.show()

# (evals, evects) = fin_model.solve_all(eig_vectors=True)


# lattice = fin_model.get_orb()
# lattice_x2 = np.concatenate([lattice, lattice])

# from dos import plot_dos

# plot_dos(evals)

def get_sigma():
    return 1j/np.sqrt(3) * np.array([[0,1,0,0,0,-1],
                                      [-1,0,1,0,0,0],
                                      [0,-1,0,1,0,0],
                                      [0,0,-1,0,1,0],
                                      [0,0,0,-1,0,1],
                                      [1,0,0,0,-1,0]])

# n_cluster = ham.shape[0]//6

# from pybott import spin_bott

# sigma = np.kron(np.eye(n_cluster),get_sigma())

def kekule_model_perso(t1=1, t2=1.5, n_side=10):    
    lattice = lr.generate_hex_grid_stretch(N_cluster_side=n_side, a=1, φ=0)
    ham = ktbr.create_tb_matrix_six_cell_obc(lattice,t1=t1,t2=t2)
    # ham = ktbr.create_tb_matrix_six_cell_pbc(lattice,t1=t1,t2=t2)
    return lattice, ham


# evals, evects = np.linalg.eigh(ham)
# n_cluster = ham.shape[0]//6
# sigma = np.kron(np.eye(n_cluster),get_sigma())
# c_sb = spin_bott(lattice, evals, evects.T, sigma, fermi_energy=0, threshold_bott=-0.2, plot_psp=True)

# print(f"{c_sb=}")




if __name__ == "__main__":
    n_side = 4
    lattice, ham = kekule_model_perso(t1=1, t2=0.9, n_side=n_side)
    n_sites = lattice.shape[0]
    class_az = 'AII2D'
    lambda_param = np.array([0,0,0])
    kappa = 0.9
    params = { "lattice" : lattice,
               "ham" : ham,
               "class_az" : class_az,
               "lambda_param" : lambda_param,
               "kappa" : kappa
               }
    # x0_values, li_values = calculate_line_li(params, x0_min=-2, x0_max=2, x0_ndots=20)
    # plt.scatter(x0_values, li_values, color="black")
    # lattice, ham = kekule_model_perso(t1=1, t2=1.5, n_side=n_side)
    # params["ham"] = ham
    # x0_values, li_values = calculate_line_li(params, x0_min=-2, x0_max=2, x0_ndots=20)
    # plt.scatter(x0_values, li_values, color="red")
    
    # plt.show()
    # exit()
    
    lis = []
    t2s = np.linspace(0.5, 2, 20)
    lambda_param = np.array([0,0,1])
    for t2 in t2s:
        # lattice, ham = kekule_model(t1=1, t2=t2, n_side=8, pbc=True)
        lattice, ham = kekule_model_perso(t1=1, t2=t2, n_side=n_side)
        print(f"dim={ham.shape[0]}")
        li = localizer_index(lattice, ham, class_az='AII2D', kappa=kappa)
        lis.append(li)
        print(f"t2={np.round(t2,2)},li={li}")

    plt.scatter(t2s, lis, color="black")
    plt.xlabel(r"$t_2$",fontsize=20)
    plt.ylabel(r"Localizer index AII2D",fontsize=20)
    plt.title(f"$N={n_sites}\\quad \\kappa={kappa}$",fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.savefig(f"li_kekule_{kappa}_{n_sites}.pdf",format="pdf",bbox_inches='tight')
    plt.show()
