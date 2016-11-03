import linecache as ln
import xml.etree.ElementTree as ET


def extractFromXML():
    '''
    This portion of the code reads the original map file and then makes a new smaller file with only node id and way id's.
    DONE ONLY ONCE.
    '''
    xmlExtracted = open("D:/Users/rajsarka/Documents/FITSIM/resources/xmlExtracted_1.xml", "w")
    xmlExtracted.write("<?xml version=\"1.0\"?>\n")
    xmlExtracted.write("<data>")
    for i in range(7, 852060):
        line = ln.getline('D:/Users/rajsarka/Documents/FITSIM/map_1.xml', i)
        # if "<node id=" in line:
        #     line = line
        xmlExtracted.write(line + "\n")

    xmlExtracted.write("</data>")
    xmlExtracted.close()


def createMap1_Map2():
    '''
    This portion of the code parses the XML files
    '''
    way_Node_Mapping = open("D:/Users/rajsarka/Documents/FITSIM/resources/way_Node_Map", "w")
    coordList = open("D:/Users/rajsarka/Documents/FITSIM/resources/node_Coordinates", "w")
    tree = ET.parse('D:/Users/rajsarka/Documents/FITSIM/resources/xmlExtracted_1.xml')
    root = tree.getroot()
    # print root.tag

    firstLineFlag = 0
    value = str
    for way in root.findall('way'):
        if firstLineFlag == 0:
            value = way.get('id')
            firstLineFlag = 1
        else:
            value = "\n" + way.get('id')
        # print way.get('id')
        for node in way.findall('nd'):
            value += "," + node.get('ref')
        # value += "\n"
        way_Node_Mapping.write(value)
        # firstLineFlag = 1
        # count += 1
        # if(count == 5):
        #     break

    way_Node_Mapping.close()

    firstLineFlag = 0
    value = str

    for node in root.findall('node'):
        if firstLineFlag == 0:
            value = node.get('id') + "," + node.get('lat') + "," + node.get('lon')
            firstLineFlag = 1
        else:
            value = "\n" + node.get('id') + "," + node.get('lat') + "," + node.get('lon')

        coordList.write(value)
        # count += 1
        # if(count == 5):
        #     break

    coordList.close()


def createMap3():
    node_Way_Mapping = open("D:/Users/rajsarka/Documents/FITSIM/resources/node_Way_Map", "w")

    line_Coord = ln.getlines('D:/Users/rajsarka/Documents/FITSIM/resources/node_Coordinates')

    flag = 0

    for line in line_Coord:
        line_Way = ln.getlines('D:/Users/rajsarka/Documents/FITSIM/resources/way_Node_Map')
        if flag == 0:
            value = ""
            flag = 1
        else:
            value = "\n"

        node_id = line.split(",")[0]
        value += node_id

        for line_1 in line_Way:

            lineList = line_1.strip().split(",")
            if node_id in lineList:
                way_id = lineList[0]
                value += "," + way_id

            else:
                continue

        node_Way_Mapping.write(value)
