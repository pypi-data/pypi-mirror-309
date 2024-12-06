from AHU.air_humide import air_humide



class AirPort:
    def __init__(self):
        self.F=0 # air humide en kg/s
        self.F_dry=0 # air sec en kg/s
        self.P = 101325 # pression
        self.h = 10000 # enthalpie spéc
        self.w = 0 # Humidité absolue
        
    def propriete(self):
        self.result="RH,Pv_sat,T="
        self.T=air_humide.Air_T_db(h=self.h, w=self.w)
        self.Pv_sat=air_humide.Air_Pv_sat(self.T)
        self.RH=air_humide.Air_RH(Pv_sat=self.Pv_sat, w=self.w, P=self.P)
        return self.result,self.RH,self.Pv_sat,self.T
    

