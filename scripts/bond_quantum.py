#!/usr/bin/env python3
"""
RBT Bond Quantum Analyzer: ħω*/π ≥ 0.081 eV Test

This script analyzes crystal structures to estimate the characteristic
phonon energy ħω*/π from the shortest light-atom bonds. According to
RBT theory, superconductivity requires ħω*/π ≥ 0.081 eV.

Usage:
    python bond_quantum.py structure.cif
    python bond_quantum.py POSCAR
"""

import sys
import os
import numpy as np
from pymatgen.core import Structure, Element
from pymatgen.io.cif import CifParser
from pymatgen.io.vasp import Poscar
from pymatgen.analysis.local_env import CrystalNN
import argparse
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

class BondQuantumAnalyzer:
    """
    Analyzes bond lengths and estimates characteristic phonon energies
    for RBT superconductivity screening.
    """
    
    # Physical constants
    HBAR = 6.582119569e-16  # eV⋅s
    PI = np.pi
    
    # Light atoms that dominate phonon frequencies (atomic mass < 20 u)
    LIGHT_ATOMS = {'H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne'}
    
    def __init__(self):
        """Initialize the bond quantum analyzer."""
        self.cnn = CrystalNN()
        self.threshold_energy = 0.081  # eV, RBT threshold for superconductivity
    
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
    
    def find_light_atom_bonds(self, structure: Structure) -> List[Dict]:
        """
        Find all bonds involving light atoms (H, Li, B, C, N, etc.).
        
        Args:
            structure: pymatgen Structure object
            
        Returns:
            List of bond dictionaries with distances and atom types
        """
        light_bonds = []
        
        print("  Analyzing bonds involving light atoms...")
        
        for i, site in enumerate(structure):
            element = site.species_string
            
            # Only analyze bonds from light atoms
            if element not in self.LIGHT_ATOMS:
                continue
            
            try:
                neighbors = self.cnn.get_nn_info(structure, i)
                
                for neighbor in neighbors:
                    j = neighbor['site_index']
                    distance = neighbor['weight']
                    neighbor_element = structure[j].species_string
                    
                    # Create bond descriptor
                    bond = {
                        'atom1_idx': i,
                        'atom2_idx': j,
                        'atom1_element': element,
                        'atom2_element': neighbor_element,
                        'distance': distance,
                        'reduced_mass': self._calculate_reduced_mass(element, neighbor_element),
                        'bond_type': f"{element}-{neighbor_element}",
                        'both_light': (element in self.LIGHT_ATOMS and 
                                     neighbor_element in self.LIGHT_ATOMS)
                    }
                    
                    light_bonds.append(bond)
                    
            except Exception as e:
                print(f"    Warning: Could not analyze bonds for atom {i} ({element}): {e}")
                continue
        
        # Remove duplicates (each bond counted twice)
        unique_bonds = []
        seen_pairs = set()
        
        for bond in light_bonds:
            pair = tuple(sorted([bond['atom1_idx'], bond['atom2_idx']]))
            if pair not in seen_pairs:
                unique_bonds.append(bond)
                seen_pairs.add(pair)
        
        print(f"  Found {len(unique_bonds)} unique light-atom bonds")
        return unique_bonds
    
    def _calculate_reduced_mass(self, element1: str, element2: str) -> float:
        """Calculate reduced mass of two atoms in atomic mass units."""
        try:
            m1 = Element(element1).atomic_mass
            m2 = Element(element2).atomic_mass
            reduced_mass = (m1 * m2) / (m1 + m2)
            return reduced_mass
        except:
            return 1.0  # Fallback
    
    def estimate_phonon_energy(self, bond_distance: float, reduced_mass: float) -> float:
        """
        Estimate characteristic phonon energy ħω*/π from bond parameters.
        
        Uses simplified harmonic oscillator model:
        ω = sqrt(k/μ) where k ∝ 1/r³ for typical covalent bonds
        
        Args:
            bond_distance: Bond length in Angstroms
            reduced_mass: Reduced mass in atomic mass units
            
        Returns:
            Energy ħω*/π in eV
        """
        # Convert units
        r_angstrom = bond_distance
        mu_amu = reduced_mass
        
        # Empirical scaling for 2-D materials (fitted to known cases)
        # This is a simplified model - real calculations would use DFT
        force_constant_scale = 100.0  # eV/Å² empirical factor
        k_force = force_constant_scale / (r_angstrom ** 2)  # Force constant
        
        # Convert reduced mass to eV⋅s²/Å²
        amu_to_ev_per_ang2 = 1.036427e-4  # Conversion factor
        mu_ev_units = mu_amu * amu_to_ev_per_ang2
        
        # Angular frequency
        omega = np.sqrt(k_force / mu_ev_units)  # rad/s in natural units
        
        # Energy ħω*/π
        energy_meV = (self.HBAR * omega / self.PI) * 1000  # Convert to meV
        energy_eV = energy_meV / 1000
        
        return energy_eV
    
    def analyze_structure(self, filepath: str) -> Dict:
        """
        Complete bond quantum analysis of a crystal structure.
        
        Args:
            filepath: Path to structure file
            
        Returns:
            Dictionary with analysis results
        """
        print(f"\n{'='*60}")
        print(f"RBT BOND QUANTUM ANALYSIS: {os.path.basename(filepath)}")
        print(f"{'='*60}")
        
        # Load structure
        structure = self.load_structure(filepath)
        
        # Find light atom bonds
        light_bonds = self.find_light_atom_bonds(structure)
        
        if not light_bonds:
            print("  ⚠️  No light-atom bonds found!")
            return {
                'filepath': filepath,
                'formula': structure.formula,
                'light_bonds': [],
                'shortest_bond': None,
                'phonon_energy_meV': 0,
                'phonon_energy_eV': 0,
                'passes_energy_test': False,
                'critical_bonds': []
            }
        
        # Calculate phonon energies for all bonds
        for bond in light_bonds:
            bond['phonon_energy_eV'] = self.estimate_phonon_energy(
                bond['distance'], bond['reduced_mass']
            )
            bond['phonon_energy_meV'] = bond['phonon_energy_eV'] * 1000
        
        # Sort by shortest bonds (highest frequencies)
        light_bonds.sort(key=lambda x: x['distance'])
        
        # Find critical bonds (highest energy)
        critical_bonds = [b for b in light_bonds if b['phonon_energy_eV'] >= self.threshold_energy]
        
        # Get the shortest bond (likely to dominate)
        shortest_bond = light_bonds[0]
        max_energy = max(bond['phonon_energy_eV'] for bond in light_bonds)
        
        results = {
            'filepath': filepath,
            'formula': structure.formula,
            'light_bonds': light_bonds,
            'shortest_bond': shortest_bond,
            'phonon_energy_meV': max_energy * 1000,
            'phonon_energy_eV': max_energy,
            'passes_energy_test': max_energy >= self.threshold_energy,
            'critical_bonds': critical_bonds,
            'threshold_meV': self.threshold_energy * 1000
        }
        
        return results
    
    def print_results(self, results: Dict):
        """Print formatted analysis results."""
        print(f"\nRESULTS:")
        print(f"  Formula: {results['formula']}")
        print(f"  Max phonon energy: {results['phonon_energy_meV']:.1f} meV")
        print(f"  Threshold energy: {results['threshold_meV']:.1f} meV")
        
        if results['passes_energy_test']:
            print(f"  ✅ PASSES energy test (ħω*/π ≥ {self.threshold_energy} eV)")
            print(f"  ➡️  Material satisfies RBT energy condition")
        else:
            print(f"  ❌ FAILS energy test (ħω*/π < {self.threshold_energy} eV)")
            print(f"  ➡️  Insufficient phonon coupling for superconductivity")
        
        if results['shortest_bond']:
            bond = results['shortest_bond']
            print(f"\nSHORTEST LIGHT-ATOM BOND:")
            print(f"  Bond: {bond['bond_type']}")
            print(f"  Distance: {bond['distance']:.3f} Å")
            print(f"  Reduced mass: {bond['reduced_mass']:.2f} u")
            print(f"  Phonon energy: {bond['phonon_energy_meV']:.1f} meV")
        
        if results['critical_bonds']:
            print(f"\nCRITICAL BONDS (above threshold):")
            for bond in results['critical_bonds'][:5]:  # Show top 5
                print(f"  {bond['bond_type']}: {bond['distance']:.3f} Å → {bond['phonon_energy_meV']:.1f} meV")
        
        print(f"\nTOTAL LIGHT-ATOM BONDS ANALYZED: {len(results['light_bonds'])}")

