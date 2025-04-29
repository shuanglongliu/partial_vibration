# Vibration of a subsystem

Python codes for managing calculations of vibrational modes of a subsystem with the rest system being fixed. The DFT and phonon calculators are VASP and Phonopy, respectively. 

## Usage

1. Put the relaxed geometry of the whole system (CONTCAR) in the same directory with the Python codes (the working directory).
2. Specify which atoms are allowed to move in the file selected_atoms.dat. Note that the indices of atoms are 1-based and the same as CONTCAR.
3. Modify INCAR, KPOINTS, and the job script in data.py.
4. Put a POTCAR file and a preconverged WAVECAR in the working directory.
5. Call the following functions in sequence

sv = subsystem_vibration() # Instantiate a subsystem vibration object
sv.get_contcar_cartesian() # Get cartesian coordinate for checking purposes
sv.get_poscar() # Get the coordinates with atomic displacement
sv.create_directories() # Create folders for all DFT calculations
sv.get_input_files() # Get the input files for all DFT calculations
sv.submit_jobs() # Submit Slurm jobs, which can be replaced by a job array
sv.check_convergence() # Check convergence of all DFT calculations
sv.get_forces() # Gather the calculated forces for all distorted systems
sv.get_vib() # Calculate vibrational modes
