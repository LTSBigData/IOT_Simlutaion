import linecache as ln
import os
import random as rn
from os import path

project_dir = path.dirname(path.dirname(os.getcwd()))

# These are constant paths that will be used for the geo-location for the users
NODE_COORD_PATH = project_dir + '/resources/node_Coordinates'
WAY_NODE_PATH = project_dir + '/resources/way_Node_Map'
NODE_WAY_PATH = project_dir + '/resources/node_Way_Map'

# Creating dictionaries for the ease of indexing
node_coord = ln.getlines(NODE_COORD_PATH)
node_coord = {int(node_coord[i].strip().split(",")[0]): node_coord[i].strip().split(",")[1:]
              for i in range(len(node_coord))}

way_node_map = ln.getlines(WAY_NODE_PATH)
way_node_map = {int(way_node_map[i].strip().split(",")[0]): map(int, way_node_map[i].strip().split(",")[1:])
                for i in range(len(way_node_map))}

node_way_map = ln.getlines(NODE_WAY_PATH)
node_way_map = {int(node_way_map[i].strip().split(",")[0]): map(int, node_way_map[i].strip().split(",")[1:])
                for i in range(len(node_way_map))}


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
    :param node_id: int: node_id
    :return: list[str: lat, str: lon]
    '''
    return node_coord[node_id]


def obtain_Next_Way(node_id, way_id=None):
    '''
    Chooses and returns ONE possible way_id from all possible, given the node_id. Uses reverse mapping of node_way_map.
    THE CHOICE MADE IS RANDOM.
    :param node_id: str: node_id
    :param way_id: str: OPTIONAL.
    :return: str: way_id
    '''
    wayList = node_way_map[node_id]
    way_choice = wayList[rn.randint(0, len(wayList) - 1)]

    # # In case we don't want to choose the same way
    # while(way_choice == way_id):
    #     way_choice = wayList[rn.randint(0, len(wayList) - 1)]

    return way_choice


def obtain_Next_Node(way_id, node_id):
    '''
    Given a way_id AND node_id, it selects another node_id adjacent to the index of the given one.
    End-element exception is taken care of.
    :param way_id: int: way_id
    :param node_id: int: node_id
    :return: int: node_id
    '''
    nodeList = way_node_map[way_id]
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
        choice = rn.choice([1, -1])  # 1 or -1 makes sure that only a single 'step' is taken
        nextNode = nodeList[node_id_index + choice]
        return nextNode


def initialize_User_Position():
    '''
    Initializes a user with on a specific node_id, way_id, lat and lon. Choice is made at random.
    :return: None
    '''
    # Choose a random 'way_id' to start from
    choice_of_way = rn.choice(way_node_map.keys())
    # Obtain the 'node_id's for 'way_id'
    way_id_list = way_node_map[choice_of_way]

    # Choose a random node within the list specific to the chosen way_id

    if len(way_id_list) == 1:  # In case there is only 1 possible node_id corresponding to the way_id
        chosen_node_toBegin = way_id_list[0]
        [lat, lon] = obtainCoordinates(chosen_node_toBegin)
    else:
        chosen_node_toBegin = way_id_list[rn.randint(0, len(way_id_list) - 1)]  # len() - 1 --> since it is inclusive
        [lat, lon] = obtainCoordinates(chosen_node_toBegin)

    return [lat, lon, chosen_node_toBegin, choice_of_way]


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
    else:
        user.sleep_count = updateSleepCount(current_sleep_count)
