# import RPi.GPIO as GPIO
import time
_lstate = 0
_rstate = 0

m1_pin1 = None
m1_pin2 = None
m2_pin1 = None
m2_pin2 = None


def destroy():
    GPIO.cleanup()


def setup(config):
    global  m1_pin1, m1_pin2, m2_pin1, m2_pin2

    # GPIO.setmode(GPIO.BOARD)
    m1_pin1 = config["m1_gpio1"]
    m1_pin2 = config["m1_gpio2"]
    m2_pin1 = config["m2_gpio1"]
    m2_pin2 = config["m2_gpio2"]

    # GPIO.setup(m1_pin1, GPIO.OUT)
    # GPIO.setup(m1_pin2, GPIO.OUT)
    # GPIO.setup(m2_pin1, GPIO.OUT)
    # GPIO.setup(m2_pin2, GPIO.OUT)
    #
    # GPIO.output(m1_pin1, GPIO.LOW)
    # GPIO.output(m1_pin2, GPIO.LOW)
    # GPIO.output(m2_pin1, GPIO.LOW)
    # GPIO.output(m2_pin2, GPIO.LOW)
    _lstate = 0
    _rstate = 0
    print('''Setting up the motor
    motor 1: ''' + str(m1_pin1) + "," + str(m1_pin2))
    print("motor 2: " + str(m2_pin1) + "," + str(m2_pin2))


def sleep2(t):
    time.sleep(t/5)


def get_state(arg = None):
    if _lstate == 1 and _rstate == 1:
        return "Forward"
    elif _lstate == 0 and _rstate == 0:
        return "Stopped"
    elif _lstate == 0 and _rstate == 1:
        return "Turning left"
    elif _rstate == 0 and _lstate == 1:
        return "Turning right"
    elif _lstate == -1 and _rstate == -1:
        return "Reverse"
    else:
        return "NA"


def get_movement():
    if _lstate == 1 or _rstate == 1:
        return 1
    elif _lstate == -1 or _rstate == -1:
        return -1
    else:
        return 0


def set_state(dir):
    if dir == 1:
        forward()
    if dir == 0:
        stop()
    if dir == -1:
        reverse()


def _lwheel_act_(dir):
    global _lstate
    _lstate= dir
    # if dir == 0:
    #     GPIO.output(m1_pin1, GPIO.LOW)
    #     GPIO.output(m1_pin2, GPIO.LOW)
    # elif dir == 1:
    #     GPIO.output(m1_pin1, GPIO.HIGH)
    #     GPIO.output(m1_pin2, GPIO.LOW)
    # elif dir == -1:
    #     GPIO.output(m1_pin1, GPIO.LOW)
    #     GPIO.output(m1_pin2, GPIO.HIGH)


def _rwheel_act_(dir):
    global _rstate
    _rstate= dir
    # if dir == 0:
    #     GPIO.output(m2_pin1, GPIO.LOW)
    #     GPIO.output(m2_pin2, GPIO.LOW)
    # elif dir == 1:
    #     GPIO.output(m2_pin1, GPIO.HIGH)
    #     GPIO.output(m2_pin2, GPIO.LOW)
    # elif dir == -1:
    #     GPIO.output(m2_pin1, GPIO.LOW)
    #     GPIO.output(m2_pin2, GPIO.HIGH)


def forward(arg=None):
    _lwheel_act_(1)
    _rwheel_act_(1)
    print(get_state())
    if arg is not None:
        sleep2((int(arg)))
        stop()


def reverse(arg=None):
    _lwheel_act_(-1)
    _rwheel_act_(-1)
    print(get_state())
    if arg is not None:
        sleep2((int(arg)))
        stop()


def turn_left(arg=None):
    m = get_movement()
    _rwheel_act_(1)
    _lwheel_act_(0)
    print(get_state())
    if arg is not None:
        sleep2((int(arg)))
    else:
        sleep2(3)
    set_state(m)
    print(get_state())


def turn_right(arg=None):
    m = get_movement()
    _rwheel_act_(0)
    _lwheel_act_(1)
    print(get_state())
    if arg is not None:
        sleep2((int(arg)))
    else:
        sleep2(3)
    set_state(m)
    print(get_state())


def reverse_left(arg=None):
    _lwheel_act_(0)
    _rwheel_act_(-1)


def reverse_right(arg=None):
    _rwheel_act_(0)
    _lwheel_act_(-1)


def stop(arg=None):
    _rwheel_act_(0)
    _lwheel_act_(0)
    print(get_state())
