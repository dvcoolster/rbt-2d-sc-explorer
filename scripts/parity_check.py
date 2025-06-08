#!/usr/bin/env python3
"""
RBT Parity Checker: K = 0 Test for 2-D Superconductor Candidates

This script takes a crystal structure (CIF, POSCAR, etc.) and determines
whether it satisfies the RBT parity condition: K = 0 (even number of 
odd-degree vertices in the crystal graph).

Usage:
    python parity_check.py structure.cif
    python parity_check.py POSCAR
"""

import sys
import os
import numpy as np
import networkx as nx
from pymatgen.core import Structure
from pymatgen.io.cif import CifParser
from pymatgen.io.vasp import Poscar
from pymatgen.analysis.local_env import CrystalNN
import argparse
from typing import Tuple, List, Dict
import warnings
warnings.filterwarnings('ignore')

class RBTParityChecker:
    """
    Analyzes crystal structures for RBT parity condition (K = 0).
    
    The parity parameter K counts odd-degree vertices in the crystal
    connectivity graph. For superconductivity, we need K = 0.
    """
    
    def __init__(self, cutoff_distance: float = 3.5):
        """
        Initialize the parity checker.
        
        Args:
            cutoff_distance: Maximum bond distance in Angstroms for graph construction
        """
        self.cutoff_distance = cutoff_distance
        self.cnn = CrystalNN()
    
    def load_structure(self, filepath: str) -> Structure:
        """Load crystal structure from various file formats."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Structure file not found: {filepath}")
        
        file_ext = os.path.splitext(filepath)[1].lower()
        
        try:
            if file_ext == '.cif':
                parser = CifParser(filepath)
                structure = parser.get_structures()[0]  # Take first structure
            elif filepath.endswith('POSCAR') or filepath.endswith('CONTCAR'):
                poscar = Poscar.from_file(filepath)
                structure = poscar.structure
            else:
                # Try pymatgen's generic structure reader
                structure = Structure.from_file(filepath)
            
            print(f"✓ Loaded structure: {structure.formula}")
            print(f"  Space group: {structure.get_space_group_info()[1]}")
            print(f"  Lattice: a={structure.lattice.a:.3f}, b={structure.lattice.b:.3f}, c={structure.lattice.c:.3f}")
            
            return structure
            
        except Exception as e:
            raise ValueError(f"Could not parse structure file {filepath}: {str(e)}")
    
    def build_connectivity_graph(self, structure: Structure) -> nx.Graph:
        """
        Build connectivity graph of the crystal structure.
        
        Args:
            structure: pymatgen Structure object
            
        Returns:
            NetworkX graph representing atomic connectivity
        """
        G = nx.Graph()
        
        # Add all atoms as nodes
        for i, site in enumerate(structure):
            G.add_node(i, 
                      element=site.species_string,
                      coords=site.coords,
                      frac_coords=site.frac_coords)
        
        # Add edges based on CrystalNN neighbor finding
        print("  Building connectivity graph...")
        
        for i, site in enumerate(structure):
            try:
                # Get neighbors using CrystalNN
                neighbors = self.cnn.get_nn_info(structure, i)
                
                for neighbor in neighbors:
                    j = neighbor['site_index']
                    distance = neighbor['weight']  # Distance in Angstroms
                    
                    # Add edge if within cutoff and not already present
                    if distance <= self.cutoff_distance and not G.has_edge(i, j):
                        G.add_edge(i, j, distance=distance)
                        
            except Exception as e:
                print(f"    Warning: Could not find neighbors for atom {i}: {e}")
                continue
        
        print(f"  Graph built: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
        return G
    
    def calculate_parity(self, graph: nx.Graph) -> Tuple[int, List[int], Dict]:
        """
        Calculate the RBT parity parameter K.
        
        Args:
            graph: NetworkX graph of atomic connectivity
            
        Returns:
            Tuple of (K value, list of odd-degree vertices, degree statistics)
        """
        degrees = dict(graph.degree())
        degree_values = list(degrees.values())
        
        # Count odd-degree vertices
        odd_vertices = [node for node, degree in degrees.items() if degree % 2 == 1]
        K = len(odd_vertices)
        
        # Statistics
        stats = {
            'total_vertices': graph.number_of_nodes(),
            'total_edges': graph.number_of_edges(),
            'min_degree': min(degree_values) if degree_values else 0,
            'max_degree': max(degree_values) if degree_values else 0,
            'avg_degree': np.mean(degree_values) if degree_values else 0,
            'odd_degree_count': K,
            'even_degree_count': len(degree_values) - K
        }
        
        return K, odd_vertices, stats
    
    def analyze_structure(self, filepath: str) -> Dict:
        """
        Complete parity analysis of a crystal structure.
        
        Args:
            filepath: Path to structure file
            
        Returns:
            Dictionary with analysis results
        """
        print(f"\n{'='*60}")
        print(f"RBT PARITY ANALYSIS: {os.path.basename(filepath)}")
        print(f"{'='*60}")
        
        # Load structure
        structure = self.load_structure(filepath)
        
        # Build connectivity graph
        graph = self.build_connectivity_graph(structure)
        
        # Calculate parity
        K, odd_vertices, stats = self.calculate_parity(graph)
        
        # Results
        results = {
            'filepath': filepath,
            'formula': structure.formula,
            'K_parity': K,
            'passes_parity_test': K == 0,
            'odd_vertices': odd_vertices,
            'graph_stats': stats,
            'structure': structure
        }
        
        return results
    
    def print_results(self, results: Dict):
        """Print formatted analysis results."""
        print(f"\nRESULTS:")
        print(f"  Formula: {results['formula']}")
        print(f"  Parity parameter K = {results['K_parity']}")
        
        if results['passes_parity_test']:
            print(f"  ✅ PASSES parity test (K = 0)")
            print(f"  ➡️  Proceed to bond quantum analysis")
        else:
            print(f"  ❌ FAILS parity test (K ≠ 0)")
            print(f"  ➡️  Skip this material - not a superconductor candidate")
        
        stats = results['graph_stats']
        print(f"\nGRAPH STATISTICS:")
        print(f"  Total atoms: {stats['total_vertices']}")
        print(f"  Total bonds: {stats['total_edges']}")
        print(f"  Degree range: {stats['min_degree']} - {stats['max_degree']}")
        print(f"  Average degree: {stats['avg_degree']:.2f}")
        print(f"  Odd-degree atoms: {stats['odd_degree_count']}")
        print(f"  Even-degree atoms: {stats['even_degree_count']}")
        
        if results['odd_vertices']:
            print(f"\nODD-DEGREE VERTICES:")
            structure = results['structure']
            for vertex in results['odd_vertices'][:10]:  # Show first 10
                site = structure[vertex]
                degree = dict(nx.degree(self.build_connectivity_graph(structure)))[vertex]
                print(f"  Atom {vertex}: {site.species_string} (degree {degree})")
            if len(results['odd_vertices']) > 10:
                print(f"  ... and {len(results['odd_vertices']) - 10} more")

def main():
    parser = argparse.ArgumentParser(
        description="RBT Parity Checker for 2-D Superconductor Screening",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python parity_check.py Li2NH.cif
    python parity_check.py POSCAR
    python parity_check.py --cutoff 4.0 structure.cif
        """
    )
    
    parser.add_argument('structure_file', 
                       help='Path to crystal structure file (CIF, POSCAR, etc.)')
    parser.add_argument('--cutoff', type=float, default=3.5,
                       help='Bond distance cutoff in Angstroms (default: 3.5)')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Suppress detailed output')
    
    args = parser.parse_args()
    
    try:
        # Initialize checker
        checker = RBTParityChecker(cutoff_distance=args.cutoff)
        
        # Analyze structure
        results = checker.analyze_structure(args.structure_file)
        
        # Print results
        if not args.quiet:
            checker.print_results(results)
        
        # Exit code: 0 if passes, 1 if fails
        exit_code = 0 if results['passes_parity_test'] else 1
        
        if args.quiet:
            print(f"K={results['K_parity']} {'PASS' if results['passes_parity_test'] else 'FAIL'}")
        
        sys.exit(exit_code)
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        sys.exit(2)

if __name__ == "__main__":
    main() 