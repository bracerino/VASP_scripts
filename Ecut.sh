#!/bin/bash

# Define the directory path to the VASP data folder
directory_path="./"

#Set parameters of energy_cutoff test and the number of processors for the VASP
ENCUT_MAX=900
ENCUT_MIN=450
ENCUT_STEP=25
NUMBER_OF_PROCESSORS=1
VASP_BINARY_NAME="vasp_gpu"


script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if the directory exists
if [ -d "$directory_path" ]; then
    # Change to the specified directory
    cd "$directory_path" || exit 1
    output_file="ENCUT_CONVERGENCE_TEST_ENERGY_and_LATT_PARAMETERS.txt"
    > "$output_file"  # Clear the file if it exists or create a new one
    echo "#Ener_Cutoff[eV] Elapsed_Time[min] Total_Ener[eV] Ener_Diff/Number_of_Atoms[eV] Latt_a[A] Latt_b[A] Latt_c[A] Alpha[°] Beta[°] Gamma[°] a_Diff[A] b_Diff[A] c_Diff[A] Alp_Diff[°] Beta_Diff[°] Gamma_Diff[°]" >> "$output_file"
    

    #Looping
    for ((encut = $ENCUT_MAX; encut >= $ENCUT_MIN; encut -= $ENCUT_STEP)); do
        file_path="INCAR"
        sed -i "s/ENCUT = [0-9]\+/ENCUT = $encut/" "$file_path"
        #sed -i '' -e "s/ENCUT = [0-9]\+/ENCUT = $encut/" "$file_path"
        echo "$encut" >> "$output_file"
        # Run the command in the current directory
        start_time=$(date +%s)
        mpirun -np $NUMBER_OF_PROCESSORS $VASP_BINARY_NAME
        
        end_time=$(date +%s)
	total_time=$((end_time - start_time))
        python3 "$script_dir/python_run.py" "$directory_path" "$total_time"
        
        echo "ENCUT set to $encut"
    done

else
    echo "Directory not found: $directory_path"
    
    
    




fi
