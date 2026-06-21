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


# Bestimme Längen der Kabel. Dazu verwende Phasengeschwindigkeit v_ph eines RG-58C/U Kabel (d=0.9mm, D=2.95mm, eps = 2.25), welche auch in verschiedenen Längen bei der Messung genutzt wurden. 
d = 0.9 # mm
D = 2.95 # mm
eps = 2.25 # = eps_0 * eps_r
L = 1/(2*np.pi)*np.log(D/d) # H/m
C = 2*np.pi*eps/(np.log(D/d)) # F/m
v_ph = 1/np.sqrt(L*C)*const.c # m/s

"""Bekomme mit dieser theoretischen Überlegung die Längen der anderen Sachen heraus."""



def get_alpha(U_0, U_1, L):
    """Es gilt die Formel U(z) = U_0 * exp(-alpha*z) mit z:Länge entlang des Kabels. 
    D.h. um alpha zu berechnen braucht man auch den Abstand zwischen den Peaks
    also U_1 = U_0 * exp(-alpha * 2*L) mit L:Länge des Kabels."""
    return 1/(2*L) * np.log(U_0/U_1)



#-----------Für Mittleres Kabel-------------------
A_0, A_1, Zero, dt, L = np.genfromtxt("raw/laenge_daempfung.csv", delimiter=",", unpack=True, skip_header=4, skip_footer=1)
L = ufloat(L, 0.01) #m
dt_mittel = dt
L_mittel = L
L_mittel_theo = dt*1e-9*v_ph/2

#Beziehe Höhe der Peaks auf Zero-Level:
U_0 = np.abs(A_0 - Zero)
U_1 = np.abs(A_1 - Zero)

alpha_mittel = get_alpha(U_0, U_1, L)

#---------------Für mittellanges Kabel------------------
A_0, A_1, Zero, dt, L = np.genfromtxt("raw/laenge_daempfung.csv", delimiter=",", unpack=True, skip_header=6)
L = ufloat(L, 0.05) #m
dt_mittellang = dt
L_mittellang = L
L_mittellang_theo = dt*1e-9**v_ph/2

#Beziehe Höhe der Peaks auf Zero-Level:
"""Es gilt die Formel U(z) = U_0 * exp(-alpha*z) mit z:Länge entlang des Kabels. 
D.h. um alpha zu berechnen braucht man auch den Abstand zwischen den Peaks
also U_1 = U_0 * exp(-alpha * 2*L) mit L:Länge des Kabels."""
U_0 = np.abs(A_0 - Zero)
U_1 = np.abs(A_1 - Zero)

alpha_mittellang = get_alpha(U_0, U_1, L)

#-------------Für das Lange Kabel--------------------:

#Berechne Dämpfungskonstante und Länge für verschiedene Kabel
A_0, A_1, Zero, dt, L = np.genfromtxt("raw/laenge_daempfung.csv", delimiter=",", unpack=True,skip_footer=2)
L = ufloat(L, 0.01) #m
dt_lang = dt 
L_lang = L
L_lang_theo = dt*1e-9*v_ph/2

#Beziehe Höhe der Peaks auf Zero-Level:
U_0 = np.abs(A_0 - Zero)
U_1 = np.abs(A_1 - Zero)
alpha_lang = get_alpha(U_0, U_1, L)


# print(alpha_lang, alpha_mittel, alpha_mittellang)

#---------Bestimme anhand von Länge und delta_t die Phasengeschindigkeit und damit das epsilon der Kabel---------------- v_ph = 2L/dt <=> L(t) = v_ph/2 * t + 0

#Lineare Regression
dt_arr = np.array([dt_lang, dt_mittel, dt_mittellang])
L_arr = unp.uarray(noms([L_lang, L_mittel, L_mittellang]), stds([L_lang, L_mittel, L_mittellang]))

#v_phas und epsilon für langes kabel epsilon = (c/v)^2 = (c*dt/(2*L))^2
e_l = (const.c * dt_arr[0]*1e-9 / (2*L_arr[0]))**2
e_m = (const.c * dt_arr[1]*1e-9 / (2*L_arr[1]))**2
e_ml = (const.c * dt_arr[2]*1e-9 / (2*L_arr[2]))**2
# print(e_l, e_m, e_ml)

write("Alphas und epsilons:\n\n")
add(f"Für L = 20m (langes Kabel):\n")
add(f"alpha = {alpha_lang:.6f} 1/m,\tepsilon = {e_l:.2f}\tL_theo = {L_lang_theo:.2f}\n")
add(f"Für L = 1.5m (mittleres Kabel):\n")
add(f"alpha = {alpha_mittel:.6f} 1/m,\tepsilon = {e_m:.2f}\tL_theo = {L_mittel_theo:.2f}\n")
add(f"Für L = 5m (mittellanges Kabel):\n")
add(f"alpha = {alpha_mittellang:.4f} 1/m,\tepsilon = {e_ml:.2f}\tL_theo = {L_mittellang_theo:.2f}\n")



#Bei dieser Auswertung merkt man, dass die Werte für das Lange Kabel nicht stimmen können, was daran liegen kann dass das Kabel nicht 20m lang ist sondern kürzer (?) 
#Dazu errechne aus der linearen Regression für die ersten zwei Werte einfach ein L und ein passendes alpha heraus und gucke wie das aussieht.

#Nehme langes Kabel werte heraus

# print(dt_arr[1:], L_arr[1:])
result = linregress(dt_arr[1:], noms(L_arr[1:]))
m = ufloat(result.slope, result.stderr)
b = ufloat(result.intercept, result.intercept_stderr)

#L(t) = m * t AND L(dt) = v_ph/2 * dt => v_ph = 2m
v_ph = 2*m*1e9
L_lang_theo = m * dt_lang
ee_l = (const.c * dt_lang*1e-9 / (2*L_lang_theo))**2
# ee_l = (const.c / v_ph)**2

# new arrays
# L_arr[0] = L_lang_theo
fig, ax = plt.subplots()
ax.errorbar(dt_arr, noms(L_arr), yerr=stds(L_arr), color="blue", fmt=".", label="Daten")
ax.errorbar(dt_arr[0], noms(L_lang_theo), yerr=stds(L_lang_theo), color="green", fmt="x", label="Geschätzter Datenpunkt")
dt_plot = np.linspace(0, np.max(dt_arr), 100)
ax.plot(dt_plot, noms(m)*dt_plot + noms(b), "r--", label="Lineare Regression")
ax.grid()
ax.legend()
ax.set(
    xlabel=r"$\Delta t \, [\mathrm{ns}]$",
    ylabel=r"$L \, [\mathrm{m}]$"
)

fig.savefig(dir + "vphase.pdf")

alpha_lang_theo = get_alpha(U_0, U_1, L_lang_theo)
e_l_theo = ee_l



add(f"Für langes Kabel errechnete Werte (basierend auf der Tendenz der anderen beiden Messpunkte):\n")
add(f"Alpha_estimated = {alpha_lang_theo:.4f} 1/m ,\tepsilon_estimated={e_l_theo:.2f} ,\t L_lang_theo = {L_lang_theo:.2f} m\n")
add(f"Koeffizienten Linregress: m = {m:.4f} m/ns, \t b = {b:.4f} m ")