import numpy as np
from scipy.optimize import fsolve
from equilibrium import Keq

def equilibrium_solve(T, P, H2_CO2_ratio, n_CO2_0=1.0, n_N2_0=0.001):
    """Solve for xi1, xi2 (extents of reaction) at fixed T, P.
    Basis: n_CO2_0 = 1 mol
    """
    n_H2_0 = H2_CO2_ratio * n_CO2_0
    n_CH3OH_0 = 0.0
    n_H2O_0 = 0.0
    n_CO_0 = 0.0

    K1 = Keq(T, 1)
    K2 = Keq(T, 2)
    P0 = 1.0  # bar reference

    def equations(x):
        xi1, xi2 = x
        n_CO2 = n_CO2_0 - xi1 - xi2
        n_H2 = n_H2_0 - 3*xi1 - xi2
        n_CH3OH = n_CH3OH_0 + xi1
        n_H2O = n_H2O_0 + xi1 + xi2
        n_CO = n_CO_0 + xi2
        n_tot = n_CO2 + n_H2 + n_CH3OH + n_H2O + n_CO + n_N2_0

        if n_CO2 <= 0 or n_H2 <= 0 or n_tot <= 0:
            return [1e6, 1e6]

        y_CO2 = n_CO2/n_tot
        y_H2 = n_H2/n_tot
        y_CH3OH = n_CH3OH/n_tot
        y_H2O = n_H2O/n_tot
        y_CO = n_CO/n_tot

        eq1 = (y_CH3OH*y_H2O)/(y_CO2*y_H2**3) * (P/P0)**(-2) - K1
        eq2 = (y_CO*y_H2O)/(y_CO2*y_H2) - K2
        return [eq1, eq2]

    # initial guess
    x0 = [0.15*n_CO2_0, 0.01*n_CO2_0]
    sol = fsolve(equations, x0, full_output=True)
    xi1, xi2 = sol[0]
    conv = (xi1+xi2)/n_CO2_0 * 100
    return xi1, xi2, conv

# Test at design point: 250C, 50 bar, H2/CO2=3.0 -- ISOTHERMAL case
T = 250 + 273.15
P = 50
xi1, xi2, conv = equilibrium_solve(T, P, 3.0)
n_CO2_0 = 1.0
n_CH3OH = xi1
selectivity = xi1/(xi1+xi2)*100
print(f"ISOTHERMAL at 250C, 50 bar, H2/CO2=3.0:")
print(f"  xi1={xi1:.5f}, xi2={xi2:.5f}")
print(f"  CO2 conversion = {conv:.2f}%  (paper claims 23.4% isothermal)")
print(f"  Methanol selectivity = {selectivity:.1f}%  (paper claims 98.3% isothermal)")
