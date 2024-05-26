#!/bin/bash
export LC_NUMERIC="en_US.UTF-8"
OUTPUT_FILE="output_all.txt"
> "$OUTPUT_FILE"


#Set path to the file which will be disturbed and deformed
directory_path="/home/lebedmi2/DATA/VASP_data/Ti_test_structures/scripts/structures"
#directory_path="."

#E.g. to create 900 structures
num_of_structures=900

name_of_input_file="Ti_36_INIT_Standard.lmp"
name_of_output_poscar="POSCAR_STD"

min_deform=-15
max_deform=15

min_disturb=0.1
max_disturb=1.0
#Set the maximum distance between any atoms
distance_separ_limit=1.5


#step=$(echo "scale=5; ($max_deform - $min_deform) / $num_of_structures" | bc)

for i in $(seq 1 $((num_of_structures)))
do
  cd $directory_path
  valid_structure=false
  while [ "$valid_structure" = false ]; do
  	#x=$(echo "scale=5; $min_deform + ($i - 1) * $step" | bc)
  	random_deform=$(awk -v min=$min_deform -v max=$max_deform -v seed=$RANDOM 'BEGIN{srand(seed); print int((min+rand()*(max-min))*1000)/1000}')
  	x=$RANDOM_FLOAT
  	random_disturb=$(awk -v min=$min_disturb -v max=$max_disturb -v seed=$RANDOM 'BEGIN{srand(seed); print int((min+rand()*(max-min))*1000)/1000}')
  	dist=$RANDOM_FLOAT_2

  	atomsk ${name_of_input_file} -disturb $random_disturb $random_disturb $random_disturb -def x $random_deform% -def y $random_deform% -def z $random_deform% -separate 	0.5 0.2 -sort species up -frac POSCAR
	
	yes | atomsk --rdf POSCAR 10 0.1
	# Create the Python script content
	TEMP_PYTHON_SCRIPT=$(mktemp /tmp/process_file_pandas.py.XXXXXX)
	cat << 'EOF' > $TEMP_PYTHON_SCRIPT
import pandas as pd
import argparse

def process_file(input_file):
    df = pd.read_csv(input_file, sep='\s+', header=None, skiprows=1, names=['Col1', 'Col2'])
    filtered_df = df[df['Col2'] != 0.0]
    print(filtered_df.iloc[0, 0])
    return filtered_df.iloc[0, 0]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process a file and return the first value of the first column after filtering.')
    parser.add_argument('name_of_input_file', type=str, help='The input file to process')
    args = parser.parse_args()
    
    result = process_file("rdf_total.dat")
    #with open("output_all.txt", 'a') as f0:
    #    f0.write(f"{args.name_of_input_file} {result}\n")
EOF
	variable_value=$(python3 "$TEMP_PYTHON_SCRIPT" "${i}_${name_of_output_poscar}_${random_disturb}_$random_deform%")
	if [ $(echo "$variable_value >= $distance_separ_limit" | bc) -eq 1 ]; then
             
                echo -e "\n\n========================================\nYes, value ${variable_value} is greater than ${distance_separ_limit}\n\n"
      		valid_structure=true
	else
        echo -e"\n\n========================================\Invalid structure generated, retrying..."
	echo "Value ${variable_value} is NOT greater than ${distance_separ_limit}\n\n"
        rm "POSCAR"
        fi
       rm $TEMP_PYTHON_SCRIPT
       done

  echo "${i}_${name_of_output_poscar}_${random_disturb}_$random_deform% ${variable_value}" >> "${OUTPUT_FILE}"
  mv "POSCAR" "${i}_${name_of_output_poscar}_${random_disturb}_$random_deform%"
  echo "Created output: ${i}_${name_of_output_poscar}_${random_disturb}_$random_deform%"
done
echo "Finished creating files."
