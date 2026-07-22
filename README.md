&lt;div align="center"&gt;

# 🧪 CO₂-to-Green Methanol
## India-Specific Techno-Economic Assessment

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg?style=for-the-badge)](tests/)

**Thermodynamic Analysis & Techno-Economic Assessment of CO₂ Hydrogenation to Green Methanol**  
*Sited at Dahej SEZ, Gujarat, India | 100,000 t/yr Nameplate Capacity*

[📄 Paper](#) · [🚀 Quick Start](#-quick-start) · [📊 Results](#-key-results) · [📖 Data](data/)

&lt;/div&gt;

---

## 📋 Table of Contents

- [🔬 Overview](#-overview)
- [🎯 Key Results](#-key-results)
- [🚀 Quick Start](#-quick-start)
- [📁 Repository Structure](#-repository-structure)
- [🔧 Methodology](#-methodology)
- [📊 Data](#-data)
- [🎨 Figures](#-figures)
- [📖 Citation](#-citation)
- [📧 Contact](#-contact)

---

## 🔬 Overview

This repository contains the **complete simulation framework** for a bottom-up techno-economic assessment (TEA) of a 100,000 t/yr green methanol plant via CO₂ hydrogenation, sited at **Dahej Special Economic Zone, Gujarat, India**.

### What This Repository Includes

| Component | Status | Description |
|-----------|--------|-------------|
| **Thermodynamic solver** | ✅ Complete | NIST Shomate equilibrium model with Newton-Raphson |
| **Adiabatic reactor** | ✅ Complete | Coupled equilibrium-energy balance solver |
| **Economic model** | ✅ Complete | Factorial cost estimation (ISBL/OSBL) |
| **Monte Carlo** | ✅ Complete | 10,000-trial uncertainty quantification |
| **Data files** | ✅ Complete | All tables from paper as CSV |
| **Figure scripts** | ✅ Complete | Matplotlib scripts for all key figures |
| **Unit tests** | ✅ Complete | 20+ tests validating against paper data |

### Why This Matters

- 🇮🇳 **First India-specific TEA** with Indian cost structures, labour rates, and location factors
- ⚡ **ISTS transmission waiver** impact explicitly quantified
- 🎯 **Breakeven H₂ price** benchmarked against India's NGHM 2030 target
- 📉 **10,000-trial Monte Carlo** for rigorous uncertainty propagation
- 🌡️ **Coupled adiabatic solve** — not isothermal approximation

---

## 🎯 Key Results

&lt;div align="center"&gt;

| Metric | Baseline | Full ISTS Waiver | NGHM 2030 Target |
|--------|:--------:|:----------------:|:----------------:|
| **LCOM** | **$1,127 /t** | **$752 /t** | **$502 /t** |
| **Breakeven H₂ Price** (commodity) | **$0.37 /kg** | — | — |
| **Gap to NGHM Target** | **$0.63 /kg BELOW** | — | — |
| **NPV** (@ $1,000/t marine fuel) | −$108 M | **+$211 M** | +$424 M |
| **IRR** | Not defined | **28%** | 48% |
| **DSCR** | &lt; 1.0 (not bankable) | **3.43** ✓ | 4.45 |
| **Carbon Intensity** (solar) | **−1.304 t CO₂/t** | — | — |

&lt;/div&gt;

### Central Finding

&gt; **The commodity-market breakeven hydrogen price of $0.37 kg⁻¹ lies $0.63 kg⁻¹ below India's NGHM 2030 target of $1.00 kg⁻¹.** This indicates green methanol can serve as a demand-side anchor for India's hydrogen economy once the Mission's target is achieved.

---

## 🚀 Quick Start

### Prerequisites

- Python ≥ 3.9
- Git

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/YOUR-USERNAME/co2-methanol-tea-india.git
cd co2-methanol-tea-india

# 2. Create virtual environment
python -m venv venv

# 3. Activate environment
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run tests to verify installation
python -m pytest tests/ -v
