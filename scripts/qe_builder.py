#!/usr/bin/env python3
"""
Quantum Espresso Input Builder for RBT Phonon Validation

This script generates Quantum Espresso (QE) input files for phonon
calculations to validate the RBT bond quantum estimates with DFT.

Usage:
    python qe_builder.py structure.cif -o scf.in
    python qe_builder.py POSCAR --phonons --prefix Li2NH
"""

import sys
import os
import numpy as np
from pymatgen.core import Structure
from pymatgen.io.cif import CifParser
from pymatgen.io.vasp import Poscar
from pymatgen.io.pwscf import PWInput
import argparse
from typing import Dict, List
import warnings
warnings.filterwarnings('ignore')

class QEInputBuilder:
    """
    Builds Quantum Espresso input files for 2-D materials phonon calculations.
    """
    
    # Pseudopotential mapping (using standard PAW/USPP)
    PSEUDOPOTENTIALS = {
        'H': 'H.pbe-rrkjus_psl.1.0.0.UPF',
        'Li': 'Li.pbe-s-rrkjus_psl.1.0.0.UPF',
        'Be': 'Be.pbe-n-rrkjus_psl.1.0.0.UPF',
        'B': 'B.pbe-n-rrkjus_psl.1.0.0.UPF',
        'C': 'C.pbe-n-rrkjus_psl.1.0.0.UPF',
        'N': 'N.pbe-n-rrkjus_psl.1.0.0.UPF',
        'O': 'O.pbe-n-rrkjus_psl.1.0.0.UPF',
        'F': 'F.pbe-n-rrkjus_psl.1.0.0.UPF',
        'Al': 'Al.pbe-n-rrkjus_psl.1.0.0.UPF',
        'Si': 'Si.pbe-n-rrkjus_psl.1.0.0.UPF',
        'P': 'P.pbe-n-rrkjus_psl.1.0.0.UPF',
        'S': 'S.pbe-n-rrkjus_psl.1.0.0.UPF',
        'Cl': 'Cl.pbe-n-rrkjus_psl.1.0.0.UPF',
    }
    
    def __init__(self):
        """Initialize the QE input builder."""
        pass
    
    def load_structure(self, filepath: str) -> Structure:
        """Load crystal structure from various file formats."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Structure file not found: {filepath}")
        
        file_ext = os.path.splitext(filepath)[1].lower()
        
        try:
            if file_ext == '.cif':
                parser = CifParser(filepath)
                structure = parser.get_structures()[0]
            elif filepath.endswith('POSCAR') or filepath.endswith('CONTCAR'):
                poscar = Poscar.from_file(filepath)
                structure = poscar.structure
            else:
                structure = Structure.from_file(filepath)
            
            print(f"✓ Loaded structure: {structure.formula}")
            return structure
            
        except Exception as e:
            raise ValueError(f"Could not parse structure file {filepath}: {str(e)}")
    
    def generate_scf_input(self, structure: Structure, prefix: str = "pwscf") -> Dict:
        """
        Generate SCF calculation input parameters.
        
        Args:
            structure: pymatgen Structure
            prefix: Calculation prefix
            
        Returns:
            Dictionary with QE input parameters
        """
        # Get unique elements and set up pseudopotentials
        elements = [str(el) for el in structure.composition.elements]
        pseudopotentials = {}
        
        for element in elements:
            if element in self.PSEUDOPOTENTIALS:
                pseudopotentials[element] = self.PSEUDOPOTENTIALS[element]
            else:
                # Generic pseudopotential name
                pseudopotentials[element] = f"{element}.pbe-n-kjpaw_psl.1.0.0.UPF"
        
        # Determine if 2-D system (look for large vacuum layer)
        lattice = structure.lattice
        c_length = lattice.c
        is_2d = c_length > 15.0  # Likely 2-D if c > 15 Å
        
        # K-point sampling
        if is_2d:
            # For 2-D: dense in-plane, minimal out-of-plane
            kpts = [8, 8, 1]
        else:
            # For 3-D: balanced sampling
            kpts = [6, 6, 6]
        
        # Energy cutoffs (depend on pseudopotentials)
        ecutwfc = 60.0  # Ry, conservative value
        ecutrho = 480.0  # Ry, typically 8x ecutwfc for PAW
        
        control_params = {
            'calculation': 'scf',
            'restart_mode': 'from_scratch',
            'prefix': prefix,
            'pseudo_dir': './pseudo',
            'outdir': './tmp',
            'verbosity': 'high'
        }
        
        system_params = {
            'ibrav': 0,
            'nat': len(structure),
            'ntyp': len(elements),
            'ecutwfc': ecutwfc,
            'ecutrho': ecutrho,
            'occupations': 'smearing',
            'smearing': 'gaussian',
            'degauss': 0.01
        }
        
        # Add 2-D specific parameters
        if is_2d:
            system_params['assume_isolated'] = '2D'
            
        electrons_params = {
            'conv_thr': 1.0e-8,
            'mixing_beta': 0.3,
            'mixing_mode': 'plain'
        }
        
        return {
            'control': control_params,
            'system': system_params,
            'electrons': electrons_params,
            'pseudopotentials': pseudopotentials,
            'kpts': kpts,
            'structure': structure
        }
    
    def generate_phonon_input(self, structure: Structure, prefix: str = "pwscf") -> Dict:
        """
        Generate phonon calculation input parameters.
        
        Args:
            structure: pymatgen Structure  
            prefix: Calculation prefix
            
        Returns:
            Dictionary with phonon input parameters
        """
        ph_params = {
            'inputph': {
                'tr2_ph': 1.0e-14,
                'prefix': prefix,
                'ldisp': True,
                'nq1': 4, 'nq2': 4, 'nq3': 1,  # Phonon q-point grid
                'alpha_mix(1)': 0.3,
                'fildyn': f'{prefix}.dyn',
                'outdir': './tmp'
            }
        }
        
        return ph_params
    
    def write_scf_input(self, params: Dict, output_file: str):
        """Write SCF input file in QE format."""
        
        with open(output_file, 'w') as f:
            # Control section
            f.write("&CONTROL\n")
            for key, value in params['control'].items():
                if isinstance(value, str):
                    f.write(f"  {key} = '{value}'\n")
                else:
                    f.write(f"  {key} = {value}\n")
            f.write("/\n\n")
            
            # System section
            f.write("&SYSTEM\n")
            for key, value in params['system'].items():
                if isinstance(value, str):
                    f.write(f"  {key} = '{value}'\n")
                else:
                    f.write(f"  {key} = {value}\n")
            f.write("/\n\n")
            
            # Electrons section
            f.write("&ELECTRONS\n")
            for key, value in params['electrons'].items():
                if isinstance(value, str):
                    f.write(f"  {key} = '{value}'\n")
                else:
                    f.write(f"  {key} = {value}\n")
            f.write("/\n\n")
            
            # Atomic species
            f.write("ATOMIC_SPECIES\n")
            structure = params['structure']
            for element in params['pseudopotentials']:
                mass = structure.composition[element].atomic_mass
                pseudo = params['pseudopotentials'][element]
                f.write(f"  {element}  {mass:.6f}  {pseudo}\n")
            f.write("\n")
            
            # Cell parameters
            f.write("CELL_PARAMETERS (angstrom)\n")
            lattice = structure.lattice.matrix
            for row in lattice:
                f.write(f"  {row[0]:12.8f}  {row[1]:12.8f}  {row[2]:12.8f}\n")
            f.write("\n")
            
            # Atomic positions
            f.write("ATOMIC_POSITIONS (crystal)\n")
            for site in structure:
                element = site.species_string
                coords = site.frac_coords
                f.write(f"  {element}  {coords[0]:12.8f}  {coords[1]:12.8f}  {coords[2]:12.8f}\n")
            f.write("\n")
            
            # K-points
            kpts = params['kpts']
            f.write("K_POINTS (automatic)\n")
            f.write(f"  {kpts[0]} {kpts[1]} {kpts[2]}  0 0 0\n")
    
    def write_phonon_input(self, params: Dict, output_file: str):
        """Write phonon input file in QE format."""
        
        with open(output_file, 'w') as f:
            f.write("&INPUTPH\n")
            for key, value in params['inputph'].items():
                if isinstance(value, str):
                    f.write(f"  {key} = '{value}'\n")
                elif isinstance(value, bool):
                    f.write(f"  {key} = .{str(value).lower()}.\n")
                else:
                    f.write(f"  {key} = {value}\n")
            f.write("/\n")
    
    def generate_run_script(self, prefix: str, output_file: str = "run_qe.sh"):
        """Generate a bash script to run the QE calculations."""
        
        script_content = f"""#!/bin/bash
