


<div align="center">

# CO2-to-Green Methanol: India-Specific Techno-Economic Assessment

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](tests/)

**Thermodynamic Analysis & Techno-Economic Assessment of CO2 Hydrogenation to Green Methanol**
*Sited at Dahej SEZ, Gujarat, India | 100,000 t/yr Nameplate Capacity*

</div>

---

## Overview

This repository contains the complete simulation framework for a bottom-up techno-economic assessment (TEA) of a 100,000 t/yr green methanol plant via CO2 hydrogenation, sited at **Dahej Special Economic Zone, Gujarat, India**.

### What This Repository Includes

| Component | Status | Description |
|-----------|--------|-------------|
| Thermodynamic solver | Complete | NIST Shomate equilibrium model with Newton-Raphson |
| Adiabatic reactor | Complete | Coupled equilibrium-energy balance solver |
| Economic model | Complete | Factorial cost estimation (ISBL/OSBL) |
| Monte Carlo | Complete | 10,000-trial uncertainty quantification |
| Data files | Complete | All tables from paper as CSV |
| Figure scripts | Complete | Matplotlib scripts for all key figures |
| Unit tests | Complete | 20+ tests validating against paper data |

### Why This Matters

- First India-specific TEA with Indian cost structures, labour rates, and location factors
- ISTS transmission waiver impact explicitly quantified
- Breakeven H2 price benchmarked against India's NGHM 2030 target
- 10,000-trial Monte Carlo for rigorous uncertainty propagation
- Coupled adiabatic solve -- not isothermal approximation

---

## Key Results

| Metric | Baseline | Full ISTS Waiver | NGHM 2030 Target |
|--------|:--------:|:----------------:|:----------------:|
| LCOM | **$1,127 /t** | **$752 /t** | **$502 /t** |
| Breakeven H2 Price (commodity) | **$0.37 /kg** | -- | -- |
| Gap to NGHM Target | **$0.63 /kg BELOW** | -- | -- |
| NPV (@ $1,000/t marine fuel) | -$108 M | **+$211 M** | +$424 M |
| IRR | Not defined | **28%** | 48% |
| DSCR | < 1.0 (not bankable) | **3.43** | 4.45 |
| Carbon Intensity (solar) | **-1.304 t CO2/t** | -- | -- |

**Central Finding:** The commodity-market breakeven hydrogen price of $0.37 kg-1 lies $0.63 kg-1 below India's NGHM 2030 target of $1.00 kg-1. This indicates green methanol can serve as a demand-side anchor for India's hydrogen economy once the Mission's target is achieved.

---

## Quick Start

### Prerequisites

- Python >= 3.9
- Git

### Installation

```bash
git clone https://github.com/YOUR-USERNAME/co2-methanol-tea-india.git
cd co2-methanol-tea-india
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m pytest tests/ -v
```

### Run the Solvers

```bash
python -m src.equilibrium      # Thermodynamic equilibrium at design point
python -m src.adiabatic        # Coupled adiabatic reactor solve
python -m src.economics        # Economic analysis
python -m src.montecarlo       # Monte Carlo simulation (10,000 trials)
```

### Generate Figures

```bash
python src/fig1_keq.py         # Figure 1: Equilibrium constants
python src/fig2_contour.py     # Figure 2: Conversion contour map
python src/fig6_tornado.py     # Figure 6: Tornado sensitivity
python src/fig8_montecarlo.py  # Figure 8: MC NPV distribution
python src/fig9_recycle.py     # Figure 9: Recycle ratio analysis
```

Figures saved to `figures/` directory in PNG (300 DPI) and PDF.

---

## Repository Structure

