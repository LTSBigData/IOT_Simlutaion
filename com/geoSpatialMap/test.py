import linecache as ln

line_Way = ln.getlines('D:/Users/rajsarka/Documents/FITSIM/resources/way_Node_Map')
count_2 = 0
#
# for line_1 in line_Way:
#     count_2 += 1
#     lineList = line_1.split(",")
#     if '25457973' in lineList:
#         print count_2
#         print line_1
#         # count_2 = 0
#     else:
#         continue

line_1 = ln.getline('D:/Users/rajsarka/Documents/FITSIM/resources/way_Node_Map', lineno=4002).strip().split(",")
print ('25457973' in line_1)
# print line_1