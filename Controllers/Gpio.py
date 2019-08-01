GPIO = None
try:
    import RPi.GPIO as GPIO
except ImportError:
    pass


OUT = None
HIGH = None
LOW = None

def _init_():
    global OUT
    global HIGH
    global LOW
    if GPIO is not None:
        OUT = GPIO.OUT
        HIGH = GPIO.HIGH
        LOW = GPIO.LOW
    else:
        OUT = "OUT"
        HIGH = "HIGH"
        LOW = "LOW"


def setmode():
    if GPIO is not None:
        GPIO.setmode(GPIO.BOARD)
    else:
        print("GPIO Setmode Board")


def setup(pin, type):
    if GPIO is not None:
        GPIO.setup(pin, type)
    else:
        print("GPIO Setup " + str(pin) + ":" + type)


def output(pin, o):
    if GPIO is not None:
        GPIO.output(pin, o)
    else:
        print("GPIO output " + str(pin) + ":" +  o)


def cleanup():
    if GPIO is not None:
        GPIO.cleanup()
    else:
        print("GPIO Cleanup")

_init_()