import linecache as ln


'''
This portion of the code just takes all the possible coordinates in the map point limits selected
and writes it in a file for use.
'''
xmlExtracted = open("D:/Users/rajsarka/Documents/FITSIM/resources/xmlExtracted.xml", "w")
for i in range(8, 295382):
    line = ln.getline('D:/Users/rajsarka/Documents/FITSIM/map', i).strip()
    if "<node id=" in line:
        line = line
        xmlExtracted.write(line + "\n")

xmlExtracted.close()

xmlExtracted = open("D:/Users/rajsarka/Documents/FITSIM/resources/xmlExtracted.xml","r")
coordList = open("D:/Users/rajsarka/Documents/FITSIM/resources/node_Coordinates.csv","w+")
count = 0
for line in xmlExtracted.readlines():
    if count == 0:
        lineElemList = line.split(" ")
        tempNodeId_1 = lineElemList[0].lstrip("<")
        # print tempNodeId_1
        tempNodeId_2 = lineElemList[1]
        node_id = tempNodeId_1 + "_" + tempNodeId_2
        latitude = lineElemList[2]
        longitude = lineElemList[3]
        finalLine = node_id + "," + latitude + "," + longitude
        coordList.write(finalLine)
        count = 1
        continue


    lineElemList = line.split(" ")
    tempNodeId_1 = lineElemList[0].lstrip("<")
    # print tempNodeId_1
    tempNodeId_2 = lineElemList[1]
    node_id =  tempNodeId_1 + "_" + tempNodeId_2
    latitude = lineElemList[2]
    longitude = lineElemList[3]
    finalLine = "\n" + node_id + "," + latitude + "," + longitude
    coordList.write(finalLine)

xmlExtracted.close()
coordList.close()