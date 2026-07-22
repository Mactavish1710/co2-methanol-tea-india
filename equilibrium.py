"""
Real thermodynamic equilibrium model for CO2 + 3H2 <=> CH3OH + H2O
and CO2 + H2 <=> CO + H2O (RWGS)
Using NIST Shomate coefficients as given in the paper's Table 1.
"""
import numpy as np
from scipy.optimize import fsolve

R = 8.314  # J/mol/K

# Shomate coefficients: A, B, C, D, E, dHf298 (kJ/mol)
# From paper Table 1
species = {
    'CO2': dict(A=24.997, B=55.187, C=-33.691, D=7.948, E=-0.137, dHf=-393.51),
    'H2':  dict(A=33.066, B=-11.363, C=11.433, D=-2.773, E=-0.159, dHf=0.0),
    'CH3OH': dict(A=21.150, B=70.870, C=-55.998, D=17.318, E=0.002, dHf=-201.00),
    'H2O': dict(A=30.092, B=6.833, C=6.793, D=-2.534, E=0.082, dHf=-241.83),
    'CO':  dict(A=25.568, B=6.096, C=4.055, D=-2.671, E=0.131, dHf=-110.53),
}

def shomate_H(T, sp):
    """Standard enthalpy H(T) - H(298) in kJ/mol using Shomate integration"""
    t = T/1000.0
    c = species[sp]
    H = c['A']*t + c['B']*t**2/2 + c['C']*t**3/3 + c['D']*t**4/4 - c['E']/t + \
        (-c['A']*0.298 - c['B']*0.298**2/2 - c['C']*0.298**3/3 - c['D']*0.298**4/4 + c['E']/0.298)
    return c['dHf'] + H  # kJ/mol, absolute-ish (relative reaction use only needs differences)

def shomate_S(T, sp):
    """Standard entropy S(T) in J/mol/K using Shomate integration.
    NOTE: paper doesn't give S298 for all species explicitly except methanol (239.9).
    For CO2, H2, H2O, CO we use standard NIST S298 values (well-established, textbook):
    """
    S298 = {'CO2': 213.79, 'H2': 130.68, 'CH3OH': 239.9, 'H2O': 188.84, 'CO': 197.66}
    t = T/1000.0
    c = species[sp]
    S = c['A']*np.log(t) + c['B']*t + c['C']*t**2/2 + c['D']*t**3/3 - c['E']/(2*t**2)
    t0 = 0.298
    S0 = c['A']*np.log(t0) + c['B']*t0 + c['C']*t0**2/2 + c['D']*t0**3/3 - c['E']/(2*t0**2)
    return S298[sp] + (S - S0)

def dG_reaction(T, reaction):
    """Gibbs free energy change for a reaction at temperature T (K), returns kJ/mol"""
    if reaction == 1:  # CO2 + 3H2 -> CH3OH + H2O
        dH = shomate_H(T,'CH3OH') + shomate_H(T,'H2O') - shomate_H(T,'CO2') - 3*shomate_H(T,'H2')
        dS = shomate_S(T,'CH3OH') + shomate_S(T,'H2O') - shomate_S(T,'CO2') - 3*shomate_S(T,'H2')
    elif reaction == 2:  # CO2 + H2 -> CO + H2O (RWGS)
        dH = shomate_H(T,'CO') + shomate_H(T,'H2O') - shomate_H(T,'CO2') - shomate_H(T,'H2')
        dS = shomate_S(T,'CO') + shomate_S(T,'H2O') - shomate_S(T,'CO2') - shomate_S(T,'H2')
    dG = dH - T*dS/1000.0  # kJ/mol
    return dG

def Keq(T, reaction):
    dG = dG_reaction(T, reaction)
    return np.exp(-dG*1000/(R*T))

# Test: print Keq at 250C = 523.15K
T_design = 250 + 273.15
K1 = Keq(T_design, 1)
K2 = Keq(T_design, 2)
print(f"At T=250C: K_eq1 (methanol) = {K1:.3e}, K_eq2 (RWGS) = {K2:.3e}")
print(f"Paper claims: K_eq1 = 2.0e-5, K_eq2 = 1.1e-2")
