


<div align="center">

# CO2-to-Green Methanol
## India-Specific Techno-Economic Assessment

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen)](tests/)

**Thermodynamic Analysis & Techno-Economic Assessment of CO2 Hydrogenation to Green Methanol**  
*100,000 t/yr Plant | Dahej SEZ, Gujarat, India*

[Quick Start](#quick-start) · [Results](#key-results) · [Data](data/) · [Citation](#citation)

</div>

---

## What Is This?

This repository contains the **complete simulation code and data** for a techno-economic study that asks a simple question:

> *Can India produce green methanol from captured CO2 and renewable hydrogen at a cost that makes business sense?*

The answer: **Yes — but only with the right policy support.**

At current hydrogen prices ($3.50/kg), the project loses money. But if India hits its National Green Hydrogen Mission target of $1.00/kg hydrogen by 2030, green methanol becomes **cheaper than imported fossil methanol** — and permanently locks away 1.3 tonnes of CO2 for every tonne produced.

### For Different Readers

| If you are... | Start here |
|--------------|-----------|
| A **chemical engineer** | [`src/equilibrium.py`](src/equilibrium.py) — rigorous thermodynamic solver |
| A **policy maker** | [`data/ists_scenarios.csv`](data/ists_scenarios.csv) — policy impact quantified |
| An **investor / banker** | [`src/economics.py`](src/economics.py) — NPV, IRR, DSCR calculations |
| A **data scientist** | [`src/montecarlo.py`](src/montecarlo.py) — 10,000-trial uncertainty analysis |
| A **reviewer** | [`tests/test_all.py`](tests/test_all.py) — 20+ validation tests against literature |
| A **student** | This README — everything explained step by step |

---

## Key Results

### The Bottom Line

| Scenario | Cost per Tonne | Project Viable? |
|----------|---------------|-----------------|
| Today (no policy help) | **$1,127/t** | No — loses $108M |
| With ISTS transmission waiver | **$752/t** | Yes — earns $211M |
| At NGHM 2030 hydrogen target | **$502/t** | Strongly yes — earns $424M |
| Fossil methanol (imported) | ~$346/t | Baseline comparison |
| Marine fuel premium | ~$1,000/t | Target market today |

### The Headline Number

**Breakeven hydrogen price for commodity methanol: $0.37/kg**

India's NGHM target: $1.00/kg by 2030.  
**Headroom: $0.63/kg below target.** This is not marginal — it is robust.

### Why This Matters for India

- India imports **88%** of its methanol, mostly from the Middle East
- The Dahej-Hazira corridor has **9.57 million tonnes/year** of capturable CO2 within 100 km
- The ISTS (inter-state transmission) waiver alone **restores project bankability** — DSCR jumps from 0.38 to 3.43
- Green methanol is **carbon-negative**: -1.304 t CO2 per tonne produced (solar power)

### Green Methanol vs. Green Ammonia

| Factor | Green Methanol | Green Ammonia |
|--------|---------------|---------------|
| Carbon intensity | **-1.304 t CO2/t** | +0.143 t CO2/t |
| Marine fuel market | **Established (60+ vessels ordered)** | Speculative |
| Port infrastructure | Standard terminal ($2M) | Cryogenic facility ($15M) |
| Safety | Flammable (Class 3) | **Toxic (Class 2.3)** |
| Indian manufacturing | **Full domestic capability** | 80% import-dependent |

**Policy implication:** NGHM Phase II should explicitly include methanol synthesis subsidies, not just ammonia.

---

## Quick Start

### Install

```bash
git clone https://github.com/YOUR-USERNAME/co2-methanol-tea-india.git
cd co2-methanol-tea-india
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m pytest tests/ -v
```

### Run

```bash
# Thermodynamic equilibrium at 250C, 50 bar
python -m src.equilibrium

# Coupled adiabatic reactor (temperature rise + equilibrium)
python -m src.adiabatic

# Full economic model
python -m src.economics

# Monte Carlo uncertainty (10,000 trials)
python -m src.montecarlo
```

### Generate Figures

```bash
python src/fig1_keq.py        # Equilibrium constants vs temperature
python src/fig2_contour.py     # CO2 conversion map
python src/fig6_tornado.py     # Sensitivity analysis
python src/fig8_montecarlo.py  # NPV probability distribution
python src/fig9_recycle.py     # Recycle ratio optimization
```

All figures save to `figures/` as PNG (300 DPI) and PDF.

---

## Repository Structure

```
co2-methanol-tea-india/
|
|-- data/                          # All paper data as CSV
|   |-- shomate_coefficients.csv          # NIST thermodynamic data
|   |-- equipment_costs.csv               # Capital costs (Table 8)
|   |-- opex_breakdown.csv                # Operating costs (Table 9)
|   |-- stream_table.csv                  # Process streams (Table 6)
|   |-- validation_points.csv             # Literature validation (Table 2)
|   |-- ists_scenarios.csv                # Policy scenarios (Table 17)
|   |-- monte_carlo_distributions.csv     # Input distributions (Table 15)
|   |-- carbon_intensity.csv              # Carbon balance (Table 13)
|   |-- methanol_vs_ammonia.csv           # Strategic comparison (Table 19)
|   |-- capex_summary.csv                 # Capital cost roll-up
|
|-- src/                           # Core solvers
|   |-- equilibrium.py             # Thermodynamic model (Newton-Raphson)
|   |-- adiabatic.py               # Coupled reactor solver
|   |-- economics.py               # Cost estimation & profitability
|   |-- montecarlo.py              # Uncertainty quantification
|   |-- utils.py                   # Helpers
|   |-- fig1_keq.py                # Figure scripts
|   |-- fig2_contour.py
|   |-- fig6_tornado.py
|   |-- fig8_montecarlo.py
|   |-- fig9_recycle.py
|
|-- tests/                         # Validation tests
|   |-- test_all.py                # 20+ tests against paper data
|
|-- figures/                       # Generated output
|-- .github/workflows/tests.yml    # Automated CI testing
|-- requirements.txt
|-- setup.py
|-- LICENSE (MIT)
|-- README.md (this file)
```

---

## The Science: How It Works

### Reaction Chemistry

CO2 captured from industrial sources reacts with green hydrogen over a copper catalyst:

```
CO2 + 3H2  -->  CH3OH + H2O        (main reaction, releases heat)
CO2 + H2   -->  CO + H2O           (side reaction, absorbs heat)
```

The problem: the main reaction likes **low temperature**, but the side reaction (RWGS) accelerates as temperature rises. In a real adiabatic reactor, the heat released pushes temperature up — **slashing methanol selectivity from 98% to 50%**. This is a central finding of this work.

### Thermodynamic Model

- Uses **NIST Shomate equations** for heat capacity, enthalpy, and entropy
- Solves two coupled nonlinear equations via **Newton-Raphson** (converges in 5-7 iterations)
- Validated against 4 independent literature sources with **2.3% mean deviation**

### Reactor Design

| Parameter | Value |
|-----------|-------|
| Type | Vertical adiabatic fixed-bed |
| Catalyst | Cu/ZnO/Al2O3 (BASF S3-85) |
| Operating | 250C inlet, 268C outlet, 50 bar |
| Modules | 6 parallel reactors |
| Capacity | 100,000 tonnes/year |

### Heat Integration

A **feed-effluent heat exchanger** recovers 900 kW of waste heat, eliminating all external heating for feed preheating. Payback: 1.3 years.

### Economics

| Item | Cost |
|------|------|
| Total Capital Investment | $55.2 million |
| Annual OPEX | $106.2 million |
| Hydrogen share of OPEX | **82.3%** |
| Levelised Cost of Methanol | $1,127/tonne |

With ISTS waiver: **LCOM drops to $752/tonne**.

### Uncertainty Analysis

10,000 Monte Carlo trials reveal:
- **29% chance** of positive NPV at baseline
- Hydrogen price is the **dominant risk factor** (Spearman rho = -0.64)
- Capital cost uncertainty is almost irrelevant (rho = -0.18)

**Takeaway:** Secure long-term hydrogen supply contracts, not construction guarantees.

---

## Data

Every number in the paper is available as a CSV file in `data/`:

| File | What It Contains |
|------|-----------------|
| `shomate_coefficients.csv` | A, B, C, D, E coefficients for 6 species |
| `equipment_costs.csv` | 11 equipment items with India location factors |
| `opex_breakdown.csv` | 6 cost categories, hydrogen dominates at 82.3% |
| `stream_table.csv` | 11 process streams, mass flows, T, P, phase |
| `validation_points.csv` | 4 literature data points for model verification |
| `ists_scenarios.csv` | 4 policy scenarios: baseline, partial waiver, full waiver, NGHM target |
| `monte_carlo_distributions.csv` | 7 input distributions with parameters |
| `carbon_intensity.csv` | Solar vs grid electricity carbon balance |
| `methanol_vs_ammonia.csv` | 16-criterion strategic comparison |
| `capex_summary.csv` | Roll-up from equipment to total investment |

---

## Figures

| Script | Output | What It Shows |
|--------|--------|---------------|
| `fig1_keq.py` | Fig 1 | How equilibrium constants change with temperature |
| `fig2_contour.py` | Fig 2 | CO2 conversion across temperature-pressure space |
| `fig6_tornado.py` | Fig 6 | Which parameters most affect project economics |
| `fig8_montecarlo.py` | Fig 8 | Probability distribution of project NPV |
| `fig9_recycle.py` | Fig 9 | How recycle ratio affects conversion and profit |

**Note:** The publication figures were generated from these solvers using AI-assisted visualization tools for final polish. All underlying numerical data is fully reproducible from the code provided here.

---

## Testing

```bash
python -m pytest tests/ -v
```

Tests validate:
- Thermodynamic properties against NIST data
- Equilibrium conversions against 4 literature sources
- Adiabatic outlet temperature and selectivity penalty
- Economic calculations (CRF, LCOM, NPV, breakeven)
- Monte Carlo reproducibility and statistical properties

---

## Citation

```bibtex
@article{soni2026greenmethanol,
  title={Thermodynamic Analysis and Techno-Economic Assessment of 
         CO2 Hydrogenation to Green Methanol: An India-Specific 
         Study with Policy Implications},
  author={Soni, Yug},
  year={2026}
}
```

```bibtex
@software{soni2026co2methanolcode,
  author = {Soni, Yug},
  title = {CO2-to-Green Methanol: India-Specific TEA},
  url = {https://github.com/YOUR-USERNAME/co2-methanol-tea-india},
  year = {2026},
  version = {1.0.0}
}
```

---

## Contact

**Yug Soni**  
Department of Chemical Engineering  
Sardar Vallabhbhai National Institute of Technology (SVNIT), Surat, India  
Email: U23CH077@ched.svnit.ac.in

---

<div align="center">

Built with rigorous thermodynamics in Surat, Gujarat

</div>
```

---

