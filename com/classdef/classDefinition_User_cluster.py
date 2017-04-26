import math
import random as rn
import time
import uuid

import numpy as np
from kafka import KafkaProducer

import com.geoSpatialMap.geoLocation_User as glu
import com.map.age_Weight_Heigt_Map_Kids as wt_ht_map
import com.map.bp_Limit_Map as bp
import com.map.user_Category_Map as category

MAX_PULSE_BELOW40 = 220
MAX_PULSE_ABOVE40 = 208
ABOVE_40_CONST = 0.75


class user(object):
    def __init__(self, age, gender, category, sleep_count, initiation_Time):
        self.age = age  # User age
        self.gender = gender  # User Gender
        self.sleep_count = sleep_count  # measure of rate of update of geo-location
        self.category = category  # category of user Eg. VeryActive, Sedentary etc.
        [self.weight, self.height] = determine_Height_And_Weight(age, gender)  # Age and gender
        self.bmi = determine_BMI(self.weight, self.height)  # Body Mass Index
        self.bfp = determine_BFP(self.age, self.gender, self.bmi)  # Body Fat Percentage
        self.bp, self.bpCategory = determine_BP(self.age, category)  # Blood Pressure and its category
        self.userID, self.deviceID = uuid.uuid4(), uuid.uuid4()  # Unique (User ID and Device ID)
        [self.lat, self.lon, self.node_id, self.way_id] = glu.initialize_User_Position()  # Position of user
        self.pulse = initPulse(self.age)
        self.temp = initBodyTemp()
        # Messages instead of being written in a file are sent as Kafka Messages to broker
        send_To_Kafka_NewUser(self)
        send_To_Kafka_User_Details(initiation_Time, self)


def determine_Height_And_Weight(age, gender):
    """
    Given age and gender, this function returns the height and weight of an user instance.
    The function takes into consideration of a kid (age <= 20) as well as for an adult (age > 20).
    For Kids there is a separate mapping of age versus height and weight kept in the package
    com.map.age_Weight_Heigt_Map_Kids

    For Adults the function just plots a random float point between the range that have been provided.
    :param age: int: age of user
    :param gender: str: gender of user
    :return: List[float: weight (in lbs), float: height (in cms)]
    """

    # FOR KIDs
    if age <= 20:
        if gender == "M":
            [weight, height] = wt_ht_map.heightWeightMap_Male[age]
            return [weight, height]
        elif gender == "F":
            [weight, height] = wt_ht_map.heightWeightMap_Female[age]
            return [weight, height]
    # FOR ADULTS
    else:
        if gender == "M":
            height = rn.uniform(172.1, 219)
            weight = rn.uniform(170, 197)
            return [weight, height]
        elif gender == "F":
            height = rn.uniform(158.1, 164.8)
            weight = rn.uniform(149, 166)
            return [weight, height]


def determine_BMI(weight, height):
    """
    Function returns the BMI (Body Mass Index) of the user given weight and height.
    The function incorporates all the conversions required to calculate BMI from lbs and cms.
    :param weight: float : weight of user (in lbs)
    :param height: float : height of user (in cms)
    :return: float : bmi of user
    """
    bmi = float((weight * 703) / math.pow((height * 0.393701), 2))
    return bmi


def determine_BFP(age, gender, bmi):
    """
    Function calculates the Body Fat Percentage of user given age, gender and bmi.
    The formula used to calculate the BFP is not extremely accurate but it serves the purpose for demo values.
    :param age: int: age of user
    :param gender: str : gender of user
    :param bmi: float : BMI value of the user
    :return:
    """
    if age <= 16:
        if gender == "M":
            bfp = (1.51 * bmi) - (0.70 * age) - 3.6 + 1.4
            return bfp
        elif gender == "F":
            bfp = (1.51 * bmi) - (0.70 * age) + 1.4
            return bfp
    elif age > 16:
        if gender == "M":
            bfp = (1.20 * bmi) + (0.23 * age) - 10.8 - 5.4
            return bfp
        elif gender == "F":
            bfp = (1.20 * bmi) + (0.23 * age) - 5.4
            return bfp


