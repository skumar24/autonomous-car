import json
from Controllers import Gpio as GPIO
from Controllers import MotorController as Motor

from Controllers import  Robot as Robot

Motor.GPIO = GPIO
Robot.GPIO = GPIO

run = False


def setup():
    with open("config.json" , "r") as f:
        config = json.load(f)
    Motor.setup(config['motor'])
    Robot.setup(config)
    pass


def test(arg=None):
    Robot.test()

# Exits the process
def destroy(arg=None):
    global run
    run = False
    print("Stopping the robot " + str(arg))
    Motor.destroy()
    Robot.destroy()
    GPIO.cleanup()
    print("Robot stopped")


# Invalid choice and usage helper
def invalid_choice(arg=None):
    print("Invalid choice made")


# Input handler
def switcher(choice_args):
    choice = choice_args[0];
    arg = None
    print(choice)
    if len(choice_args) > 1:
        arg= choice_args[1]

    sw = {
        "w" : Motor.forward,
        "a" : Motor.turn_left,
        "s" : Motor.stop,
        "d" : Motor.turn_right,
        "x" : Motor.reverse,
        "exit" : destroy,
        "?" : Motor.get_state,
        "start" : Robot.start,
        "stop" : Robot.stop,
        "1" : Robot.track1,
        "2": Robot.track2,
        "3": Robot.track3,
        "4" : Robot.track4,
        "5": Robot.track5
    }
    func = sw.get(choice, invalid_choice)
    res = func(arg)
    if res is not None:
        print(func(arg))


# Constant loop to make choice and execute
def loop():
    global run
    run = True
    while run:
        choice = input("> ")
        choice = choice.lower().split(" ")
        switcher(choice)


# Entry point
if __name__ == '__main__':
    print ('Robot starting ... ')
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()