def main():
    parser = argparse.ArgumentParser(
        description="RBT Bond Quantum Analyzer for Phonon Energy Estimation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python bond_quantum.py Li2NH.cif
    python bond_quantum.py POSCAR
    python bond_quantum.py --threshold 0.090 structure.cif
        """
    )
    
    parser.add_argument('structure_file', 
                       help='Path to crystal structure file (CIF, POSCAR, etc.)')
    parser.add_argument('--threshold', type=float, default=0.081,
                       help='Energy threshold in eV (default: 0.081)')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Suppress detailed output')
    
    args = parser.parse_args()
    
    try:
        # Initialize analyzer
        analyzer = BondQuantumAnalyzer()
        analyzer.threshold_energy = args.threshold
        
        # Analyze structure
        results = analyzer.analyze_structure(args.structure_file)
        
        # Print results
        if not args.quiet:
            analyzer.print_results(results)
        
        # Exit code: 0 if passes, 1 if fails
        exit_code = 0 if results['passes_energy_test'] else 1
        
        if args.quiet:
            energy_meV = results['phonon_energy_meV']
            threshold_meV = results['threshold_meV']
            status = 'PASS' if results['passes_energy_test'] else 'FAIL'
            print(f"ħω*/π={energy_meV:.1f}meV (threshold={threshold_meV:.1f}meV) {status}")
        
        sys.exit(exit_code)
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        sys.exit(2)

if __name__ == "__main__":
    main() 