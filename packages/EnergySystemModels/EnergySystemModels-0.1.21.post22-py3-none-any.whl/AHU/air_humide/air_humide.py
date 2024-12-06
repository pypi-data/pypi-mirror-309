from math import*
import numpy as np



def Air_xH2O(T_db=None,T_wb=None,RH=None,w=None,h=None):
      Mdry=28.965
      Mv=18.01528
      if (T_wb is not None and w is None):
        w=Air_w(T_db=T_db,T_wb=T_wb)
      if RH is not None:
        w=Air_w(T_db=T_db,RH=RH)     
      xH2O=w*Mdry/(w*Mdry+Mv*1000)
      return round(xH2O,4)

def func_Pv_sat(T_db) :

#calcul de la pression de vapeur sat
# référence : 2013 ASRHAE Handbook—Fundamentals (SI) - CHAPTER 1 - PSYCRHOMETRICS - Equations (5) and (6) - Hyland and Wexler 1983 equations
# Pv_sat = saturation pressure, Pa
# Tk = absolute temperature, K = °C + 273.15


	C1 = -5.6745359 * 10 ** 3
	C2 = 6.3925247 * 10 ** 0
	C3 = -9.677843 * 10 ** (-3)
	C4 = 6.2215701 * 10 ** (-7)
	C5 = 2.0747825 * 10 ** (-9)
	C6 = -9.484024 * 10 ** (-13)
	C7 = 4.1635019 * 10 ** (0)
	C8 = -5.8002206 * 10 ** (3)
	C9 = 1.3914993 * 10 ** (0)
	C10 = -4.8640239 * 10 ** (-2)
	C11 = 4.1764768 * 10 ** (-5)
	C12 = -1.4452093 * 10 ** (-8)
	C13 = 6.5459673 * 10 ** (0)

	Tk = T_db + 273.15

	if T_db < 0 : #valable entre -100 et 0 °C

		Pv_sat = exp(C1 / Tk + C2 + C3 * Tk + C4 * Tk ** 2 + C5 * Tk ** 3 + C6 * Tk ** 4 + C7 * log(Tk))
	else :  #valable entre 0 et 200 °C

		Pv_sat = exp(C8 / Tk + C9 + C10 * Tk + C11 * Tk ** 2 + C12 * Tk ** 3 + C13 * log(Tk))
		




	return Pv_sat

# def Air_RH(w=None, P=101325.0, Pv_sat=None, T_db=None,T_wb=None):
#     if Pv_sat is None:
#         if T_db is None:
#             raise ValueError("Either Pv_sat or T_db must be provided")
#         else:
#             Pv_sat = func_Pv_sat(T_db)
# 	if w is None:
# 	 	if T_wb is None:
# 			raise ValueError("Either w or T_wb must be provided")
# 		else:
# 			w_w=Air_w(RH=100,T_db=T_wb)
# 			h=Air_h(T_db=T_wb,w=w_w)
# 			w=Air_w(h=h,T_db=T_db)

#     Pv = P * (w / 1000) / ((w / 1000) + 0.62198)
#     RH = (Pv / Pv_sat) * 100
#     return RH

def Air_RH(w=None, P=101325.0, Pv_sat=None, T_db=None, T_wb=None,h=None):

    if (w is not None and h is not None and T_db is None):
        T_db=Air_T_db(w=w,h=h)
    if Pv_sat is None:
        if T_db is None:
            raise ValueError("Either Pv_sat or T_db must be provided")
        else:
            # Calculer la pression de vapeur saturée à partir de T_db
            Pv_sat = func_Pv_sat(T_db)

    if w is None:
        if T_wb is None:
            raise ValueError("Either w or T_wb must be provided")
        else:
            # Calculer w à partir de T_wb en supposant que l'humidité relative est 100
            w_w = Air_w(RH=100, T_db=T_wb)  # Calculer l'humidité absolue à saturation (RH = 100)
            h = Air_h(T_db=T_wb, w=w_w)  # Calculer l'enthalpie de l'air humide à T_wb et w_w
            w = Air_w(h=h, T_db=T_db)  # Calculer w pour la température de bulbe sec T_db avec l'enthalpie h

    # Calculer la pression partielle de la vapeur d'eau Pv
    Pv = P * (w / 1000) / ((w / 1000) + 0.62198)

    # Calculer l'humidité relative RH
    RH = (Pv / Pv_sat) * 100

    return round(RH,2)


