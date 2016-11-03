import linecache as ln
import random as rn

# These are constant paths that will be used for the geo-location for the users
NODE_COORD_PATH = 'D:/Users/rajsarka/Documents/FITSIM/resources/node_Coordinates'
WAY_NODE_PATH = 'D:/Users/rajsarka/Documents/FITSIM/resources/way_Node_Map'
NODE_WAY_PATH = 'D:/Users/rajsarka/Documents/FITSIM/resources/node_Way_Map'

node_coord = ln.getlines(NODE_COORD_PATH)
way_node_map = ln.getlines(WAY_NODE_PATH)
node_way_map = ln.getlines(NODE_WAY_PATH)


# print len(node_coord)
# print len(way_node_map)
# print len(node_way_map)

def updateSleepCount(sleep_count, category=None):
    '''
    Function updates the sleep_count per user. VERY_ACTIVE users always updates location data.
    Every other users, sends data after a time interval. Location is sent only when the sleep_count = 0.
    Once zero, the counter is simply resets.
    :param sleep_count: int: usr.user.sleep_count
    :param category: int: category of user --> Whether very_active, sedentary etc.
    :return: int: updated sleep count. If current sleep_count = 0, then reset timer.
    '''
    if category == 5:
        return 0
    else:
        if sleep_count == 0:
            if category == 4:
                return 1
            elif category == 3:
                return 2
            elif category == 2:
                return 3
            elif category == 1:
                return 4
        else:
            return sleep_count - 1


def obtainCoordinates(node_id):
    '''
    Returns latitude and longitude for given node_id
    :param node_id: str: node_id
    :return: list[str: lat, str: lon]
    '''
    for line in node_coord:
        lineList = line.strip().split(",")
        if lineList[0] == node_id:
            lat = lineList[1]
            lon = lineList[2]
            return [lat, lon]
        else:
            continue


def obtainNodeId(lat, lon):
    '''
    Returns node_id given lat and lon. NOTE: Not used yet.
    :param lat: str: latitude
    :param lon: str: longitude
    :return: str: node_id
    '''
    for line in node_coord:
        lineList = line.strip().split(",")
        if lineList[1] == lat and lineList[2] == lon:
            node_id = lineList[0]
            return node_id
        else:
            continue


def obtain_Next_Way(node_id, way_id=None):
    '''
    Chooses and returns ONE possible way_id from all possible, given the node_id. Uses reverse mapping of node_way_map.
    THE CHOICE MADE IS RANDOM.
    :param node_id: str: node_id
    :param way_id: str: OPTIONAL.
    :return: str: way_id
    '''
    # way_id = None since that allows selection of the same way_id possible.
    wayList = []
    for line in node_way_map:
        if line.strip().split(",")[0] == node_id:
            # [1:] is done since the first --> [0]th element is the way_id
            wayList = line.strip().split(",")[1:]
            break
        else:
            continue
    way_choice = wayList[rn.randint(0, len(wayList) - 1)]

    # # In case we don't want to choose the same way
    # while(way_choice == way_id):
    #     way_choice = wayList[rn.randint(0, len(wayList) - 1)]

    return way_choice


def obtain_Next_Node(way_id, node_id):
    '''
    Given a way_id AND node_id, it selects another node_id adjacent to the index of the given one.
    End-element exception is taken care of.
    :param way_id: str: way_id
    :param node_id: str: node_id
    :return: str: node_id
    '''
    nodeList = []
    for line in way_node_map:
        if line.strip().split(",")[0] == way_id:
            # [1:] is done since the first --> [0]th element is the node_id
            nodeList = line.strip().split(",")[1:]
            break
        else:
            continue

    nodeListLength = len(nodeList)
    # index() methods gives the index of an element in a list. It ranges from 0 to (len(list) - 1)
    node_id_index = nodeList.index(node_id)
    # First element correction
    if node_id_index == 0:
        nextNode = nodeList[node_id_index + 1]
        return nextNode
    # Last element correction
    elif node_id_index == nodeListLength - 1:
        nextNode = nodeList[node_id_index - 1]
        return nextNode
    else:
        choice = rn.choice([1, -1])
        nextNode = nodeList[node_id_index + choice]
        return nextNode


def initialize_User_Position():
    '''
    Initializes a user with on a specific node_id, way_id, lat and lon. Choice is made at random.
    :return: None
    '''
    # This gives a line number corresponding to one of the way id's
    choice_of_way = rn.randint(1, len(way_node_map))  # Starts at 1 since ln.getline() starts from 1
    # Get the line and strip 'n' split to obtain way_id and node_id's
    way_id_list = ln.getline(WAY_NODE_PATH, choice_of_way).strip().split(",")
    way_id = way_id_list[0]
    # Choose a random node within the list specific to the chosen way_id
    if len(way_id_list) == 3:  # In case there are only 2 possible node_id's corresponding to the way_id
        chosen_node_toBegin = way_id_list[rn.choice([1, 2])]
        [lat, lon] = obtainCoordinates(chosen_node_toBegin)
    else:
        chosen_node_toBegin = way_id_list[rn.randint(1, len(way_id_list) - 1)]  # Begin at 1 since [0] is way_id
        [lat, lon] = obtainCoordinates(chosen_node_toBegin)

    return [lat, lon, chosen_node_toBegin, way_id]


def updateLocation_User(user):
    '''
    Update the location AND sleep_count of an user.
    If sleep_count = 0 --> only then is the location updated. Else just the sleep_count is updated.
    :param user: usr.user object
    :return: None
    '''
    # lat and lon are explicitly required ONLY WHEN there is a need for interpolation
    # current_lat = user.lat
    # current_lon = user.lon
    current_sleep_count = user.sleep_count
    if current_sleep_count == 0:
        current_node_ID = user.node_id
        next_way_ID = obtain_Next_Way(current_node_ID)
        next_node_ID = obtain_Next_Node(next_way_ID, current_node_ID)
        [user.lat, user.lon] = obtainCoordinates(next_node_ID)
        user.node_id = next_node_ID
        user.way_id = next_way_ID
        user.sleep_count = updateSleepCount(current_sleep_count, category=user.category)
        return None
    else:
        user.sleep_count = updateSleepCount(current_sleep_count)
        return None
