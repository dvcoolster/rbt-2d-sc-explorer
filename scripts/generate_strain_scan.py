#!/usr/bin/env python3
"""
Generate strain scan simulation inputs for 2D materials.
Supports Li2NH, BeC3H9, and other materials.
"""

import argparse
import pathlib
import sys
from pymatgen.core import Structure

# Material-specific parameters
MATERIAL_PARAMS = {
    'Li2NH': {
        'ecutwfc': 60.0,
        'ecutrho': 480.0,
        'kgrid': [12, 12, 1],
        'qgrid': [6, 6, 1],
        'pseudos': {
            'Li': 'Li.pbe-spn-kjpaw_psl.1.0.0.UPF',
            'N': 'N.pbe-n-kjpaw_psl.1.0.0.UPF',
            'H': 'H.pbe-kjpaw_psl.1.0.0.UPF'
        }
    },
    'BeC3H9': {
        'ecutwfc': 80.0,
        'ecutrho': 640.0,
        'kgrid': [16, 16, 1],
        'qgrid': [8, 8, 1],
        'pseudos': {
            'Be': 'Be.pbe-spn-kjpaw_psl.1.0.0.UPF',
            'C': 'C.pbe-n-kjpaw_psl.1.0.0.UPF',
            'H': 'H.pbe-kjpaw_psl.1.0.0.UPF'
        }
    },
    'MgB2H4': {
        'ecutwfc': 70.0,
        'ecutrho': 560.0,
        'kgrid': [14, 14, 1],
        'qgrid': [7, 7, 1],
        'pseudos': {
            'Mg': 'Mg.pbe-spn-kjpaw_psl.1.0.0.UPF',
            'B': 'B.pbe-n-kjpaw_psl.1.0.0.UPF',
            'H': 'H.pbe-kjpaw_psl.1.0.0.UPF'
        }
    }
}

def generate_scf_input(material: str, strain_percent: int, structure: Structure, output_dir: pathlib.Path):
    """Generate SCF input file for a given strain."""
    
    params = MATERIAL_PARAMS[material]
    
    # Apply strain to lattice
    strained_lattice = structure.lattice.copy()
    strain_factor = 1 + strain_percent / 100.0
    
    # For 2D materials, apply strain in-plane (a,b) only
    new_matrix = strained_lattice.matrix.copy()
    new_matrix[0] *= strain_factor  # a vector
    new_matrix[1] *= strain_factor  # b vector
    # c vector unchanged for 2D materials
    
    strained_structure = Structure(new_matrix, structure.species, structure.frac_coords)
    
    # Calculate celldm parameters
    a = strained_structure.lattice.a
    c = strained_structure.lattice.c
    celldm1 = a * 1.8897259886  # Convert Angstrom to bohr
    celldm3 = c / a
    
    scf_content = f"""&CONTROL
   calculation = 'scf'
   restart_mode = 'from_scratch'
   prefix = '{material}_strain_{strain_percent:+03d}'
   outdir = './tmp'
   pseudo_dir = './pseudo'
   etot_conv_thr = 1.0d-6
/

&SYSTEM
   ibrav = 4
   celldm(1) = {celldm1:.6f}
   celldm(3) = {celldm3:.6f}
   nat = {len(strained_structure)}
   ntyp = {len(set(strained_structure.species))}
   ecutwfc = {params['ecutwfc']}
   ecutrho = {params['ecutrho']}
   occupations = 'smearing'
   smearing = 'gaussian'
   degauss = 0.02
   assume_isolated = '2D'
/

&ELECTRONS
   conv_thr = 1.0d-10
   mixing_beta = 0.3
   mixing_mode = 'plain'
   electron_maxstep = 100
/

ATOMIC_SPECIES
"""
    
    # Add atomic species
    species_written = set()
    for site in strained_structure:
        element = str(site.specie)
        if element not in species_written:
            atomic_mass = site.specie.atomic_mass
            pseudo = params['pseudos'][element]
            scf_content += f"{element}  {atomic_mass:.6f}  {pseudo}\n"
            species_written.add(element)
    
    scf_content += "\nATOMIC_POSITIONS crystal\n"
    
    # Add atomic positions
    for site in strained_structure:
        element = str(site.specie)
        x, y, z = site.frac_coords
        scf_content += f"{element}  {x:.6f}  {y:.6f}  {z:.6f}\n"
    
    scf_content += f"\nK_POINTS automatic\n"
    scf_content += f"{params['kgrid'][0]} {params['kgrid'][1]} {params['kgrid'][2]} 0 0 0\n"
    
    # Write file
    scf_file = output_dir / "scf.in"
    scf_file.write_text(scf_content)
    
    return scf_file

