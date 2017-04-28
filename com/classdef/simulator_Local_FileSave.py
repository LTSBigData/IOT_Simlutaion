import datetime as dt
import os
import random
from datetime import time
from os import path

import numpy

import classDefinition_User_Local_FileSave as usr
import com.geoSpatialMap.geoLocation_User as glu

##########################################################################

project_dir = path.dirname(path.dirname(os.getcwd()))

# Define the output file paths
# For Mac and linux
user_history = project_dir + '/output/user_history_' + str(dt.datetime.today()) + '.csv'
user_register = project_dir + '/output/user_master_data_' + str(dt.datetime.today()) + '.csv'

# # For windows machines
# user_history = project_dir + '\\output\\user_history_' + str(dt.datetime.now().date().today()) + '.csv'
# user_register = project_dir + '\\output\\user_master_data_' + str(dt.datetime.now().date().today()) + '.csv'

user_history = usr.fileInitiate(user_history)
user_register = usr.fileInitiate(user_register)

##########################################################################

MUL = "*** MASTER USER LIST *** "
currentDate = dt.date.today()

# This is midnight time for the current date
midnight_time = dt.datetime.combine(currentDate, time())
print "Current System Datetime (Made Midnight Explicitly)" + str(midnight_time)
# This is the master list of all the user object with the device
master_User_List = []

# This will server as the total number of users for the while loop
print MUL + "Initialized with size = " + str(len(master_User_List))
# count = len(master_User_List)
# usr.send_To_Kafka_CountOfUsers(count, midnight_time.date())

# Initiate the simulation world time with today's date at 00:00:00 hrs
simulation_World_Time = midnight_time


#############################################################################

def updateUserList(time_1, n=1):
    """
    This pre-populates the Master User List AND adding new users to the MUL.
    :param n: int: serves as the pre-population argument. Denotes initial number of user in MUL
    :return: None
    """
    # Pre-population
    if n != 1:
        for i in numpy.arange(n):
            age, gender = assign_Age_Gender()
            add_User_To_List(age, gender, simulation_World_Time=time_1)
        return None

    # adding n = 1 users to MUL
    age, gender = assign_Age_Gender()
    add_User_To_List(age, gender, simulation_World_Time=time_1)


def add_User_To_List(age, gender, simulation_World_Time):
    """
    Used to add to the MUL. User Category are provided depending on which the category is chosen.
    For e.g. --> VERY_ACTIVE users has 15% chances of being chosen and so on and so forth. Once the category is
    assigned, according the age, gender the user is instantiated. Sleep_count is a measure that is specific to each
    category. Essentially it means that for category say for example 5, sleep_count = 0. This implies that the
    user of that category will update it's location after that many counts --> so it 'sleeps' for that amount.
    :param age: int: age of user
    :param gender: str: Gender of user
    :return: None
    """
    userCategoryWeights = numpy.array([15, 20, 30, 20, 15])
    userCategoryWeights = userCategoryWeights / 100.0
    choices = ["VERY_ACTIVE", "MOD_ACTIVE", "LIGHT_ACTIVE", "SEDENTARY", "NO_ACTIVITY"]
    # 0th element since list with single element is returned
    choice_of_userCategory = numpy.random.choice(choices, 1, p=userCategoryWeights)[0]

    if choice_of_userCategory == "VERY_ACTIVE":
        sleep_count = 0
        master_User_List.append(usr.user(age=age, gender=gender, category=5, sleep_count=sleep_count,
                                         initiation_Time=simulation_World_Time, user_register_file=user_register,
                                         user_history_file=user_history))
        return None

    elif choice_of_userCategory == "MOD_ACTIVE":
        sleep_count = 1
        master_User_List.append(usr.user(age=age, gender=gender, category=4, sleep_count=sleep_count,
                                         initiation_Time=simulation_World_Time, user_register_file=user_register,
                                         user_history_file=user_history))
        return None

    elif choice_of_userCategory == "LIGHT_ACTIVE":
        sleep_count = 2
        master_User_List.append(usr.user(age=age, gender=gender, category=3, sleep_count=sleep_count,
                                         initiation_Time=simulation_World_Time, user_register_file=user_register,
                                         user_history_file=user_history))
        return None

    elif choice_of_userCategory == "SEDENTARY":
        sleep_count = 3
        master_User_List.append(usr.user(age=age, gender=gender, category=2, sleep_count=sleep_count,
                                         initiation_Time=simulation_World_Time, user_register_file=user_register,
                                         user_history_file=user_history))
        return None

    elif choice_of_userCategory == "NO_ACTIVITY":
        sleep_count = 4
        master_User_List.append(usr.user(age=age, gender=gender, category=1, sleep_count=sleep_count,
                                         initiation_Time=simulation_World_Time, user_register_file=user_register,
                                         user_history_file=user_history))
        return None


def assign_Age_Gender():
    """
    Function simply produces an age and a gender according the weights/probabilities pre-provided. Takes no arg.
    :return: int: age, str: gender_Choice
    """
    age_Weights = numpy.array([24.1, 64.8, 11.1])
    age_Weights = age_Weights / 100.0
    age_Category = [1, 2, 3]
    gender_Weights = numpy.array([50.2, 49.8])
    gender_Weights = gender_Weights / 100.0
    gender_Category = ["M", "F"]
    age_choice = numpy.random.choice(age_Category, 1, p=age_Weights)[0]
    gender_Choice = numpy.random.choice(gender_Category, 1, p=gender_Weights)[0]
    [age_Low_Limit, age_Up_Limit] = get_Age_Limits(age_choice)
    age = random.randint(age_Low_Limit, age_Up_Limit)
    return age, gender_Choice


def get_Age_Limits(category):
    """
    Function returns the limits of age for assign_Age_Gender(). Created for modularity ONLY.
    :param category: int: category here represents the number 1, 2, 3 which basically has 3 different limits.
    :return: list:[lower limit, upper limit]
    """
    if category == 1:
        return [5, 17]
    elif category == 2:
        return [18, 64]
    elif category == 3:
        return [65, 70]


#############################################################################


# Pre-populating the master user list
updateUserList(simulation_World_Time, n=5000)

print MUL + "Pre-populated with :" + str(len(master_User_List)) + " users"

# Updating simulation world time by 5 minutes in order to keep model consistency. Doesn't make much difference.
simulation_World_Time = simulation_World_Time + dt.timedelta(minutes=5)

# total_hours keeps a measure of the time in the simulation.
total_hours = (24 * 60) / 5

print dt.datetime.now()

while (total_hours != 0):
    # print "Time in Simulation" + str(simulation_World_Time)

    weights = numpy.array([80, 20]) / 100.0

    # # For even further randomised data generation w.r.t. prob of user_creation
    # p = random.uniform(0.0, 0.3)
    # q = 1.0 - p
    # weights = numpy.array([p, q])

    choices = [0, 1]
    choice = numpy.random.choice(choices, 1, p=weights)
    if choice == 1:
        simulation_World_Time = simulation_World_Time + dt.timedelta(milliseconds=10)
        updateUserList(simulation_World_Time)
        # print "New User Added!!"
        continue
    else:
        for i in range(len(master_User_List)):
            glu.updateLocation_User(master_User_List[i])
            usr.updatePulseTemp_User(master_User_List[i])
            usr.user_current_data(simulation_World_Time, master_User_List[i], user_history)

    simulation_World_Time = simulation_World_Time + dt.timedelta(minutes=5)
    total_hours -= 1

user_history.close()
user_register.close()

print dt.datetime.now()
print len(master_User_List)
