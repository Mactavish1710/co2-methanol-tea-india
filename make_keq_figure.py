import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from equilibrium import Keq

mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.size'] = 9
mpl.rcParams['axes.linewidth'] = 0.6
mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['ytick.direction'] = 'in'

T_C = np.linspace(200, 310, 100)
T_K = T_C + 273.15

K1 = np.array([Keq(T, 1) for T in T_K])
K2 = np.array([Keq(T, 2) for T in T_K])

fig, ax1 = plt.subplots(figsize=(6.0, 4.2))

ax1.semilogy(T_C, K1, color='#4C72B0', linewidth=1.6, label=r'$K_{eq,1}$ (CO$_2$ hydrogenation)')
ax1.semilogy(T_C, K2, color='#C44E52', linewidth=1.6, linestyle='--', label=r'$K_{eq,2}$ (RWGS)')

# design point marker
T_design = 250
K1_design = Keq(250+273.15, 1)
K2_design = Keq(250+273.15, 2)
ax1.scatter([T_design], [K1_design], color='#4C72B0', edgecolor='black', s=50, zorder=5)
ax1.scatter([T_design], [K2_design], color='#C44E52', edgecolor='black', s=50, zorder=5, marker='D')
ax1.axvline(T_design, color='gray', linestyle=':', linewidth=0.8, alpha=0.7)

ax1.set_xlabel('Temperature (\u00b0C)')
ax1.set_ylabel('Equilibrium constant, $K_{eq}$')
ax1.set_title('Equilibrium Constants vs. Temperature\n(computed from NIST Shomate data)', fontsize=10)
ax1.legend(loc='center left', fontsize=8, frameon=False)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

ax1.text(T_design+3, K1_design, f'  {K1_design:.2e}', fontsize=7, va='center')
ax1.text(T_design+3, K2_design, f'  {K2_design:.2e}', fontsize=7, va='center')

plt.tight_layout()
plt.savefig('/home/claude/co2-methanol-tea/figures/keq.pdf', dpi=300, bbox_inches='tight')
plt.savefig('/home/claude/co2-methanol-tea/figures/keq.png', dpi=200, bbox_inches='tight')
print(f"Saved keq.pdf/.png -- K1(250C)={K1_design:.3e}, K2(250C)={K2_design:.3e}")
