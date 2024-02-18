# Base directory containing the original files
base_dir="."
# Target directory where new directories and files will be created
target_dir="${base_dir}/POSCARs"

mkdir -p "$target_dir"
for file in "$base_dir"/*; do
    if [ -f "$file" ]; then
        filename=$(basename -- "$file")
        dir_name="$target_dir/$filename"
        mkdir -p "$dir_name"
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
