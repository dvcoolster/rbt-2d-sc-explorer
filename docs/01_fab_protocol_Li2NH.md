# Li₂NH Fabrication Protocol
## 2-D Room-Temperature Superconductor Candidate

**Target**: 50 nm Li₂NH film with 10 nm BN protective cap  
**Timeline**: 2-3 days (including characterization)  
**Success metric**: R(T) < 10 nΩ from 300-350K

---

## Materials & Equipment Required

### Substrates
- Si/SiO₂ wafers (300 nm oxide, diced to 1×1 cm)
- Alternatively: Sapphire (0001) for better lattice match

### Deposition Sources
- **Lithium**: 99.9% pure Li metal (Alfa Aesar)
- **Nitrogen**: Ultra-high purity N₂ gas (99.999%)
- **Ammonia**: Anhydrous NH₃ (99.99%, research grade)
- **Boron nitride**: h-BN sputter target (Kurt Lesker)

### Equipment
- DC/RF magnetron sputter system
- Plasma-enhanced CVD (PECVD) chamber
- Rapid thermal processor (RTP)
- Load-lock with glove box interface
- XPS for surface analysis

---

## Step-by-Step Protocol

### Day 1: Substrate Preparation & Li Deposition

#### 1.1 Substrate Cleaning (30 min)
```bash
# Standard RCA clean
1. Acetone sonication: 10 min
2. IPA sonication: 10 min  
3. DI water rinse: 5 min
4. N₂ blow dry
5. O₂ plasma: 2 min @ 100W (removes organic residues)
```

#### 1.2 Lithium Base Layer Deposition (45 min)
```bash
# Sputter conditions
Base pressure: < 5×10⁻⁷ Torr
Working pressure: 3 mTorr Ar
Power: 50W DC
Rate: ~0.5 Å/s
Target thickness: 25 nm
Substrate temp: Room temperature (critical - Li melts at 180°C)

# Process
1. Load substrate in sputter chamber
2. Pump to base pressure  
3. Strike plasma at low power (10W)
4. Ramp to 50W over 2 min
5. Deposit 25 nm Li (monitor with QCM)
6. Cool under vacuum for 15 min
```

**⚠️ Critical**: Keep Li deposition chamber separate from other metals to avoid contamination.

#### 1.3 In-Situ Nitridation (60 min)
```bash
# Convert Li → Li₃N intermediate
1. Introduce ultra-pure N₂: 10 mTorr
2. Generate N₂ plasma: 300W RF, 13.56 MHz
3. Expose Li film: 30 min @ room temperature
4. Monitor with QMS: N₂⁺ and Li⁺ signals
5. Pump to base pressure
```

Expected result: Formation of Li₃N nucleation layer

---

### Day 2: NH₃ Processing & Film Completion

#### 2.1 Ammonia Treatment (RTP Chamber)
```bash
# Li₃N + NH₃ → Li₂NH + LiH reaction pathway
Temperature ramp: 25°C → 200°C @ 5°C/min
NH₃ flow: 50 sccm (diluted with 200 sccm N₂)
Pressure: 1 Torr
Hold time: 60 min @ 200°C
Cool down: Natural cooling under NH₃ flow

# Expected reactions:
# Li₃N + NH₃ → Li₂NH + LiNH₂
# LiNH₂ → Li₂NH + NH₃ (thermodynamically favored)
```

**Safety**: Use ammonia scrubber and gas monitors. NH₃ is toxic and corrosive.

#### 2.2 Film Annealing & Crystallization
```bash
# Promote 2-D ordering
Temperature: 300°C
Atmosphere: Ultra-pure N₂ (no O₂!)
Time: 2 hours
Ramp rate: 2°C/min up and down
```

#### 2.3 Surface Analysis Checkpoint
```bash
# XPS verification (30 min measurement)
Expected peaks:
- Li 1s: 55.7 eV (Li₂NH environment)
- N 1s: 395.8 eV (amide nitrogen)
- O 1s: Minimal (<2 at.% - indicates good passivation)

# If O 1s > 5%: Film is oxidized, restart process
```

---

### Day 3: BN Capping & Device Preparation

#### 3.1 Boron Nitride Protective Cap
```bash
# Prevent oxidation during ex-situ processing
Technique: RF magnetron sputtering
Target: h-BN (99.5% pure)
Power: 200W RF @ 13.56 MHz
Gas: Ar/N₂ mixture (80:20)
Pressure: 5 mTorr
Rate: ~0.2 Å/s
Thickness: 10 nm
Substrate temp: 100°C (promotes sp² bonding)
```

#### 3.2 Film Characterization
```bash
# Thickness verification
Tool: Stylus profilometer
Expected: 50 ± 5 nm Li₂NH + 10 ± 2 nm BN

# Crystal structure
Tool: Grazing incidence XRD (GIXRD)
Target peaks: Li₂NH (001) at 2θ ≈ 12°, (002) at 24°

# Morphology  
Tool: AFM or SEM
Target: Smooth, continuous film, RMS < 2 nm
```

---

## Quality Control Checkpoints

### ✅ Day 1 Success Criteria
- [ ] Li film thickness: 25 ± 2 nm
- [ ] Surface roughness: < 1 nm RMS
- [ ] No visible oxidation (film stays metallic)

### ✅ Day 2 Success Criteria  
- [ ] XPS Li 1s peak shifts from 55.0 eV (metal) to 55.7 eV (amide)
- [ ] N 1s peak appears at 395.8 eV
- [ ] Oxygen content < 2 at.%
- [ ] Film remains continuous (no dewetting)

### ✅ Day 3 Success Criteria
- [ ] BN cap is conformal and pinhole-free
- [ ] Total stack thickness: 60 ± 5 nm
- [ ] XRD shows Li₂NH crystalline peaks
- [ ] Ready for device fabrication

---

## Common Issues & Troubleshooting

| Problem | Symptoms | Solution |
|---------|----------|----------|
| **Li oxidation** | Film turns from silver to brown | Improve base pressure, check O₂ leaks |
| **Dewetting** | Islands instead of continuous film | Lower deposition rate, cool substrate |
| **Incomplete reaction** | Mixed Li/Li₃N phases in XPS | Increase NH₃ treatment time/temperature |
| **BN delamination** | Flaking during handling | Clean surface better before BN deposition |

---

## Next Steps

Upon successful fabrication:
1. **Pattern devices**: Follow standard photolithography for Hall bars
2. **Electrical contacts**: Ti/Au (5/50 nm) by e-beam evaporation  
3. **Measurement**: 4-probe R(T) from 300-350K per measurement playbook
4. **Target result**: R < 10 nΩ indicates superconductivity

**🎯 Success = Nature paper submission within 1 week!**

---

## Notes for Deep's Lab

- **Li handling**: Store and transfer Li in Ar glove box (Li reacts with air in seconds)
- **Chamber dedication**: Dedicate one chamber to Li to avoid cross-contamination
- **Safety**: NH₃ requires specialized gas handling - coordinate with EHS
- **Backup plan**: If Li₂NH fails, try Li₄NH using same protocol with longer Li deposition

**Contact**: Open GitHub issue for real-time troubleshooting support 