# def Air_w( RH=None, P=101325.0,Pv_sat=None,T_db=None,h=None,T_wb=None):

# 	if Pv_sat is None:
# 		if T_db is None:
# 			raise ValueError("Either Pv_sat or T_db must be provided")
# 		else:
# 			Pv_sat = func_Pv_sat(T_db)
	
# 	if RH is not None:
# 		Pv = Pv_sat * (RH / 100)
		
# 		if Pv<P:
# 			w = 0.62198 * Pv / (P - Pv) * 1000
# 		else:
# 			w =None
# 	if T_wb is not None:
# 		w_w = Air_w(RH=100, T_db=T_wb)  # Calculer l'humidité absolue à saturation (RH = 100)
#         h = Air_h(T_db=T_wb, w=w_w)  # Calculer l'enthalpie de l'air humide à T_wb et w_w
#         w = Air_w(h=h, T_db=T_db)  # Calculer w pour la température de bulbe sec T_db avec l'enthalpie h

# 	if h is not None:
# 		w   = ((h-1.006 * T_db)/(2501 + 1.0805 * T_db))*1000
	
# 	return w

def Air_w(RH=None, P=101325.0, Pv_sat=None, T_db=None, h=None, T_wb=None):
    # Calcul de la pression de vapeur saturée (Pv_sat) si elle n'est pas fournie

 
    if Pv_sat is None and T_db is not None:
       Pv_sat = func_Pv_sat(T_db)

    # Calcul de l'humidité absolue à partir de l'humidité relative
    if RH is not None and Pv_sat is not None:
        Pv = Pv_sat * (RH / 100)
        
        if Pv < P:
            w = 0.62198 * Pv / (P - Pv) * 1000
        else:
            w = None

    # Calcul de l'humidité absolue à partir de la température de bulbe humide (T_wb)
    if T_wb is not None:
        w_w = Air_w(RH=100, T_db=T_wb)  # Calculer l'humidité absolue à saturation (RH = 100)
        h = Air_h(T_db=T_wb, w=w_w)     # Calculer l'enthalpie de l'air humide à T_wb et w_w
        w = Air_w(h=h, T_db=T_db)       # Calculer w pour la température de bulbe sec T_db avec l'enthalpie h

    # Calcul de l'humidité absolue à partir de l'enthalpie (h) si elle est fournie
    if h is not None and T_db is not None:
        w = ((h - 1.006 * T_db) / (2501 + 1.0805 * T_db)) * 1000

    # Cas où T_db est inconnu, mais h et RH sont fournis
    if T_db is None and h is not None and RH is not None:
        tolerance = 0.1

        # Fonction à résoudre : écart entre l'enthalpie calculée et l'enthalpie fournie
        def equation(T_db):
            # Calcul de la pression de vapeur saturée Pv_sat à T_db
            Pv_sat = func_Pv_sat(T_db)

            # Calcul de l'humidité absolue w à partir de RH et T_db
            Pv = Pv_sat * (RH / 100)
            w = 0.62198 * Pv / (P - Pv) * 1000

            # Calcul de l'enthalpie à partir de w et T_db
            h_calc = 1.006 * T_db + (w * (2501 + 1.0805 * T_db)) / 1000

            # Retourne l'écart entre l'enthalpie calculée et l'enthalpie fournie
            return h_calc - h
        
        # Estimation initiale pour T_db (on peut commencer avec 20°C)
        T_db_initial_guess = 20
        
        # Utilisation de fsolve pour résoudre l'équation
        T_db_solution = fsolve(equation, T_db_initial_guess, xtol=tolerance)

        # fsolve retourne un tableau, donc il faut accéder à la première valeur
        T_db_solution = T_db_solution[0]

        # Calcul de l'humidité absolue correspondante
        Pv_sat = func_Pv_sat(T_db_solution)
        Pv = Pv_sat * (RH / 100)
        w = 0.62198 * Pv / (P - Pv) * 1000
        ################""

    return round(w,3)


