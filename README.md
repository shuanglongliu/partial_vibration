# Vibration of a subsystem

Python codes for managing calculations of vibrational modes of a subsystem with the rest system being fixed. The DFT and phonon calculators are VASP and Phonopy, respectively. 

## Usage

1. Put the relaxed geometry of the whole system (CONTCAR) in the same directory with the Python codes (the working directory).
2. Specify which atoms are allowed to move in the file selected_atoms.dat. Note that the indices of atoms are 1-based and the same as CONTCAR.
3. Modify INCAR, KPOINTS, and the job script in data.py.
4. Put a POTCAR file and a preconverged WAVECAR in the working directory.
5. Call the following functions in sequence
   
   5.1 **sv = subsystem_vibration()** # Instantiate a subsystem vibration object
   
   5.2 **sv.get_contcar_cartesian()** # Get cartesian coordinates for checking purpose
   
   5.3 **sv.get_poscars()** # Get atomic coordinates for all displacements
   
   5.4 **sv.create_directories()** # Create folders for all DFT calculations
   
   5.5 **sv.get_input_files()** # Get input files for all DFT calculations
   
   5.6 **sv.submit_jobs()** # Submit slurm jobs, which can be replaced by a job array
   
   5.7 **sv.check_convergence()** # Check convergence of all DFT calculations
   
   5.8 **sv.get_forces()** # Gather forces for all distorted systems
   
   5.9 **sv.get_vib()** # Calculate vibrational modes
