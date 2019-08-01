import json
from Controllers import MotorController as Motor

run = False


def setup():
    with open("config.json" , "r") as f:
        config = json.load(f)
    Motor.setup(config['motor'])
    pass


# Exits the process
def destroy(arg=None):
    global run
    run = False
    print("Stopping the robot " + str(arg))
    Motor.destroy()
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
        "?" : Motor.get_state
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