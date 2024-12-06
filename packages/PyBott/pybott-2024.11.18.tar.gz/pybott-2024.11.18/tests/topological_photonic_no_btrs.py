import matplotlib.pyplot as plt
import numpy as np

from rich import traceback
traceback.install()

import sys
sys.path.append("../../chapter-2-thesis/code")
import lattice_r as lr
sys.path.append("../../chapter-4-thesis/code")
import Gd

from localizer import calculate_line_li, localizer_index

plt.rc("text", usetex=True)
plt.rc("font", family="serif", serif="Computer Modern")

if __name__ == "__main__":
    n_side = 200
    delta_b = 12
    delta_ab = 0
    k0 = 2*np.pi*0.05
    kappa = 10
    
    lattice = lr.generate_hex_hex_stretch(n=n_side, a=1, φ=0, s=1.01)        
    ham = Gd.create_matrix_TE_plates(lattice, 0, 0, k0, 3)
    # plt.imshow(np.abs(ham-np.conj(ham.T)))
    # plt.show()
    # evals, evects = np.linalg.eig(ham)
    # plt.scatter(np.real(evals), np.imag(evals))
    # plt.show()
    # exit()
    # print(ham.shape)
    # print(ham.shape[0] % 4)

    # exit()

    # size_hex_values = np.linspace(0.9, 1.1, 100)
    # li_values = []
    # for s in size_hex_values:
    #     lattice = lr.generate_hex_hex_stretch(n=n_side, a=1, φ=0, s=s)
    #     ham = Gd.create_matrix_TE_plates(lattice, 0, 0, k0, 3)
    #     li = localizer_index(lattice, ham, class_az='AII2D', lambda_param=np.array([0.2, 0, 10]), kappa=kappa)
    #     li_values.append(li)
    #     print(f"{s=},{li=}")

    # data = np.column_stack((size_hex_values, li_values))
    # np.savetxt("data.csv", data, delimiter=",", header="size_hex_values,li_values", comments='')

    data = np.loadtxt("li_tp_no_btrs.csv", delimiter=",", skiprows=1)
    data_sc = np.loadtxt("spin_chern_2.csv", delimiter=",", skiprows=1)
    size_hex_values = data[:, 0]
    li_values = data[:, 1]

    size_hex_values_sc = data_sc[:, 0]
    sc_values = data_sc[:, 1]

    n_sites = lattice.shape[0]

    plt.scatter(size_hex_values_sc, -sc_values, color="black", label="SC")
    plt.scatter(size_hex_values, li_values, color="red", label="LI")
    plt.xlabel(r"Size of the hexagon cell $R$",fontsize=20)
    plt.ylabel("Localizer index AII2D",fontsize=20)
    plt.title(f"$N={n_sites}\\quad \\kappa={kappa}$",fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.legend(fontsize=20)
    plt.savefig("li_tp_no_btrs.pdf",format="pdf",bbox_inches='tight')
    plt.show()
    exit()
    class_az = 'AII2D'
    lambda_param = np.array([0.2,0,-7])
    kappa = 10
    params = { "lattice" : lattice,
               "ham" : ham,
               "class_az" : class_az,
               "lambda_param" : lambda_param,
               "kappa" : kappa
               }
    x0_min = -1000
    x0_max = 1000
    x0_ndots = 50
    
    x0_values, li_values = calculate_line_li(params, x0_min=x0_min, x0_max=x0_max, x0_ndots=x0_ndots, which_param=0)
    plt.scatter(x0_values, li_values, color="black")
    lattice = lr.generate_hex_hex_stretch(n=n_side, a=1, φ=0, s=0.9)
    ham = Gd.create_matrix_TE(lattice, 0, 0, k0)
    params["ham"] = ham
    x0_values, li_values = calculate_line_li(params, x0_min=x0_min, x0_max=x0_max, x0_ndots=x0_ndots, which_param=0)
    plt.scatter(x0_values, li_values, color="red")
    plt.show()
    exit()

