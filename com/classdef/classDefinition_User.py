import com.map.age_Weight_Heigt_Map_Kids as wt_ht_map
import com.map.bp_Limit_Map as bp
import random as rn
import math
import numpy as np
import uuid
from kafka import KafkaProducer


class user(object):
    # We'll be using the __init__ as a constructor for noActivity level
    def __init__(self, age, gender, category):
        self.age = age
        self.gender = gender
        [self.weight, self.height] = determine_Height_And_Weight(age, gender)
        self.bmi = determine_BMI(self.weight, self.height)
        self.bfp = determine_BFP(self.age, self.gender, self.bmi)
        self.bp, self.bpCategory = determine_BP(self.age, category)
        self.userID, self.deviceID = uuid.uuid1(), uuid.uuid4()

    #
    # @classmethod
    # def veryActive(self, age, gender):
    #     self.age = age
    #     self.gender = gender
    #     [self.weight, self.height] = determine_Height_And_Weight(age, gender)
    #     self.bmi = determine_BMI(self.weight, self.height)
    #     self.bfp = determine_BFP(self.age, self.gender, self.bmi)
    #     self.bp, self.bpCategory = determine_BP(self.age, 5)
    #     self.userID, self.deviceID = uuid.uuid1(), uuid.uuid4()
    #     return self
    #     # print 1
    #
    # @classmethod
    # def moderatelyActive(self, age, gender):
    #     self.age = age
    #     self.gender = gender
    #     [self.weight, self.height] = determine_Height_And_Weight(age, gender)
    #     self.bmi = determine_BMI(self.weight, self.height)
    #     self.bfp = determine_BFP(self.age, self.gender, self.bmi)
    #     self.bp, self.bpCategory = determine_BP(self.age, 4)
    #     self.userID, self.deviceID = uuid.uuid1(), uuid.uuid4()
    #     return self
    #     # print 2
    #
    # @classmethod
    # def lightlyActive(self, age, gender):
    #     self.age = age
    #     self.gender = gender
    #     [self.weight, self.height] = determine_Height_And_Weight(age, gender)
    #     self.bmi = determine_BMI(self.weight, self.height)
    #     self.bfp = determine_BFP(self.age, self.gender, self.bmi)
    #     self.bp, self.bpCategory = determine_BP(self.age, 3)
    #     self.userID, self.deviceID = uuid.uuid1(), uuid.uuid4()
    #     return self
    #     # print 3
    #
    # @classmethod
    # def sedentary(self, age, gender):
    #     self.age = age
    #     self.gender = gender
    #     [self.weight, self.height] = determine_Height_And_Weight(age, gender)
    #     self.bmi = determine_BMI(self.weight, self.height)
    #     self.bfp = determine_BFP(self.age, self.gender, self.bmi)
    #     self.bp, self.bpCategory = determine_BP(self.age, 2)
    #     self.userID, self.deviceID = uuid.uuid1(), uuid.uuid4()
    #     return self


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
            return [weight,height]


