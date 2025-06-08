# Measurement Playbook: Room-Temperature Superconductivity Detection
## 4-Probe Resistance Protocol for Li₂NH Films

**Objective**: Detect resistance drop R(T) < 10 nΩ from 300-350K  
**Timeline**: 1 day (device prep + measurement)  
**Success criteria**: Flat resistance curve at target temperature

---

## Equipment Required

### Primary Measurement Setup
- **Nano-ohmmeter**: Keithley 2182A or equivalent (1 nΩ resolution)
- **Current source**: Keithley 6221 or 6220 (1 pA - 100 mA range)
- **Temperature controller**: LakeShore 331 or 336
- **Probe station**: Cascade or SuSS with heated chuck (up to 400K)
- **Low-noise cables**: Triaxial for current, twisted-pair for voltage

### Device Fabrication Tools
- **Photolithography**: Standard UV exposure system
- **Etching**: RIE or ion beam etching
- **Metallization**: E-beam evaporator (Ti/Au contacts)
- **Wire bonding**: Ultrasonic wire bonder

---

## Part 1: Device Preparation (3-4 hours)

### 1.1 Hall Bar Patterning
```bash
# Standard photolithography for 4-probe geometry
Device dimensions:
- Channel length: 100 μm (L)
- Channel width: 50 μm (W)  
- Contact pad size: 50×50 μm
- Contact separation: 25 μm (voltage probes)

Process:
1. Spin photoresist: AZ5214E, 4000 rpm, 30 s
2. Pre-bake: 90°C, 60 s
3. UV exposure: 12 mJ/cm² through Hall bar mask
4. Development: AZ developer, 45 s
5. Post-bake: 120°C, 2 min
```

### 1.2 Film Etching (Optional)
```bash
# Only if device isolation needed
Tool: Ar ion beam etching (gentle, avoid damage)
Rate: 0.5 nm/s
Depth: 30 nm (partial etch, leave 20 nm)
Monitor: Optical emission spectroscopy (Li and N lines)

# Alternative: Use shadow mask during deposition (preferred)
```

### 1.3 Contact Metallization
```bash
# Ti adhesion layer + Au top contact
Chamber: E-beam evaporator
Base pressure: < 5×10⁻⁸ Torr
Deposition rate: 0.2 Å/s (Ti), 0.5 Å/s (Au)

Layer stack:
1. Ti: 5 nm (contact layer, low work function)
2. Au: 50 nm (low resistance, wire bondable)

# Critical: No O₂ exposure between BN etch and Ti deposition
```

### 1.4 Contact Annealing
```bash
# Form ohmic contacts
Temperature: 200°C (below Li₂NH degradation)
Atmosphere: Forming gas (95% N₂ + 5% H₂)
Time: 30 min
Heating rate: 5°C/min

# Check contact resistance: < 1 Ω⋅μm (good contact)
```

---

## Part 2: Electrical Characterization

### 2.1 Initial Contact Check (15 min)
```bash
# 4-probe contact resistance at room temperature
Measurement: DC I-V sweep
Current range: ±100 μA
Voltage compliance: ±10 V
Data points: 21 points (-100 to +100 μA)

Target results:
- Linear I-V (ohmic contacts)
- Contact resistance < 1 Ω⋅μm
- No rectification or gating effects
```

### 2.2 Room Temperature Baseline (30 min)
```bash
# Establish baseline resistance before heating
Temperature: 295 K (stable ±0.1 K)
Current: 1 μA DC (non-heating)
Integration time: 10 s per point
Duration: 30 min (check stability)

Expected baseline:
- Sheet resistance: 10-1000 Ω/□ (typical for thin films)
- Time stability: <5% drift over 30 min
- Low noise: <0.1% of signal
```

### 2.3 Temperature Sweep Protocol
```bash
# Critical measurement: R(T) from 300-350K
Heating rate: 1 K/min (slow for thermal equilibrium)
Current: 1 μA (constant current mode)
Temperature points: Every 1 K
Stabilization: 60 s at each temperature
Voltage averaging: 10 samples per point

# Data logging
File format: CSV with columns [T(K), R(Ω), V(V), I(A), time]
Real-time plotting: R vs T to monitor for transitions
```

---

## Part 3: Critical Temperature Detection

### 3.1 Superconducting Transition Identification
```bash
# Look for characteristic signatures
1. Resistance drop: R decreases sharply with increasing T
2. Onset temperature: 50% resistance drop point
3. Zero resistance: R < 10 nΩ (instrument limited)
4. Critical current: Switch to I-V measurements

# Tc determination
Method 1: 50% criterion (onset)
Method 2: Zero resistance criterion (< 10 nΩ)
Method 3: dR/dT maximum (transition midpoint)
```

