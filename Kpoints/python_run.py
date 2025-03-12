from py4vasp import Calculation
import sys
import re
import math
import numpy as np
import matplotlib.pyplot as plt

pattern = r"ENCUT"


# Get the input value from the command-line argument
input_value = sys.argv[1]
print("DIRECTORY: {}".format(input_value))
calc = input_value
calc=Calculation.from_path(input_value)

# Read the existing values from the input file
input_file_path = sys.argv[1]+'/K_SAMPLING_CONVERGENCE_TEST_ENERGY_and_LATT_PARAMETERS.txt'
#input_file_path="/home/lebedmi2/VASP_calculations_ALL/test_only"+'/output.txt'
with open(input_file_path, 'r') as file:
    lines = file.readlines()

# Add the new value to the last line

structure = calc.structure.to_dict()
number_of_atoms = float(calc.structure.number_atoms()) #====== NEW
print(structure['lattice_vectors'])
para_a = math.sqrt(np.dot(structure['lattice_vectors'][0], structure['lattice_vectors'][0]))

para_b = math.sqrt(np.dot(structure['lattice_vectors'][1], structure['lattice_vectors'][1]))
para_b = round(para_b, 5)
para_c = math.sqrt(np.dot(structure['lattice_vectors'][2], structure['lattice_vectors'][2]))
para_c = round(para_c, 5)
alpha = math.degrees(math.acos((np.dot(structure['lattice_vectors'][1], structure['lattice_vectors'][2])) / (para_b * para_c))) #b a c
beta = math.degrees(math.acos(
    (np.dot(structure['lattice_vectors'][0], structure['lattice_vectors'][2])) / (para_a * para_c)))  # a a c
gamma = math.degrees(math.acos(
    (np.dot(structure['lattice_vectors'][0], structure['lattice_vectors'][1])) / (para_a * para_b)))  # a a b
#para_a = f"{round(para_a, 5):.5f}"
#para_b = f"{round(para_b, 5):.5f}"
#para_c = f"{round(para_c, 5):.5f}"
#alpha = f"{round(alpha, 3):.5f}"
#beta = f"{round(beta, 3):.5f}"
#gamma = f"{round(gamma, 3):.5f}"
#RECIPROCAL LATTICE VECTORS
volume = para_a*para_b*para_c*math.sqrt( 1-math.cos(math.radians(alpha))**2 - math.cos(math.radians(beta))**2 - math.cos(math.radians(gamma))**2 
+ 2*math.cos(math.radians(alpha))*math.cos(math.radians(beta))*math.cos(math.radians(gamma)) )
a_stars =para_b*para_c*math.sin(math.radians(alpha))/volume
b_stars =para_a*para_c*math.sin(math.radians(beta))/volume
c_stars =para_a*para_b*math.sin(math.radians(gamma))/volume
k_spacing=float(sys.argv[3])
print("K_SPACING: {} {} {}".format(a_stars/k_spacing,b_stars/k_spacing,c_stars/k_spacing))
#k_a_stars = round(a_stars/k_spacing,0)
#k_b_stars = round(b_stars/k_spacing,0)
#k_c_stars = round(c_stars/k_spacing,0)
k_a_stars = a_stars/k_spacing
if int(k_a_stars)>=1:
	k_a_stars = int(k_a_stars) if (k_a_stars - int(k_a_stars)<= 0.4) else int(k_a_stars)+1
else:
	k_a_stars=1
k_b_stars = b_stars/k_spacing
if int(k_b_stars)>=1:
	k_b_stars = int(k_b_stars) if (k_b_stars - int(k_b_stars)<= 0.4) else int(k_b_stars)+1
else:
	k_b_stars=1
k_c_stars = c_stars/k_spacing
if int(k_c_stars)>=1:
	k_c_stars = int(k_c_stars) if (k_c_stars - int(k_c_stars)<= 0.4) else int(k_c_stars)+1
else:
	k_c_stars=1
print("K_SPACING ZAOKROUHLENO: {} {} {}".format(k_a_stars,k_b_stars,k_c_stars))

# Save the modified content back to the input file
if len(lines)>2:
    old_value=lines[1].split()
    print("OLD VAL============= {}".format(old_value))
    max_value = float(old_value[5])
    change = round((calc.energy.to_numpy() - max_value) / number_of_atoms,5) 
    change = f"+{change:.5f}" if calc.energy.to_numpy() - max_value >= 0 else f"{change:.5f}"
    best_lat_a = float(old_value[7])
    best_lat_b = float(old_value[8])
    best_lat_c = float(old_value[9])
    best_alpha = float(old_value[10])
    best_beta= float(old_value[11])
    best_gamma = float(old_value[12])
    change_lat_a = f"+{round(para_a - best_lat_a,5):.5f}" if para_a - best_lat_a >= 0 else f"{round(para_a - best_lat_a,5):.5f}"
    change_lat_b = f"+{round(para_b - best_lat_b,5):.5f}" if para_b - best_lat_b >= 0 else f"{round(para_b - best_lat_b,5):.5f}"
    change_lat_c = f"+{round(para_c - best_lat_c,5):.5f}" if para_c - best_lat_c >= 0 else f"{round(para_c - best_lat_c,5):.5f}"
    change_alpha = f"+{round(alpha - best_alpha,3):.3f}" if alpha - best_alpha >= 0 else f"{round(alpha - best_alpha,3):.3f}"
    change_beta = f"+{round(beta - best_beta,3):.3f}" if beta - best_beta >= 0 else f"{round(beta - best_beta,3):.3f}"
    change_gamma= f"+{round(gamma - best_gamma,3):.3f}" if gamma - best_gamma >= 0 else f"{round(gamma - best_gamma,3):.3f}"
    para_a = f"{round(para_a, 5):.5f}"
    para_b = f"{round(para_b, 5):.5f}"
    para_c = f"{round(para_c, 5):.5f}"
    alpha = f"{round(alpha, 3):.3f}"
    beta = f"{round(beta, 3):.3f}"
    gamma = f"{round(gamma, 3):.3f}"
    k_spacing=f"{round(k_spacing, 3):.3f}"
    
    time_trails=round(float(sys.argv[2]) / 60, 2)
    time_trails = f"{time_trails:.2f}"
    rounded_energy = np.round(calc.energy.to_numpy(), 7)
    lines[-1] = "{} {} {} {} {}\t{} {}\t{} {} {} {} {} {}\t{} {} {} {} {} {}\n".format(str(k_spacing), str(k_a_stars), str(k_b_stars), str(k_c_stars), str(time_trails),   str(f"{rounded_energy:.7f}"), str(change), 
    str(para_a), str(para_b),str(para_c), str(alpha), str(beta), str(gamma), 
    str(change_lat_a), str(change_lat_b), str(change_lat_c), str(change_alpha), str(change_beta), str(change_gamma))
    print("Correctly written to the output file")
