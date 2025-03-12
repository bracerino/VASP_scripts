from py4vasp import Calculation
import sys
import re
import math
import numpy as np
pattern = r"ENCUT"


# Get the input value from the command-line argument
input_value = sys.argv[1]
print("DIRECTORY: {}".format(input_value))
calc = input_value
calc=Calculation.from_path(input_value)

# Read the existing values from the input file
input_file_path = sys.argv[1]+'/ENCUT_CONVERGENCE_TEST_ENERGY_and_LATT_PARAMETERS.txt'
#input_file_path="/home/lebedmi2/VASP_calculations_ALL/test_only"+'/output.txt'
with open(input_file_path, 'r') as file:
    lines = file.readlines()

# Add the new value to the last line

structure = calc.structure.to_dict()
number_of_atoms = float(calc.structure.number_atoms()) #======== NEW
print(" NUMBER OF ATOOOOOOOOOOOOOOMS {}".format(number_of_atoms))
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

# Save the modified content back to the input file
if len(lines)>2:
    old_value=lines[1].split()
    print("OLD VAL============= {}".format(old_value))
    max_value = float(old_value[2])
    change = round((calc.energy.to_numpy() - max_value) / number_of_atoms,5) # ======== NEW
    change = f"+{change:.5f}" if calc.energy.to_numpy() - max_value >= 0 else f"{change:.5f}"
    best_lat_a = float(old_value[4])
    best_lat_b = float(old_value[5])
    best_lat_c = float(old_value[6])
    best_alpha = float(old_value[7])
    best_beta= float(old_value[8])
    best_gamma = float(old_value[9])
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
    
    time_trails=round(float(sys.argv[2]) / 60, 2)
    time_trails = f"{time_trails:.2f}"
    rounded_energy = np.round(calc.energy.to_numpy(), 7) 
    print("ROUNDED DIFFERENCE: {}".format(rounded_energy))
    lines[-1] = "{} {}\t{} {}\t{} {} {} {} {} {}\t{} {} {} {} {} {}\n".format(lines[-1].strip(), str(time_trails),  str(f"{rounded_energy:.7f}"), str(change), 
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
    time_trails=round(float(sys.argv[2]) / 60, 2)
    time_trails = f"{time_trails:.2f}"
    rounded_energy = np.round(calc.energy.to_numpy(), 7)
    lines[-1] = "{} {}\t{} {}\t{} {} {} {} {} {}\t{} {} {} {} {} {}\n".format(lines[-1].strip(), str(time_trails), str(f"{rounded_energy:.7f}"), str("+0.00000"), 
    str(para_a), str(para_b),str(para_c), str(alpha), str(beta), str(gamma), 
    str("+0.00000"), str("+0.00000"), str("+0.00000"), str("+0.000"), str("+0.000"), str("+0.000"))
    #lines[-1] = lines[-1].strip() + ' ' + str(round(calc.energy.to_numpy(), 7)) + ' 0.0000 ' + str(time_trails) + '\n'
    print("Correctly written to the output file")
with open(input_file_path, 'w') as file:
    file.writelines(lines)
import matplotlib.pyplot as plt


file_name = "ENCUT_CONVERGENCE_TEST_ENERGY_and_LATT_PARAMETERS.txt"
output_image = "Ecut_plot.png"  # Name of the output image file

ener_cutoff = []
ener_diff_per_atom = []
elapsed_time = []

with open(file_name, "r") as file:
    lines = file.readlines()
    # Skip the header
    for line in lines[1:]:
        columns = line.split()
        ener_cutoff.append(float(columns[0]))  # Energy Cutoff [eV]
        elapsed_time.append(float(columns[1]))  # Elapsed Time [min]
        ener_diff_per_atom.append(float(columns[3]))  # Energy Difference per Atom [eV]


fig, ax1 = plt.subplots(figsize=(8, 5))


ax1.plot(ener_cutoff, ener_diff_per_atom, marker='o', linestyle='-', color='b', label="Energy Difference per Atom")
ax1.set_xlabel("Energy Cutoff [eV]")
ax1.set_ylabel("Energy Difference per Atom [eV]", color='b')
ax1.tick_params(axis='y', labelcolor='b')


ax2 = ax1.twinx()
ax2.plot(ener_cutoff, elapsed_time, marker='s', linestyle='--', color='g', label="Elapsed Time")
ax2.set_ylabel("Elapsed Time [min]", color='g')
ax2.tick_params(axis='y', labelcolor='g')
ax1.axhline(y=0.001, color='#ADD8E6', linestyle='--', linewidth=3, label="Threshold (1 meV/atom)")
ax1.text(x=min(ener_cutoff), y=0.001 - 0.00005, s="Threshold (0.001 eV)", color='gray', fontsize=10, ha='left')


#ax1.grid(True)
fig.tight_layout()

# Save the plot as an image file
plt.savefig(output_image, dpi=300, bbox_inches='tight')