def determine_BP(age, activityFlag):
    """
    Function calculates the blood pressure of the user. Blood pressure have been categorised into 6 different
    categories:
    "LOW", "NORMAL", "PREHYP", "HYP_1", "HYP_2", "HYP_CR"
    With each user's activityFlag ranging from 1 to 5, 1 being least active and 5 being very active,
    a random blood pressure category is assigned to each user depending on the likelihood of that user's activity flag
    sustaining ANY ONE of the 6 blood pressure categories.

    For e.g.
    For activityFlag == 5 -> 'veryActive' user chances of him/her having pressure:
    LOW -> 7% likelihood, NORMAL -> 80% likelihood, PREHYP -> 7% likelihood,
    HYP_1 -> 4% likelihood, HYP_2 -> 1% likelihood, HYP_CR -> 1% likelihood

    Once the blood pressure choice is assigned, returnBP_Value function is called which provides numerical values.

    :param age: int : age of user
    :param activityFlag: int : flag (1 to 5) mapping activity level of user
    :return: List : [[float : Systolic Pressure, float: Diastolic Pressure], str: Blood Pressure Category]
    """
    if activityFlag == 5:  # for VeryActive Users
        # respective weights of the blood pressure categories
        bpWts = np.array([7, 80, 7, 4, 1, 1]) / 100.0
        # blood pressure categories
        bpChoices = ["LOW", "NORMAL", "PREHYP", "HYP_1", "HYP_2", "HYP_CR"]
        # choice is a numpy array element containing 1 single string value in its 0th element.
        choice = np.random.choice(bpChoices, 1, p=bpWts)[0]
        bpList = returnBP_Value(choice, age)
        return bpList, choice

    elif activityFlag == 4:  # for ModeratelyActive Users
        # respective weights of the blood pressure categories
        bpWts = np.array([10, 65, 10, 8, 6, 1]) / 100.0
        # blood pressure categories
        bpChoices = ["LOW", "NORMAL", "PREHYP", "HYP_1", "HYP_2", "HYP_CR"]
        # choice is a numpy array element containing 1 single string value in its 0th element.
        choice = np.random.choice(bpChoices, 1, p=bpWts)[0]
        bpList = returnBP_Value(choice, age)
        return bpList, choice

    elif activityFlag == 3:  # for LightlyActive Users
        # respective weights of the blood pressure categories
        bpWts = np.array([15, 50, 12, 10, 9, 4]) / 100.0
        # blood pressure categories
        bpChoices = ["LOW", "NORMAL", "PREHYP", "HYP_1", "HYP_2", "HYP_CR"]
        # choice is a numpy array element containing 1 single string value in its 0th element.
        choice = np.random.choice(bpChoices, 1, p=bpWts)[0]
        bpList = returnBP_Value(choice, age)
        return bpList, choice

    elif activityFlag == 2:  # for Sedentary Users
        # respective weights of the blood pressure categories
        bpWts = np.array([20, 40, 15, 12, 10, 3]) / 100.0
        # blood pressure categories
        bpChoices = ["LOW", "NORMAL", "PREHYP", "HYP_1", "HYP_2", "HYP_CR"]
        # choice is a numpy array element containing 1 single string value in its 0th element.
        choice = np.random.choice(bpChoices, 1, p=bpWts)[0]
        bpList = returnBP_Value(choice, age)
        return bpList, choice

    elif activityFlag == 1:  # for NoActive Users
        # respective weights of the blood pressure categories
        bpWts = np.array([25, 20, 20, 18, 10, 7]) / 100.0
        # blood pressure categories
        bpChoices = ["LOW", "NORMAL", "PREHYP", "HYP_1", "HYP_2", "HYP_CR"]
        # choice is a numpy array element containing 1 single string value in its 0th element.
        choice = np.random.choice(bpChoices, 1, p=bpWts)[0]
        bpList = returnBP_Value(choice, age)
        return bpList, choice


