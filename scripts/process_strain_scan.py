#!/usr/bin/env python3
"""
Post-process QE strain scan results to extract λ values and predict Tc.
"""

import re
import pathlib
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

def extract_lambda_from_ph(ph_file: pathlib.Path) -> dict:
    """Extract lambda and related values from phonon output."""
    content = ph_file.read_text()
    
    # Extract lambda
    lambda_match = re.search(r'lambda\s*=\s*([\d.]+)', content)
    if not lambda_match:
        raise ValueError(f"Could not find lambda in {ph_file}")
    
    # Extract omega_log
    wlog_match = re.search(r'omega\(log\)\s*=\s*([\d.]+)\s*K\s*=\s*([\d.]+)\s*cm-1', content)
    
    # Extract Tc
    tc_match = re.search(r'Estimated Allen-Dynes Tc\s*=\s*([\d.]+)\s*K', content)
    
    return {
        'lambda': float(lambda_match.group(1)),
        'omega_log_K': float(wlog_match.group(1)) if wlog_match else None,
        'omega_log_cm': float(wlog_match.group(2)) if wlog_match else None,
        'Tc_AD': float(tc_match.group(1)) if tc_match else None
    }

def check_phonon_stability(dyn_file: pathlib.Path) -> tuple[bool, float]:
    """Check if all phonon frequencies are positive."""
    content = dyn_file.read_text()
    
    # Extract all frequencies
    freq_matches = re.findall(r'freq\(\s*\d+\)\s*=\s*([-\d.]+)\s*\[cm-1\]', content)
    if not freq_matches:
        return True, 0.0  # Assume stable if no frequencies found
    
    frequencies = [float(f) for f in freq_matches]
    min_freq = min(frequencies)
    
    return min_freq >= 0, min_freq

def calculate_tc_mcmillan(lambda_val: float, omega_log: float, mu_star: float = 0.1) -> float:
    """Calculate Tc using McMillan formula."""
    if lambda_val <= mu_star:
        return 0.0
    
    numerator = omega_log / 1.45
    denominator = (1 + lambda_val) * np.exp(1.04 * (1 + lambda_val) / (lambda_val - mu_star * (1 + 0.62 * lambda_val)))
    
    return numerator / denominator

