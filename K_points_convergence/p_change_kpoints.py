from py4vasp import Calculation
import sys
import re
import math
import numpy as np


# Get the input value from the command-line argument
input_value = sys.argv[1]
print("DIRECTORY: {}".format(input_value))


# Read the existing values from the input file
input_file_path = sys.argv[1]+'/K_SAMPLING_CONVERGENCE_TEST_ENERGY_and_LATT_PARAMETERS.txt'
#input_file_path="/home/lebedmi2/VASP_calculations_ALL/test_only"+'/output.txt'
with open(input_file_path, 'r') as file:
    lines = file.readlines()

# Add the new value to the last line

#NEEDed to add if condition. If it is the first run of the VASP in the directory, OUTCAR does not exists, so py4vasp cannot be used. Then I need to read the structure data from the POSCAR in the first run of the loop
if int(sys.argv[3])>1:
	calc=Calculation.from_path(input_value)
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

	#RECIPROCAL LATTICE VECTORS
	volume = para_a*para_b*para_c*math.sqrt( 1-math.cos(math.radians(alpha))**2 - math.cos(math.radians(beta))**2 - math.cos(math.radians(gamma))**2 
	+ 2*math.cos(math.radians(alpha))*math.cos(math.radians(beta))*math.cos(math.radians(gamma)) )
	a_stars =para_b*para_c*math.sin(math.radians(alpha))/volume
	b_stars =para_a*para_c*math.sin(math.radians(beta))/volume
	c_stars =para_a*para_b*math.sin(math.radians(gamma))/volume
	k_spacing=float(sys.argv[2])
	#k_a_stars = str(round(a_stars/k_spacing,0)).rstrip('.0')
	#k_b_stars = str(round(b_stars/k_spacing,0)).rstrip('.0')
	#k_c_stars = str(round(c_stars/k_spacing,0)).rstrip('.0')
	k_a_stars = a_stars/k_spacing
	k_b_stars = b_stars/k_spacing
	k_c_stars = c_stars/k_spacing
	if int(k_a_stars)>=1:
		k_a_stars = int(k_a_stars) if (k_a_stars - int(k_a_stars)<= 0.4) else int(k_a_stars)+1
	else:
		k_a_stars=1
	if int(k_b_stars)>=1:
		k_b_stars = int(k_b_stars) if (k_b_stars - int(k_b_stars)<= 0.4) else int(k_b_stars)+1
	else:
		k_b_stars=1
	if int(k_c_stars)>=1:
		k_c_stars = int(k_c_stars) if (k_c_stars - int(k_c_stars)<= 0.4) else int(k_c_stars)+1
	else:
		k_c_stars=1
	print("K_SPACING: {} {} {}".format(k_a_stars,k_b_stars,k_c_stars))

	input_file_KPOINTS = sys.argv[1]+'/KPOINTS'
	with open(input_file_KPOINTS, 'r') as file:
	    lines = file.readlines()
	lines[3]= '{} {} {}\n'.format(k_a_stars,k_b_stars,k_c_stars)
	with open(input_file_KPOINTS,'w') as file:
	    file.writelines(lines)
else:
	# Define the input file path
	input_file =  sys.argv[1]+'/POSCAR'
	# Initialize an empty dictionary to store the data
	structure = {}
	# Read the input file and extract lines 3 to 5
	with open(input_file, 'r') as file:
		lines = file.readlines()[2:5]

	# Process and store the data in the dictionary
	for i, line in enumerate(lines, start=3):
		values = [float(val) for val in line.split()]
		structure[f'line_{i}'] = np.array(values)
		print(math.sqrt(np.dot(structure['line_3'],structure['line_3'])))
	# Print the dictionary with NumPy arrays
	para_a = math.sqrt(np.dot(structure['line_3'], structure['line_3']))
	para_b = math.sqrt(np.dot(structure['line_4'], structure['line_4']))
	para_b = round(para_b, 5)
	para_c = math.sqrt(np.dot(structure['line_5'], structure['line_5']))
	para_c = round(para_c, 5)
	alpha = math.degrees(math.acos((np.dot(structure['line_4'], structure['line_5'])) / (para_b * para_c))) #b a c
	beta = math.degrees(math.acos(
	    (np.dot(structure['line_3'], structure['line_5'])) / (para_a * para_c)))  # a a c
	gamma = math.degrees(math.acos(
	    (np.dot(structure['line_3'], structure['line_4'])) / (para_a * para_b)))  # a a b

	#RECIPROCAL LATTICE VECTORS
	volume = para_a*para_b*para_c*math.sqrt( 1-math.cos(math.radians(alpha))**2 - math.cos(math.radians(beta))**2 - math.cos(math.radians(gamma))**2 
	+ 2*math.cos(math.radians(alpha))*math.cos(math.radians(beta))*math.cos(math.radians(gamma)) )
	a_stars =para_b*para_c*math.sin(math.radians(alpha))/volume
	b_stars =para_a*para_c*math.sin(math.radians(beta))/volume
	c_stars =para_a*para_b*math.sin(math.radians(gamma))/volume
	k_spacing=float(sys.argv[2])
	k_a_stars = a_stars/k_spacing
	k_b_stars = b_stars/k_spacing
	k_c_stars = c_stars/k_spacing
	if int(k_a_stars)>=1:
		k_a_stars = int(k_a_stars) if (k_a_stars - int(k_a_stars)<= 0.4) else int(k_a_stars)+1
	else:
		k_a_stars=1
	if int(k_b_stars)>=1:
		k_b_stars = int(k_b_stars) if (k_b_stars - int(k_b_stars)<= 0.4) else int(k_b_stars)+1
	else:
		k_b_stars=1
	if int(k_c_stars)>=1:
		k_c_stars = int(k_c_stars) if (k_c_stars - int(k_c_stars)<= 0.4) else int(k_c_stars)+1
	else:
		k_c_stars=1
	print("K_SPACING: {} {} {}".format(k_a_stars,k_b_stars,k_c_stars))

	input_file_KPOINTS = sys.argv[1]+'/KPOINTS'
	with open(input_file_KPOINTS, 'r') as file:
	    lines = file.readlines()
	lines[3]= '{} {} {}\n'.format(k_a_stars,k_b_stars,k_c_stars)
	with open(input_file_KPOINTS,'w') as file:
	    file.writelines(lines)
