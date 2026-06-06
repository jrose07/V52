import uncertainties.unumpy as unp
import numpy as np
from scipy.optimize import curve_fit
from addons import write, add, latex_float, tab_to_latex as tab2tex
from scipy.stats import linregress
from uncertainties import ufloat
from uncertainties.unumpy import nominal_values as noms, std_devs as stds
import scipy.constants as const
import matplotlib.pyplot as plt

dir = "content/plots/"
dir_tab = "content/tables/"

#Importiere Daten
f, R, L, C, Z, phi = np.genfromtxt("raw/RCL.csv", delimiter=",", skip_header=1, unpack=True)

#Kreisfrequenz
omega = 2*np.pi*f #[kHz]

#Add Uncertainties
R = unp.uarray(R, 0.001)
L = unp.uarray(L, 0.01)
C = unp.uarray(C, 0.001)

#Bestimme G aus Werten
"""Es gilt G = 2pi sigma / ln(D/d) mit:
D, d: Durchmesser der Leiter des Koaxialkabels (d:innen, D:außen)
sigma = f * Im(epsilon_r)
Bei diesem Kabel: d=0.9mm, D=2.95mm, epsilon_r = 2.25 (Aus Anleitung)
"""
d = 0.9 #mm
D = 2.95 #mm
epsilon = 2.25

G = 2*np.pi*omega*epsilon / np.log(D/d)

#Plotte R,L,G,C in Abhängigkeit von omega

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2, figsize=(10, 8))

ax1.errorbar(omega, noms(R), yerr=stds(R), color="red", fmt=".")
ax1.set(title="R(ω)", xlabel="ω [rad/s]", ylabel=r"$R \, [\Omega]$")
ax1.grid()

ax2.errorbar(omega, noms(L), yerr=stds(L), color="green", fmt=".")
ax2.set(title="L(ω)", xlabel="ω [rad/s]", ylabel=r"$L \, [\mu H]$")
ax2.grid()

ax3.plot(omega, G, "b.")
ax3.set(title="G(ω)", xlabel="ω [rad/s]", ylabel=r"$G \, [\frac{kS}{m}]$")
ax3.grid()

ax4.errorbar(omega, noms(C), yerr=stds(C), color="k", fmt=".")
ax4.set(title="C(ω)", xlabel="ω [rad/s]", ylabel=r"$C \, [nF]$")
ax4.grid()

fig.tight_layout()
fig.savefig(dir + "RCL.pdf")