else:
    para_a = f"{round(para_a, 5):.5f}"
    para_b = f"{round(para_b, 5):.5f}"
    para_c = f"{round(para_c, 5):.5f}"
    alpha = f"{round(alpha, 3):.3f}"
    beta = f"{round(beta, 3):.3f}"
    gamma = f"{round(gamma, 3):.3f}"
    k_spacing=f"{round(k_spacing, 3):.3f}"
    time_trails=round(float(sys.argv[2]) / 60, 2)
    time_trails = f"{time_trails:.2f}"
    rounded_energy = np.round(calc.energy.to_numpy(), 7)
    lines[-1] = "{} {} {} {} {}\t{} {}\t{} {} {} {} {} {}\t{} {} {} {} {} {}\n".format(str(k_spacing), str(k_a_stars), str(k_b_stars), str(k_c_stars), str(time_trails), str(f"{rounded_energy:.7f}"), str("+0.00000"), 
    str(para_a), str(para_b),str(para_c), str(alpha), str(beta), str(gamma), 
    str("+0.00000"), str("+0.00000"), str("+0.00000"), str("+0.000"), str("+0.000"), str("+0.000"))
    #lines[-1] = lines[-1].strip() + ' ' + str(round(calc.energy.to_numpy(), 7)) + ' 0.0000 ' + str(time_trails) + '\n'
    print("Correctly written to the output file")
with open(input_file_path, 'w') as file:
    file.writelines(lines)


file_name = "K_SAMPLING_CONVERGENCE_TEST_ENERGY_and_LATT_PARAMETERS.txt"
output_image = "Kpoints_plot.png"  # Name of the output image file

k_sampling = []
k_grid = []
ener_diff_per_atom = []
elapsed_time = []

# Read the file
with open(file_name, "r") as file:
    lines = file.readlines()

    # Skip the header (first line)
    for line in lines[1:]:
        columns = line.split()

        # Extract relevant values
        k_sampling.append(float(columns[0]))  # k-spacing [A^-1]
        k_grid.append(f"{columns[1]}x{columns[2]}x{columns[3]}")  # k_a x k_b x k_c grid
        elapsed_time.append(float(columns[4]))  # Elapsed Time [min]
        ener_diff_per_atom.append(abs(float(columns[6])))  # Absolute Energy Difference per Atom [eV]

filtered_data = [(k_sampling[0], k_grid[0], elapsed_time[0], ener_diff_per_atom[0])] + [
    (k, g, t, e) for k, g, t, e in zip(k_sampling[1:], k_grid[1:], elapsed_time[1:], ener_diff_per_atom[1:])
    if t != 0 and e != 0
]


k_sampling_filtered, k_grid_filtered, elapsed_time_filtered, ener_diff_per_atom_filtered = zip(*filtered_data)

# Create custom x-axis labels combining k-sampling values and k-grid sizes
x_labels_filtered = [f"{k} ({g})" for k, g in zip(k_sampling_filtered, k_grid_filtered)]
x_positions = range(len(k_sampling_filtered))


fig, ax1 = plt.subplots(figsize=(8, 5))
ax1.axhline(y=0.001, color='#ADD8E6', linestyle='--', linewidth=2, label="Threshold 1 meV/atom")
ax1.text(x=max(x_positions), y=0.0015 - 0.00005, s="Threshold\n1 meV/atom", color='gray', fontsize=10, ha='left')
ax1.axhline(y=0.000, color='#ADD8E6', linestyle='--', linewidth=1)

# Plot Energy Difference per Atom
ax1.plot(x_positions, ener_diff_per_atom_filtered, marker='o', linestyle='-', color='b', label="Energy Difference per Atom", zorder=2)
ax1.set_xlabel("K-Spacing (Monkhorst-Pack grid) [Å$^{-1}$]")
ax1.set_ylabel("Energy Difference per Atom [eV]", color='b')
ax1.tick_params(axis='y', labelcolor='b')
ax1.invert_xaxis()
ax1.set_ylim(-0.001, 0.015)

# Create a second y-axis for elapsed time
ax2 = ax1.twinx()
ax2.plot(x_positions, elapsed_time_filtered, marker='s', linestyle='--', color='g', label="Elapsed Time", alpha=0.5)
ax2.set_ylabel("Elapsed Time [min]", color='g')
ax2.tick_params(axis='y', labelcolor='g')


ax1.set_xticks(x_positions)
ax1.set_xticklabels(x_labels_filtered, rotation=45, ha="right")

fig.tight_layout()
plt.savefig(output_image, dpi=300, bbox_inches='tight')



