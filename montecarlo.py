import numpy as np

np.random.seed(42)
N = 10000

# Input distributions exactly as stated in paper Table 15
# H2 price: Lognormal, mean=3.50, std=0.70, range [2.0, 6.0]
# For lognormal, need to convert mean/std of the distribution to underlying normal params
def lognormal_params(mean, std):
    sigma2 = np.log(1 + (std/mean)**2)
    mu = np.log(mean) - sigma2/2
    sigma = np.sqrt(sigma2)
    return mu, sigma

mu_h2, sigma_h2 = lognormal_params(3.50, 0.70)
H2_price = np.random.lognormal(mu_h2, sigma_h2, N)
H2_price = np.clip(H2_price, 2.0, 6.0)

# Methanol price: Normal, mean=1000, std=150, range [500,1500]
MeOH_price = np.random.normal(1000, 150, N)
MeOH_price = np.clip(MeOH_price, 500, 1500)

# CO2 cost: Triangular, [25, 45, 75]
CO2_cost = np.random.triangular(25, 45, 75, N)

# Electricity: Normal, mean=0.07, std=0.0105, range [0.04,0.10]
Elec = np.random.normal(0.07, 0.0105, N)
Elec = np.clip(Elec, 0.04, 0.10)

# CAPEX: Triangular [44.2, 55.2, 69.0] $M
CAPEX = np.random.triangular(44.2, 55.2, 69.0, N)

# OPEX multiplier: Uniform [0.90, 1.10]
OPEX_mult = np.random.uniform(0.90, 1.10, N)

# Capacity factor: Normal mean=0.90, std=0.045, range[0.75,1.00]
CF = np.random.normal(0.90, 0.045, N)
CF = np.clip(CF, 0.75, 1.00)

# --- Economic model, using base-case relationships from the paper ---
# Base case (deterministic): H2=3.50, MeOH=1000, CO2=45, Elec=0.07, CAPEX=55.2, CF=0.90
# gives OPEX=106.22M, LCOM=1127, NPV=-108M (marine fuel)

# Reconstruct OPEX as function of inputs using paper's OPEX breakdown (Table 14):
# H2 feedstock: 87.44M at H2=3.50 -> so H2 consumption = 87.44/3.50 = 24.983 M kg/yr (matches paper's 24.98)
H2_consumption = 87.44/3.50  # M kg/yr, fixed by stoichiometry (not random)
CO2_consumption = 16.85/45.0  # M tonnes/yr fixed by stoichiometry = 0.3744 Mt/yr (matches paper 374,450 t/yr)

# annual production fixed at 100,000 t/yr scaled by capacity factor relative to base 0.90
production = 100000 * (CF/0.90)

OPEX = (H2_consumption * H2_price * 1e6         # H2 cost, $
        + CO2_consumption*1e6 * CO2_cost        # CO2 cost, $
        + Elec/0.07 * 0.82e6                    # non-H2 electricity scales with elec price, base 0.82M
        + 0.14e6 + 0.43e6 + 0.54e6               # catalyst, labour, maintenance (fixed, small)
        ) * OPEX_mult / 1e6   # convert to $M

CRF = 0.1175
Annualised_CAPEX = CRF * CAPEX

LCOM = (Annualised_CAPEX + OPEX) * 1e6 / production  # $/tonne

Revenue_marine = MeOH_price * production / 1e6  # $M, at marine fuel price
NPV_marine = -(Annualised_CAPEX + OPEX - Revenue_marine) * 8.514  # rough annuity factor at 10%,20yr for illustration

# proper NPV via full annuity discounting given annual net cash flow, 20yr, 10%
i = 0.10; n = 20
annuity_factor = (1-(1+i)**-n)/i
annual_net_cf = Revenue_marine - OPEX  # $M/yr operating margin (CAPEX handled separately)
NPV = -CAPEX + annual_net_cf * annuity_factor

print("=== REAL MONTE CARLO RESULTS (10,000 iterations, seed=42) ===")
print(f"Mean LCOM: ${LCOM.mean():.0f}/t   (paper claims ~$1,125/t)")
print(f"90% CI LCOM: [${np.percentile(LCOM,5):.0f}, ${np.percentile(LCOM,95):.0f}]  (paper claims [$1020,$1240])")
print()
print(f"Mean NPV: ${NPV.mean():.1f}M   (paper claims ~-$120M)")
print(f"Median NPV: ${np.median(NPV):.1f}M   (paper claims ~-$115M)")
print(f"Std dev NPV: ${NPV.std():.1f}M   (paper claims ~$52M)")
print(f"P(NPV>0): {(NPV>0).mean()*100:.1f}%   (paper claims 42%)")
print(f"5% VaR: ${np.percentile(NPV,5):.1f}M   (paper claims -$185M)")
print()
# Spearman correlations
from scipy.stats import spearmanr
rho_meoh, _ = spearmanr(MeOH_price, NPV)
rho_h2, _ = spearmanr(H2_price, NPV)
rho_capex, _ = spearmanr(CAPEX, NPV)
print(f"Spearman rho (MeOH price, NPV): {rho_meoh:.2f}   (paper claims +0.70)")
print(f"Spearman rho (H2 price, NPV): {rho_h2:.2f}   (paper claims -0.64)")
print(f"Spearman rho (CAPEX, NPV): {rho_capex:.2f}   (paper claims -0.18)")
