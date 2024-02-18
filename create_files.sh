#!/bin/bash

#E.g. to create 900 structures, set '899'
num_of_structures=899
name_of_input_file="Ti_36_INIT_Standard.lmp"
name_of_output_poscar="POSCAR_STD"
min_deform=-15
max_deform=15

min_disturb=0.1
max_disturb=1.0


#step=$(echo "scale=5; ($max_deform - $min_deform) / $num_of_structures" | bc)

for i in $(seq 1 $((num_of_structures+1)))
do
  #x=$(echo "scale=5; $min_deform + ($i - 1) * $step" | bc)
  random_deform=$(awk -v min=$min_deform -v max=$max_deform -v seed=$RANDOM 'BEGIN{srand(seed); print int((min+rand()*(max-min))*1000)/1000}')
  x=$RANDOM_FLOAT
  random_disturb=$(awk -v min=$min_disturb -v max=$max_disturb -v seed=$RANDOM 'BEGIN{srand(seed); print int((min+rand()*(max-min))*1000)/1000}')
  dist=$RANDOM_FLOAT_2

  atomsk ${name_of_input_file} -disturb $random_disturb $random_disturb $random_disturb -def x $random_deform% -def y $random_deform% -def z $random_deform% POSCAR

  mv "POSCAR" "${i}_${name_of_output_poscar}_${random_disturb}_$random_deform%"
  echo "Created output: ${i}_${name_of_output_poscar}_${random_disturb}_$random_deform%"
done