def returnBP_Value(bpChoice, age):
    """
    Function is called from within determine_BP. It returns numerical values according to user age and the choice
    of blood pressure category the user have assigned to. It uses com.map.bp_Limit_Map to map normal blood pressure
    for user depending on age of user. All ages 60+ have a constant normal as can be seen from the mapping.
    com.map.bp_Limit_Map also provides the mapping for blood pressure limits for different blood pressure categories.

    The numerical values are calculated as follows:-
    for specific blood pressure category--->
        obtain Systolic Pressure [Low, High] + Diastolic Pressure [Low, High]
        obtain normal systolic and diastolic pressure for specific age.
        obtain systolic correlation limits by the formula: LOWER LIMIT:(systolic low - normal systolic / age)
                                                            UPPER LIMIT:(systolic high - normal systolic / age)
        obtain diastolic correlation limits by the formula: LOWER LIMIT:(diastolic low - normal diastolic / age)
                                                            UPPER LIMIT:(diastolic high - normal diastolic / age)

        Once limits for both the systolic and diastolic correlations are obtained, randomly choose a value between them.
        FINAL SYSTOLIC VALUE = normal systolic value + randomly chosen correlation between range * age
        FINAL DIASTOLIC VALUE = normal diastolic value + randomly chosen correlation between range * age

    :param bpChoice: str: blood pressure category
    :param age: int: age of user
    :return: List[float : Systolic Pressure, float: Diastolic Pressure]
    """
    if age >= 60:
        # Any age above 60 is taken into a single category hence ageKey is set to be 60 for age_Normal_BP_Map
        ageKey = 60
        # using com.map.bp_Limit_Map we obtain the normal blood pressure values and the blood pressure limits
        [normalSystolic, normalDiastolic] = bp.age_Normal_BP_Map[ageKey]
        [sysLow, sysUp, diasLow, diasUp] = bp.bp_Limit_Map[bpChoice]
        # The correlation values are calculated for both the diastolic and systolic pressure
        [sys_Corr_Low, sys_Corr_Up] = [((sysLow - normalSystolic) / float(age)),
                                       ((sysUp - normalSystolic) / float(age))]

        [dias_Corr_Low, dias_Corr_Up] = [((diasLow - normalDiastolic) / float(age)),
                                         ((diasUp - normalDiastolic) / float(age))]
        # A random floating point value is chosen between the range for both Systolic and Diastolic Pressure
        sys_Corr_Final = rn.uniform(sys_Corr_Low, sys_Corr_Up)
        dias_Corr_Final = rn.uniform(dias_Corr_Low, dias_Corr_Up)
        # the final value is calculated as per the previous formula
        value = [math.ceil(normalSystolic + sys_Corr_Final * age), math.ceil(normalDiastolic + dias_Corr_Final * age)]
        return value
    else:
        # using com.map.bp_Limit_Map we obtain the normal blood pressure values and the blood pressure limits
        [normalSystolic, normalDiastolic] = bp.age_Normal_BP_Map[age]
        [sysLow, sysUp, diasLow, diasUp] = bp.bp_Limit_Map[bpChoice]
        # The correlation values are calculated for both the diastolic and systolic pressure
        [sys_Corr_Low, sys_Corr_Up] = [((sysLow - normalSystolic) / float(age)),
                                       ((sysUp - normalSystolic) / float(age))]

        [dias_Corr_Low, dias_Corr_Up] = [((diasLow - normalDiastolic) / float(age)),
                                         ((diasUp - normalDiastolic) / float(age))]
        # A random floating point value is chosen between the range for both Systolic and Diastolic Pressure
        sys_Corr_Final = rn.uniform(sys_Corr_Low, sys_Corr_Up)
        dias_Corr_Final = rn.uniform(dias_Corr_Low, dias_Corr_Up)
        # the final value is calculated as per the previous formula
        value = [math.ceil(normalSystolic + sys_Corr_Final * age), math.ceil(normalDiastolic + dias_Corr_Final * age)]
        return value


def getPulseTargetLimit(age, MAXPULSE_Limit=False):
    if not MAXPULSE_Limit:
        if age <= 40:
            value = MAX_PULSE_BELOW40 - age
            targetLow = math.ceil(value * 0.50)
            targetHigh = math.ceil(value * 0.85)
            return [targetLow, targetHigh]
        else:
            value = MAX_PULSE_ABOVE40 - (0.75 * age)
            targetLow = math.ceil(value * 0.50)
            targetHigh = math.ceil(value * 0.85)
            return [targetLow, targetHigh]
    elif MAXPULSE_Limit:
        if age <= 40:
            value = MAX_PULSE_BELOW40 - age
            targetLow = math.ceil(value * 0.50)
            targetHigh = math.ceil(value * 0.85)
            return [targetLow, targetHigh, value]
        else:
            value = MAX_PULSE_ABOVE40 - (0.75 * age)
            targetLow = math.ceil(value * 0.50)
            targetHigh = math.ceil(value * 0.85)
            return [targetLow, targetHigh, value]


