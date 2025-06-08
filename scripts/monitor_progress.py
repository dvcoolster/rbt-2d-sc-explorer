#!/usr/bin/env python3
"""
Live monitoring script for RBT 2D superconductor calculations.
Shows real-time progress, system status, and recent results.
"""

import os
import time
import pathlib
import subprocess
from datetime import datetime
import pandas as pd

def clear_screen():
    """Clear terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')

def get_git_status():
    """Get current git status."""
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True)
        return len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
    except:
        return 0

def count_files_in_strain_folders():
    """Count output files in strain folders."""
    total_files = 0
    completed = 0
    
    for folder in pathlib.Path(".").glob("strain_*pc"):
        scf_exists = (folder / "scf.out").exists()
        ph_exists = (folder / "ph.out").exists()
        dyn_exists = (folder / "dyn0").exists()
        
        if scf_exists:
            total_files += 1
        if ph_exists:
            total_files += 1
        if dyn_exists:
            total_files += 1
            
        if scf_exists and ph_exists and dyn_exists:
            completed += 1
    
    return total_files, completed

def get_latest_results():
    """Get latest Tc results if available."""
    csv_file = pathlib.Path("strain_scan_results.csv")
    if not csv_file.exists():
        return None
    
    try:
        df = pd.read_csv(csv_file)
        max_tc_idx = df['Tc_AD_K'].idxmax()
        return df.loc[max_tc_idx]
    except:
        return None

def format_time_ago(file_path):
    """Format how long ago a file was modified."""
    if not file_path.exists():
        return "N/A"
    
    mtime = file_path.stat().st_mtime
    elapsed = time.time() - mtime
    
    if elapsed < 60:
        return f"{int(elapsed)}s ago"
    elif elapsed < 3600:
        return f"{int(elapsed/60)}m ago"
    elif elapsed < 86400:
        return f"{int(elapsed/3600)}h ago"
    else:
        return f"{int(elapsed/86400)}d ago"

def main():
    """Main monitoring loop."""
    print("Starting RBT 2D-SC Explorer Progress Monitor...")
    print("Press Ctrl+C to exit\n")
    
    try:
        while True:
            clear_screen()
            
            # Header
            print("=" * 80)
            print(f"RBT 2D-SC EXPLORER MONITOR | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("=" * 80)
            
            # Project status
            print("\n📁 PROJECT STATUS:")
            print(f"   Working directory: {pathlib.Path.cwd()}")
            uncommitted = get_git_status()
            if uncommitted > 0:
                print(f"   Git status: {uncommitted} uncommitted changes")
            else:
                print("   Git status: ✓ Clean")
            
            # Strain folders
            strain_folders = list(pathlib.Path(".").glob("strain_*pc"))
            print(f"\n📊 STRAIN CALCULATIONS:")
            print(f"   Total strain points: {len(strain_folders)}")
            
            if strain_folders:
                total_files, completed = count_files_in_strain_folders()
                print(f"   Completed calculations: {completed}/{len(strain_folders)}")
                print(f"   Total output files: {total_files}")
                
                # Show individual folder status
                print("\n   Strain point status:")
                for folder in sorted(strain_folders):
                    strain = folder.name.replace("strain_", "").replace("pc", "")
                    scf = "✓" if (folder / "scf.out").exists() else "○"
                    ph = "✓" if (folder / "ph.out").exists() else "○"
                    dyn = "✓" if (folder / "dyn0").exists() else "○"
                    
                    print(f"     {strain:>4}%: SCF[{scf}] PH[{ph}] DYN[{dyn}]")
            
            # Latest results
            print("\n🔬 LATEST RESULTS:")
            results = get_latest_results()
            if results is not None:
                print(f"   Best strain: {results['strain_%']:+d}%")
                print(f"   Maximum Tc: {results['Tc_AD_K']:.1f} K")
                print(f"   Lambda: {results['lambda']:.3f}")
                print(f"   Status: {'✓ Stable' if results['stable'] else '⚠️  Unstable'}")
                
                if results['Tc_AD_K'] >= 300:
                    print("\n   🎉 ROOM-TEMPERATURE SUPERCONDUCTIVITY ACHIEVED!")
                else:
                    gap = 300 - results['Tc_AD_K']
                    print(f"\n   📊 Gap to room temperature: {gap:.1f} K")
            else:
                print("   No results available yet")
            
            # Recent files
            print("\n📄 RECENT FILES:")
            recent_files = [
                ("Analysis plot", pathlib.Path("strain_scan_analysis.png")),
                ("Results CSV", pathlib.Path("strain_scan_results.csv")),
                ("Li2NH CIF", pathlib.Path("structures/Li2NH_optimized.cif")),
            ]
            
            for name, path in recent_files:
                age = format_time_ago(path)
                status = "✓" if path.exists() else "○"
                print(f"   [{status}] {name}: {age}")
            
            # Available commands
            print("\n⚡ QUICK COMMANDS:")
            print("   • python scripts/generate_strain_scan.py  - Generate strain inputs")
            print("   • python scripts/mock_qe_calculations.py  - Run mock calculations")
            print("   • python scripts/process_strain_scan.py  - Process results")
            print("   • rbt-parity structures/Li2NH_optimized.cif  - Check K value")
            print("   • git status  - Check repository status")
            
            # System resources (simplified)
            print("\n💻 SYSTEM:")
            print(f"   Python: {subprocess.run(['python', '--version'], capture_output=True, text=True).stdout.strip()}")
            print(f"   Environment: {os.environ.get('VIRTUAL_ENV', 'No venv').split('/')[-1]}")
            
            print("\n" + "=" * 80)
            print("Refreshing in 5 seconds... Press Ctrl+C to exit")
            
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped. Goodbye!")
        return 0

if __name__ == "__main__":
    main() 