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
input_file_path = sys.argv[1]+'/K_SAMPLING_CONVERGENCE_TEST_ENERGY_and_LATT_PARAMETERS.txt'
#input_file_path="/home/lebedmi2/VASP_calculations_ALL/test_only"+'/output.txt'
with open(input_file_path, 'r') as file:
    lines = file.readlines()

# Add the new value to the last line

structure = calc.structure.to_dict()
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
    change = round(calc.energy.to_numpy() - max_value,4) 
    change = f"+{change:.4f}" if calc.energy.to_numpy() - max_value >= 0 else f"{change:.4f}"
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
    lines[-1] = "{} {} {} {} {}\t{} {}\t{} {} {} {} {} {}\t{} {} {} {} {} {}\n".format(str(k_spacing), str(k_a_stars), str(k_b_stars), str(k_c_stars), str(time_trails), str(f"{rounded_energy:.7f}"), str("+0.0000"), 
    str(para_a), str(para_b),str(para_c), str(alpha), str(beta), str(gamma), 
    str("+0.00000"), str("+0.00000"), str("+0.00000"), str("+0.000"), str("+0.000"), str("+0.000"))
    #lines[-1] = lines[-1].strip() + ' ' + str(round(calc.energy.to_numpy(), 7)) + ' 0.0000 ' + str(time_trails) + '\n'
    print("Correctly written to the output file")
with open(input_file_path, 'w') as file:
    file.writelines(lines)
print("I have finished! Gimme more work!")