# Quantum Espresso calculation script for {prefix}
# Generated by RBT QE Builder

# Set number of processors (adjust based on your system)
NPROC=4

# Paths (adjust based on your QE installation)
PW_COMMAND="mpirun -np $NPROC pw.x"
PH_COMMAND="mpirun -np $NPROC ph.x"

echo "Starting RBT-QE phonon calculation for {prefix}"
echo "=========================================="

# Create necessary directories
mkdir -p tmp pseudo

echo "Step 1: SCF calculation"
$PW_COMMAND < {prefix}_scf.in > {prefix}_scf.out
if [ $? -ne 0 ]; then
    echo "ERROR: SCF calculation failed!"
    exit 1
fi

echo "Step 2: Phonon calculation"  
$PH_COMMAND < {prefix}_ph.in > {prefix}_ph.out
if [ $? -ne 0 ]; then
    echo "ERROR: Phonon calculation failed!"
    exit 1
fi

echo "Step 3: Post-processing"
# Calculate phonon DOS and dispersion
dynmat.x < {prefix}_dynmat.in > {prefix}_dynmat.out
q2r.x < {prefix}_q2r.in > {prefix}_q2r.out
matdyn.x < {prefix}_matdyn.in > {prefix}_matdyn.out

echo "Calculation completed successfully!"
echo "Check {prefix}_matdyn.out for phonon frequencies"
"""
        
        with open(output_file, 'w') as f:
            f.write(script_content)
        
        # Make executable
        os.chmod(output_file, 0o755)
        print(f"✓ Created run script: {output_file}")

def main():
    parser = argparse.ArgumentParser(
        description="Quantum Espresso Input Builder for RBT Phonon Validation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python qe_builder.py Li2NH.cif -o scf
    python qe_builder.py POSCAR --phonons --prefix graphane
    python qe_builder.py structure.cif --full --nproc 8
        """
    )
    
    parser.add_argument('structure_file', 
                       help='Path to crystal structure file (CIF, POSCAR, etc.)')
    parser.add_argument('-o', '--output', default='pwscf',
                       help='Output file prefix (default: pwscf)')
    parser.add_argument('--prefix', default=None,
                       help='Calculation prefix (default: based on structure file)')
    parser.add_argument('--phonons', action='store_true',
                       help='Generate phonon calculation inputs')
    parser.add_argument('--full', action='store_true',
                       help='Generate complete calculation workflow')
    parser.add_argument('--nproc', type=int, default=4,
                       help='Number of processors for run script (default: 4)')
    
    args = parser.parse_args()
    
    try:
        # Initialize builder
        builder = QEInputBuilder()
        
        # Load structure
        structure = builder.load_structure(args.structure_file)
        
        # Set prefix
        if args.prefix:
            prefix = args.prefix
        else:
            prefix = os.path.splitext(os.path.basename(args.structure_file))[0]
        
        print(f"Generating QE inputs for: {prefix}")
        print(f"Formula: {structure.formula}")
        
        # Generate SCF input
        scf_params = builder.generate_scf_input(structure, prefix)
        scf_file = f"{args.output}_scf.in"
        builder.write_scf_input(scf_params, scf_file)
        print(f"✓ Created SCF input: {scf_file}")
        
        # Generate phonon inputs if requested
        if args.phonons or args.full:
            ph_params = builder.generate_phonon_input(structure, prefix)
            ph_file = f"{args.output}_ph.in"
            builder.write_phonon_input(ph_params, ph_file)
            print(f"✓ Created phonon input: {ph_file}")
        
        # Generate full workflow if requested
        if args.full:
            run_script = f"run_{prefix}.sh"
            builder.generate_run_script(prefix, run_script)
            
            print(f"\n{'='*50}")
            print("FULL QE WORKFLOW GENERATED:")
            print(f"1. SCF: {scf_file}")
            print(f"2. Phonons: {ph_file}")
            print(f"3. Run script: {run_script}")
            print(f"\nTo run: ./{run_script}")
            print("(Make sure pseudopotentials are in ./pseudo/)")
        
        print("\n✅ QE input generation completed successfully!")
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 