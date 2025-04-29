# ====================================================================================================
# Python code for calculating the vibrational modes of a part of a system with the rest of the system
# frozen using VASP, phonopy, and ase.
# 
# For the ease of reference, the moving part is called "molecule" and the whole system is called
# "system".
# 
# The system geometry is read from the CONTCAR file, and the indices of the selected atoms are read
# from the file "selected_atoms.dat". The indices of atoms are 1-based and defined in CONTCAR.
# ====================================================================================================

import os
import copy
import subprocess
import numpy as np
from ase.io import read, write
from data import *

class partial_vibration:
    def __init__(self):
      self.molecule_indices = np.loadtxt(file_selected_atoms, comments='#')
      self.molecule_indices = self.molecule_indices.astype(int)
      self.natom = len(self.molecule_indices)
      self.nconf = self.natom*6 
  
      self.system = read("CONTCAR")
      self.positions = self.system.get_positions()
      self.natom_all = len(self.system)

      self.step = 0.01 # Ang
      self.distorted_system = copy.deepcopy(self.system)

    def get_contcar_cartesian(self):
        """
        Obtain the system geometry in Cartesian coordinates.
        """
        write("CONTCAR_cart.vasp", self.system, format="vasp", direct=False)
  
    def set_dir_name(self, idisplacement=1):
        """
        Set the directory name for the distorted system.
        """
        self.dir_name = "{:04d}".format(idisplacement)
  
    def get_poscars(self):
        """
        Obtain the POSCAR files for each distortion of the molecule.
        """
        for iatom in range(self.natom):
          counter = 0
          for iaxis in range(3):
            for idirection in [-1, 1]:
              counter = counter + 1
              idisplacement = 6*iatom + counter
  
              dpos = np.zeros([3])
              dpos[iaxis] = idirection * self.step
              distorted_positions = copy.deepcopy(self.positions)
              distorted_positions[self.molecule_indices[iatom]-1] = self.positions[self.molecule_indices[iatom]-1] + dpos
              self.distorted_system.set_positions(distorted_positions) 

              self.set_dir_name(idisplacement)
              fname = "POSCAR-" + self.dir_name
              write(fname, self.distorted_system, format="vasp")
  
              print("The distorted system is written to {:s}".format(fname))
  
    def create_directories(self):
        for iatom in range(self.natom):
          counter = 0
          for iaxis in range(3):
            for idirection in [-1, 1]:
              counter = counter + 1
              idisplacement = 6*iatom + counter
              self.set_dir_name(idisplacement)
              subprocess.run(["mkdir", '-p', self.dir_name])
  
              print("The directory {:s} is created".format(self.dir_name))
  
    def get_input_files(self):
        for iatom in range(self.natom):
        # for iatom in range(1):
          counter = 0
          for iaxis in range(3):
            for idirection in [-1, 1]:
              counter = counter + 1
              idisplacement = 6*iatom + counter
              self.set_dir_name(idisplacement)

              os.chdir(self.dir_name)
              os.system("pwd")
              with open("INCAR", "w") as f:
                f.write(incar)
              subprocess.run(["ln", "-sf", rootdir + "/POSCAR-{:03d}".format(idisplacement), "POSCAR"])
              subprocess.run(["ln", "-sf", rootdir + "/POTCAR", "."])
              with open("KPOINTS", "w") as f:
                f.write(kpoints)
              subprocess.run(["ln", "-sf", rootdir + "/WAVECAR", "."])
              with open("vasp.job", "w") as f:
                f.write(job_script)
              os.chdir(rootdir)
  
    def submit_jobs(self):
        for iatom in range(self.natom):
          counter = 0
          for iaxis in range(3):
            for idirection in [-1, 1]:
              counter = counter + 1
              idisplacement = 6*iatom + counter
              self.set_dir_name(idisplacement)

              os.chdir(self.dir_name)
              os.system("pwd")
              subprocess.run(["sbatch", "vasp.job"])
              # subprocess.run(["sleep", "3"])
              os.chdir(rootdir)
  
    def check_convergence(self):
        for iatom in range(self.natom):
            counter = 0
            for iaxis in range(3):
                for idirection in [-1, 1]:
                    counter = counter + 1
                    idisplacement = 6*iatom + counter
                    self.set_dir_name(idisplacement)

                    os.chdir(self.dir_name)
                    os.system("pwd")
                    try:
                        # Capture the output of the command
                        output = subprocess.run(["grep", "EDIFF is reached", "OUTCAR"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True)
                        # print(output.stdout)
                        
                        # Check if the standard output of the previous command is empty
                        if output.stdout:
                            # print("{:s}: Converged".format(dname))
                            pass
                        else:
                            print("{:s}: Not converged".format(dname))
                    except:
                        print("{:s}: Error".format(dname))
                    os.chdir(rootdir)

    def get_forces(self):
        with open("FORCE_SETS", "w") as f:
          f.write("{:<6d}\n".format(self.natom))
          f.write("{:<6d}\n\n".format(self.nconf))
      
          for iatom in range(self.natom):
            counter = 0
            for iaxis in range(3):
              for idirection in [-1, 1]:
                f.write("{:<6d}\n".format(iatom+1))
                #f.write("{:<6d}\n".format(molecule[iatom]))
      
                dpos = np.zeros([3])
                dpos[iaxis] = idirection * self.step
                f.write(("{:20.16f} {:20.16f} {:20.16f}\n").format(*dpos))
      
                counter = counter + 1
                idisplacement = 6*iatom + counter
                self.set_dir_name(idisplacement)
        
                os.chdir(self.dir_name)
                os.system("pwd")
                properties = read("vasprun.xml")
                forces = properties.get_forces()
                for iiatom in range(self.natom):
                  f.write(("{:16.10f} {:16.10f} {:16.10f}\n").format(*(forces[self.molecule_indices[iiatom]-1])))
                f.write("\n")
                os.chdir(rootdir)

    def get_vib():
        all_atoms = []
        for iatom in range(self.natom_all):
          all_atoms.append(iatom)
      
        other_atoms = list(set(all_atoms) - set(self.molecule_indices-1))
        del system[other_atoms]
        write("POSCAR", system) # To be tested when molecue == system
      
        mesh = """DIM = 1 1 1
        MP = 1 1 1
        SYMMETRY = .FALSE.
        EIGENVECTORS = .TRUE.
        DOS = .TRUE.
        """
      
        with open("mesh.conf", "w") as f:
          f.write(mesh)
      
        subprocess.run(["phonopy", "-t", "-p", "mesh.conf"])

if __name__ == "__main__":
    sv = partial_vibration()
    # sv.get_contcar_cartesian()
    # sv.get_poscars()
    # sv.create_directories()
    # sv.get_input_files()
    # sv.submit_jobs()
    # sv.check_convergence()
    # sv.get_forces()
    # sv.get_vib()

