#!/bin/bash

vasp_run="mpirun -np 1 vasp_gpu_mkl"
directory_path="/home/lebedmi2/DATA/VASP_data/Ti_test_structures/POSCARs" # Update with your directory path

#Checking if the files with names of VASP directories exists. If yes, do not create it but continue with its content
if [ ! -f "directory_list.txt" ]; then
    search_dir="$directory_path" # Ensure this variable is defined before running the script
    dir_list="directory_list.txt"
    touch "$dir_list" # This is optional since '>>' will create the file if it doesn't exist

    for dir in "$search_dir"/*; do
        if [ -d "$dir" ]; then
            echo "FOUND DIR: $(basename "$dir")"
            echo "$(basename "$dir")" >> "$dir_list"
        fi
    done

    # Sort the directory list after collecting all directory names
    temp_file=$(mktemp)
    sort -V -t '_' -k 1,1 "$dir_list" > "$temp_file"
    mv "$temp_file" "$dir_list"
else
    # The file exists, inform the user
    echo -e "The file 'directory_list.txt' with names of folders on which to run VASP calculations already exists.\nContinuing with it."
fi

vasp_file_name="OSZICAR" # Update with your vasp file name
directories_file="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)/directory_list.txt"
start_dir=$(pwd)
output_file="${directory_path}/OUTPUT_END_of_CYCLES_LIST.txt"
if [ ! -f "${directory_path}/OUTPUT_END_of_CYCLES_LIST.txt" ]; then
	echo -e "#FOLDER_NAME\tLAST_DAV_CYCLE\tCONVERGED?\tNELM\tTIME[min]" > "$output_file"
fi

mapfile -t dir_names < "$directories_file"
# Loop over the array of directory names



# Loop over directories in directory_path
#while IFS= read -r dir_name; do
for dir_name in "${dir_names[@]}"; do
    folder_path="${directory_path}/$dir_name"
    echo "$folder_path"
    if [ -d "$folder_path" ]; then # Ensure it's a directory 
        cd "$folder_path"
        start_time=$(date +%s)
        $vasp_run
        # Check if vasp_file_name exists in h
        if [ -f "$vasp_file_name" ]; then
            echo "FOUND FILE $vasp_file_name in FOLDER $folder_name"
            # Get the last and second last lines of the file
            last_line=$(tail -n 1 "$vasp_file_name")
            second_last_line=$(tail -n 2 "$vasp_file_name" | head -n 1)
            # Split the lines into arrays
            read -ra last_line_arr <<< "$last_line"
            read -ra second_last_line_arr <<< "$second_last_line"
            echo "$last_line"
            echo "$second_last_line"
            # Check if the last_line_arr[1] is a number
            echo "${last_line_arr[1]}"
            NELM=$(grep "^NELM" INCAR | awk '{print $3}')
	    if [ -z "$NELM" ]; then
       		NELM=60
            fi
            echo "NELM value: $NELM"
            if [[ "${last_line_arr[1]}" == "F=" ]]; then
                if [ "${last_line_arr[1]}" == "F=" ]; then
                    if [[ "${second_last_line_arr[1]}" == "$NELM" ]]; then
                    	cycle_finished_yes_no="NO"
                    	cycle_number="${second_last_line_arr[1]}"
			nelm=$NELM
                    else
			nelm=$NELM
                    	cycle_finished_yes_no="YES"
                    	cycle_number="${second_last_line_arr[1]}"
                    fi 
                else
                    cycle_finished_yes_no="NO_$NELM"
                    cycle_number="${last_line_arr[1]}"
                fi
            else
                # If last_line_arr[1] is not a number, set cycle_number to zero
                cycle_finished_yes_no="NO_STOPPED"
                cycle_number="0"
            fi
            cd "$start_dir" || exit
            # Append to output file
            end_time=$(date +%s) # Get end time of the loop iteration
            duration=$(echo "scale=2; ($end_time - $start_time) / 60" | bc)
            
            
            echo -e "$folder_path\t$cycle_number\t$cycle_finished_yes_no\t$nelm\t$duration" >> "$output_file"
            sed -i "/^$dir_name$/d" "$directories_file"
        else
            echo "------- NOT FOUND $vasp_file_name in FOLDER $(basename "$folder_name") -------"
            cd "$start_dir" || exit
            # Append to output file
            end_time=$(date +%s) # Get end time of the loop iteration
            duration=$(echo "scale=2; ($end_time - $start_time) / 60" | bc)
            echo -e "$folder_path\t0\tNO\tERROR\t$duration" >> "$output_file"
            sed -i "/^$dir_name$/d" "$directories_file"
        fi
    fi
done #< "$directories_file"
rm -f $directories_file
echo "FINISHED. OUTPUT IS IN THE FILE: $output_file"
