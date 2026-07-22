import numpy as np
from scipy.optimize import fsolve
from equilibrium import Keq, shomate_H

R = 8.314

def Cp(T, sp):
    """Heat capacity at temperature T (K) from Shomate, J/mol/K"""
    from equilibrium import species
    t = T/1000.0
    c = species[sp]
    if sp == 'CH3OH':
        # paper uses linear supplement for methanol: Cp = 21.23 + 0.0766*T (T in Celsius per context, check)
        # Actually paper says over 200-300C range; let's use Shomate formula for consistency in this check
        return c['A'] + c['B']*t + c['C']*t**2 + c['D']*t**3 + c['E']/t**2
    return c['A'] + c['B']*t + c['C']*t**2 + c['D']*t**3 + c['E']/t**2

def adiabatic_solve(T_in, P, H2_CO2_ratio, n_CO2_0=1.0):
    """Solve coupled equilibrium + adiabatic energy balance.
    H_in(T_in) = H_out(T_ad), solve for xi1, xi2, T_ad simultaneously.
    """
    n_H2_0 = H2_CO2_ratio * n_CO2_0
    P0 = 1.0

    def equations(x):
        xi1, xi2, T_ad = x
        T_ad_K = T_ad  # already in K

        K1 = Keq(T_ad_K, 1)
        K2 = Keq(T_ad_K, 2)

        n_CO2 = n_CO2_0 - xi1 - xi2
        n_H2 = n_H2_0 - 3*xi1 - xi2
        n_CH3OH = xi1
        n_H2O = xi1 + xi2
        n_CO = xi2
        n_tot = n_CO2 + n_H2 + n_CH3OH + n_H2O + n_CO

        if n_CO2 <= 1e-8 or n_H2 <= 1e-8 or n_tot <= 0:
            return [1e6, 1e6, 1e6]

        y_CO2 = n_CO2/n_tot
        y_H2 = n_H2/n_tot
        y_CH3OH = n_CH3OH/n_tot
        y_H2O = n_H2O/n_tot
        y_CO = n_CO/n_tot

        eq1 = (y_CH3OH*y_H2O)/(y_CO2*y_H2**3) * (P/P0)**(-2) - K1
        eq2 = (y_CO*y_H2O)/(y_CO2*y_H2) - K2

        # Energy balance: enthalpy of reactants at T_in = enthalpy of products at T_ad
        # H_in = sum(n_i,0 * H_i(T_in)); H_out = sum(n_i * H_i(T_ad))
        # Using Shomate H (kJ/mol) referenced consistently
        H_in = n_CO2_0*shomate_H(T_in,'CO2') + n_H2_0*shomate_H(T_in,'H2')
        H_out = n_CO2*shomate_H(T_ad_K,'CO2') + n_H2*shomate_H(T_ad_K,'H2') + \
                n_CH3OH*shomate_H(T_ad_K,'CH3OH') + n_H2O*shomate_H(T_ad_K,'H2O') + \
                n_CO*shomate_H(T_ad_K,'CO')

        eq3 = (H_in - H_out)  # kJ, should be 0 (adiabatic, no work)

        return [eq1, eq2, eq3/10.0]  # scale eq3 for solver conditioning

    T_in_K = 250 + 273.15
    x0 = [0.15, 0.02, T_in_K + 20]
    sol = fsolve(equations, x0, full_output=True, xtol=1e-10)
    xi1, xi2, T_ad = sol[0]
    ier = sol[2]
    msg = sol[3]

    conv = (xi1+xi2)/n_CO2_0*100
    sel = xi1/(xi1+xi2)*100 if (xi1+xi2)>0 else 0

    return xi1, xi2, T_ad, conv, sel, ier, msg

T_in = 250 + 273.15
P = 50
xi1, xi2, T_ad, conv, sel, ier, msg = adiabatic_solve(T_in, P, 3.0)

print(f"COUPLED ADIABATIC SOLVE (real Newton-Raphson via scipy.fsolve):")
print(f"  Converged: {ier==1} -- {msg}")
print(f"  xi1={xi1:.5f}, xi2={xi2:.5f}")
print(f"  T_adiabatic = {T_ad-273.15:.1f} C   (paper claims 268.9 C)")
print(f"  CO2 conversion = {conv:.2f}%   (paper claims 21.1%)")
print(f"  Methanol selectivity = {sel:.2f}%   (paper claims 50.4%)")
