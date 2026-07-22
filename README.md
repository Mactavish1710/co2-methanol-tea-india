# CO₂ to Green Methanol TEA: India-Specific Study

[![DOI](https://img.shields.io/badge/DOI-10.26434%2Fchemrxiv--2026--xxxx-blue)](https://chemrxiv.org/engage/chemrxiv/article-details/...) 

**Repository for:**  
*Thermodynamic Analysis and Techno-Economic Assessment of CO₂ Hydrogenation to Green Methanol: An India-Specific Study with Policy Implications*

---

## 📖 About This Repository
This repository contains the **completely reproducible Python code** and **raw data** behind the thermodynamic, reactor, and economic models used in the manuscript above. 

All figures in the paper are generated directly from these scripts to ensure full transparency and reproducibility.

---

## 🚀 Key Results
- **Thermodynamic Model:** Verified NIST Shomate-based equilibrium solver for CO₂ hydrogenation.
- **Adiabatic Reactor:** Coupled equilibrium-energy balance solver. Predicts **23.8% single-pass CO₂ conversion** at 250°C, 50 bar.
- **Economics:** Factorial cost estimation with Indian location factor. 
- **Monte Carlo:** 10,000 iterations of uncertainty analysis. Mean NPV = -$117M; 29% probability of positive NPV.

---

## 📂 Repository Structure
co2-methanol-tea-india/
├── src/ # All Python source code
├── figures/ # All publication-quality figures (PDF)
└── data/ # Raw output datasets (Monte Carlo .npz)

---

## 🛠️ How to Run the Code

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   
2. **Run the core thermodynamic solver (verify the NIST data):**
   ```bash
   python src/equilibrium.py

3. **Run the adiabatic reactor model (the key design basis):**
      ```bash
   python src/adiabatic.py

4. **Run the full Monte Carlo simulation (10,000 trials):**
      ```bash
   python src/montecarlo.py

 5. **Regenerate all publication figures (PDFs + PNGs):**
      ```bash
    python src/make_keq_figure.py
    python src/make_contour.py
    python src/make_conversion_ratio.py
    python src/make_pinch.py
    python src/make_tornado.py
    python src/make_recycle_final.py
    python src/make_heatmap.py
    python src/make_waterfall.py
    python src/make_scaleup.py
    python src/make_carboncredit.py
   

