import dartv2b
import time

if __name__ == "__main__":
    mybot = dartv2b.DartV2()

    # place your work here
    print ("Encoder Microcode Version : ",mybot.encoders.get_version())
    print ("Rear encoders before : ",mybot.get_rear_odos())

    for ileg in range(2):
        mybot.set_speed (100, 100)
        for i in range(10):
            print ("Rear encoders [L,R]",mybot.get_rear_odos())
            time.sleep(0.5)
        mybot.set_speed (100, -100)
        time.sleep(1.33) # empirical !! may change with cpu !!! 
        mybot.set_speed (0,0)

    odo_left,odo_right = mybot.get_rear_odos()
    
    print ("Rear encoders after : ",[odo_left,odo_right])
    deltaOdoLeft = mybot.delta_rear_odometers(side="left")
    deltaOdoRight = mybot.delta_rear_odometers(side="right")
    print ("Delta odometer left :", deltaOdoLeft)
    print ("Delta odometer right :", deltaOdoRight)
    print ("Delta odometers :",mybot.delta_rear_odometers())
    
    print ("Battery Voltage : %.2f V"%(mybot.encoders.battery_voltage()))
    
    mybot.end() # clean end of the robot mission