```
co2-methanol-tea-india/
|
|-- data/                          # All paper data as CSV
|   |-- shomate_coefficients.csv          # Table 1: NIST thermodynamic data
|   |-- equipment_costs.csv               # Table 8: Capital cost breakdown
|   |-- opex_breakdown.csv                # Table 9: Operating costs
|   |-- stream_table.csv                  # Table 6: Process streams
|   |-- validation_points.csv             # Table 2: Literature validation
|   |-- ists_scenarios.csv                # Table 17: Policy scenarios
|   |-- monte_carlo_distributions.csv     # Table 15: Input distributions
|   |-- carbon_intensity.csv              # Table 13: Carbon balance
|   |-- methanol_vs_ammonia.csv           # Table 19: Strategic comparison
|   |-- capex_summary.csv                 # Capital cost roll-up
|
|-- src/                           # Core Python solvers
|   |-- __init__.py
|   |-- equilibrium.py             # Thermodynamic equilibrium model
|   |-- adiabatic.py               # Coupled adiabatic reactor solver
|   |-- economics.py               # Factorial cost estimation
|   |-- montecarlo.py              # Monte Carlo uncertainty
|   |-- utils.py                   # Unit conversions & helpers
|   |-- fig1_keq.py                # Figure 1: Equilibrium constants
|   |-- fig2_contour.py            # Figure 2: Conversion contour map
|   |-- fig6_tornado.py            # Figure 6: Tornado sensitivity
|   |-- fig8_montecarlo.py         # Figure 8: MC NPV distribution
|   |-- fig9_recycle.py            # Figure 9: Recycle ratio analysis
|
|-- tests/                         # Unit tests (20+ cases)
|   |-- __init__.py
|   |-- test_all.py                # Validation against paper data
|
|-- figures/                       # Generated figures (output)
|
|-- .github/workflows/             # CI/CD
|   |-- tests.yml                  # Automated testing on push
|
|-- .gitignore
|-- LICENSE                        # MIT License
|-- README.md                      # This file
|-- requirements.txt               # Python dependencies
|-- setup.py                       # Package installation
```

---

## Methodology

### 1. Thermodynamic Equilibrium Model

```
CO2 + 3H2 <=> CH3OH + H2O     dH298 = -49.0 kJ/mol   (Primary)
CO2 + H2  <=> CO + H2O        dH298 = +41.2 kJ/mol   (RWGS)
```

- Data: NIST Chemistry WebBook (Shomate equations, 298-1300 K)
- Solver: Newton-Raphson with analytical Jacobian (tol = 1e-8)
- Validation: MAPD = 2.3% against literature

### 2. Coupled Adiabatic Reactor

Solves simultaneously:
- Chemical equilibrium constraints at outlet temperature
- Energy balance: H_in(T_in) = H_out(T_ad)

Key finding: Adiabatic temperature rise to 268C causes severe selectivity penalty (50.4% vs. 98.3% isothermal) due to RWGS acceleration.

### 3. Economic Model

| Cost Category | Method | India Factor |
|--------------|--------|-------------|
| Equipment | Vendor quotes + Turton correlations | 0.72 (domestic) / 0.97+15% duty (import) |
| ISBL | 3.2 x TPEC | -- |
| OSBL | 20% of ISBL | -- |
| Location factor | 0.72 | Indian labour rates ($15-25/h) |

### 4. Monte Carlo (10,000 trials, seed=42)

| Parameter | Distribution | Mean |
|-----------|-------------|------|
| H2 price | Lognormal | $3.50/kg |
| Methanol price | Normal | $1,000/t |
| CO2 cost | Triangular | $45/t |
| CAPEX | Triangular | $55.2M |

---

## Data

All data from the paper is provided as machine-readable CSV files in `data/`:

