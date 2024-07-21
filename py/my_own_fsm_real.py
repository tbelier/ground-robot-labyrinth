import fsm
import time
import sys
import dartatouille_real


# global variables
f = fsm.fsm();  # finite state machine

# create a robot (to be replaced by dartv2)
myBot = dartatouille_real.Dartatouille()

dmax = 1.5
for isn in range(4):
	myBot.sonars.set_dist_max(isn+1,2.0)
myBot.sonars.set_dist_max(5,dmax)

# test mode 2 on 4 sonars
print ("test mode 2 (sync)  ...")
mode = 2
for isn in range(4):
	myBot.sonars.set_mode(isn+1,mode)
 
myBot.imu.fast_heading_calibration(1867, 4415, -5805, -3377)

time_start = time.time()
time_begin = 1.0 # wait 5 s before turning at the beginning
odo0 = myBot.get_front_odos()[0]
magx0,magy0 = myBot.imu.read_mag_raw()[0],myBot.imu.read_mag_raw()[1]
cap0 = myBot.imu.heading_deg(magx0,magy0)
cap_initial= myBot.imu.heading_deg(magx0,magy0)
cnt = 180
deltacap = 90
dir = ""


# functions (actions of the fsm)
def doWait():
	print("J'attends")
	global time_start,time_begin
	#si j'ai attendu 2 secondes je pars
	if time.time() > time_start+time_begin: # auto start in 5 seconds
		myBot.init_Cap()
		event="endWait"
	else:
		event="wait"
	return event


def doTurn(): 
	global dir, deltacap  #cap_initial
	print("Je tourne")
	myBot.turn(dir)
	if myBot.checkTurn(dir):
		event = "endTurn"
	else:
		event = "stayRot"
	return event

def doObstacle():
	global dir, cap0
	print("Je vois un obstacle")
	dir = myBot.obstacle(0.25,dir)
	print(dir)
	if myBot.checkObstacle(dir):
		magraw = myBot.imu.read_mag_raw()
		cap0 = myBot.imu.heading_deg(magraw[0],magraw[1])
		myBot.update_CapEnd(cap0, deltacap, dir)
		myBot.update_currentcap(dir)
		event = "endObstacle"
		
	else:
		event = "stayObstacle"
	return event

def doForward():
	print("Je vais tout droit")
	myBot.new_f(50)
	if myBot.checkForward(0.5):
		event = "endFollowWall"
		myBot.stop()
		time.sleep(1)
	elif myBot.checkForwardLine():
		event = "end"
	else:
		event = "staySM"
	return event

def doStop():
	myBot.stop()
	print ("I stop myself!")
	event=None
	return event

if __name__== "__main__":
	
	# define the states
	f.add_state("Idle")
	f.add_state("Obstacle")
	f.add_state("Rot")
	f.add_state("FollowWall")
	f.add_state("Stop")

	# defines the events
	f.add_event("wait")
	f.add_event("stayRot")
	f.add_event("staySM")
	f.add_event("stayObstacle")

	f.add_event("endWait")
	f.add_event("endTurn")
	f.add_event("endObstacle")
	f.add_event("endFollowWall")
	f.add_event("end")

	# defines the transition matrix
	# current state, next state, event, action in next state
	f.add_transition ("Idle","Idle","wait",doWait)
	f.add_transition("Rot", "Rot", "stayRot", doTurn)
	f.add_transition("Obstacle", "Obstacle", "stayObstacle", doObstacle)
	f.add_transition("FollowWall", "FollowWall", "staySM", doForward)

	f.add_transition ("Idle","Obstacle","endWait",doObstacle)
	f.add_transition ("Rot","FollowWall","endTurn",doForward)
	f.add_transition ("FollowWall","Obstacle","endFollowWall",doObstacle)
	f.add_transition ("Obstacle","Rot","endObstacle",doTurn)
	f.add_transition ("FollowWall","Stop","end",doStop)



	# initial state
	f.set_state ("Idle")
	# first event
	f.set_event ("wait")
	# end state
	f.set_end_state ("Stop")

 
	# fsm loop
	run = True   
	while (run):
		funct = f.run () # function to be executed in the new state
		if f.curState != f.endState:
			newEvent = funct() # new event when state action is finished
			print ("New Event : ",newEvent)
			f.set_event(newEvent) # set new event for next transition
		else:
			funct()
			run = False
			
	print ("End of the programm")

