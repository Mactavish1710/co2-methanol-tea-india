import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from adiabatic import adiabatic_solve

mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.size'] = 9
mpl.rcParams['axes.linewidth'] = 0.6
mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['ytick.direction'] = 'in'

T_in = 250 + 273.15
P = 50
xi1, xi2, T_ad, X_SP_pct, sel, ier, msg = adiabatic_solve(T_in, P, 3.0)
X_SP = X_SP_pct / 100.0

Rs = np.linspace(0.01, 0.98, 100)
X_overall = X_SP / (1 - Rs*(1 - X_SP))

base_idx = np.argmin(np.abs(Rs - 0.90))
X_base = X_overall[base_idx]

# Production rate scales with overall conversion, normalized to paper's 100kt/yr = 274 t/day at R=0.90
prod_rate = (X_overall / X_base) * (100000/365)

# Recycle compressor power - real engineering assumption stated in paper (linear 850->2850 kW)
comp_power = 850 + Rs*(2850-850)

# NPV using the SAME verified economic model as the tornado/Monte Carlo analysis
CO2_base = 374450.0
CO2_fresh = CO2_base * (X_base/X_overall)
H2_cost_base = 87.44
CO2_cost_base = 16.85
H2_cost = H2_cost_base * (CO2_fresh/CO2_base)
CO2_cost = CO2_cost_base * (CO2_fresh/CO2_base)
comp_opex = comp_power*7920*0.07/1e6
OPEX = H2_cost + CO2_cost + comp_opex + 0.14+0.43+0.54
CAPEX = 55.2
CRF = 0.1175
Revenue = 1000*100000/1e6
i=0.10; n=20
af = (1-(1+i)**-n)/i
NPV = -CAPEX + (Revenue-OPEX)*af

fig, axes = plt.subplots(2, 2, figsize=(7.5, 6))

axes[0,0].axhline(X_SP*100, color='#999999', linestyle='--', linewidth=0.8, label='Single-pass (constant)')
axes[0,0].plot(Rs, X_overall*100, color='#4C72B0', linewidth=1.6, label='Overall conversion')
axes[0,0].scatter([0.90],[X_base*100], color='white', edgecolor='#4C72B0', marker='o', s=45, zorder=5)
axes[0,0].set_xlabel('Recycle ratio, R')
axes[0,0].set_ylabel('CO$_2$ conversion (%)')
axes[0,0].set_title('(a) Conversion vs. R', fontsize=9)
axes[0,0].legend(fontsize=7, frameon=False)

axes[0,1].plot(Rs, prod_rate, color='#55A868', linewidth=1.6)
axes[0,1].scatter([0.90],[prod_rate[base_idx]], color='white', edgecolor='#55A868', marker='o', s=45, zorder=5)
axes[0,1].set_xlabel('Recycle ratio, R')
axes[0,1].set_ylabel('Methanol production (t/day)')
axes[0,1].set_title('(b) Production rate vs. R', fontsize=9)

axes[1,0].plot(Rs, comp_power, color='#C44E52', linewidth=1.6)
axes[1,0].scatter([0.90],[comp_power[base_idx]], color='white', edgecolor='#C44E52', marker='o', s=45, zorder=5)
axes[1,0].set_xlabel('Recycle ratio, R')
axes[1,0].set_ylabel('Recycle compressor power (kW)')
axes[1,0].set_title('(c) Compressor duty vs. R', fontsize=9)

axes[1,1].plot(Rs, NPV, color='#8172B2', linewidth=1.6)
axes[1,1].scatter([0.90],[NPV[base_idx]], color='white', edgecolor='#8172B2', marker='o', s=45, zorder=5,
                   label=f'Base case R=0.90\n(NPV=${NPV[base_idx]:.0f}M)')
axes[1,1].axhline(0, color='gray', linestyle=':', linewidth=0.7)
axes[1,1].set_xlabel('Recycle ratio, R')
axes[1,1].set_ylabel('NPV ($ million)')
axes[1,1].set_title('(d) NPV vs. R (deterministic model)', fontsize=9)
axes[1,1].legend(fontsize=7, frameon=False, loc='upper left')

for ax in axes.flat:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('/home/claude/co2-methanol-tea/figures/recycle.pdf', dpi=300, bbox_inches='tight')
plt.savefig('/home/claude/co2-methanol-tea/figures/recycle.png', dpi=200, bbox_inches='tight')
print(f"Saved recycle.pdf/.png")
print(f"NPV at R=0.90: ${NPV[base_idx]:.1f}M")
print(f"NPV monotonically {'increases' if NPV[-1]>NPV[0] else 'decreases'} with R across modelled range")
print(f"NOTE: this model does not include the inert-gas dilution penalty at high R described")
print(f"in the text (Section 7.5) -- it shows the monotonic trend absent that effect, consistent")
print(f"with the paper's honest framing that a full steady-state inert balance is future work.")