def generate_ph_input(material: str, strain_percent: int, output_dir: pathlib.Path):
    """Generate phonon input file."""
    
    params = MATERIAL_PARAMS[material]
    
    ph_content = f"""&INPUTPH
   tr2_ph = 1.0d-16
   prefix = '{material}_strain_{strain_percent:+03d}'
   outdir = './tmp'
   fildyn = '{material}_strain_{strain_percent:+03d}.dyn'
   fildvscf = '{material}_strain_{strain_percent:+03d}.dvscf'
   fildrho = '{material}_strain_{strain_percent:+03d}.drho'
   alpha_mix(1) = 0.3
   nmix_ph = 4
   trans = .true.
   epsil = .true.
   zue = .true.
   electron_phonon = 'interpolated'
   el_ph_sigma = 0.005
   el_ph_nsigma = 10
   ldisp = .true.
   nq1 = {params['qgrid'][0]}
   nq2 = {params['qgrid'][1]}
   nq3 = {params['qgrid'][2]}
/
"""
    
    ph_file = output_dir / "ph.in"
    ph_file.write_text(ph_content)
    
    return ph_file

def main():
    parser = argparse.ArgumentParser(description='Generate strain scan for 2D superconductor candidates')
    parser.add_argument('--material', required=True, choices=list(MATERIAL_PARAMS.keys()),
                        help='Material to generate strain scan for')
    parser.add_argument('--output', type=pathlib.Path, required=True,
                        help='Output directory for strain scan')
    parser.add_argument('--strains', nargs='+', type=int, default=[-3, -2, -1, 0, 1, 2, 3],
                        help='Strain percentages to calculate')
    parser.add_argument('--structure', type=pathlib.Path,
                        help='Structure file (CIF). If not provided, uses structures/{material}_optimized.cif')
    
    args = parser.parse_args()
    
    # Load structure
    if args.structure:
        structure_file = args.structure
    else:
        structure_file = pathlib.Path(f"structures/{args.material}_optimized.cif")
    
    if not structure_file.exists():
        print(f"ERROR: Structure file {structure_file} not found!")
        sys.exit(1)
    
    try:
        structure = Structure.from_file(str(structure_file))
    except Exception as e:
        print(f"ERROR: Could not load structure from {structure_file}: {e}")
        sys.exit(1)
    
    print(f"Generating strain scan for {args.material}")
    print(f"Structure: {structure_file}")
    print(f"Output directory: {args.output}")
    print(f"Strain points: {args.strains}%")
    print()
    
    # Create output directory
    args.output.mkdir(parents=True, exist_ok=True)
    
    # Generate strain points
    for strain in args.strains:
        strain_dir = args.output / f"{strain:+03d}"
        strain_dir.mkdir(exist_ok=True)
        
        print(f"  Generating strain {strain:+3d}%: ", end="")
        
        try:
            scf_file = generate_scf_input(args.material, strain, structure, strain_dir)
            ph_file = generate_ph_input(args.material, strain, strain_dir)
            
            # Create README
            readme_content = f"""# Strain {strain:+d}% for {args.material}

Generated by generate_strain_scan.py

## Files:
- scf.in: Self-consistent field calculation
- ph.in: Phonon calculation with electron-phonon coupling

## Run sequence:
1. pw.x < scf.in > scf.out
2. ph.x < ph.in > ph.out

## Expected strain effects:
- Lattice parameter change: {1 + strain/100:.3f}x
- Expected lambda change: {"increase" if strain < 0 else "decrease"}
"""
            (strain_dir / "README.md").write_text(readme_content)
            
            print(f"✓ Generated scf.in, ph.in, README.md")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n✅ Strain scan generated in {args.output}")
    print(f"   Materials parameters used: {MATERIAL_PARAMS[args.material]}")
    print(f"   Total strain points: {len(args.strains)}")

if __name__ == "__main__":
    main() 