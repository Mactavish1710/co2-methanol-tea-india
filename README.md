
<div align="center">

# CO2-to-Green Methanol
## India-Specific Techno-Economic Assessment

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Thermodynamic Analysis & Techno-Economic Assessment of CO2 Hydrogenation to Green Methanol**  
*100,000 t/yr | Dahej SEZ, Gujarat, India*

</div>

---

## What This Is

Complete simulation framework for a 100,000 t/yr green methanol plant via CO2 hydrogenation. Sited at Dahej SEZ, Gujarat — chosen for its 9.57 Mt/yr capturable CO2, Kutch solar corridor, and 60 km from Hazira port.

**Core question:** Can India produce green methanol at a cost that makes business sense?

**Answer:** Not yet at today's hydrogen prices ($3.50/kg). But at India's NGHM 2030 target of $1.00/kg, green methanol becomes cheaper than imported fossil methanol — and locks away 1.3 tonnes of CO2 per tonne produced.

---

## Key Results

| Scenario | LCOM ($/t) | NPV ($M) | Viable? |
|----------|-----------|----------|---------|
| Baseline (no policy) | 1,127 | -108 | No |
| Full ISTS waiver | 752 | +211 | Yes |
| NGHM 2030 target ($1/kg H2) | 502 | +424 | Strongly yes |

**Breakeven hydrogen price: $0.37/kg** — $0.63/kg below NGHM 2030 target.

---

## Quick Start

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
python -m src.equilibrium      # Thermodynamic equilibrium
python -m src.adiabatic        # Coupled adiabatic reactor
python -m src.economics        # Cost model
python -m src.montecarlo       # 10,000-trial uncertainty
```

### Generate Figures

```bash
python src/fig1_keq.py
python src/fig2_contour.py
python src/fig6_tornado.py
python src/fig8_montecarlo.py
python src/fig9_recycle.py
```

---

## Repository Structure

```
co2-methanol-tea-india/
|-- data/              # 10 CSV files from paper tables
|-- src/               # Core solvers + figure scripts
|-- tests/             # 20+ validation tests
|-- figures/           # Generated output
|-- docs/              # Extended methodology
|-- .github/workflows/ # CI testing
```

---

## What the Code Does

### Thermodynamic Equilibrium (`src/equilibrium.py`)

Two reactions:
```
CO2 + 3H2 <=> CH3OH + H2O        (methanol synthesis)
CO2 + H2  <=> CO + H2O           (RWGS)
```

Solves coupled nonlinear equations via Newton-Raphson using NIST Shomate data. Converges in 5-7 iterations.

| Condition | CO2 Conversion | MeOH Selectivity |
|-----------|---------------|------------------|
| Isothermal (250C, 50 bar) | 24.7% | 66.6% |
| Adiabatic (250C inlet) | 23.8% | 50.4% |

The adiabatic temperature rise to 268C slashes selectivity via RWGS acceleration — a central finding.

### Economics (`src/economics.py`)

Factorial cost estimation with India-specific location factor (0.72). Hydrogen dominates OPEX at 82.3%.

### Monte Carlo (`src/montecarlo.py`)

10,000 trials (seed=42). Hydrogen price is the dominant risk factor (Spearman rho = -0.64). Capital cost uncertainty is almost irrelevant (rho = -0.18).

---

## Data

All paper tables as machine-readable CSV in `data/`:

| File | Content |
|------|---------|
| `shomate_coefficients.csv` | NIST thermodynamic data |
| `equipment_costs.csv` | Capital cost breakdown |
| `opex_breakdown.csv` | Operating costs |
| `stream_table.csv` | Process streams |
| `ists_scenarios.csv` | Policy scenario analysis |
| `monte_carlo_distributions.csv` | Input distributions |
| `carbon_intensity.csv` | Gate-to-gate carbon balance |
| `methanol_vs_ammonia.csv` | Strategic comparison |

---

## Figures

| Script | Output |
|--------|--------|
| `fig1_keq.py` | Equilibrium constants vs temperature |
| `fig2_contour.py` | CO2 conversion contour map |
| `fig6_tornado.py` | Sensitivity analysis |
| `fig8_montecarlo.py` | NPV probability distribution |
| `fig9_recycle.py` | Recycle ratio optimization |

Publication figures were polished with AI-assisted visualization tools (Figure Labs, SciFig) using exact numerical data from these solvers. Underlying data is fully reproducible from the code provided.

---

## Testing

```bash
python -m pytest tests/ -v
```

Validates against NIST data and 4 literature sources (Portha, Graaf, Perez-Fortes).

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
  year = {2026}
}
```

---

## Contact

**Yug Soni**  
Department of Chemical Engineering, SVNIT Surat, India  
U23CH077@ched.svnit.ac.in
```



⭐ **Star this repository if you find it useful!**

🔬 Built with rigorous thermodynamics in **Surat, Gujarat** 🇮🇳

</div>
```



