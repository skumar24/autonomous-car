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
    time.sleep(0.001)
    pass


def look_left():
    global servo_angle
    # if servo_angle == 180:
    #     print("Servo 180, already on left")
    #     return
    for i in range(0, 181, 1):
        look(i)
    time.sleep(0.05)
    servo_angle = 180


def look_right():
    global servo_angle
    # if servo_angle == 0:
    #     print("Servo 0, already on right")
    #     return
    for i in range(180, -1, -1):
        look(i)
    time.sleep(0.05)
    servo_angle = 0


# def look_forward():
#     global servo_angle
#     if servo_angle == 80:
#         return
#     if servo_angle == 180:
#         for i in range(180, 111, -1):
#             look(i)
#     else:
#         for i in range(0, 49, 1):
#             look(i)
#     servo_angle = 80



def get_path_data():
    path_data = []
    global servo_angle
    if servo_angle == 0:
        print("Getting path data from right to left")
        for i in range(0, 181, 1):
            look(i)
            # time.sleep(0.01)
            path_data.append((i, get_distance()))
            servo_angle = 180
    elif servo_angle == 180:
        print("Getting path data from left to right")
        for i in range(180, 0, -1):
            look(i)
            # time.sleep(0.01)
            path_data.append((i, get_distance()))
            servo_angle = 0
    return path_data


def get_distance_infront(pathdata): # special function to find out distance in front after looking on front sides as well
    pd = [d for d in pathdata if 70 < d[0] < 90]

    min_dir = min(pd, key=lambda x: x[1])
    min_dist = min_dir[1]
    return min_dist



def get_dir_by_pathdata(pathdata, onlyturn = False):
    if onlyturn:
        pathdata = [d for d in pathdata if 0 <= d[0] <= 50 or 130 <= d[0] <= 180]
    max_dir = max(pathdata, key=lambda x: x[1])
    min_dir = min(pathdata, key=lambda x: x[1])
    min_dist = min_dir[1]
    max_dist = max_dir[1]
    if not onlyturn:
        if max_dist <= 15:
            return "reverse"
        elif max_dir[0] <= 80:
            if min_dist <=20:
                return "turnright_quick"
            else:
                return "turnright"
        elif max_dir[0] >= 140:
            if min_dist <= 20:
                return "turnleft_quick"
            else:
                return "turnleft"
        else:
            return "forward"
    else: # Only in case of reverse, look for left and right to find space to turn
        if max_dist <= 15:
            return "reverse"
        elif max_dir[0] <= 80:
            if min_dist <= 20:
                return "turnleft_quick"
            else:
                return "turnleft"
        elif max_dir[0] >=100:
            if min_dist <=20:
                return "turnright_quick"
            else:
                return "turnright"






def get_path_priority(curr_movement):
    global current_priority
    path_priority = None
    get_from_pd = True
    is_turning = current_priority == "turnleft" or current_priority == "turnright" or current_priority == "turnleft_quick" or current_priority == "turnright_quick"
    path_data = get_path_data()
    d = get_distance_infront(path_data)
    print("Distance in front: " + str(d))
    if d < 12:
        path_priority = "reverse"
    if d < 20 and (current_priority == "forward" or current_priority is None):
        path_priority = "reverse"

    if path_priority is None and current_priority is None: # Move forward if it begins and there is space
        path_priority = "forward"

    if path_priority is None and curr_movement >= 0: # If movement is forward
        if current_priority == "forward":
            # Just look forward
            if d < 40: # If distance in fwd is < 40, start looking for options
                get_from_pd = True
            else:
                path_priority = current_priority
                get_from_pd = False
        elif is_turning:
            get_from_pd = False
            if d < 40:
                path_priority = current_priority
            else:
                #time.sleep(2)
                path_priority = "forward"

        if get_from_pd:
            # look_forward()
            path_priority = get_dir_by_pathdata(path_data)
    elif path_priority is None: # If movement is reverse
        if is_turning:
            get_from_pd = False
            if d < 40:
                path_priority = current_priority
            else:
                #time.sleep(2)
                path_priority = "forward"
        if get_from_pd:
            # look_forward()
            path_priority = get_dir_by_pathdata(path_data, True)
    print("Path priority: " + str(path_priority) + " (Prev: " + str(current_priority) + ")")
    current_priority = path_priority
    return path_priority


def print_vars():
    global servo_angle
    print(servo_angle)