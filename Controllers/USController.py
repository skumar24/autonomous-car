GPIO = None
current_priority = None

def destroy():
    pass;

def setup(config):
    pass;


def look(angle):
    pass

def look_left():
    look(180)
    pass

def look_right():
    look(0)
    pass

def look_forward():
    look(90)
    pass


def get_distance():
    return 0

def get_dir_by_pathdata(pathdata, onlyturn = False):
    if onlyturn:
        pathdata = [p for p in pathdata if 0 <= p[0] <= 50 or 130 <= p[0] <= 180]
    max_dir = max(pathdata, key=lambda x: x[1])
    max_dist = max_dir[1]
    if max_dist < 10:
        return "reverse"
    elif max_dir <= 80:
        return "turnright"
    elif max_dir >= 100:
        return "turnleft"
    else:
        return "forward"


def get_path_priority(curr_movement):
    global current_priority
    check_all = True
    path_data = []

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

        if check_all:
            look_right()
            for i in range(0, 180, 10):
                look(i)
                path_data.append((i, get_distance()));
            look_forward()
            path_priority = get_dir_by_pathdata(path_data)
    else:
        look_right()
        for i in range(0, 180, 10):
            look(i)
            path_data.append((i, get_distance()));
        look_forward()
        path_priority = get_dir_by_pathdata(path_data, True)
    current_priority = path_priority
    return  path_priority