def determine_BMI(weight,height):
    """
    Function returns the BMI (Body Mass Index) of the user given weight and height.
    The function incorporates all the conversions required to calculate BMI from lbs and cms.
    :param weight: float : weight of user (in lbs)
    :param height: float : height of user (in cms)
    :return: float : bmi of user
    """
    bmi = float((weight * 703)/ math.pow((height * 0.393701 ), 2))
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
            bfp = (1.51 * bmi) - (0.70 * age) - (3.6) + 1.4
            return bfp
        elif gender == "F":
            bfp = (1.51 * bmi) - (0.70 * age) + 1.4
            return bfp
    elif age > 16:
        if gender == "M":
            bfp = (1.20 * bmi) + (0.23 * age) - (10.8) - 5.4
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
    if activityFlag == 5: # for VeryActive Users
        # respective weights of the blood pressure categories
        bpWts = np.array([7, 80, 7, 4, 1, 1])
        bpWts = bpWts/100.0
        # blood pressure categories
        bpChoices = ["LOW", "NORMAL", "PREHYP", "HYP_1", "HYP_2", "HYP_CR"]
        # choice is a numpy array element containing 1 single string value in its 0th element.
        choice = np.random.choice(bpChoices, 1, p=bpWts)[0]
        bpList = returnBP_Value(choice, age)
        return bpList, choice

    elif activityFlag == 4:  # for ModeratelyActive Users
        # respective weights of the blood pressure categories
        bpWts = np.array([10, 65, 10, 8, 6, 1])
        bpWts = bpWts/100.0
        # blood pressure categories
        bpChoices = ["LOW", "NORMAL", "PREHYP", "HYP_1", "HYP_2", "HYP_CR"]
        # choice is a numpy array element containing 1 single string value in its 0th element.
        choice = np.random.choice(bpChoices, 1, p=bpWts)[0]
        bpList = returnBP_Value(choice, age)
        return bpList, choice

    elif activityFlag == 3:  # for LightlyActive Users
        # respective weights of the blood pressure categories
        bpWts = np.array([15, 50, 12, 10, 9, 4])
        bpWts = bpWts/100.0
        # blood pressure categories
        bpChoices = ["LOW", "NORMAL", "PREHYP", "HYP_1", "HYP_2", "HYP_CR"]
        # choice is a numpy array element containing 1 single string value in its 0th element.
        choice = np.random.choice(bpChoices, 1, p=bpWts)[0]
        bpList = returnBP_Value(choice, age)
        return bpList, choice

    elif activityFlag == 2:  # for Sedentary Users
        # respective weights of the blood pressure categories
        bpWts = np.array([20, 40, 15, 12, 10, 3])
        bpWts = bpWts/100.0
        # blood pressure categories
        bpChoices = ["LOW", "NORMAL", "PREHYP", "HYP_1", "HYP_2", "HYP_CR"]
        # choice is a numpy array element containing 1 single string value in its 0th element.
        choice = np.random.choice(bpChoices, 1, p=bpWts)[0]
        bpList = returnBP_Value(choice, age)
        return bpList, choice

    elif activityFlag == 1:  # for NoActive Users
        # respective weights of the blood pressure categories
        bpWts = np.array([25, 20, 20, 18, 10, 7])
        bpWts = bpWts/100.0
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

        [dias_Corr_Low, dias_Corr_Up] = [((diasLow - normalDiastolic)/float(age)),
                                         ((diasUp - normalDiastolic)/float(age))]
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

        [dias_Corr_Low, dias_Corr_Up] = [((diasLow - normalDiastolic)/float(age)),
                                         ((diasUp - normalDiastolic)/float(age))]
        # A random floating point value is chosen between the range for both Systolic and Diastolic Pressure
        sys_Corr_Final = rn.uniform(sys_Corr_Low, sys_Corr_Up)
        dias_Corr_Final = rn.uniform(dias_Corr_Low, dias_Corr_Up)
        # the final value is calculated as per the previous formula
        value = [math.ceil(normalSystolic + sys_Corr_Final * age), math.ceil(normalDiastolic + dias_Corr_Final * age)]
        return value


def printUserDetails(user):
    """
    Function takes in a user object and print all its elements
    :param user: user object
    :return: None
    """
    floatingPointFormatter = '{:7.3f}'
    value = "Age: " + str(user.age)+ " yrs"  + " | "
    value += "Gender: " + user.gender + " | "
    value += "Weight: " + floatingPointFormatter.format(user.weight) + " lbs" + " | "
    value += "Height: " + floatingPointFormatter.format(user.height) + " cm" +" | "
    value += " BMI: " + floatingPointFormatter.format(user.bmi) + " | "
    value += "BFP: " + floatingPointFormatter.format(user.bfp) + "%" + " | "
    value += "Blood Pressure: (" + str(user.bp[0]) + "," + str(user.bp[1]) + ")" + " mmHg" + " | "
    value += "Blood Pressure Category: " + user.bpCategory + " | "
    value += "User ID: " + str(user.userID) + " | "
    value += "Device ID: " + str(user.deviceID)
    print value
    # return value

def send_To_Kafka(user):
    producer_Topic_1 = 'python-test'
    producer = KafkaProducer(bootstrap_servers='localhost:9092')
    message = printUserDetails(user)
    producer.send(producer_Topic_1, message)
    producer.flush()

def send_Time_To_Kafka(time):
    producer_Topic_1 = 'python-test'
    producer = KafkaProducer(bootstrap_servers='localhost:9092')
    producer.send(producer_Topic_1, time)
    producer.flush()