def main():
    print("=" * 60)
    print("POST-PROCESSING STRAIN SCAN RESULTS")
    print("=" * 60)
    
    # Find all strain folders
    strain_folders = sorted(pathlib.Path(".").glob("strain_*pc"))
    if not strain_folders:
        print("ERROR: No strain folders found!")
        return
    
    results = []
    
    for folder in strain_folders:
        strain_str = folder.name.replace("strain_", "").replace("pc", "")
        strain = int(strain_str)
        
        # Check for output files
        ph_file = folder / "ph.out"
        dyn_file = folder / "dyn0"
        
        if not ph_file.exists():
            print(f"  ⚠️  Missing ph.out in {folder}")
            continue
        
        try:
            # Extract data
            ph_data = extract_lambda_from_ph(ph_file)
            
            # Check stability
            stable = True
            min_freq = 0.0
            if dyn_file.exists():
                stable, min_freq = check_phonon_stability(dyn_file)
            
            # Calculate additional Tc estimates
            tc_mcmillan = None
            if ph_data['omega_log_K']:
                tc_mcmillan = calculate_tc_mcmillan(
                    ph_data['lambda'], 
                    ph_data['omega_log_K']
                )
            
            result = {
                'strain_%': strain,
                'lambda': ph_data['lambda'],
                'omega_log_cm-1': ph_data['omega_log_cm'],
                'Tc_AD_K': ph_data['Tc_AD'],
                'Tc_McMillan_K': tc_mcmillan,
                'stable': stable,
                'min_freq_cm-1': min_freq
            }
            
            results.append(result)
            
            status = "✓ STABLE" if stable else "⚠️  UNSTABLE"
            print(f"  {status} Strain {strain:+3d}%: λ = {ph_data['lambda']:.3f}, Tc = {ph_data['Tc_AD']:.1f} K")
            
        except Exception as e:
            print(f"  ❌ Error processing {folder}: {e}")
    
    if not results:
        print("ERROR: No valid results found!")
        return
    
    # Create DataFrame
    df = pd.DataFrame(results)
    df = df.sort_values('strain_%')
    
    # Save CSV
    csv_file = "strain_scan_results.csv"
    df.to_csv(csv_file, index=False)
    print(f"\n📊 Results saved to {csv_file}")
    
    # Create plots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    
    # 1. Lambda vs strain
    stable_mask = df['stable']
    ax1.plot(df['strain_%'], df['lambda'], 'o-', color='blue', markersize=8)
    ax1.scatter(df.loc[~stable_mask, 'strain_%'], df.loc[~stable_mask, 'lambda'], 
                color='red', s=100, marker='x', label='Unstable')
    ax1.set_xlabel('Strain (%)')
    ax1.set_ylabel('Electron-phonon coupling λ')
    ax1.set_title('Electron-Phonon Coupling vs Strain')
    ax1.grid(True, alpha=0.3)
    ax1.axhline(y=0.84, color='gray', linestyle='--', alpha=0.5, label='Reference')
    if (~stable_mask).any():
        ax1.legend()
    
    # 2. Tc vs strain
    ax2.plot(df['strain_%'], df['Tc_AD_K'], 'o-', color='green', markersize=8, label='Allen-Dynes')
    if df['Tc_McMillan_K'].notna().any():
        ax2.plot(df['strain_%'], df['Tc_McMillan_K'], 's-', color='orange', markersize=6, label='McMillan')
    ax2.scatter(df.loc[~stable_mask, 'strain_%'], df.loc[~stable_mask, 'Tc_AD_K'], 
                color='red', s=100, marker='x')
    ax2.set_xlabel('Strain (%)')
    ax2.set_ylabel('Critical Temperature (K)')
    ax2.set_title('Predicted Tc vs Strain')
    ax2.grid(True, alpha=0.3)
    ax2.axhline(y=300, color='red', linestyle='--', alpha=0.5, label='Room temp')
    ax2.legend()
    
    # 3. Omega_log vs strain
    ax3.plot(df['strain_%'], df['omega_log_cm-1'], 'o-', color='purple', markersize=8)
    ax3.scatter(df.loc[~stable_mask, 'strain_%'], df.loc[~stable_mask, 'omega_log_cm-1'], 
                color='red', s=100, marker='x')
    ax3.set_xlabel('Strain (%)')
    ax3.set_ylabel('ω_log (cm⁻¹)')
    ax3.set_title('Logarithmic Average Phonon Frequency vs Strain')
    ax3.grid(True, alpha=0.3)
    
    # 4. Tc vs lambda
    ax4.scatter(df['lambda'], df['Tc_AD_K'], c=df['strain_%'], s=100, cmap='coolwarm', edgecolor='black')
    cbar = plt.colorbar(ax4.collections[0], ax=ax4, label='Strain (%)')
    ax4.set_xlabel('λ')
    ax4.set_ylabel('Tc (K)')
    ax4.set_title('Tc vs λ (colored by strain)')
    ax4.grid(True, alpha=0.3)
    ax4.axhline(y=300, color='red', linestyle='--', alpha=0.5)
    
    # Overall figure adjustments
    fig.suptitle(f'Li₂NH Strain Scan Analysis - {datetime.now().strftime("%Y-%m-%d")}', fontsize=14)
    plt.tight_layout()
    
    # Save plot
    plot_file = "strain_scan_analysis.png"
    plt.savefig(plot_file, dpi=150, bbox_inches='tight')
    print(f"📈 Plots saved to {plot_file}")
    
    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    max_tc_idx = df['Tc_AD_K'].idxmax()
    max_tc_row = df.loc[max_tc_idx]
    
    print(f"Optimal strain: {max_tc_row['strain_%']:+d}%")
    print(f"Maximum Tc: {max_tc_row['Tc_AD_K']:.1f} K")
    print(f"Corresponding λ: {max_tc_row['lambda']:.3f}")
    print(f"Phonon stability: {'✓ Stable' if max_tc_row['stable'] else '⚠️  Unstable'}")
    
    if max_tc_row['Tc_AD_K'] >= 300:
        print("\n🎉 ROOM-TEMPERATURE SUPERCONDUCTIVITY PREDICTED!")
        print("   Recommend experimental validation at this strain.")
    else:
        print(f"\n📊 Tc below room temperature by {300 - max_tc_row['Tc_AD_K']:.1f} K")
        print("   Consider exploring different materials or larger strains.")
    
    print("=" * 60)

if __name__ == "__main__":
    main() 