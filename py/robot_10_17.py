import dartv2b
import time
def goLineOdo(speed,duration):
    k1,k2=1,1
    mybot.set_speed(k1 * speed, k2 * speed)
    time.sleep(duration)

def setTurnSimple(cnt,speed):
    dt = 10e-3 #10ms
    cntOk = False
    odo_L,odo_R = mybot.get_front_odos()
    odo_L_End = odo_L + cnt
    odo_R_End = odo_R - cnt
    mybot.set_speed(speed, -speed)
    while not(cntOk):
        odo_L,odo_R = mybot.get_front_odos()
        odo_L_Err = odo_L_End-odo_L
        if odo_L_Err < 0:
            cntOk = True
            mybot.set_speed(0,0)
        else :
            time.sleep(dt)
def stop():
    mybot.set_speed(0,0)

def go_until_wall(d, last):
    while (mybot.set_sonar_0_to_99(mybot.get_cardinal_sonars()[0])+last)/2 > d:
        last = mybot.set_sonar_0_to_99(mybot.get_cardinal_sonars()[0])
        mybot.set_speed(speed,speed)

if __name__ == "__main__":

    mybot = dartv2b.DartV2()

    dmax = 1.5
    for isn in range(4):
        mybot.sonars.set_dist_max(isn + 1, 2.0)
    mybot.sonars.set_dist_max(5, dmax)

    mode = 2
    for isn in range(4):
        mybot.sonars.set_mode(isn + 1, mode)

    speed = 100
    print(mybot.set_sonar_0_to_99(mybot.get_cardinal_sonars()[0]))
    last = 0
    while True:
        go_until_wall(0.3,last)
        mybot.set_speed(0,0)
        time.sleep(1)
        setTurnSimple(250,100) #si cnt = 256 --> tourne de pi/2



    mybot.end()  # clean end of the robot mission

