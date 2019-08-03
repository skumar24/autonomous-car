import time
GPIO = None
current_priority = None

MAX_DISTANCE = 220          #define the maximum measured distance
timeOut = MAX_DISTANCE*60   #calculate timeout according to the maximum measured distance
OFFSE_DUTY = 0.5        #define pulse offset of servo
SERVO_MIN_DUTY = 2 +OFFSE_DUTY     #define pulse duty cycle for minimum angle of servo
SERVO_MAX_DUTY = 11.5+OFFSE_DUTY    #define pulse duty cycle for maximum angle of servo

trigPin = None
echoPin = None
servoPin = None
servo_angle = 0


def destroy():
    global trigPin
    GPIO.output(trigPin, GPIO.LOW)
    GPIO.cleanup()


def setup(config):
    global trigPin, echoPin, p, servoPin
    print('Setting up ultrasonic sensor...')
    GPIO.setmode()  # numbers GPIOs by physical location
    trigPin = config["us_trig"]
    echoPin = config["us_echo"]
    servoPin = config["servo_pin"]

    GPIO.setup(trigPin, GPIO.OUT)  #
    GPIO.setup(echoPin, GPIO.IN)  #
    GPIO.setup(servoPin, GPIO.OUT)  # Set servoPin's mode is output
    GPIO.output(servoPin, GPIO.LOW)  # Set servoPin to low
    p = GPIO.PWM(servoPin, 50)  # set Frequece to 50Hz
    if p is not None:
        p.start(0)  # Duty Cycle = 0

def servoWrite(angle):      # make the servo rotate to specific angle (0-180 degrees)
    if(angle<0):
        angle = 0
    elif(angle > 180):
        angle = 180
    if p is not None:
        p.ChangeDutyCycle(map(angle,0,180,SERVO_MIN_DUTY,SERVO_MAX_DUTY))#map the angle to duty cycle and output it
    else:
        print("Looking in " + str(angle))


def map( value, fromLow, fromHigh, toLow, toHigh):
    return (toHigh-toLow)*(value-fromLow) / (fromHigh-fromLow) + toLow


def pulseIn(pin,level,timeOut): # function pulseIn: obtain pulse time of a pin
    t0 = time.time()
    while GPIO.inp(pin) != level:
        if (time.time() - t0) > timeOut*0.000001:
            return 0
    t0 = time.time()
    while GPIO.inp(pin) == level:
        if (time.time() - t0) > timeOut*0.000001:
            return 0
    pulseTime = (time.time() - t0)*1000000
    return pulseTime


def get_distance():
    GPIO.output(trigPin, GPIO.HIGH)  # make trigPin send 10us high level
    time.sleep(0.00001)  # 10us
    GPIO.output(trigPin, GPIO.LOW)
    pingTime = pulseIn(echoPin, GPIO.HIGH, timeOut)  # read plus time of echoPin
    distance = pingTime * 340.0 / 2.0 / 10000.0  # the sound speed is 340m/s, and calculate distance
    if distance == 0:
        return get_distance()
    else:
        return distance


def look(angle):
    servoWrite(angle)
    time.sleep(0.5)


current_dir = None
def get_direction():
    global current_dir
    dir = None
    look(90) # look forward
    DIF = get_distance()
    if DIF < 35:
        DIF = get_distance()
    print("DEBUG: DIF:", str(DIF))
    if DIF < 35 or current_dir == "reverse":
        if current_dir == "stop" or current_dir == "reverse":
            look(0)
            DIR = get_distance()
            if DIR < 35:
                DIR = get_distance()
            look(180)
            DIL = get_distance()
            if DIL < 35:
                DIL = get_distance()
            if DIR > DIL and DIR > 35:
                dir = "turnright"
            elif DIL > DIR and DIL > 35:
                dir = "turnleft"
            else:
                dir = "reverse"
        else:
            dir = "stop"
    else:
        dir = "forward"
    look(90)
    current_dir = dir
    return current_dir



def print_vars():
    global servo_angle
    print(servo_angle)