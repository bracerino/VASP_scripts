#!/bin/bash

#CHANGE THE INPUT DIRECTORY WHERE TO RUN THE GEOM. OPTIMIZATION WITH IBRION = 2, then IBRION = 1
INPUT_DIR="./"
NUMBER_OF_PROCESSORS=10
VASP_BINARY_NAME="vasp_aocl"



cd "$INPUT_DIR"
input_file="INCAR"
search_text="IBRION"
replacement_text="IBRION = 2"
search_text_2="NSW"
replacement_text_2="NSW = 10"

sed -i "/$search_text/c\\$replacement_text" "$input_file"
sed -i "/$search_text_2/c\\$replacement_text_2" "$input_file"
mpirun -np $NUMBER_OF_PROCESSORS $VASP_BINARY_NAME
echo "GEOM. OPTIMIZATION FINISHED WITH IBRION = 2"


if [[ -f "CONTCAR" ]]; then
    # Check if POSCAR exists
    if [[ -f "POSCAR" ]]; then
        # Rename original POSCAR to POSCAR_old
        mv "POSCAR" "POSCAR_old"
    fi

    # Rename OUTCAR to POSCAR
    mv "CONTCAR" "POSCAR"
    echo "=================================================================================================================================="
    echo "Files renamed successfully!"
    echo "=================================================================================================================================="
else
    echo "=================================================================================================================================="
    echo "OUTCAR does not exist in the directory. No files renamed."
    echo "=================================================================================================================================="
fi

replacement_text="IBRION = 1"
replacement_text_2="NSW = 100"
sed -i "/$search_text/c\\$replacement_text" "$input_file"
sed -i "/$search_text_2/c\\$replacement_text_2" "$input_file"
mpirun -np $NUMBER_OF_PROCESSORS $VASP_BINARY_NAME
echo "GEOM. OPTIMIZATION FINISHED WITH IBRION = 1"