### 3.2 Critical Current Measurement
```bash
# Only if zero resistance achieved
Current sweep: 0 → 10 mA in 0.1 mA steps
Temperature: Hold at Tc + 5K
Compliance: ±1 V
Stop condition: Voltage > 1 μV (quench detection)

Target: Ic > 1 mA/cm² (practical superconductor)
```

### 3.3 Magnetic Field Response (Confirmation)
```bash
# Verify superconductivity vs metal transition
Apply field: 0 → 1000 Oe perpendicular to film
Temperature: Fixed at Tc
Current: 0.1 μA (low perturbation)

Expected: Resistance increase with field (flux flow)
Critical field: Hc2 ~ 100-1000 Oe for thin films
```

---

## Part 4: Data Analysis & Reporting

### 4.1 Success Criteria Checklist
- [ ] **Zero resistance**: R < 10 nΩ at T > 300K
- [ ] **Temperature range**: Flat R(T) from Tc to 350K  
- [ ] **Reproducibility**: Multiple devices show same Tc
- [ ] **Critical current**: Ic > 0.1 mA (practical threshold)
- [ ] **Field response**: Resistance increases with H-field

### 4.2 Data Quality Checks
```python
# Python analysis template
import numpy as np
import matplotlib.pyplot as plt

# Load data
data = np.loadtxt('RT_sweep.csv', delimiter=',', skiprows=1)
T, R, V, I = data.T

# Quality checks
stability = np.std(R[T < 300]) / np.mean(R[T < 300])  # < 5%
noise_level = np.std(np.diff(R)) / np.mean(R)  # < 1%
zero_resistance = np.min(R[T > 300])  # < 10 nΩ

print(f"Baseline stability: {stability*100:.1f}%")
print(f"Noise level: {noise_level*100:.1f}%") 
print(f"Minimum resistance: {zero_resistance*1e9:.1f} nΩ")
```

### 4.3 Publication-Quality Plot
```python
# Generate final R(T) plot for paper
plt.figure(figsize=(8, 6))
plt.plot(T, R*1e9, 'b-', linewidth=2, label='Li₂NH film')
plt.axhline(y=10, color='r', linestyle='--', label='Detection limit')
plt.xlabel('Temperature (K)', fontsize=14)
plt.ylabel('Resistance (nΩ)', fontsize=14)
plt.title('Room-Temperature Superconductivity in Li₂NH', fontsize=16)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=12)
plt.xlim(295, 355)
plt.ylim(0, 50)

# Mark critical temperature
Tc_idx = np.where(R < 10e-9)[0][0]
Tc = T[Tc_idx]
plt.axvline(x=Tc, color='g', linestyle=':', linewidth=2, 
           label=f'Tc = {Tc:.1f} K')

plt.tight_layout()
plt.savefig('RBT_superconductivity.pdf', dpi=300)
plt.show()

print(f"Critical temperature: {Tc:.1f} K")
if Tc > 300:
    print("🎯 ROOM-TEMPERATURE SUPERCONDUCTIVITY ACHIEVED!")
```

---

## Troubleshooting Guide

| Issue | Symptoms | Solution |
|-------|----------|----------|
| **High contact resistance** | Non-linear I-V, high noise | Re-anneal contacts, check cleaning |
| **Baseline drift** | R increases with time | Check vacuum, temperature stability |
| **No zero resistance** | R plateaus above 10 nΩ | Check current level, contact quality |
| **False transition** | R drop but increases again | Likely Joule heating, reduce current |
| **Noisy data** | Large scatter in R(T) | Shield cables, check ground loops |

---

## Success Protocol

### If R < 10 nΩ Achieved:
1. **Immediate verification**: Repeat measurement on same device
2. **Device reproducibility**: Test 3+ devices from same wafer
3. **Batch reproducibility**: Fabricate new wafer, repeat process
4. **External validation**: Send samples to collaborator for independent measurement

### Data Package for Publication:
- [ ] R(T) curves for multiple devices
- [ ] I-V characteristics showing critical current
- [ ] H-field dependence confirming superconductivity
- [ ] XRD/XPS confirming Li₂NH phase
- [ ] Temperature/current/field parameters

### Submission Timeline:
- **Day 1**: Complete measurements and analysis
- **Day 2**: Prepare figures and write draft
- **Day 3**: Submit to Nature/Science (rush article)

---

## Notes for Deep's Lab

**🚨 If successful**: This represents the first practical room-temperature superconductor
- Contact media relations immediately 
- Secure IP protection before publication
- Prepare for intense scrutiny and replication requests

**📞 Emergency contact**: Open GitHub issue with "URGENT: RT Superconductivity" for immediate support

**🔒 Data security**: Backup all measurement data immediately. This could be Nobel Prize-worthy! 