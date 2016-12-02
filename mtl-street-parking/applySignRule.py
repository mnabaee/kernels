from time import gmtime, strftime
import time, datetime
from datetime import datetime
import calendar

HALF_PARAM = 0.80

def epochInMins():
    return int(time.time() / 60)
print( epochInMins() )

def parseEpochInMins(epochInMins):
    #print('epoch', epochInMins)
    dt = datetime.fromtimestamp(epochInMins*60)
    
    startDayInYear = (dt.month-1)*30 + dt.day
    startDayInWeek = dt.weekday()
    startTimeInDay = dt.hour * 60 + dt.minute
    return (startDayInYear, startDayInWeek, startTimeInDay)

def getForSummer(signRules):
    for rule in signRules:
        if rule[0] == 'forsummer':
            return rule[1]
    return None
def getDays(signRules):
    for rule in signRules:
        if rule[0] == 'day':
            return rule[1]
    return None
def getHour(signRules):
    for rule in signRules:
        if rule[0] == 'hour':
            return rule[1]
    return None
def getNumHourRules(signRules):
    cnt = 0
    for rule in signRules:
        if rule[0] == 'hour':
            cnt += 1
    return cnt
def getMainRule(signRules):
    if signRules[0][0] == 'mainrule' and signRules[0][1] == 'noparking':
        return 'noparking'
    if signRules[0][0] == 'mainrule' and signRules[0][1] == 'parking':
        return 'parking'
    return 'noparking'
            
def getDurationCanPark(mainrule, signHour, startHourInDay):
    if signHour[0] > signHour[1]:
        if (startHourInDay >= signHour[1] or startHourInDay < signHour[0]) and mainrule == 'noparking':
            return -1
        elif (startHourInDay >= signHour[1]) and mainrule == 'parking':
            return 24*60 - startHourInDay + signHour[0]
        elif (startHourInDay < signHour[0]) and mainrule == 'parking':
            return signHour[0] - startHourInDay
        elif mainrule == 'noparking':
            return signHour[0] - startHourInDay
        elif mainrule == 'parking':
            return -1
        #print(' ERROR!!! Hour Range for Sign is bad!', signHour)
        #return -1
    if mainrule == 'noparking':
        if startHourInDay >= signHour[0] and startHourInDay < signHour[1]:
            return -1
        elif startHourInDay < signHour[0]:
            return signHour[0] - startHourInDay
        else:
            return 24*60 - startHourInDay
            
    elif mainrule == 'parking':
        if startHourInDay < signHour[0] and startHourInDay > signHour[1]:
            return -1
        else:
            return signHour[1] - startHourInDay

def applySign_(signRules, startTime, duration):
    startDayInYear, startDayInWeek, startTimeInDay = startTime
    #print(startDayInYear, startDayInWeek, startTimeInDay)
    
    #Check summer/winter
    forsummerRange = getForSummer(signRules)
    if forsummerRange != None:
        if startDayInYear < forsummerRange[0] or startDayInYear > forsummerRange[1]:
            if getMainRule(signRules) == 'noparking':
                return 'green'
            else:
                return 'red'
    
    days = getDays(signRules)
    if days != None:
        if not startDayInWeek in days:
            if getMainRule(signRules) == 'noparking':
                #print('green', days)
                return 'green'
            else:
                return 'red'
        
    hours = getHour(signRules)
    if hours != None:
        timeWeHave_ = getDurationCanPark(getMainRule(signRules), hours, startTimeInDay)
        #print(timeWeHave_)
        if timeWeHave_ == -1:
            return 'red'
        elif timeWeHave_ >= HALF_PARAM * duration:
            return 'green'
        else:
            return 'orange'
    
    if getMainRule(signRules) == 'noparking':
        return 'red'
    else:
        return 'green'
        
    
def applySign(signRules, startTimeInEpochMins, durationInMIns):
    if type(signRules) == str:
        ldict = locals()
        exec('e=' + signRules ,globals(), ldict)
        #print(ldict['e'])
        signRules = ldict['e']
    return applySign_(signRules, parseEpochInMins(startTimeInEpochMins), durationInMIns)