from Controllers import MotorController as Motor
from Controllers import USController as Sonar


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
        dir = Sonar.get_path_priority(Motor.get_movement())
        if dir == "forward" and Motor.get_state() != "Forward":
            Motor.forward()
        elif dir == "turnleft" and Motor.get_state() != "Turning Left":
            Motor.turn_left(1)
        elif dir == "turnright" and Motor.get_state() != "Turning Right":
            Motor.turn_right(1)
        elif dir == "reverse" and Motor.get_state() != "Reverse":
            Motor.reverse()


def stop(arg=None):
    global is_running
    is_running = False
    Motor.stop()