# This script converts all POSCAR or CIF files into .XYZ file and append them also into one complete .XYZ as a trajectory
import os
import re
from ase.io import read, write

def numeric_key(filename):
    m = re.match(r"(\d+)", filename)
    return int(m.group(1)) if m else float('inf')

def convert_all(folder="."):
    files = [f for f in os.listdir(folder)
             if f.lower().endswith(".cif") or "poscar" in f.lower() or f.lower().endswith(".vasp")]
    files.sort(key=numeric_key)

    all_frames = []

    for f in files:
        path = os.path.join(folder, f)
        try:
            atoms = read(path)
        except Exception as e:
            print(f"Failed to read {f}: {e}")
            continue
        outname = os.path.splitext(f)[0] + ".xyz"
        write(os.path.join(folder, outname), atoms, format="extxyz")

        # Collect for trajectory
        all_frames.append(atoms)

        print(f"Converted {f} → {outname}")

    if all_frames:
        traj_path = os.path.join(folder, "trajectory.xyz")
        write(traj_path, all_frames, format="extxyz")
        print(f"\nTrajectory written → {traj_path}")
    else:
        print("No valid POSCAR or CIF files found.")

if __name__ == "__main__":
    convert_all(".")
