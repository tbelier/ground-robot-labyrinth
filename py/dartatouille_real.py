from dartv2b import *
import sys
import time
import numpy as np


def sawtooth(x):
	return (x+180)%(2*180)-180


class Dartatouille(DartV2):
    def __init__(self):
        super().__init__()
        self.L_value = []
        self.mem_dl = 0
        self.mem_dr = 0
        self.imu = Imu9IO()
        self.cnt_vir = 0
        self.capEnd = 0
        self.currentcap = 0
        self.currentcap_ind = 0
        self.listcap = [] #F,+90,backwards,-90
        
    def init_Cap(self):
        magraw = self.imu.read_mag_raw()
        self.listcap.append(self.imu.heading_deg(magraw[0],magraw[1]))
        self.listcap.append((self.listcap[0] + 90)%360)
        self.listcap.append((self.listcap[1] + 90)%360)
        self.listcap.append((self.listcap[2] + 90)%360)
        print("j'ai bien initialise mon cap ^^ uwu <3")
        self.currentcap = self.listcap[0]
        
    def new_f(self,speed):
        dt = 0.15
        df,dl,db,dr = self.get_cardinal_sonars()  
        if dl >= 99.9 or dl <= 0: dl = self.mem_dl
        if dr >= 99.9 or dr <= 0: dr = self.mem_dr
        kp = 85
        kd = -10
        if dl > 0.3 :
            spd = kp*(0.35-dr) + kd*(dr-self.mem_dr)/dt 
        elif dr > 0.3 :
            spd = -kp*(0.35-dl) - kd*(dl-self.mem_dl)/dt
        else :
            spd = kp*(dl-dr)/2 + kd*(dl-self.mem_dl)/dt 
        self.set_speed(speed - spd, speed + spd)   
        time.sleep(dt)
        
    def checkForward(self,distance):
        df,dl,db,dr = self.get_cardinal_sonars()
        if dl>=99.9:
            self.mem_dl = 0.5
        else:
            self.mem_dl = dl
        if dr>=99.9:
            self.mem_dr = 0.5
        else:
            self.mem_dr = dr
        df = self.filtre_moy_gliss_n(df)
        wall = False
        if df <= distance:
            wall = True
        return wall
    
    def checkForwardLine(self):
        return False
    
    def turn(self,dir):
        i = 0
        a = 1.5
        magraw = self.imu.read_mag_raw()
        capMes = self.imu.heading_deg(magraw[0],magraw[1])
        deltaspeed = a*abs(sawtooth(self.currentcap - capMes))
        if dir=="Left":
            i = -1
        elif dir=="Right":
            i = 1
        if deltaspeed <= 70:
            self.set_speed(i*70,-i*70)
        else :
            self.set_speed(i*(deltaspeed),-i*(deltaspeed))
        time.sleep(0.1)
            
    def checkTurn(self,dir):
        if dir=="Front":
            return True
        capOk = False
        magraw = self.imu.read_mag_raw()
        capMes = self.imu.heading_deg(magraw[0],magraw[1])
        if dir=="Right":
            capErr = sawtooth(self.currentcap - capMes)
            if abs(capErr) < 10:
                capOk = True
        elif dir=="Left":
            capErr = sawtooth(self.currentcap - capMes)
            if abs(capErr) < 10:
                capOk = True
        if capOk:
            self.L_value = [1.0,1.0,1.0,1.0,1.0]
        return capOk

    def obstacle(self,distance,dir):
        df,dl,db,dr = self.get_cardinal_sonars()
        if dl >= 99.9 or dl<=0:
            dl = self.mem_dl
        if dr >= 99.9 or dr<=0:
            dr = self.mem_dr
        
        if dir=="":
            return "Front"
        if df >= 0.45:
            return "Front"
        
        if dl <= 0.3 and dr <= 0.3:
            time.sleep(0.2)
            return "Restart"
        elif dl >= distance and dl==max([dl,dr]):
            self.cnt_vir += 1
            return "Left"
        elif dr >= distance and dr==max([dl,dr]):
            self.cnt_vir -= 1 
            return "Right"
        else:
            time.sleep(0.2)
            return "Restart"
    
    def checkObstacle(self, dir):
        obstacleOk = False
        if dir=="Left" or dir=="Right" or dir=="Front":
            obstacleOk = True
        return obstacleOk 
        
    def stop(self):
        self.set_speed(0,0)
    
    def update_CapEnd(self, cap_initial, deltacap, dir):
        i=0
        if dir=="Left":
            i = 1
        elif dir=="Right":
            i = -1
        self.capEnd = (cap_initial + i*deltacap)%360
    
    def update_currentcap(self,dir):
        if dir == 'Left':
            self.currentcap_ind += 1
        elif dir == 'Right' :
            self.currentcap_ind -= 1
        self.currentcap_ind %= 4
        self.currentcap = self.listcap[self.currentcap_ind]
        
    def filtre_moy_gliss_n(self,new_value,n=5):
        if new_value <= 0 and len(self.L_value)!=0 : new_value = self.L_value[-1]
        if new_value >= 99.9 and len(self.L_value)!=0 : new_value = self.L_value[-1]
        if len(self.L_value) < n :
            self.L_value.append(new_value)
        else :
            for k in range(1,len(self.L_value)):
                self.L_value[k-1]= self.L_value[k] #je décale tous les éléments vers la gauche
            self.L_value[n-1] = new_value #et j'ajoute le nouveau
        return np.mean(self.L_value)   
        

if __name__=="__main__":
    mybot = Dartatouille()
    dmax = 1.5
    for isn in range(4):
        mybot.sonars.set_dist_max(isn+1,2.0)
    mybot.sonars.set_dist_max(5,dmax)

    # test mode 2 on 4 sonars
    print ("test mode 2 (sync)  ...")
    mode = 2
    for isn in range(4):
        mybot.sonars.set_mode(isn+1,mode)
    mybot.sonars.set_mode(1,1)
    mybot.sonars.set_mode(2,0)
    
    mybot.wallFollow(100,9,0.25)
    mybot.end()
    