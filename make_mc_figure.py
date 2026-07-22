import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.size'] = 9
mpl.rcParams['axes.linewidth'] = 0.6
mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['ytick.direction'] = 'in'

data = np.load('/home/claude/mc_results.npz')
NPV = data['NPV']

mean_npv = NPV.mean()
var5 = np.percentile(NPV, 5)
p_pos = (NPV > 0).mean() * 100

fig, ax1 = plt.subplots(figsize=(7.0, 4.5))

n, bins, patches = ax1.hist(NPV, bins=60, color='#4C72B0', edgecolor='white',
                              linewidth=0.3, alpha=0.85)
ax1.set_xlabel('Net Present Value (\\$ million)')
ax1.set_ylabel('Frequency (count)')
ax1.axvline(0, color='#C44E52', linestyle='--', linewidth=1.2, label='NPV = 0 breakeven')
ax1.axvline(mean_npv, color='black', linestyle='-', linewidth=1.0, alpha=0.7)

# cumulative on secondary axis
ax2 = ax1.twinx()
sorted_npv = np.sort(NPV)
cdf = np.arange(1, len(sorted_npv)+1) / len(sorted_npv)
ax2.plot(sorted_npv, cdf*100, color='#333333', linewidth=1.3)
ax2.set_ylabel('Cumulative probability (%)')
ax2.set_ylim(0, 100)

ax1.legend(loc='upper left', frameon=False, fontsize=8)

ax1.text(0.02, 0.85,
         f'Mean NPV = \${mean_npv:.0f}M\n5% VaR = \${var5:.0f}M\nP(NPV>0) = {p_pos:.0f}%\nN = 10,000 (seed=42)',
         transform=ax1.transAxes, fontsize=7.5, verticalalignment='top',
         bbox=dict(boxstyle='round', facecolor='white', edgecolor='#cccccc', linewidth=0.5))

ax1.spines['top'].set_visible(False)
ax2.spines['top'].set_visible(False)

plt.title('Monte Carlo NPV Distribution (10,000 iterations)', fontsize=10)
plt.tight_layout()
plt.savefig('/home/claude/co2-methanol-tea/figures/montecarlo.pdf', dpi=300, bbox_inches='tight')
plt.savefig('/home/claude/co2-methanol-tea/figures/montecarlo.png', dpi=200, bbox_inches='tight')
print("Saved montecarlo.pdf and .png -- REAL DATA, actually plotted from mc_results.npz")