# def Air_h(T_db=None, w=None, T_wb=None):
# 	if (T_db is not None and w is not None) :
# 		Enthalpie = 1.006 * T_db + (w / 1000) * (2501 + 1.0805 * T_db)
#     elif (T_db is not None and T_wb is not None) :
# 		w=Air_w(T_db=T_db, T_wb=T_wb)
# 		Enthalpie = 1.006 * T_db + (w / 1000) * (2501 + 1.0805 * T_db)
# 	else:
# 		Enthalpie=None
# 	return Enthalpie
def Air_T_wb(T_db=None, RH=None, P=101325.0,w=None,h=None):
    """
    Calcule la température de bulbe humide (T_wb) en utilisant les équations d'enthalpie et d'humidité.
    """
    if (w is not None and h is not None):
        T_db=Air_T_db(w=w,h=h)

    # if T_db is None or RH is None:
    #     raise ValueError("T_db et RH sont requis pour calculer T_wb.")

    # Humidité absolue à T_db et RH
    if w is None:
        w = Air_w(RH=RH, P=P, T_db=T_db)

    # Fonction à résoudre pour trouver T_wb
    def equation(T_wb):
        w_wb = Air_w(RH=100, P=P, T_db=T_wb)  # Humidité absolue à saturation à T_wb
        h = 1.006 * T_db + (w / 1000) * (2501 + 1.0805 * T_db)  # Enthalpie à T_db
        h_wb = 1.006 * T_wb + (w_wb / 1000) * (2501 + 1.0805 * T_wb)  # Enthalpie à T_wb
        return h - h_wb

    # Résolution numérique pour T_wb
    T_wb_initial_guess = T_db - 5  # Devine initiale pour la résolution
    T_wb_solution = fsolve(equation, T_wb_initial_guess)[0]

    return round(T_wb_solution,2)



def Air_h(T_db=None, w=None, T_wb=None, RH=None):
    # Si T_db et w sont fournis
    if RH is not None:
        w=Air_w(T_db=T_db,RH=RH)
    
    # Si T_db et T_wb sont fournis
    if T_wb is not None:
        w = Air_w(T_db=T_db, T_wb=T_wb)  
       
    if T_db is not None and w is not None:
        Enthalpie = 1.006 * T_db + (w / 1000) * (2501 + 1.0805 * T_db)
    
    # Si aucune des conditions précédentes n'est remplie
    else:
        Enthalpie = None
    
    return round(Enthalpie,3)


     
# def Air_rho_hum(T_db=None, RH=None, P=101325,T_wb=None):

# 	if RH is None and T_wb is not None:
#         Air_RH(T_db=T_db,T_wb=T_wb)
     
# 	Tk = T_db + 273.15
# 	Rv = 461
# 	Ra = 287.66
# 	Psat = func_Pv_sat(T_db)


# 	Pv = Psat * (RH / 100)
# 	rho_v = Pv / (Rv * Tk)
# 	rho_a = (P - Pv) / (Ra * Tk)

# 	Rah = Ra / (1 - ((RH / 100) * Psat / P) * (1 - Ra / Rv))

# 	rho_hum = (rho_a * Ra + rho_v * Rv) / Rah

# 	return rho_hum

def Air_rho_hum(T_db=None, RH=None, P=101325, T_wb=None,w=None,h=None):
    if (w is not None and h is not None):
        T_db=Air_T_db(w=w,h=h)
        RH=Air_RH(w=w,h=h)
    if RH is None and T_wb is not None:
        RH = Air_RH(T_db=T_db, T_wb=T_wb)  # Calculer RH si T_wb est fourni
    
    if (T_db is not None and RH is None and w is not None):
        RH=Air_RH(T_db=T_db, w=w)
    
    Tk = T_db + 273.15  # Conversion en Kelvin
    Rv = 461  # Constante des gaz pour la vapeur d'eau (J/(kg·K))
    Ra = 287.66  # Constante des gaz pour l'air sec (J/(kg·K))
    Psat = func_Pv_sat(T_db)  # Pression de vapeur saturée à T_db
    
    # Pression partielle de vapeur d'eau
    Pv = Psat * (RH / 100)
    
    # Masse volumique des constituants
    rho_v = Pv / (Rv * Tk)  # Masse volumique de la vapeur d'eau
    rho_a = (P - Pv) / (Ra * Tk)  # Masse volumique de l'air sec
    
    # Calcul de la constante des gaz pour l'air humide
    Rah = Ra / (1 - ((RH / 100) * Psat / P) * (1 - Ra / Rv))
    
    # Masse volumique de l'air humide
    rho_hum = (rho_a * Ra + rho_v * Rv) / Rah
    
    return round(rho_hum,3)



