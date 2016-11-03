import datetime as dt
import linecache as ln

WAY_NODE_PATH = 'D:/Users/rajsarka/Documents/FITSIM/resources/way_Node_Map'
way_node_map = ln.getlines(WAY_NODE_PATH)

# for line in way_node_map:
#     lineList = line.strip().split(",")
#     if len(lineList) == 1 or len(lineList) == 3:
#         print True
#         break
#     else:
#         continue

a = [1, 2, 3, 4, 5, 6, 7, 8, 9]
b = []
b = a
print b
print dt.datetime.now()
# choice = 3
# count = 0
# aa = 3
# while(aa == choice):
#     aa = a[random.randint(0, len(a) - 1)]
#     print aa
#     count += 1
# print count
