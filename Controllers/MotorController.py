import time
GPIO = None
_lstate = 0
_rstate = 0

m1_pin1 = None
m1_pin2 = None
m2_pin1 = None
m2_pin2 = None


def destroy():
    GPIO.output(m1_pin1, GPIO.LOW)
    GPIO.output(m1_pin2, GPIO.LOW)
    GPIO.output(m2_pin1, GPIO.LOW)
    GPIO.output(m2_pin2, GPIO.LOW)


def setup(config):
    global  m1_pin1, m1_pin2, m2_pin1, m2_pin2
    GPIO.setmode()
    m1_pin1 = config["m1_gpio1"]
    m1_pin2 = config["m1_gpio2"]
    m2_pin1 = config["m2_gpio1"]
    m2_pin2 = config["m2_gpio2"]

    GPIO.setup(m1_pin1, GPIO.OUT)
    GPIO.setup(m1_pin2, GPIO.OUT)
    GPIO.setup(m2_pin1, GPIO.OUT)
    GPIO.setup(m2_pin2, GPIO.OUT)

    GPIO.output(m1_pin1, GPIO.LOW)
    GPIO.output(m1_pin2, GPIO.LOW)
    GPIO.output(m2_pin1, GPIO.LOW)
    GPIO.output(m2_pin2, GPIO.LOW)
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


# Get the movement of car, is it moving forward, backward or stopped. Left/Right doesnt affect
def get_movement():
    if _lstate == 1 or _rstate == 1:
        return 1
    elif _lstate == -1 or _rstate == -1:
        return -1
    else:
        return 0


# Move/Stop the car, 1 fwd, -1 backward, 0 stop
def set_state(dir):
    if dir == 1:
        forward()
    if dir == 0:
        stop()
    if dir == -1:
        reverse()


# Act left wheel
def _lwheel_act_(dir):
    global _lstate
    _lstate= dir
    if dir == 0:
        GPIO.output(m1_pin1, GPIO.LOW)
        GPIO.output(m1_pin2, GPIO.LOW)
    elif dir == 1:
        GPIO.output(m1_pin1, GPIO.HIGH)
        GPIO.output(m1_pin2, GPIO.LOW)
    elif dir == -1:
        GPIO.output(m1_pin1, GPIO.LOW)
        GPIO.output(m1_pin2, GPIO.HIGH)


# Act right wheel
def _rwheel_act_(dir):
    global _rstate
    _rstate= dir
    if dir == 0:
        GPIO.output(m2_pin1, GPIO.LOW)
        GPIO.output(m2_pin2, GPIO.LOW)
    elif dir == 1:
        GPIO.output(m2_pin1, GPIO.HIGH)
        GPIO.output(m2_pin2, GPIO.LOW)
    elif dir == -1:
        GPIO.output(m2_pin1, GPIO.LOW)
        GPIO.output(m2_pin2, GPIO.HIGH)


# Move forward with specific time specified, else forever
def forward(arg=None):
    _lwheel_act_(1)
    _rwheel_act_(1)
    print(get_state())
    if arg is not None:
        sleep2((int(arg)))
        stop()


# Move reverse with specific time specified, else forever
def reverse(arg=None):
    _lwheel_act_(-1)
    _rwheel_act_(-1)
    print(get_state())
    if arg is not None:
        sleep2((int(arg)))
        stop()


# Turn left with specific time specified, else 3 time units. Then continue last state
def turn_left(arg=None):
    m = get_movement()
    # If car is stopped or was moving fwd, then turn in forward direction else reverse
    _rwheel_act_(1 if m >= 0 else -1)
    _lwheel_act_(0)
    print(get_state())
    if arg is not None:
        sleep2((int(arg)))
    else:
        sleep2(3)
    set_state(m)
    print(get_state())


# Turn right with specific time specified, else 3 time units. Then continue last state
def turn_right(arg=None):
    m = get_movement()
    _rwheel_act_(0)
    # If car is stopped or was moving fwd, then turn in forward direction else reverse
    _lwheel_act_(1 if m >= 0 else -1)
    print(get_state())
    if arg is not None:
        sleep2((int(arg)))
    else:
        sleep2(3)
    set_state(m)
    print(get_state())


# Turn left with specific time specified, else 3 time units. Then Stop
def reverse_left(arg=None):
    _lwheel_act_(0)
    _rwheel_act_(-1)
    print(get_state())
    if arg is not None:
        sleep2((int(arg)))
    else:
        sleep2(3)
    set_state(0)
    print(get_state())

# Turn right with specific time specified, else 3 time units. Then Stop
def reverse_right(arg=None):
    _rwheel_act_(0)
    _lwheel_act_(-1)
    print(get_state())
    if arg is not None:
        sleep2((int(arg)))
    else:
        sleep2(3)
    set_state(0)
    print(get_state())


def stop(arg=None):
    _rwheel_act_(0)
    _lwheel_act_(0)
    print(get_state())
