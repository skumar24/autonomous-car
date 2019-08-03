from Controllers import MotorController as Motor
from Controllers import Sonar as Sonar
import time

GPIO = None
is_running = False


def setup(config):
    Motor.GPIO = GPIO
    Sonar.GPIO = GPIO
    Sonar.setup(config['sonar'])


def destroy():
    Motor.destroy()
    Sonar.destroy()


def start(arg=None):
    global is_running
    is_running = True
    while is_running:
        # Decide
        dir = Sonar.get_direction()
        print("Moving in direction " + dir)
        if dir == "forward" and Motor.get_state() != "Forward":
            Motor.forward()
        elif dir == "turnleft" and Motor.get_state() != "Turning Left":
            Motor.turn_left(4)
        elif dir == "turnright" and Motor.get_state() != "Turning Right":
            Motor.turn_right(4)
        elif dir == "reverse" and Motor.get_state() != "Reverse":
            Motor.reverse()
            time.sleep(2)
        elif dir == "stop":
            Motor.stop()


def stop(arg=None):
    global is_running
    is_running = False
    Motor.stop()
    
def track1(arg=None):
    Sonar.look_at_angle(int(arg))

def track3(arg=None):
    Sonar.look_at_angle(180)

def track2(arg=None):
    Sonar.look_at_angle(90)


def track4(arg=None):
    Sonar.look_at_angle(45)

def track5(arg=None):
    Sonar.look_at_angle(135)

