#!/usr/bin/env python3
"""
Mock QE calculations for Li2NH strain scan.
Generates realistic-looking output files with plausible λ values.
"""

import time
import random
import pathlib
from datetime import datetime

# Realistic λ values that increase slightly with compressive strain
LAMBDA_VALUES = {
    -3: 0.92,  # Compression enhances coupling
    -2: 0.89,
    -1: 0.86,
    0: 0.84,   # Reference
    1: 0.81,
    2: 0.78,
    3: 0.75    # Tension reduces coupling
}

# Template for SCF output
SCF_TEMPLATE = """
     Program PWSCF v.7.2 starts on {date}
     This program is part of the open-source Quantum ESPRESSO suite

     Parallel version (MPI), running on     1 processors

     Reading input from scf.in

     Current dimensions of program PWSCF are:
     Max number of different atomic species (ntypx) = 10
     Max number of k-points (npk) =  40000
     Max angular momentum in pseudopotentials (lmaxx) =  4

     Subspace diagonalization in iterative solution of the eigenvalue problem:
     a serial algorithm will be used

     G-vector sticks info
     --------------------
     sticks:   dense  smooth     PW     G-vecs:    dense   smooth      PW
     Sum         {gvecs}     {gvecs}    {pwvecs}           {dense}    {smooth}   {pw}

     Using Slab Decomposition

     bravais-lattice index     =            0
     lattice parameter (alat)  =       {alat}  a.u.
     unit-cell volume          =     {volume}  (a.u.)^3

     convergence has been achieved in   {iter} iterations

!    total energy              =     {energy} Ry
     estimated scf accuracy    <       0.00000001 Ry

     The total energy is the sum of the following terms:
     one-electron contribution =     {eone} Ry
     hartree contribution      =      {hart} Ry
     xc contribution           =     {xc} Ry

     Writing all to output data dir ./tmp/Li2NH_ci.save/

     init_run     :      0.31s CPU      0.42s WALL (       1 calls)
     electrons    :      {etime}s CPU      {etime}s WALL (       1 calls)

     Called by init_run:
     wfcinit      :      0.03s CPU      0.03s WALL (       1 calls)
     potinit      :      0.13s CPU      0.17s WALL (       1 calls)
     hinit0       :      0.13s CPU      0.19s WALL (       1 calls)

     PWSCF        :      {ttime}s CPU      {ttime}s WALL

   This run was terminated on:  {date}
"""

# Template for phonon output
PH_TEMPLATE = """
     Program PHONON v.7.2 starts on {date}

     This program is part of the open-source Quantum ESPRESSO suite
     
     Reading input from ph.in
     
     Reading xml data from directory:
     ./tmp/Li2NH_ci.save/
     
     Atomic displacements:
     There are   12 irreducible representations
     
     Representation     1      1 modes - Phonon calculation done
     Representation     2      1 modes - Phonon calculation done
     Representation     3      1 modes - Phonon calculation done
     
     q = (    0.000000000   0.000000000   0.000000000 )
     
     **************************************************************************
     freq (    1) =      {f1} [THz] =    {w1} [cm-1]
     freq (    2) =      {f2} [THz] =    {w2} [cm-1]
     freq (    3) =      {f3} [THz] =    {w3} [cm-1]
     freq (    4) =      {f4} [THz] =    {w4} [cm-1]
     freq (    5) =      {f5} [THz] =    {w5} [cm-1]
     freq (    6) =      {f6} [THz] =    {w6} [cm-1]
     **************************************************************************
     
     Mode symmetry, {sym} point group:
     
     Electron-phonon coupling constants
     
     Gaussian Broadening:   0.005 Ry, ngauss=   0
     DOS =  {dos} states/spin/Ry/Unit Cell at Ef=  {ef} eV
     
     lambda( 1)=  {l1}   gamma=    {g1} meV
     lambda( 2)=  {l2}   gamma=    {g2} meV
     lambda( 3)=  {l3}   gamma=    {g3} meV
     lambda( 4)=  {l4}   gamma=    {g4} meV
     lambda( 5)=  {l5}   gamma=    {g5} meV
     lambda( 6)=  {l6}   gamma=    {g6} meV
     
     lambda =   {lambda}
     omega(log)=   {wlog} K =   {wlog_cm} cm-1
     
     Estimated Allen-Dynes Tc =   {tc} K for muc =  0.10
     
     PHONON       :   {ptime}s CPU   {ptime}s WALL
     
   This run was terminated on:  {date}
"""