def getTemp(next_Temp_Cat):
    if next_Temp_Cat == 1:
        [low_lim, up_lim] = [36.5, 37.5]
        temp = rn.uniform(low_lim, up_lim)
        return temp
    elif next_Temp_Cat == 2:
        [low_lim, up_lim] = [37.5, 38.3]
        temp = rn.uniform(low_lim, up_lim)
        return temp
    elif next_Temp_Cat == 3:
        [low_lim, up_lim] = [38.3, 39.5]
        temp = rn.uniform(low_lim, up_lim)
        return temp
    elif next_Temp_Cat == 4:
        [low_lim, up_lim] = [39.5, 41.5]
        temp = rn.uniform(low_lim, up_lim)
        return temp


def getNextTemp():
    weights = np.array([85, 14, 0.5, 0.5]) / 100.0
    temp_category = [1, 2, 3, 4]
    next_Temp_Cat = np.random.choice(temp_category, 1, p=weights)
    next_Temp = getTemp(next_Temp_Cat)
    return next_Temp


def getStdDev_WRT_Temp(a, b, temp):
    """
    Returns either sigma or -sigma of 2 numbers.
    :param a: float: Number 1
    :param b: float: Number 2
    :param temp: float: current temperature
    :return: float: sigma or -sigma
    """
    choice = 0
    tempFormatter = '{:4.2f}'
    current_temp = temp
    next_temp = tempFormatter.format(getNextTemp())
    if current_temp == next_temp:
        choice = 0.0
    elif current_temp < next_temp:
        choice = 1.0
    elif current_temp > next_temp:
        choice = -1.0
    stdDev = np.std([float(a), float(b)]) / 100.0
    value = stdDev * choice
    return [value, next_temp]


def getPulseValue(pulse_Choice, currentPulse, maxLim_Pulse, temp):
    if pulse_Choice == 1:
        lowLim = 0.20 * maxLim_Pulse  # 20% of MAX
        upLim = 0.40 * maxLim_Pulse  # 40% of MAX
        value = math.ceil(rn.uniform(lowLim, upLim))  # first choice is between 20 -- 40 %
        # Instead of returning just a random value within the range, this finds the standard deviation and then simply
        # adds that to the present pulse rate (can be both positive and negative) so that it has a continuation.
        # Same logic for all the values of pulse_Choice
        [toAdd, next_temp] = getStdDev_WRT_Temp(value, currentPulse, temp)
        return [(value + toAdd), next_temp]
    elif pulse_Choice == 2:
        lowLim = 0.40 * maxLim_Pulse  # 40% of MAX
        upLim = 0.50 * maxLim_Pulse  # 50% of MAX
        value = math.ceil(rn.uniform(lowLim, upLim))  # first choice is between 40 -- 50 %
        [toAdd, next_temp] = getStdDev_WRT_Temp(value, currentPulse, temp)
        return [(value + toAdd), next_temp]
    elif pulse_Choice == 3:
        lowLim = 0.50 * maxLim_Pulse  # 50% of MAX
        upLim = 0.85 * maxLim_Pulse  # 85% of MAX
        value = math.ceil(rn.uniform(lowLim, upLim))  # first choice is between 40 -- 50 %
        [toAdd, next_temp] = getStdDev_WRT_Temp(value, currentPulse, temp)
        return [(value + toAdd), next_temp]
    elif pulse_Choice == 4:
        lowLim = 0.85 * maxLim_Pulse  # 85% of MAX
        upLim = 0.95 * maxLim_Pulse  # 95% of MAX
        value = math.ceil(rn.uniform(lowLim, upLim))  # first choice is between 40 -- 50 %
        [toAdd, next_temp] = getStdDev_WRT_Temp(value, currentPulse, temp)
        return [(value + toAdd), next_temp]


def initPulse(age):
    """
    When user is instantiated, it assigns a normal pulse rate.
    :param age: int: Age of user
    :return value: float: Initial pulse rate of user
    """
    [targetLow, targetHigh] = getPulseTargetLimit(age)
    value = math.ceil(rn.uniform(targetLow, targetHigh))
    return value


def initBodyTemp():
    """
    Assigns a normal body temperature when an user instantiates
    :return: str: body temperature in celsius
    """
    tempFormatter = '{:4.2f}'
    lower_limit = 36.5
    upper_limit = 37.5
    value = rn.uniform(lower_limit, upper_limit)
    return tempFormatter.format(value)


