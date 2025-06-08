# BeC₃H₉ Fabrication Standard Operating Procedure

**Material**: Beryllium Tricarbide Nonahydride (BeC₃H₉)  
**Target**: 2D superconducting films for RT-SC evaluation  
**Author**: RBT 2D-SC Explorer Team  
**Revision**: 1.0  
**Date**: 2024-06-09  

## ⚠️ CRITICAL BERYLLIUM SAFETY WARNING

**Beryllium and its compounds are EXTREMELY HAZARDOUS**

### Permissible Exposure Limit (PEL)
- **OSHA PEL**: 2.0 μg/m³ (8-hour TWA)
- **Action Level**: 0.2 μg/m³ (8-hour TWA)
- **Short-term exposure**: 5.0 μg/m³ (15-minute max)

### Required Personal Protective Equipment (PPE)
- **Respirator**: NIOSH-approved HEPA filter or supplied-air respirator
- **Gloves**: Double-layer nitrile (inner) + chemical-resistant (outer)
- **Clothing**: Disposable Tyvek suit with hood
- **Eye protection**: Chemical splash goggles
- **Footwear**: Disposable shoe covers

### Waste Disposal
- **ALL beryllium-contaminated materials must be treated as hazardous waste**
- Use dedicated beryllium waste containers (yellow labels)
- Never dispose of in regular trash or wash down drains
- Contact EH&S for proper disposal procedures

---

## Pre-Fabrication Requirements

### Equipment Setup
1. **Fume Hood**: Certified for beryllium work with face velocity >100 fpm
2. **CVD Chamber**: Dedicated beryllium-compatible system
3. **Gas Lines**: Ultra-pure H₂, CH₄, and carrier gases
4. **Substrate**: Si/SiO₂ wafers, cleaned with piranha solution

### Material Preparation
- **Beryllium source**: Be(C₂H₅)₂ (diethylberyllium) - EXTREMELY TOXIC
- **Carbon source**: CH₄ (methane)
- **Hydrogen source**: H₂ (ultra-pure, 99.999%)

---

## Fabrication Protocol

### Phase 1: Chamber Preparation (Day 1)
1. **Chamber cleaning** with H₂ plasma at 300°C for 2 hours
2. **Leak check** - must achieve <1×10⁻⁸ Torr base pressure
3. **Temperature calibration** of substrate heater
4. **Gas flow calibration** for all precursors

### Phase 2: Substrate Preparation (Day 1)
1. Load Si/SiO₂ substrates into load-lock
2. **Outgas** substrates at 200°C for 30 minutes
3. **Surface clean** with Ar plasma (50W, 5 minutes)
4. Cool to growth temperature (450°C)

### Phase 3: CVD Growth (Day 2)
1. **Pre-treatment**: H₂ flow at 100 sccm, 450°C, 10 minutes
2. **Be deposition**: 
   - Be(C₂H₅)₂ flow: 0.5 sccm
   - Substrate temperature: 450°C
   - Time: 30 minutes
3. **C-H incorporation**:
   - CH₄ flow: 50 sccm
   - H₂ flow: 200 sccm
   - Temperature: 400°C
   - Time: 60 minutes
4. **Annealing**: 500°C in H₂ atmosphere for 30 minutes

### Phase 4: Post-Growth Treatment (Day 3)
1. **Cool-down** under H₂ flow to prevent oxidation
2. **Chamber purge** with N₂ for 15 minutes
3. **Sample extraction** using beryllium handling protocols
4. **Initial characterization**: Raman, XRD, thickness

---

## Quality Control Checkpoints

| Parameter | Target Value | Measurement Method |
|-----------|--------------|-------------------|
| Film thickness | 2-5 nm | AFM/Ellipsometry |
| Crystallinity | XRD peak FWHM <0.5° | X-ray diffraction |
| C/Be ratio | 3.0 ± 0.2 | XPS/EDX |
| H content | ~75 at% | SIMS/NRA |
| Sheet resistance | <100 Ω/□ at 300K | 4-probe measurement |

---

## Emergency Procedures

### Beryllium Exposure Response
1. **Immediate**: Remove person from exposure area
2. **Decontamination**: Shower with lukewarm water for 15 minutes
3. **Medical**: Contact occupational health immediately
4. **Monitoring**: Beryllium lymphocyte proliferation test (BeLPT)

### Spill Response
1. **Evacuate** non-essential personnel
2. **Contain** spill with beryllium spill kit materials
3. **Notify** EH&S and facility management
4. **Decontaminate** area per beryllium cleanup procedures

---

## Expected Results

Based on theoretical calculations:
- **λ (electron-phonon coupling)**: ~3.4
- **Predicted Tc**: >300K (pending DFT confirmation)
- **Critical current density**: >10⁶ A/cm² at 77K
- **Upper critical field**: >20 T

---

## References
- OSHA Beryllium Standard (29 CFR 1910.1024)
- RBT Theory for 2D Superconductors (internal)
- CVD Growth of 2D Materials (DOI: 10.1038/nature12385)

---

**IMPORTANT**: This SOP must be reviewed with EH&S before any beryllium work begins. All personnel must complete beryllium safety training and medical surveillance program enrollment. 