from dartv2b import *
import sys
import time
import numpy as np

class Dartatouille(DartV2):
    def __init__(self):
        super().__init__()
        self.L_value = []
        self.mem_dl = 0
        self.mem_dr = 0
     
    def forward(self, speed, distance):
        delta = 2
        df,dl,db,dr = self.get_cardinal_sonars()
        print("dl : ", dl)
        print("dr : ", dr)
        if dr==99.9:
            print("Gauche")
            self.set_speed(speed-delta,speed+delta)
        elif dl==99.9:
            print("Droite")
            self.set_speed(speed+delta,speed-delta)
        elif dl-distance >= 0.02:
            print("Gauche")
            self.set_speed(speed-delta,speed+delta)
        elif dl-distance <= -0.02:
            print("Droite")
            self.set_speed(speed+delta,speed-delta)
        else:
            self.set_speed(speed,speed)
        time.sleep(0.05)
        
    def checkForward(self,distance):
        df,dl,db,dr = self.get_cardinal_sonars()
        if dl==99.9:
            self.mem_dl = 0.5
        else:
            self.mem_dl = dl
        if dr==99.9:
            self.mem_dr = 0.5
        else:
            self.mem_dr = dr
        df = self.filtre_moy_gliss_n(df) 
        wall = False
        if df <= distance:
            wall = True
        return wall
    
    #TODO : Complete with function to got to stop
    def checkForwardLine(self):
        return False
    
    def turn(self,dir):
        i = 0
        if dir=="Left":
            i = -1
        elif dir=="Right":
            i = 1
        self.set_speed(i*100,-i*100)
        time.sleep(0.05)
    
    def checkTurn(self,odo0,cnt,dir):
        if dir=="Front":
            return True
        cntOk = False
        odoMes = self.get_front_odos()[0]
        if dir=="Right":
            odoEnd = odo0 + cnt
            odoErr = odoEnd - odoMes
            if odoErr < 0:
                cntOk = True
        elif dir=="Left":
            odoEnd = odo0 - cnt
            odoErr = odoEnd - odoMes
            if odoErr > 0:
                cntOk = True
        if cntOk:
            print("Fin du tour")
            self.L_value = [1.0,1.0,1.0,1.0,1.0]
        return cntOk

    #TODO : Quand le sonar voit 99.9, on pleure
    def obstacle(self,distance,dir):
        df,dl,db,dr = self.get_cardinal_sonars()
        print("df : ", df)
        print("dl : ", dl)
        print("dr : ", dr)
        print("mem_dl : ", self.mem_dl)
        print("mem_dr : ", self.mem_dr)
        if dl == 99.9 or dl<=0:
            dl = self.mem_dl
        if dr == 99.9 or dr<=0:
            dr = self.mem_dr
        if dir=="":
            return "Front"
        elif dl >= distance and dl==max([dl,dr]):
            return "Left"
        elif dr >= distance and dr==max([dl,dr]):
            return "Right"
        else:
            print("PAAAANIK")
            
    def checkObstacle(self, dir):
        obstacleOk = False
        print('Check Obstacle')
        if dir=="Left" or dir=="Right" or dir=="Front":
            obstacleOk = True
        return obstacleOk 
        
    def stop(self):
        self.set_speed(0,0)
    
    def filtre_moy_gliss_n(self,new_value,n=5):
        if new_value <= 0 and len(self.L_value)!=0 : new_value = self.L_value[-1]
        if new_value == 99.9 and len(self.L_value)!=0 : new_value = self.L_value[-1]
        if len(self.L_value) < n :
            self.L_value.append(new_value)
        else :
            for k in range(1,len(self.L_value)):
                self.L_value[k-1]= self.L_value[k] #je décale tous les éléments vers la gauche
            self.L_value[n-1] = new_value #et j'ajoute le nouveau

        return np.mean(self.L_value)   
            

if __name__=="__main__":
    mybot = Dartatouille()
    #print ("Front encoders before : ",mybot.get_front_encoders())
    #mybot.setTurnSimple(256)
    #print ("Front encoders after : ",mybot.get_front_encoders())
    #mybot.goLineOdo(100,5)
    dmax = 1.5
    for isn in range(4):
        mybot.sonars.set_dist_max(isn+1,2.0)
    mybot.sonars.set_dist_max(5,dmax)

    # test mode 2 on 4 sonars
    print ("test mode 2 (sync)  ...")
    mode = 2
    for isn in range(4):
        mybot.sonars.set_mode(isn+1,mode)
    
    mybot.wallFollow(100,9,0.25)
    mybot.end()
    