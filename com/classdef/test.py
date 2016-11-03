import datetime as dt
import random
from datetime import time

import numpy

import classDefinition_User as usr
import com.geoSpatialMap.geoLocation_User as glu

MUL = "*** MASTER USER LIST *** "
currentDate = dt.date.today()

# This is midnight time for the current date
midnight_time = dt.datetime.combine(currentDate, time())
print midnight_time
# This is the master list of all the user object with the device
master_User_List = []
# This will server as the total number of users for the while loop
master_User_List_Length = len(master_User_List)
print MUL + "Initialized with size = " + str(master_User_List_Length)

# Printing 1 simulation world's day's data
# Total Number of users = 10 (pre-existing)

def updateUserList(n=1):
    # This is for pre-populating the Master User List
    if n != 1:
        for i in numpy.arange(n):
            age, gender = assign_Age_Gender()
            add_User_To_List(age, gender)
        return None
    age, gender = assign_Age_Gender()
    add_User_To_List(age, gender)


def add_User_To_List(age, gender):
    userCategoryWeights = numpy.array([15, 20, 30, 20, 15])
    userCategoryWeights = userCategoryWeights/100.0
    choices = ["VERY_ACTIVE", "MOD_ACTIVE", "LIGHT_ACTIVE", "SEDENTARY", "NO_ACTIVITY"]
    choice_of_userCategory = numpy.random.choice(choices, 1, p=userCategoryWeights)[0]

    if choice_of_userCategory == "VERY_ACTIVE":
        sleep_count = 0
        master_User_List.append(usr.user(age, gender, 5, sleep_count))
        value = "User added with | Age: "
        value += str(age) + " | "
        value += "Gender: " + str(gender) + " | "
        value += "Type: " + choice_of_userCategory
        # print value
        # print len(master_User_List)
        return None

    elif choice_of_userCategory == "MOD_ACTIVE":
        sleep_count = 1
        master_User_List.append(usr.user(age, gender, 4, sleep_count))
        value = "User added with | Age: "
        value += str(age) + " | "
        value += "Gender: " + str(gender) + " | "
        value += "Type: " + choice_of_userCategory
        # print value
        # print len(master_User_List)
        return None

    elif choice_of_userCategory == "LIGHT_ACTIVE":
        sleep_count = 2
        master_User_List.append(usr.user(age, gender, 3, sleep_count))
        value = "User added with | Age: "
        value += str(age) + " | "
        value += "Gender: " + str(gender) + " | "
        value += "Type: " + choice_of_userCategory
        # print value
        # print len(master_User_List)
        return None

    elif choice_of_userCategory == "SEDENTARY":
        sleep_count = 3
        master_User_List.append(usr.user(age, gender, 2, sleep_count))
        value = "User added with | Age: "
        value += str(age) + " | "
        value += "Gender: " + str(gender) + " | "
        value += "Type: " + choice_of_userCategory
        # print value
        # print len(master_User_List)
        return None

    elif choice_of_userCategory == "NO_ACTIVITY":
        sleep_count = 4
        master_User_List.append(usr.user(age, gender, 1, sleep_count))
        value = "User added with | Age: "
        value += str(age) + " | "
        value += "Gender: " + str(gender) + " | "
        value += "Type: " + choice_of_userCategory
        # print value
        # print len(master_User_List)
        return None


def assign_Age_Gender():
    age_Weights = numpy.array([24.1, 64.8, 11.1])
    age_Weights = age_Weights/100.0
    age_Category = [1, 2, 3]
    gender_Weights = numpy.array([50.2, 49.8])
    gender_Weights = gender_Weights/100.0
    gender_Category = ["M", "F"]
    age_choice = numpy.random.choice(age_Category, 1, p=age_Weights)[0]
    gender_Choice = numpy.random.choice(gender_Category, 1, p=gender_Weights)[0]
    [age_Low_Limit, age_Up_Limit] = get_Age_Limits(age_choice)
    age = random.randint(age_Low_Limit, age_Up_Limit)
    return age, gender_Choice


def get_Age_Limits(category):
    if category == 1:
        return [5, 17]
    elif category == 2:
        return [18, 64]
    elif category == 3:
        return [65, 100]

# Pre-populating the master user list
updateUserList(n=4)

print MUL + "Pre-populated with :" + str(len(master_User_List)) + " users"

for i in range(5):
    updateUserList()

master_User_List_Length = len(master_User_List)

print MUL + "Total users : " + str(master_User_List_Length)

total_hours = 12
simulation_World_Time = midnight_time

print dt.datetime.now()

while(total_hours != 0):
    print simulation_World_Time
    print dt.datetime.now()
    usr.send_Time_To_Kafka(str(simulation_World_Time))
    for i in range(master_User_List_Length):

        usr.printUserDetails(master_User_List[i])
        glu.updateLocation_User(master_User_List[i])

    simulation_World_Time = simulation_World_Time + dt.timedelta(hours=1)
    total_hours -= 1
    print dt.datetime.now()

print dt.datetime.now()