| File | Paper Table | Content |
|------|------------|---------|
| shomate_coefficients.csv | Table 1 | NIST Shomate A-E, dHf298 |
| equipment_costs.csv | Table 8 | Itemized capital costs with location factors |
| opex_breakdown.csv | Table 9 | Annual operating cost breakdown |
| stream_table.csv | Table 6 | Complete process stream data |
| validation_points.csv | Table 2 | Literature validation data |
| ists_scenarios.csv | Table 17 | ISTS waiver scenario analysis |
| monte_carlo_distributions.csv | Table 15 | Input distributions |
| carbon_intensity.csv | Table 13 | Gate-to-gate carbon balance |
| methanol_vs_ammonia.csv | Table 19 | Strategic comparison |
| capex_summary.csv | -- | Capital cost roll-up |

---

## Figures

Matplotlib scripts are provided for all key figures. The publication figures in the manuscript were generated using these numerical results with additional AI-assisted visualization tools for final polish.

| Script | Figure | Description |
|--------|--------|-------------|
| src/fig1_keq.py | Fig 1 | Equilibrium constants vs. temperature |
| src/fig2_contour.py | Fig 2 | CO2 conversion contour map |
| src/fig6_tornado.py | Fig 6 | Tornado sensitivity analysis |
| src/fig8_montecarlo.py | Fig 8 | Monte Carlo NPV distribution |
| src/fig9_recycle.py | Fig 9 | Recycle ratio sensitivity |

All scripts save to `figures/` in both PNG (300 DPI) and PDF formats.

---

## Testing

```bash
python -m pytest tests/ -v                           # Run all tests
python -m pytest tests/test_all.py::TestAdiabaticSolver -v   # Specific class
python -m pytest tests/ --cov=src --cov-report=html   # With coverage
```

Test coverage:
- Shomate thermodynamics (Cp, H, S, Keq)
- Equilibrium solver (design point, pressure/temperature trends)
- Literature validation (Portha, Graaf, Perez-Fortes)
- Adiabatic solver (convergence, outlet temp, selectivity penalty)
- Economics (CRF, LCOM, NPV, breakeven)
- Monte Carlo (reproducibility, correlations)

---

## India-Specific Context

### Site: Dahej SEZ, Gujarat

| Advantage | Details |
|-----------|---------|
| CO2 supply | 9.57 Mt/yr within 100 km (GNFC: $20-30/t, Reliance: $35-45/t) |
| Renewable energy | Kutch solar corridor (6.0-6.5 kWh/m2/day) |
| Port access | 60 km from Hazira -> marine fuel bunkering |
| Industrial ecosystem | Existing chemical infrastructure |

### Policy: ISTS Charge Waiver

The full Inter-State Transmission System (ISTS) charge waiver is the single most powerful policy lever:
- Reduces delivered electricity cost by 39% ($0.087 -> $0.053/kWh)
- Cuts hydrogen cost from $3.50 -> $2.00/kg
- Restores project bankability (DSCR: <1.0 -> 3.43)
- Closes 60% of the cost gap to NGHM 2030 target

---

## Citation

If you use this code or data in your research, please cite:

```bibtex
@article{soni2024greenmethanol,
  title={Thermodynamic Analysis and Techno-Economic Assessment of 
         CO2 Hydrogenation to Green Methanol: An India-Specific 
         Study with Policy Implications},
  author={Soni, Yug},
  year={2024}
}
```

```bibtex
@software{soni2024co2methanolcode,
  author = {Soni, Yug},
  title = {CO2-to-Green Methanol: India-Specific TEA},
  url = {https://github.com/YOUR-USERNAME/co2-methanol-tea-india},
  year = {2024},
  version = {1.0.0}
}
```

---

## Contact

**Yug Soni**
Department of Chemical Engineering
Sardar Vallabhbhai National Institute of Technology (SVNIT), Surat
Email: U23CH077@ched.svnit.ac.in

---

<div align="center">

Star this repository if you find it useful!

Built with rigorous thermodynamics in Surat, Gujarat

</div>
```

---

**Remember to replace `YOUR-USERNAME` with your actual GitHub username in two places:**
1. `git clone https://github.com/YOUR-USERNAME/...`
2. Software citation URL: `https://github.com/YOUR-USERNAME/...`
