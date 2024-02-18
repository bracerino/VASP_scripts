import os
# ============ INPUTS, modify these =====================
#Directory which contains other directories, each of them with different POSCAR for the VASP calculation
INPUT_POSCAR_FOLDER = f'/home/lebedmi2/DATA/VASP_data/Ti_test_structures/POSCARs'
INPUT_VASP_POTENTIALS_FOLDER = f'/home/lebedmi2/DATA/VASP_data/Ti_test_structures/potencials/potPAW_PBE.54'
#========================================================


POSCAR_name = 'POSCAR'
def create_potcar(INPUT_POSCAR_FOLDER, INPUT_VASP_POTENTIALS_FOLDER, POSCAR_name):
    OUTPUT_POTCAR = os.path.join(INPUT_POSCAR_FOLDER, 'POTCAR')
    POSCAR_file_path = os.path.join(INPUT_POSCAR_FOLDER, POSCAR_name)
    with open(OUTPUT_POTCAR, 'w') as f:
        f.write("")

    # Check if the POSCAR file exists and is not empty.
    if os.path.exists(POSCAR_file_path) and os.path.getsize(POSCAR_file_path) > 0:
        print(f"FOUND {POSCAR_name}, can proceed.")

        with open(POSCAR_file_path, 'r') as f:
            # Extract element symbols and their counts from the POSCAR file.
            lines = f.readlines()
            elements = lines[5].strip().split()
            elements_counts = lines[6].strip().split()
            print(f"============= ELEMENTS FOUND IN POSCAR AND THEIR COUNT: {elements}, {elements_counts}")

            # Prepare lists for elements and their counts.
            elements_counts_loop = [str(element) for element in elements_counts]
            elements_loop = [str(element) for element in elements]
            print(elements_counts_loop)
            # Identify elements with zero count to be removed.
            idx_to_pop = []
            for idx, element_count in enumerate(elements_counts_loop):
                if element_count == '0':
                    print(
                        f"-----> {elements_loop[idx]} has {element_count} count in {POSCAR_name}.\nSkipping and will NOT ADD it to the POTCAR file.\n"
                        f"Will drop it from the {POSCAR_name} FILE. ")
                    idx_to_pop.append(idx)
            # Remove elements with zero count from the lists.
            for i in sorted(idx_to_pop, reverse=True):
                elements.pop(i)
                elements_counts.pop(i)

            print(f"============= ELEMENTS AND THEIR COUNT AFTER DROPPING THE ZERO COUNTS: {elements}, {elements_counts}")
            for idx, element_count in enumerate(elements_counts):
                if element_count == '0':
                    print(
                        f"-----> {elements[idx]} has {element_count} count in {POSCAR_name}.\nSkipping and will NOT ADD it to the POTCAR file.")

                else:
                    if elements[idx] in os.listdir(INPUT_VASP_POTENTIALS_FOLDER):
                        print(f"-----> {elements[idx]} FOUND in the potentials directory. Added to the POTCAR.")
                        element_pot_dir = os.path.join(INPUT_VASP_POTENTIALS_FOLDER, elements[idx], 'POTCAR')
                        with open(element_pot_dir, 'r') as f:
                            lines_read = f.readlines()
                        with open(OUTPUT_POTCAR, 'a') as f:
                            f.writelines(lines_read)
                            print("SUCCESSFULLY ADDED.")
        with open(POSCAR_file_path, 'w+') as f:
            elements.append('\n')
            elements_counts.append('\n')
            lines[5] = ' '.join(elements)
            lines[6] = ' '.join(elements_counts)
            f.writelines(lines)
    else:
        print(f"There is NO {POSCAR_name} in {INPUT_POSCAR_FOLDER} OR the file is EMPTY. \n"
              f"Put {POSCAR_name} into this folder.")
    print("FINISHED.")

print(INPUT_POSCAR_FOLDER)
for folder in os.listdir(INPUT_POSCAR_FOLDER):
    INPUT_POSCAR_FOLD = os.path.join(INPUT_POSCAR_FOLDER, folder)
    if os.path.isdir(INPUT_POSCAR_FOLD):
        print(f"=========== CHECKING FOLDER {INPUT_POSCAR_FOLD}")
        if os.path.isdir(INPUT_POSCAR_FOLD) and POSCAR_name in os.listdir(INPUT_POSCAR_FOLD) :
            print(f"PROCEEDING to create POTCAR.")
            create_potcar(INPUT_POSCAR_FOLD, INPUT_VASP_POTENTIALS_FOLDER, POSCAR_name)
        else:
            print(f"NO {POSCAR_name}, SKIPPING.")