def updatePulse_BodyTemp(age, category, bpCategory, pulse, temp):
    """
    Returns a pulse rate value of the user.
    :param age: int: Age of user
    :param category: int: Activity Category of user. Ranges from 5 to 1. 5 being most active.
    :param bpCategory: str: Blood Pressure category of the user. Consists of 6 categories.
    :param pulse: float: Current Pulse Rate of the user.
    :param temp: float: Current temperature of the user.
    :return: float: next pulse rate value
    """
    # Taking only the maximum pulse of that age. It is 3rd element of the returned list
    maxLim_Pulse = getPulseTargetLimit(age, MAXPULSE_Limit=True)[2]
    if bpCategory == "LOW":
        if category == 5:
            pulseCategory = [1, 2, 3, 4]
            weights = np.array([2, 34, 59, 5]) / 100.0
            pulse_choice = np.random.choice(pulseCategory, 1, p=weights)[0]
            [pulse_Choice_Value, next_temp] = getPulseValue(pulse_choice, pulse, maxLim_Pulse, temp)
            return [pulse_Choice_Value, next_temp]
        elif category == 4:
            pulseCategory = [1, 2, 3, 4]
            weights = np.array([2.2, 37.7, 55, 5.1]) / 100.0
            pulse_choice = np.random.choice(pulseCategory, 1, p=weights)[0]
            [pulse_Choice_Value, next_temp] = getPulseValue(pulse_choice, pulse, maxLim_Pulse, temp)
            return [pulse_Choice_Value, next_temp]
        elif category == 3:
            pulseCategory = [1, 2, 3, 4]
            weights = np.array([2.4, 41.4, 51, 5.2]) / 100.0
            pulse_choice = np.random.choice(pulseCategory, 1, p=weights)[0]
            [pulse_Choice_Value, next_temp] = getPulseValue(pulse_choice, pulse, maxLim_Pulse, temp)
            return [pulse_Choice_Value, next_temp]
        elif category == 2:
            pulseCategory = [1, 2, 3, 4]
            weights = np.array([2.6, 45.1, 47, 5.3]) / 100.0
            pulse_choice = np.random.choice(pulseCategory, 1, p=weights)[0]
            [pulse_Choice_Value, next_temp] = getPulseValue(pulse_choice, pulse, maxLim_Pulse, temp)
            return [pulse_Choice_Value, next_temp]
        elif category == 1:
            pulseCategory = [1, 2, 3, 4]
            weights = np.array([2.8, 48.8, 43, 5.4]) / 100.0
            pulse_choice = np.random.choice(pulseCategory, 1, p=weights)[0]
            [pulse_Choice_Value, next_temp] = getPulseValue(pulse_choice, pulse, maxLim_Pulse, temp)
            return [pulse_Choice_Value, next_temp]

    elif bpCategory == "NORMAL":
        if category == 5:
            pulseCategory = [1, 2, 3, 4]
            weights = np.array([1, 23, 69, 7]) / 100.0
            pulse_choice = np.random.choice(pulseCategory, 1, p=weights)[0]
            [pulse_Choice_Value, next_temp] = getPulseValue(pulse_choice, pulse, maxLim_Pulse, temp)
            return [pulse_Choice_Value, next_temp]
        elif category == 4:
            pulseCategory = [1, 2, 3, 4]
            weights = np.array([1.2, 25.6, 66, 7.2]) / 100.0
            pulse_choice = np.random.choice(pulseCategory, 1, p=weights)[0]
            [pulse_Choice_Value, next_temp] = getPulseValue(pulse_choice, pulse, maxLim_Pulse, temp)
            return [pulse_Choice_Value, next_temp]
        elif category == 3:
            pulseCategory = [1, 2, 3, 4]
            weights = np.array([1.4, 28.2, 63, 7.4]) / 100.0
            pulse_choice = np.random.choice(pulseCategory, 1, p=weights)[0]
            [pulse_Choice_Value, next_temp] = getPulseValue(pulse_choice, pulse, maxLim_Pulse, temp)
            return [pulse_Choice_Value, next_temp]
        elif category == 2:
            pulseCategory = [1, 2, 3, 4]
            weights = np.array([1.6, 30.8, 60, 7.6]) / 100.0
            pulse_choice = np.random.choice(pulseCategory, 1, p=weights)[0]
            [pulse_Choice_Value, next_temp] = getPulseValue(pulse_choice, pulse, maxLim_Pulse, temp)
            return [pulse_Choice_Value, next_temp]
        elif category == 1:
            pulseCategory = [1, 2, 3, 4]
            weights = np.array([1.8, 33.2, 57, 8]) / 100.0
            pulse_choice = np.random.choice(pulseCategory, 1, p=weights)[0]
            [pulse_Choice_Value, next_temp] = getPulseValue(pulse_choice, pulse, maxLim_Pulse, temp)
            return [pulse_Choice_Value, next_temp]

    elif bpCategory == "PREHYP":
        if category == 5:
            pulseCategory = [1, 2, 3, 4]
            weights = np.array([0.5, 12.5, 79, 8]) / 100.0
            pulse_choice = np.random.choice(pulseCategory, 1, p=weights)[0]
            [pulse_Choice_Value, next_temp] = getPulseValue(pulse_choice, pulse, maxLim_Pulse, temp)
            return [pulse_Choice_Value, next_temp]
        elif category == 4:
            pulseCategory = [1, 2, 3, 4]
            weights = np.array([0.6, 15.2, 76, 8.2]) / 100.0
            pulse_choice = np.random.choice(pulseCategory, 1, p=weights)[0]
            [pulse_Choice_Value, next_temp] = getPulseValue(pulse_choice, pulse, maxLim_Pulse, temp)
            return [pulse_Choice_Value, next_temp]
        elif category == 3:
            pulseCategory = [1, 2, 3, 4]
            weights = np.array([0.7, 17.9, 73, 8.4]) / 100.0
            pulse_choice = np.random.choice(pulseCategory, 1, p=weights)[0]
            [pulse_Choice_Value, next_temp] = getPulseValue(pulse_choice, pulse, maxLim_Pulse, temp)
            return [pulse_Choice_Value, next_temp]
        elif category == 2:
            pulseCategory = [1, 2, 3, 4]
            weights = np.array([0.8, 20.6, 70, 8.6]) / 100.0
            pulse_choice = np.random.choice(pulseCategory, 1, p=weights)[0]
            [pulse_Choice_Value, next_temp] = getPulseValue(pulse_choice, pulse, maxLim_Pulse, temp)
            return [pulse_Choice_Value, next_temp]
        elif category == 1:
            pulseCategory = [1, 2, 3, 4]
            weights = np.array([0.9, 23.3, 67, 8.8]) / 100.0
            pulse_choice = np.random.choice(pulseCategory, 1, p=weights)[0]
            [pulse_Choice_Value, next_temp] = getPulseValue(pulse_choice, pulse, maxLim_Pulse, temp)
            return [pulse_Choice_Value, next_temp]

    elif bpCategory == "HYP_1":
        if category == 5:
            pulseCategory = [1, 2, 3, 4]
            weights = np.array([0.5, 0.5, 79, 20]) / 100.0
            pulse_choice = np.random.choice(pulseCategory, 1, p=weights)[0]
            [pulse_Choice_Value, next_temp] = getPulseValue(pulse_choice, pulse, maxLim_Pulse, temp)
            return [pulse_Choice_Value, next_temp]
        elif category == 4:
            pulseCategory = [1, 2, 3, 4]
            weights = np.array([0.6, 3.2, 76, 20.2]) / 100.0
            pulse_choice = np.random.choice(pulseCategory, 1, p=weights)[0]
            [pulse_Choice_Value, next_temp] = getPulseValue(pulse_choice, pulse, maxLim_Pulse, temp)
            return [pulse_Choice_Value, next_temp]
        elif category == 3:
            pulseCategory = [1, 2, 3, 4]
            weights = np.array([0.7, 5.9, 73, 20.4]) / 100.0
            pulse_choice = np.random.choice(pulseCategory, 1, p=weights)[0]
            [pulse_Choice_Value, next_temp] = getPulseValue(pulse_choice, pulse, maxLim_Pulse, temp)
            return [pulse_Choice_Value, next_temp]
        elif category == 2:
            pulseCategory = [1, 2, 3, 4]
            weights = np.array([0.8, 8.6, 70, 20.6]) / 100.0
            pulse_choice = np.random.choice(pulseCategory, 1, p=weights)[0]
            [pulse_Choice_Value, next_temp] = getPulseValue(pulse_choice, pulse, maxLim_Pulse, temp)
            return [pulse_Choice_Value, next_temp]
        elif category == 1:
            pulseCategory = [1, 2, 3, 4]
            weights = np.array([0.9, 11.3, 67, 20.8]) / 100.0
            pulse_choice = np.random.choice(pulseCategory, 1, p=weights)[0]
            [pulse_Choice_Value, next_temp] = getPulseValue(pulse_choice, pulse, maxLim_Pulse, temp)
            return [pulse_Choice_Value, next_temp]

    elif bpCategory == "HYP_2":
        if category == 5:
            pulseCategory = [1, 2, 3, 4]
            weights = np.array([0.5, 0.5, 69, 30]) / 100.0
            pulse_choice = np.random.choice(pulseCategory, 1, p=weights)[0]
            [pulse_Choice_Value, next_temp] = getPulseValue(pulse_choice, pulse, maxLim_Pulse, temp)
            return [pulse_Choice_Value, next_temp]
        elif category == 4:
            pulseCategory = [1, 2, 3, 4]
            weights = np.array([0.6, 3.2, 66, 30.2]) / 100.0
            pulse_choice = np.random.choice(pulseCategory, 1, p=weights)[0]
            [pulse_Choice_Value, next_temp] = getPulseValue(pulse_choice, pulse, maxLim_Pulse, temp)
            return [pulse_Choice_Value, next_temp]
        elif category == 3:
            pulseCategory = [1, 2, 3, 4]
            weights = np.array([0.7, 5.9, 63, 30.4]) / 100.0
            pulse_choice = np.random.choice(pulseCategory, 1, p=weights)[0]
            [pulse_Choice_Value, next_temp] = getPulseValue(pulse_choice, pulse, maxLim_Pulse, temp)
            return [pulse_Choice_Value, next_temp]
        elif category == 2:
            pulseCategory = [1, 2, 3, 4]
            weights = np.array([0.8, 8.6, 60, 30.6]) / 100.0
            pulse_choice = np.random.choice(pulseCategory, 1, p=weights)[0]
            [pulse_Choice_Value, next_temp] = getPulseValue(pulse_choice, pulse, maxLim_Pulse, temp)
            return [pulse_Choice_Value, next_temp]
        elif category == 1:
            pulseCategory = [1, 2, 3, 4]
            weights = np.array([0.9, 11.3, 57, 30.8]) / 100.0
            pulse_choice = np.random.choice(pulseCategory, 1, p=weights)[0]
            [pulse_Choice_Value, next_temp] = getPulseValue(pulse_choice, pulse, maxLim_Pulse, temp)
            return [pulse_Choice_Value, next_temp]

    elif bpCategory == "HYP_CR":
        if category == 5:
            pulseCategory = [1, 2, 3, 4]
            weights = np.array([0.5, 0.5, 59, 40]) / 100.0
            pulse_choice = np.random.choice(pulseCategory, 1, p=weights)[0]
            [pulse_Choice_Value, next_temp] = getPulseValue(pulse_choice, pulse, maxLim_Pulse, temp)
            return [pulse_Choice_Value, next_temp]
        elif category == 4:
            pulseCategory = [1, 2, 3, 4]
            weights = np.array([0.6, 3.2, 55, 41.2]) / 100.0
            pulse_choice = np.random.choice(pulseCategory, 1, p=weights)[0]
            [pulse_Choice_Value, next_temp] = getPulseValue(pulse_choice, pulse, maxLim_Pulse, temp)
            return [pulse_Choice_Value, next_temp]
        elif category == 3:
            pulseCategory = [1, 2, 3, 4]
            weights = np.array([0.7, 5.9, 51, 42.4]) / 100.0
            pulse_choice = np.random.choice(pulseCategory, 1, p=weights)[0]
            [pulse_Choice_Value, next_temp] = getPulseValue(pulse_choice, pulse, maxLim_Pulse, temp)
            return [pulse_Choice_Value, next_temp]
        elif category == 2:
            pulseCategory = [1, 2, 3, 4]
            weights = np.array([0.8, 8.6, 47, 43.6]) / 100.0
            pulse_choice = np.random.choice(pulseCategory, 1, p=weights)[0]
            [pulse_Choice_Value, next_temp] = getPulseValue(pulse_choice, pulse, maxLim_Pulse, temp)
            return [pulse_Choice_Value, next_temp]
        elif category == 1:
            pulseCategory = [1, 2, 3, 4]
            weights = np.array([0.9, 11.3, 43, 44.8]) / 100.0
            pulse_choice = np.random.choice(pulseCategory, 1, p=weights)[0]
            [pulse_Choice_Value, next_temp] = getPulseValue(pulse_choice, pulse, maxLim_Pulse, temp)
            return [pulse_Choice_Value, next_temp]


