# Base directory containing the original files
directory_path="/home/lebedmi2/DATA/VASP_data/Ti_test_structures/scripts/structures"

target_dir="${directory_path}/POSCARs"
# Ensure the target directory exists
mkdir -p "$target_dir"

# Loop over each file in the base directory
for file in "$directory_path"/*; do
    if [ -f "$file" ]; then
        # Extract the full filename without the path
        filename=$(basename -- "$file")

        # Create a directory with the name of the file inside the target directory
        dir_name="$target_dir/$filename"

        # Ensure the directory exists
        mkdir -p "$dir_name"

        # Move and rename the file to 'POSCAR' within the new directory
        cp "$file" "$dir_name/POSCAR"
        cp "./INCAR" "$dir_name/"
        cp "./KPOINTS" "$dir_name/"
        #cp "./POTCAR" "$dir_name/"
    fi
done

rm -r -f "${target_dir}/INCAR"
rm -r -f "${target_dir}/KPOINTS"
rm -r -f "${target_dir}/POTCAR"
rm -r -f ${target_dir}/*.lmp
rm -r -f ${target_dir}/*.sh
echo "Finished creating folders for the VASP calculations."
