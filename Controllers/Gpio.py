import random
GPIO = None

try:
    import RPi.GPIO as GPIO
except ImportError:
    pass

OUT = None
HIGH = None
LOW = None
IN = None


def _init_():
    global OUT,HIGH,LOW,IN

    if GPIO is not None:
        OUT = GPIO.OUT
        HIGH = GPIO.HIGH
        LOW = GPIO.LOW
        IN = GPIO.IN
    else:
        OUT = "OUT"
        HIGH = "HIGH"
        LOW = "LOW"
        IN = "IN"


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
        print("GPIO output " + str(pin) + ":" + o)


def inp(pin):
    if GPIO is not None:
        return GPIO.input(pin)
    else:
        return "LOW" if random.uniform(0, 1) == 0 else "HIGH"

def PWM(pin, freq):
    if GPIO is not None:
        return GPIO.PWM(pin, freq)
    else:
        print("GPIO PWM")
        return None


def cleanup():
    if GPIO is not None:
        GPIO.cleanup()
    else:
        print("GPIO Cleanup")

_init_()