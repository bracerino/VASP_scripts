#!/bin/bash

# Define the directory path to the VASP data folder
directory_path="./"

# Set parameters of the equidistant k_spacing and the number of processors for VASP
k_spacing_MIN=0.02
k_spacing_MAX=0.1
STEP=0.0025
NUMBER_OF_PROCESSORS=1
VASP_BINARY_NAME="vasp_gpu"


var_helpful=1
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if the directory exists
if [ -d "$directory_path" ]; then
    # Change to the specified directory
    cd "$directory_path" || exit 1
    output_file="K_SAMPLING_CONVERGENCE_TEST_ENERGY_and_LATT_PARAMETERS.txt"
    > "$output_file"  # Clear the file if it exists or create a new one
    echo "#k_sampling [A-1] k_a k_b k_c Elapsed_Time[min] Total_Ener[eV] Ener_Diff/Number_of_Atoms[eV] Latt_a[A] Latt_b[A] Latt_c[A] Alpha[°] Beta[°] Gamma[°] a_Diff[A] b_Diff[A] c_Diff[A] Alp_Diff[°] Beta_Diff[°] Gamma_Diff[°]" >> "$output_file"
    previous_values=""
    current_values=1
    # Looping using Python for floating-point arithmetic
    for k_spacing in $(python3 -c "for i in range(int($k_spacing_MIN * 10000), int($k_spacing_MAX * 10000) + 1, int($STEP * 10000)): print(i / 10000.0)"); do
        file_path="INCAR"
        # Replace the value in the file
        # Your sed command that may produce errors
        echo "$k_spacing" >> "$output_file"
        python3 "$script_dir/p_change_kpoints.py" "$directory_path" "$k_spacing" "$var_helpful"  .
         	
    	current_values=$(sed -n '4p' "KPOINTS")
       	echo "THIRD LINE $current_values"
        start_time=$(date +%s)
        if [ -f "WAVECAR" ]; then
    	    rm WAVECAR
    	fi
    	if [ "$previous_values" != "$current_values" ]; then
    		echo "NOOOOOOOOOOOOOOOOOOOOOOOOOT SKIPPING: $previous_values different than $current_values"
            	mpirun -np $NUMBER_OF_PROCESSORS $VASP_BINARY_NAME
        else
        	echo "I HAVE SKIPED BECAUSE:::: $previous_values ======= $current_values"
        fi
        end_time=$(date +%s)
        total_time=$((end_time - start_time))
        python3 "$script_dir/python_run.py" "$directory_path" "$total_time" "$k_spacing"
        echo "k_spacing set to $k_spacing"
        previous_values="$current_values"
        #previous_values="$current_values"
    	((var_helpful++)) # Moved inside the loop
    	echo "==================================================== END OF ONE RUN ===================================================="
    done
    
else
    echo "Directory not found: $directory_path"
fi