def updatePulseTemp_User(user):
    [user.pulse, user.temp] = updatePulse_BodyTemp(user.age, user.category, user.bpCategory, user.pulse, user.temp)


# def printUserDetails(user):
#     """
#     Function takes in a user object and print all its elements
#     :param user: user object
#     :return: None
#     """
#     floatingPointFormatter = '{:7.3f}'
#     value = "Age: " + str(user.age) + " yrs" + " | "
#     value += "Gender: " + user.gender + " | "
#     value += "Weight: " + floatingPointFormatter.format(user.weight) + " lbs" + " | "
#     value += "Height: " + floatingPointFormatter.format(user.height) + " cm" + " | "
#     value += " BMI: " + floatingPointFormatter.format(user.bmi) + " | "
#     value += "BFP: " + floatingPointFormatter.format(user.bfp) + "%" + " | "
#     value += "Blood Pressure: (" + str(user.bp[0]) + "," + str(user.bp[1]) + ")" + " mmHg" + " | "
#     value += "Blood Pressure Category: " + user.bpCategory + " | "
#     # value += "User Category: " + str(user.category) + " | "
#     value += "Pulse Rate: " + str(user.pulse) + " /min" + " | "
#     value += "User ID: " + str(user.userID) + " | "
#     value += "Device ID: " + str(user.deviceID) + " | "
#     value += "Location: Lat: " + user.lat + ", Lon: " + user.lon + " | "
#     value += "Current NodeID: " + user.node_id + " | "
#     value += "Current WayID: " + user.way_id
#     print value
#     # return value


