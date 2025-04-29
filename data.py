import os

rootdir = os.path.dirname(os.path.realpath(__file__)) + "/"

file_selected_atoms = "selected_atoms.dat"

incar = """
SYSTEM = vasp

#### sym ####
#ISYM = 0

#### system size ####
#NBANDS = 448
#NELECT = 383.0

#### accuracy ####
PREC = Accurate
ENCUT = 600
LREAL = A

#### density functional ####

## optB86b-vdW
#GGA = MK 
#PARAM1 = 0.1234 
#PARAM2 = 1.0000
#LUSE_VDW = .TRUE.
#AGGAC = 0.0000

## LDA
#GGA = CA

#### parallelization ####
#KPAR = 4
NCORE = 8

#### electronic optimization ####
EDIFF = 1E-8
NELM = 120
#NELMIN = 10
#NELMDL = -8
AMIX = 0.3
AMIX_MAG = 0.6
AMIX_MIN = 0.05
BMIX = 0.0001
BMIX_MAG = 0.0001
ALGO = All

#### structural relaxation ####
# NSW = 30
# IBRION = 1
# ISIF = 2
# EDIFFG = -0.005
# POTIM = 0.3

#### magnetism: accuracy ####
LASPH = T
GGA_COMPAT = F

#### magnetism: collinear spin ####
#ISPIN = 2
#MAGMOM = 3.0 3.0 3.0 1000*0.0
#NUPDOWN = 9

#### magnetism: noncollinear spin, SOC ####
LSORBIT = T
SAXIS = 0 0 1
MAGMOM = 0.0 0.0 2.0 1000*0.0

#### magnetism: constraint ####
I_CONSTRAINED_M = 1
M_CONSTR =  0.0 0.0 2.0 1000*0.0

LAMBDA =  10.0
RWIGS =  1.588 0.820 0.741 0.863 0.370 1.45 1.16 1.164

#### magnetism: orbital moment ####
# LORBMOM = T

#### charge, wavefunction ####
ISTART = 1
ICHARG = 0
LWAVE = F
LCHARG = F
LAECHG = F
LMAXMIX = 6

#### dos ####
ISMEAR = 0
SIGMA = 0.002
#NEDOS = 501
#EMIN = -15
#EMAX = 10
#LORBIT = 11

#### Partial Charge ####
#LPARD = T
#EINT = -5.0000  -4.7355
#EINT = -4.7355 -4.0500

#### vdW ####
IVDW = 11

#### LDA+U ####
LDAU = T
LDAUTYPE = 1
LDAUPRINT = 1
LDAUL = 3 -1 -1 -1 -1 -1 -1 -1
LDAUU = 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 
LDAUJ = 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 

#### HSE ####
#LHFCALC = T 
#HFSCREEN = 0.2 
#PRECFOCK = Accurate
#ALGO = All 
#TIME = 0.35

#### wann ####
#LWANNIER90 = .T.
#LWRITE_UNK = .TRUE.

### polarization ###
#IDIPOL = 4
#LMONO = T
#LDIPOL = T
#LCALCPOL = T
#DIPOL = 0.5 0.5 0.5 

### occupation matrix control ###
#OCCEXT = 1
"""

kpoints = """k-points
0
gamma
  1  1  1 
  0  0  0
"""

job_script_hipergator_cpu = """#!/bin/bash

#SBATCH --account=m2qm-efrc
#SBATCH --qos=m2qm-efrc-b
#SBATCH --job-name=TmL1
#SBATCH --partition=hpg-default
#SBATCH --nodes=1
#SBATCH --ntasks=32
##SBATCH --cpus-per-task=1
##SBATCH --ntasks-per-node=64
##SBATCH --ntasks-per-socket=8
#SBATCH --mem=256gb
#SBATCH --distribution=cyclic:cyclic
#SBATCH -t 4-00:00:00
#SBATCH --error=error
#SBATCH --output=output
#SBATCH --mail-type=All
#SBATCH --mail-user=user_name@northeastern.edu

module purge
module load intel/2020.0.166  openmpi/4.1.6 vasp/6.4.3

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/pmix/3.2.5/lib

source ~/.bash_aliases; keep_log

export OMP_NUM_THREADS=1

srun --mpi=pmix -n 32 vasp_ncl

rm -rf core.* DOSCAR CONTCAR PROCAR XDATCAR CHG  CHGCAR  error  IBZKPT  output  PCDAT  REPORT vasp.job
"""

job_script_hipergator_gpu = """#!/bin/bash

#SBATCH --job-name=TmL1
#SBATCH --mem-per-cpu=50gb
#SBATCH -t 4-00:00:00
#SBATCH -p gpu --gpus=a100:4
#SBATCH --account=m2qm-efrc
#SBATCH --qos=m2qm-efrc
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --ntasks-per-node=4
#SBATCH --error=error
#SBATCH --output=output
#SBATCH --mail-type=ALL
#SBATCH --mail-user=user_name@ufl.edu

module load nvhpc/23.7  openmpi/4.1.6 vasp/6.4.3

source ~/.bash_aliases; keep_log; vp_continue_relaxation

mpirun -n 4 vasp_ncl

#rm -rf DOSCAR PROCAR vasprun.xml core.*
"""

job_script_perlmutter_gpu = """#!/bin/bash

#SBATCH -A m3346_g
#SBATCH -J TmL1
#SBATCH -C gpu
#SBATCH -q regular
#SBATCH -t 6:00:00
#SBATCH -N 1
#SBATCH -n 4
#SBATCH -c 32
#SBATCH -G 4
#SBATCH --exclusive
#SBATCH --error=error
#SBATCH --output=output
#SBATCH --mail-type=ALL
#SBATCH --mail-user=user_name@ufl.edu

export OMP_NUM_THREADS=1
export OMP_PLACES=threads
export OMP_PROC_BIND=spread

module load vasp/6.4.3-gpu

source ~/.bash_aliases; keep_log

srun -n 4 -c 32 --cpu-bind=cores --gpu-bind=none vasp_ncl

rm -rf CHG CHGCAR DOSCAR PROCAR
"""

job_script = job_script_hipergator_cpu

