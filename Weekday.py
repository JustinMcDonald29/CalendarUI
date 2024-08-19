from enum import Enum

class Weekday(Enum):
    SUN1 = 11
    SUN2 = 12
    SUN3 = 13
    SUN4 = 14
    SUN5 = 15
    MON1 = 21
    MON2 = 22
    MON3 = 23
    MON4 = 24
    TUES1 = 31
    TUES2 = 32
    TUES3 = 33
    TUES4 = 34
    TUES5 = 35
    WED1 = 41
    WED2 = 42
    WED3 = 43
    WED4 = 44
    WED5 = 45
    THURS1 = 51
    THURS2 = 52
    THURS3 = 53
    THURS4 = 54
    THURS5 = 55
    FRI1 = 61
    FRI2 = 62
    FRI3 = 63
    FRI4 = 64
    SAT1 = 71
    SAT2 = 72
    SAT3 = 73
    SAT4 = 74
    SAT5 = 75


    @classmethod
    def from_dict(cls, slots):
        out = list()
        days = ("Sun", "Mon", "Tues", "Wed", "Thurs", "Fri", "Sat")
        hours = ("6", "7", "8", "9", "10")
        for k in slots:
            for item in slots[k]:
                entry = Weekday((days.index(k) + 1) * 10 + (hours.index(item.split(":")[0]) + 1))
                if int(item[0]) == 6 or int(item[0]) == 9 or int(item[0]) == 10: 
                    out.append(entry)
                else:
                    out.insert(0, entry)
        out.sort(key = lambda day: day.value)
        return out
    
    @classmethod
    def to_string(cls, weekday):
        if int(str(weekday.value)[0]) == 2 or int(str(weekday.value)[0]) == 6:
            suf = ":30"
        else:
            suf = ":00"
        out = (str.capitalize("".join([char for char in weekday.name if char.isalpha()]))) + " " + str(weekday.value + 5) + suf


    @classmethod
    def t_print(cls):
        return True


