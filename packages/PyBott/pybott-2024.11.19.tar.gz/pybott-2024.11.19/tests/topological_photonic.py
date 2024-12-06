import matplotlib.pyplot as plt
import numpy as np

from rich import traceback
traceback.install()

import sys
sys.path.append("../../chapter-2-thesis/code")
import lattice_r as lr
sys.path.append("../../chapter-4-thesis/code")
import Gd

from localizer import calculate_line_li, plot_heatmap, localizer_index

if __name__ == "__main__":
    n_side = 200
    delta_b = 12
    delta_ab = 0
    k0 = 2*np.pi*0.05
    
    lattice = lr.generate_hex_hex_stretch(n=n_side, a=1, φ=0)
    ham = Gd.create_matrix_TE(lattice, delta_b, delta_ab, k0)
    n_sites = lattice.shape[0]
    # x,y = lattice.T
    # plt.scatter(x,y,color="black")
    # plt.show()

    class_az = 'A2D'
    lambda_param = np.array([0,0,0])
    kappa = 10
    params = { "lattice" : lattice,
               "ham" : ham,
               "class_az" : class_az,
               "lambda_param" : lambda_param,
               "kappa" : kappa
               }

    # plot_heatmap(params, 30, 8)
    # exit()
    
    delta_b_values = np.linspace(-12,12,24)
    delta_ab_values = np.linspace(-12,12,24)
    li_values = np.zeros((len(delta_b_values), len(delta_ab_values)))

    for i, delta_b in enumerate(delta_b_values):
        for j, delta_ab in enumerate(delta_ab_values):
            ham = Gd.create_matrix_TE(lattice, delta_b, delta_ab, k0)
            li = localizer_index(lattice, ham, kappa=kappa)
            li_values[i, j] = li
            print(f"{delta_b},{delta_ab=},{li=}")

    # plt.figure(figsize=(8, 6))
    plt.imshow(li_values, extent=(delta_ab_values[0], delta_ab_values[-1], delta_b_values[0], delta_b_values[-1]), 
               origin='lower', aspect='auto', cmap='coolwarm')
    # plt.colorbar(label="Localizer Index (li)",fontsize=20)
    plt.xlabel(r"$\Delta_{AB}$",fontsize=20)
    plt.ylabel(r"$\Delta_{B}$",fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.title(f"$N={n_sites}\\quad \\kappa={kappa}\\quad \\lambda = 0$",fontsize=20)
    plt.savefig(f"topological_photonic_pd_{kappa}.pdf",format="pdf",bbox_inches='tight')
    plt.show()
    exit()


    plt.scatter(delta_b_values, li_values, color="black")
    plt.xlabel(r"$\Delta_{\mathrm{B}}$",fontsize=20)
    plt.ylabel("Localizer index A2D",fontsize=20)
    plt.title(f"$N={n_sites}\\quad \\kappa={kappa}\\quad \\lambda = 0$",fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.savefig(f"topological_photonic_{kappa}.pdf",format="pdf",bbox_inches='tight')
    plt.show()
    exit()
    
    x0_min = -10
    x0_max = 10
    x0_ndots = 20
    x0_values, li_values = calculate_line_li(params, x0_min=x0_min, x0_max=x0_max, x0_ndots=x0_ndots, which_param=0)
    plt.scatter(x0_values, li_values, color="black")
    ham = Gd.create_matrix_TE(lattice, 0, 12, k0)
    params["ham"] = ham
    x0_values, li_values = calculate_line_li(params, x0_min=x0_min, x0_max=x0_max, x0_ndots=x0_ndots, which_param=0)
    plt.scatter(x0_values, li_values, color="red")
    plt.xlabel("",fontsize=20)
    plt.ylabel("",fontsize=20)
    plt.title("",fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.savefig(".pdf",format="pdf",bbox_inches='tight')
    plt.show()
    exit()

