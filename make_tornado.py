import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from adiabatic import adiabatic_solve

mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.size'] = 9
mpl.rcParams['axes.linewidth'] = 0.6

T_in=250+273.15; P=50
xi1,xi2,T_ad,X_SP_pct,sel,ier,msg = adiabatic_solve(T_in,P,3.0)
X_SP = X_SP_pct/100
R=0.90
X_overall = X_SP/(1-R*(1-X_SP))

CAPEX_base=55.2
H2_cost_base=87.44
CO2_cost_base=16.85
other_opex = 0.82+0.14+0.43+0.54
CRF=0.1175
i=0.10; n=20
af=(1-(1+i)**-n)/i
production=100000

def NPV_calc(H2_price=3.50, CO2_price=45, MeOH_price=1000, CAPEX=CAPEX_base, elec_mult=1.0):
    H2_cost = H2_cost_base*(H2_price/3.50)
    CO2_cost = CO2_cost_base*(CO2_price/45)
    OPEX = H2_cost+CO2_cost+other_opex*elec_mult
    AnnCAPEX = CRF*CAPEX
    Revenue = MeOH_price*production/1e6
    return -CAPEX + (Revenue-OPEX)*af

base_NPV = NPV_calc()

params = [
    ('Hydrogen price', 'H2_price', 3.50),
    ('Methanol selling price', 'MeOH_price', 1000),
    ('CO2 feedstock cost', 'CO2_price', 45),
    ('CAPEX', 'CAPEX', 55.2),
]

results = []
for name, key, base_val in params:
    low = NPV_calc(**{key: base_val*0.8})
    high = NPV_calc(**{key: base_val*1.2})
    results.append((name, low, high))

# sort by swing magnitude
results.sort(key=lambda x: abs(x[2]-x[1]))

fig, ax = plt.subplots(figsize=(6.5, 3.5))
names = [r[0] for r in results]
lows = [r[1] for r in results]
highs = [r[2] for r in results]
y_pos = np.arange(len(names))

for idx, (name, low, high) in enumerate(results):
    left = min(low, high)
    width = abs(high-low)
    color = '#C44E52' if high < low else '#4C72B0'
    ax.barh(idx, width, left=left, height=0.55, color='#4C72B0', alpha=0.75, edgecolor='black', linewidth=0.5)
    ax.text(low, idx, f' {low:.0f}', va='center', ha='right' if low<base_NPV else 'left', fontsize=7.5)
    ax.text(high, idx, f'{high:.0f} ', va='center', ha='left' if high>base_NPV else 'right', fontsize=7.5)

ax.axvline(base_NPV, color='black', linestyle='--', linewidth=1.0, label=f'Base case NPV = ${base_NPV:.0f}M')
ax.axvline(0, color='gray', linestyle=':', linewidth=0.8)
ax.set_yticks(y_pos)
ax.set_yticklabels(names)
ax.set_xlabel('NPV ($ million)')
ax.set_title('NPV Sensitivity to \u00b120% Parameter Variation', fontsize=10)
ax.legend(loc='lower right', fontsize=7.5, frameon=False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('/home/claude/co2-methanol-tea/figures/tornado.pdf', dpi=300, bbox_inches='tight')
plt.savefig('/home/claude/co2-methanol-tea/figures/tornado.png', dpi=200, bbox_inches='tight')
print("Saved tornado.pdf/.png -- real sensitivity data")
for name, low, high in results:
    print(f'{name}: [{low:.1f}, {high:.1f}]M, swing={abs(high-low):.1f}M')
