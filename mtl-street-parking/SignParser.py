import re
days = ['LUN', 'MAR', 'MER', 'JEU', 'VEN', 'SAM', 'DIM']
def dayStr(index):
    return days[index]
def dayIndex(day_):
    for i in range(len(days)):
        if day_.startswith(days[i]):
            return i
    return -1
def daysInBetween(day1, day2):
    day_1 = dayIndex(day1)
    day_2 = dayIndex(day2)
    if day_1 != -1 and day_2 != -1 and day_1 < day_2:
        #return days[day_1:day_2 + 1]
        return range(day_1, day_2 + 1)
    else:
        #print(' +++ error! day1=%s, day2=%s'% (day1, day2))
        return []
def readHour(str_):
    m = re.compile('(\d\d)h:*(\d\d)-(\d\d)h:*(\d\d)').match(str_)
    if m:
        h1 = int(m.group(1)) * 60 + int(m.group(2))
        h2 = int(m.group(3)) * 60 + int(m.group(4))
        return (h1, h2)
    m = re.compile('(\d\d)h:*(\d\d) A (\d\d)h:*(\d\d)').match(str_)
    if m:
        h1 = int(m.group(1)) * 60 + int(m.group(2))
        h2 = int(m.group(3)) * 60 + int(m.group(4))
        return (h1, h2)
    m = re.compile('(\d\d)H À (\d\d)H').match(str_)
    if m:
        h1 = int(m.group(1)) * 60
        h2 = int(m.group(2)) * 60
        return (h1, h2)
    m = re.compile('(\d\d)h-(\d\d)h').match(str_)
    if m:
        h1 = int(m.group(1)) * 60 
        h2 = int(m.group(2)) * 60 
        return (h1, h2)
    m = re.compile('(\d){1}h - (\d)*h').match(str_)
    if m:
        h1 = int(m.group(1)) * 60 
        h2 = int(m.group(2)) * 60 
        return (h1, h2)
    return (-1, -1)
    
def pat1(str_):
    errs = 0
    rules = []
    
    m = re.compile('.*(\\\P)').match(str_)
    if m:
        str_ = str_[0 : str_.find(m.group(1))] + str_[ str_.find(m.group(1)) + len(m.group(1)): ]
        rules.append(['mainrule', 'noparking', ''])

    m = re.compile('.*(P)').match(str_)
    if m:
        str_ = str_[0 : str_.find(m.group(1))] + str_[ str_.find(m.group(1)) + len(m.group(1)): ]
        rules.append(['mainrule', 'parking', ''])

    m = re.compile('.*(\\\A)').match(str_)
    if m:
        str_ = str_[0 : str_.find(m.group(1))] + str_[ str_.find(m.group(1)) + len(m.group(1)): ]
        rules.append(['mainrule', 'noparking', ''])

    #print('doing str ', str_)
    m = re.compile('.*(\d\dh:*\d\d-\d\dh:*\d\d|\d\dh:*\d\d A \d\dh:*\d\d|\d\dH À \d\dH|\d\dh-\d\dh|(\d){1}h - \d*h).*').match(str_)
    if m:
        str_ = str_[0 : str_.find(m.group(1))] + str_[ str_.find(m.group(1)) + len(m.group(1)): ]
        #print(m.group(0), ' ---- ', str_)
        h1, h2 = readHour(m.group(1))
        rules.append(['hour', [h1, h2] ])
        
        
    m = re.compile('.*((\w\w\w).* AU (\w\w\w)\w*.*)').match(str_)
    if m:
        str_ = str_[0 : str_.find(m.group(1))] + str_[ str_.find(m.group(1)) + len(m.group(1)): ]
        #print(m.group(0), ' ---- ', str_)
        days_ = daysInBetween(m.group(2), m.group(3))
        #if len(days_) == 0:
            #print(m.group(0))
        rules.append(['day', days_ ])
        
    m = re.compile('.*(1 MARS AU 1 DEC\.)').match(str_)
    if m:
        str_ = str_[0 : str_.find(m.group(1))] + str_[ str_.find(m.group(1)) + len(m.group(1)): ]
        rules.append(['forsummer', [1+2*30, 1+11*30]] )

    m = re.compile('.*(1 AVRIL AU 1 DEC\.)').match(str_)
    if m:
        str_ = str_[0 : str_.find(m.group(1))] + str_[ str_.find(m.group(1)) + len(m.group(1)): ]
        rules.append(['forsummer', [1+3*30, 1+11*30]])
        
    m = re.compile('.*(1er AVRIL - 30 NOV)').match(str_)
    if m:
        str_ = str_[0 : str_.find(m.group(1))] + str_[ str_.find(m.group(1)) + len(m.group(1)): ]
        rules.append(['forsummer', [1+3*30, 11*30]])

    m = re.compile('.*(1ER AVRIL - 30 NOV)').match(str_)
    if m:
        str_ = str_[0 : str_.find(m.group(1))] + str_[ str_.find(m.group(1)) + len(m.group(1)): ]
        rules.append(['forsummer', [1+3*30, 11*30]])

    m = re.compile('.*(15 MARS AU 15 NOV)').match(str_)
    if m:
        str_ = str_[0 : str_.find(m.group(1))] + str_[ str_.find(m.group(1)) + len(m.group(1)): ]
        rules.append(['forsummer', [15+2*30, 15+10*30]])

        
    m = re.compile('.*(LUNDI|MARDI|MERCREDI|JEUDI|VENDREDI|SAMDI|DIMANCHE)\.*').match(str_)
    if m:
        str_ = str_[0 : str_.find(m.group(1))] + str_[ str_.find(m.group(1)) + len(m.group(1)): ]
        rules.append(['day', [dayIndex(m.group(1))] ])
        
    m = re.compile('.*(LUN|MAR|MER|JEU|VEN|SAM|DIM)\.*').match(str_)
    if m:
        str_ = str_[0 : str_.find(m.group(1))] + str_[ str_.find(m.group(1)) + len(m.group(1)): ]
        rules.append(['day', [dayIndex(m.group(1))] ] )
        
    return (rules, str_)

def doPat(str_):
    l1 = len(str_)
    rules = []
    while True:
        newrules, str_ = pat1(str_)
        if len(newrules) == 0:
            break
        else:
            rules.extend(newrules)
    
    #post-process rules
    finalrules = []
    dayss = []
    for rule in rules:
        if rule[0] == 'day':
            dayss.extend(rule[1])
        else:
            finalrules.append(rule)
    finalrules.append(['day', dayss])
    return (finalrules, str_)