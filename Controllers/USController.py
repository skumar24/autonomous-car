import time
GPIO = None
current_priority = None

MAX_DISTANCE = 220          #define the maximum measured distance
timeOut = MAX_DISTANCE*60   #calculate timeout according to the maximum measured distance
OFFSE_DUTY = 0.5        #define pulse offset of servo
SERVO_MIN_DUTY = 2.5+OFFSE_DUTY     #define pulse duty cycle for minimum angle of servo
SERVO_MAX_DUTY = 12.5+OFFSE_DUTY    #define pulse duty cycle for maximum angle of servo

trigPin = None
echoPin = None
servoPin = None

def destroy():
    global trigPin
    GPIO.output(trigPin, GPIO.LOW)
    GPIO.cleanup()


def setup(config):
    global trigPin, echoPin, p, servoPin
    print('Settiung up ultrasonic sensor...')
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
    return distance


def look(angle):
    servoWrite(angle)
    pass

def look_left():
    look(180)
    pass

def look_right():
    look(0)
    pass

def look_forward():
    look(80)
    pass


def track1():
    for i in range(0, 181, 1):
        look(i)
        time.sleep(0.001)


def track2():
    for i in range(180, -1, -1):
        look(i)
        time.sleep(0.001)

def get_dir_by_pathdata(pathdata, onlyturn = False):
    if onlyturn:
        pathdata = [p for p in pathdata if 0 <= p[0] <= 50 or 130 <= p[0] <= 180]
    max_dir = max(pathdata, key=lambda x: x[1])
    max_dist = max_dir[1]
    if not onlyturn:
        if max_dist <= 10:
            return "reverse"
        elif max_dir <= 80:
            return "turnright"
        elif max_dir >= 100:
            return "turnleft"
        else:
            return "forward"
    else: # Only in case of reverse, look for left and right to find space to turn
        if max_dist <=8:
            return "reverse"
        elif max_dir <= 80:
            return "turnleft"
        elif max_dir >=100:
            return "turnright"


def get_path_priority(curr_movement):
    global current_priority
    check_all = True
    path_data = []
    is_turning = current_priority == "turnleft" or current_priority == "turnright"
    if curr_movement >= 0:
        look_forward()
        d = get_distance()

        if current_priority == "forward":
            # Just look forward
            if d < 25:
                check_all = True
            else:
                path_priority = current_priority
                check_all = False
        elif is_turning:
            check_all = False
            if d < 25:
                path_priority = current_priority
            else:
                path_priority = "forward"

        if check_all:
            look_right()
            for i in range(0, 180, 10):
                look(i)
                path_data.append((i, get_distance()));
            look_forward()
            path_priority = get_dir_by_pathdata(path_data)
    else:
        look_forward()
        d = get_distance()
        if is_turning:
            check_all = False
            if d < 25:
                path_priority = current_priority
            else:
                path_priority = "forward"
        if check_all:
            look_right()
            for i in range(0, 181, 10):
                look(i)
                path_data.append((i, get_distance()));
            look_forward()
            path_priority = get_dir_by_pathdata(path_data, True)
    current_priority = path_priority
    return path_priority