def Air_v_hum(T_db=None, RH=None, P=101325,T_wb=None,w=None,h=None):
    rho_hum=Air_rho_hum(T_db=T_db, RH=RH, P=P,T_wb=T_wb,w=w,h=h)
    v_hum=1/rho_hum
    return round(v_hum,3)





from scipy.optimize import fsolve
from math import exp, log

def Air_T_db(RH=None, w=None, h=None, Pv_sat=None, P=101325):
    if RH is not None and w is not None:
        # Calcul de T_db à partir de RH et w
        def equations(T_db):
            Pv_sat_calculated = func_Pv_sat(T_db)
            Pv = P * (w / 1000) / (0.62198 + w / 1000)
            return Pv_sat_calculated * RH / 100 - Pv

        T_db_initial_guess = 20.0
        T_db_solution = fsolve(equations, T_db_initial_guess)
        return round(T_db_solution[0],3)

    elif h is not None and w is not None:
        # Calcul de T_db à partir de h et w
        T_db_solution=(h - (w / 1000) * 2501) / (1.006 + (w / 1000) * 1.0805)
        return round(T_db_solution,2)

    elif Pv_sat is not None:
        # Calcul de T_db à partir de Pv_sat
        def inverse_Pv_sat(T_db):
            return func_Pv_sat(T_db) - Pv_sat

        T_db_initial_guess = 20.0
        T_db_solution = fsolve(inverse_Pv_sat, T_db_initial_guess)[0]
        return round(T_db_solution,3)

    else:
        raise ValueError("Insufficient parameters provided for T_db calculation")


##################""

def Tw(Td, RH) :   #calcul de la temp du bulbe humide
	Tw = Td * atan(0.151977 * (RH + 8.313659) ** (1 / 2)) + atan(Td + RH) - atan(RH - 1.676331) + 0.00391838 * (RH) ** (3 / 2) * atan(0.023101 * RH) - 4.686035
#Tw = 20 * atan(0.151977 * (50 + 8.313659) ** (1 / 2)) + atan(20 + 50) - atan(50 - 1.676331) + 0.00391838 * (50) ** (3 / 2) * atan(0.023101 * 50) - 4.686035
	return round(Tw,3)


#Wet-Bulb Temperature from Relative Humidity and Air Temperature
#ROLAND STULL
#University of British Columbia, Vancouver, British Columbia, Canada
#(Manuscript received 14 July 2011, in final form 28 August 2011)


def w(Pv_sat, RH, P):



	Pv = Pv_sat * (RH / 100)
	w= 0.62198 * Pv / (P - Pv) * 1000


	return w


def RH(Pv_sat, w, P=101325.0):
	Pv = P * (w / 1000) / ((w / 1000) + 0.62198)
	RH = (Pv / Pv_sat) * 100
	return RH


def T_sat(w_target):

	T = -100
	Erreur = Air_w(func_Pv_sat(T), 100) - w_target


	while Erreur <= 0 :
		T = T + 0.02
		Erreur = Air_w(func_Pv_sat(T), 100) - w_target



	T_sat = T

	return T_sat



def T_Humidifier(w_target, HA_init, Tinit):

	T = -100
	Erreur = -Enthalpie(Tinit, HA_init) + Enthalpie(T, w_target)

	while Erreur < 0 :
		T = T + 0.01
		Erreur = -Enthalpie(Tinit, HA_init) + Enthalpie(T, w_target)
 


	T_Humidifier = T - 0.01

	return T_Humidifier




def T_rosee(Pv):
	T = -100
	Erreur = -Pv + func_Pv_sat(T)

	while Erreur < 0 :
		T = T + 0.01
		Erreur = -Pv + func_Pv_sat(T)
  


	T_rosee = T - 0.01

	return T_rosee