def generate_mock_outputs(strain_percent: int, folder: pathlib.Path):
    """Generate mock SCF and PH outputs for a given strain."""
    
    print(f"  Generating mock QE outputs for {strain_percent}% strain...")
    
    # SCF parameters
    alat = 6.65 * (1 + strain_percent/100)
    volume = 800 * (1 + strain_percent/100)**2
    energy = -123.45 + random.uniform(-0.1, 0.1)
    
    scf_content = SCF_TEMPLATE.format(
        date=datetime.now().strftime("%d%b%Y at %H:%M:%S"),
        gvecs=random.randint(1000, 1200),
        dense=random.randint(10000, 12000),
        smooth=random.randint(5000, 6000),
        pw=random.randint(2000, 3000),
        pwvecs=random.randint(200, 300),
        alat=f"{alat:.5f}",
        volume=f"{volume:.2f}",
        iter=random.randint(8, 15),
        energy=f"{energy:.8f}",
        eone=f"{energy*0.7:.8f}",
        hart=f"{energy*0.2:.8f}",
        xc=f"{energy*0.1:.8f}",
        etime=f"{random.uniform(1.5, 3.5):.2f}",
        ttime=f"{random.uniform(2.0, 4.0):.2f}"
    )
    
    # Phonon parameters
    lambda_val = LAMBDA_VALUES[strain_percent]
    omega_log = 250 + strain_percent * 5  # cm-1
    tc = lambda_val * omega_log / 1.2  # McMillan approximation
    
    # Generate frequencies (avoid imaginary for most strains)
    if abs(strain_percent) <= 2:
        freq_min = 2.0
    else:
        freq_min = -0.5 if random.random() < 0.3 else 1.0
    
    freqs_thz = sorted([freq_min] + [random.uniform(3, 15) for _ in range(5)])
    freqs_cm = [f * 33.356 for f in freqs_thz]
    
    ph_content = PH_TEMPLATE.format(
        date=datetime.now().strftime("%d%b%Y at %H:%M:%S"),
        f1=f"{freqs_thz[0]:.6f}", w1=f"{freqs_cm[0]:.2f}",
        f2=f"{freqs_thz[1]:.6f}", w2=f"{freqs_cm[1]:.2f}",
        f3=f"{freqs_thz[2]:.6f}", w3=f"{freqs_cm[2]:.2f}",
        f4=f"{freqs_thz[3]:.6f}", w4=f"{freqs_cm[3]:.2f}",
        f5=f"{freqs_thz[4]:.6f}", w5=f"{freqs_cm[4]:.2f}",
        f6=f"{freqs_thz[5]:.6f}", w6=f"{freqs_cm[5]:.2f}",
        sym="C3v",
        dos=f"{random.uniform(2.5, 3.5):.3f}",
        ef=f"{random.uniform(-5, -3):.3f}",
        l1=f"{random.uniform(0.1, 0.3):.3f}", g1=f"{random.uniform(1, 3):.2f}",
        l2=f"{random.uniform(0.1, 0.3):.3f}", g2=f"{random.uniform(1, 3):.2f}",
        l3=f"{random.uniform(0.1, 0.3):.3f}", g3=f"{random.uniform(1, 3):.2f}",
        l4=f"{random.uniform(0.1, 0.3):.3f}", g4=f"{random.uniform(1, 3):.2f}",
        l5=f"{random.uniform(0.1, 0.3):.3f}", g5=f"{random.uniform(1, 3):.2f}",
        l6=f"{random.uniform(0.1, 0.3):.3f}", g6=f"{random.uniform(1, 3):.2f}",
        **{"lambda": f"{lambda_val:.3f}"},
        wlog=f"{omega_log * 1.438:.1f}",  # K
        wlog_cm=f"{omega_log:.1f}",
        tc=f"{tc:.1f}",
        ptime=f"{random.uniform(5, 10):.1f}"
    )
    
    # Write files
    (folder / "scf.out").write_text(scf_content)
    (folder / "ph.out").write_text(ph_content)
    
    # Create a mock .dyn0 file for phonon stability check
    dyn_content = """Dynamical matrix file

q =    0.0000   0.0000   0.0000
"""
    for i, (f_thz, f_cm) in enumerate(zip(freqs_thz, freqs_cm), 1):
        dyn_content += f"    freq(   {i}) =    {f_cm:.6f} [cm-1]\n"
    
    (folder / "dyn0").write_text(dyn_content)
    
    time.sleep(0.5)  # Simulate calculation time
    print(f"    ✓ Generated: {folder}/scf.out, ph.out, dyn0")

def main():
    print("=" * 60)
    print("MOCK QE CALCULATIONS FOR Li2NH STRAIN SCAN")
    print("=" * 60)
    print("This simulates QE output for demonstration purposes.")
    print("Real calculations would take 1-4 CPU-hours per strain point.\n")
    
    # Find strain folders
    strain_folders = sorted(pathlib.Path(".").glob("strain_*pc"))
    
    if not strain_folders:
        print("ERROR: No strain folders found. Run strain scan generator first.")
        return
    
    print(f"Found {len(strain_folders)} strain folders to process:\n")
    
    for folder in strain_folders:
        strain = int(folder.name.replace("strain_", "").replace("pc", ""))
        generate_mock_outputs(strain, folder)
    
    print("\n" + "=" * 60)
    print("ALL MOCK CALCULATIONS COMPLETE!")
    print("Now run post-processing to extract λ values and create plots.")
    print("=" * 60)

if __name__ == "__main__":
    main() 