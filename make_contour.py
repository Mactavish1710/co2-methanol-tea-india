import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.optimize import fsolve
from equilibrium import Keq

mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.size'] = 9
mpl.rcParams['axes.linewidth'] = 0.6

def equilibrium_conversion(T_C, P, H2_CO2=3.0, n_CO2_0=1.0, n_N2_0=0.001):
    T = T_C + 273.15
    K1 = Keq(T, 1)
    K2 = Keq(T, 2)
    n_H2_0 = H2_CO2*n_CO2_0
    P0 = 1.0

    def eqs(x):
        xi1, xi2 = x
        n_CO2 = n_CO2_0 - xi1 - xi2
        n_H2 = n_H2_0 - 3*xi1 - xi2
        n_CH3OH = xi1
        n_H2O = xi1+xi2
        n_CO = xi2
        n_tot = n_CO2+n_H2+n_CH3OH+n_H2O+n_CO+n_N2_0
        if n_CO2<=1e-9 or n_H2<=1e-9:
            return [1e6,1e6]
        y_CO2=n_CO2/n_tot; y_H2=n_H2/n_tot; y_CH3OH=n_CH3OH/n_tot; y_H2O=n_H2O/n_tot; y_CO=n_CO/n_tot
        eq1 = (y_CH3OH*y_H2O)/(y_CO2*y_H2**3)*(P/P0)**(-2) - K1
        eq2 = (y_CO*y_H2O)/(y_CO2*y_H2) - K2
        return [eq1,eq2]

    sol = fsolve(eqs, [0.15,0.02], full_output=True)
    xi1,xi2 = sol[0]
    return (xi1+xi2)*100  # conversion %

# Grid: T from 200-300C, P from 30-80 bar
Ts = np.linspace(200, 300, 25)
Ps = np.linspace(30, 80, 25)
TT, PP = np.meshgrid(Ts, Ps)
XX = np.zeros_like(TT)

for i in range(len(Ps)):
    for j in range(len(Ts)):
        XX[i,j] = equilibrium_conversion(TT[i,j], PP[i,j])

fig, ax = plt.subplots(figsize=(6.5,5))
cf = ax.contourf(TT, PP, XX, levels=20, cmap='viridis')
cs = ax.contour(TT, PP, XX, levels=np.arange(0,50,5), colors='white', linewidths=0.5)
ax.clabel(cs, inline=True, fontsize=6, fmt='%d%%')

# design point
X_design = equilibrium_conversion(250, 50)
ax.scatter([250],[50], color='red', s=80, edgecolor='white', zorder=5, marker='o')
ax.annotate(f'Design point\n({250}\u00b0C, 50 bar)\nX={X_design:.1f}%', xy=(250,50), xytext=(260,65),
            fontsize=7.5, color='white',
            arrowprops=dict(arrowstyle='->', color='white', lw=0.8))

ax.axvline(270, color='red', linestyle='--', linewidth=1.0, alpha=0.7)
ax.text(271, 32, 'Sintering limit\n(270\u00b0C)', fontsize=6.5, color='red')

ax.set_xlabel('Temperature (\u00b0C)')
ax.set_ylabel('Pressure (bar)')
ax.set_title('Equilibrium CO$_2$ Conversion (%) - Isothermal\n(computed by solving equilibrium at each T,P)', fontsize=10)
cbar = fig.colorbar(cf, ax=ax)
cbar.set_label('CO$_2$ conversion (%)')

plt.tight_layout()
plt.savefig('/home/claude/co2-methanol-tea/figures/conversion_contour.pdf', dpi=300, bbox_inches='tight')
plt.savefig('/home/claude/co2-methanol-tea/figures/conversion_contour.png', dpi=200, bbox_inches='tight')
print(f"Saved conversion_contour.pdf/.png -- design point conversion = {X_design:.2f}%")
print(f"Conversion at 30bar/250C: {equilibrium_conversion(250,30):.2f}%")
print(f"Conversion at 80bar/250C: {equilibrium_conversion(250,80):.2f}%")