from scipy.optimize import fsolve

def Air_T_dp(w=None, P=101325,T_wb=None, T_db=None, RH=None, h=None):
    """
    Calcule la température de rosée en fonction de w_target (rapport d'humidité) et P (pression atmosphérique).
    """


    if (w is None and T_wb is not None and T_db is not None):
        w=Air_w(T_wb=T_wb, T_db=T_db)
    
    if (w is None and RH is not None and T_db is not None):
        w=Air_w(RH=RH, T_db=T_db)

    if (w is None and h is not None and T_db is not None):
        w=Air_w(h=h, T_db=T_db)
    
    if (w is None and h is not None):
        w=Air_w(h=h, RH=100)
    

    # Fonction d'erreur pour trouver T où Pv_sat(T) correspond à w
    def error_function(T):
        Pv_sat = func_Pv_sat(T)
        w_calc = 0.62198 * Pv_sat / (P - Pv_sat) * 1000
        return w_calc - w

    # Résolution avec une estimation initiale
    T_initial_guess = 10.0  # Vous pouvez ajuster cela selon les besoins
    T_rosee_solution = fsolve(error_function, T_initial_guess)

    return round(T_rosee_solution[0],2)








def Enthalpie(T, w):
	Enthalpie = 1.006 * T + (w / 1000) * (2501 + 1.0805 * T)
	return Enthalpie
    
def Temperature(Enthalpie, w):
	T=(Enthalpie-(w / 1000) *2501)/(1.006+ (w / 1000) *1.0805)
    
	return T

def T_Enthalpie_Ha(Enthalpie, w):

	T_Enthalpie_Ha = (Enthalpie - (w / 1000) * 2501) / (1.006 + (w / 1000) * 1.0805)

	return T_Enthalpie_Ha



#def Temperature_Melange(m1, T1, RH1, m2, T2, RH2)

#Temperature_Melange = T_Enthalpie_Ha((Enthalpie(T1, (w(func_Pv_sat(T1), RH1))) * (m1 / (1 + (w(func_Pv_sat(T1), RH1)) / 1000)) + (Enthalpie(T2, (w(func_Pv_sat(T2), RH2)))) * (m2 / (1 + (w(func_Pv_sat(T2), RH2)) / 1000))) / ((m2 / (1 + (w(func_Pv_sat(T2), RH2)) / 1000)) + (m1 / (1 + (w(func_Pv_sat(T1), RH1)) / 1000))), 1000 * (((m2 / (1 + (w(func_Pv_sat(T2), RH2)) / 1000)) * ((w(func_Pv_sat(T2), RH2)) / 1000)) + ((m1 / (1 + (w(func_Pv_sat(T1), RH1)) / 1000)) * ((w(func_Pv_sat(T1), RH1)) / 1000))) / ((m2 / (1 + (w(func_Pv_sat(T2), RH2)) / 1000)) + (m1 / (1 + (w(func_Pv_sat(T1), RH1)) / 1000))))
#return
#def HA_Melange(m1, T1, RH1, m2, T2, RH2)

#HA_Melange = 1000 * (((m2 / (1 + (w(func_Pv_sat(T2), RH2)) / 1000)) * ((w(func_Pv_sat(T2), RH2)) / 1000)) + ((m1 / (1 + (w(func_Pv_sat(T1), RH1)) / 1000)) * ((w(func_Pv_sat(T1), RH1)) / 1000))) / ((m2 / (1 + (w(func_Pv_sat(T2), RH2)) / 1000)) + (m1 / (1 + (w(func_Pv_sat(T1), RH1)) / 1000)))
#return


#ρ_hum

def rho_ah(T, RH, P):

	Tk = T + 273.15


	Rv = 461
	Ra = 287.66
	Psat = func_Pv_sat(T)


	Pv = Psat * (RH / 100)
	rho_v = Pv / (Rv * Tk)
	rho_a = (P - Pv) / (Ra * Tk)

	Rah = Ra / (1 - ((RH / 100) * Psat / P) * (1 - Ra / Rv))

	rho_ah = (rho_a * Ra + rho_v * Rv) / Rah

	return rho_ah