def getUser_FITBIT(user):
    value = str(user.userID) + ","
    value += user.lat + ","
    value += user.lon + ","
    value += str(user.pulse) + ","
    value += user.temp + ","
    value += str(user.age) + ","
    value += user.bpCategory
    return value


def getHost(value=0):
    if value == 1:
        return 'localhost:9092'
    else:
        return 'DIN16000309:9092'  # Enter any other host server id here


def send_To_Kafka_User_Details(timestring, user):
    """
    Sends an user data to Kafka. Serves as the kafka-producer.
    :param user: usr.user object : user from the MUL
    :return: None
    """
    stringFormatter = '{:13.0f}'
    producer_Topic_1 = 'fitbit'
    producer = KafkaProducer(bootstrap_servers='localhost:9092')
    # message = printUserDetails(user)
    message = producer_Topic_1 + "," + str(timestring) + "," + getUser_FITBIT(user) + "," + stringFormatter.format(
        time.time() * 1000)
    producer.send(producer_Topic_1, message)
    producer.flush()


def getUser_Details(user):
    floatingPointFormatter = '{:7.3f}'
    value = str(user.age) + ","
    value += user.gender + ","
    value += category.user_Category[user.category] + ","
    value += floatingPointFormatter.format(user.weight) + ","
    value += floatingPointFormatter.format(user.height) + ","
    value += floatingPointFormatter.format(user.bmi) + ","
    value += floatingPointFormatter.format(user.bfp) + ","
    value += user.bpCategory + ","
    value += str(user.bp[0]) + "," + str(user.bp[1]) + ","
    value += str(user.userID) + ","
    value += str(user.deviceID)
    return value


def send_To_Kafka_NewUser(user):
    """
    Sends the time to Kafka. Redundant at this point. Just for testing purpose being used.
    :return: None
    """
    producer_Topic_1 = 'new-user-notification'
    producer = KafkaProducer(bootstrap_servers='localhost:9092')
    message = producer_Topic_1 + "," + getUser_Details(user)
    producer.send(producer_Topic_1, message)
    producer.flush()


def send_To_Kafka_CountOfUsers(count, timestring):
    stringFormatter = '{:13.0f}'
    producer_Topic_1 = 'user-list-length'
    producer = KafkaProducer(bootstrap_servers='localhost:9092')
    message = "(" + str(1) + "," + stringFormatter.format(time.time() * 1000) + ")"
    producer.send(producer_Topic_1, message)
    producer.flush()


def send_To_Kafka_Sales(date, count):
    producer_Topic_1 = 'sales'
    producer = KafkaProducer(bootstrap_servers='localhost:9092')
    message = producer_Topic_1 + "," + str(date) + "," + str(count)
    producer.send(producer_Topic_1, message)
    producer.flush()

    # print np.std([1.0, 2.0])
