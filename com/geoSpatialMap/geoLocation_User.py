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
    for line in node_coord:
        lineList = line.strip().split(",")
        if lineList[0] == node_id:
            lat = lineList[1]
            lon = lineList[2]
            return [lat, lon]
        else:
            continue


def obtainNodeId(lat, lon):
    for line in node_coord:
        lineList = line.strip().split(",")
        if lineList[1] == lat and lineList[2] == lon:
            node_id = lineList[0]
            return node_id
        else:
            continue


def obtain_Next_Way(node_id, way_id=None):
    # way_id = None since that allows selection of the same way_id possible.
    wayList = []
    for line in node_way_map:
        if line.strip().split(",")[0] == node_id:
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
    nodeList = []
    for line in way_node_map:
        if line.strip().split(",")[0] == way_id:
            nodeList = line.strip().split(",")[1:]
            break
        else:
            continue

    nodeListLength = len(nodeList)
    node_id_index = nodeList.index(node_id)

    if node_id_index == 0:
        nextNode = nodeList[node_id_index + 1]
        return nextNode
    elif node_id_index == nodeListLength - 1:
        nextNode = nodeList[node_id_index - 1]
        return nextNode
    else:
        choice = rn.choice([1, -1])
        nextNode = nodeList[node_id_index + choice]
        return nextNode


def initialize_User_Position():
    # This is give a line number corresponding to one of the way id's
    choice_of_way = rn.randint(1, len(way_node_map))
    # Get the line and string 'n' split to obtain way_id and node_id's
    way_id_list = ln.getline(WAY_NODE_PATH, choice_of_way).strip().split(",")
    way_id = way_id_list[0]
    # Choose a random node within the list specific to the chosen way_id
    if len(way_id_list) == 3:
        chosen_node_toBegin = way_id_list[rn.choice([1, 2])]
        [lat, lon] = obtainCoordinates(chosen_node_toBegin)
        # way_id = way_id_list[0]
    else:
        chosen_node_toBegin = way_id_list[rn.randint(1, len(way_id_list) - 1)]
        [lat, lon] = obtainCoordinates(chosen_node_toBegin)
        # way_id = way_id_list[0]

    return [lat, lon, chosen_node_toBegin, way_id]


def updateLocation_User(user):
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
