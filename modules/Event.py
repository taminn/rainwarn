import time
import datetime


def calc_weekday(y, m, d):
    if m == 1 or m == 2:
        m += 12
        y -= 1
    return (d+2*m+3*(m+1)//5+y+y//4-y//100+y//400+1) % 7


class event_time():
    def __init__(self, year=0, month=0, day=0, hour=0, minute=0):
        self.year, self.month, self.day, self.hour, self.minute = year, month, day, hour, minute
        self.weekday = -1

    def value(self):
        if self.year == -1 or self.month == -1 or self.day == -1 or self.hour == -1 or self.minute == -1:
            return float('inf')
        else:
            return self.year*600000+self.month*45000+self.day*1440+self.hour*60+self.minute

    def __add__(self, x):
        month_day_num = [31, 29 if (self.year % 4 == 0 and self.year % 100 != 0 or self.year %
                                    400 == 0) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        res = event_time(self.year+x.year, self.month+x.month,
                         self.day+x.day, self.hour+x.hour, self.minute+x.minute)
        if res.minute > 60:
            res.hour += res.minute//60
            res.minute %= 60
        if res.hour > 24:
            res.day += res.hour//24
            res.hour %= 24
        while res.day > month_day_num[res.month-1]:
            self.day -= month_day_num[self.month-1]
            self.month += 1
            if self.month > 12:
                self.month = 1
                self.year += 1
                month_day_num[1] = 29 if (
                    self.year % 4 == 0 and self.year % 100 != 0 or self.year % 400 == 0) else 28

    def __eq__(self, x):
        return ((self.year == x.year or self.year == -1 or x.year == -1)
                and (self.month == x.month or self.month == -1 or x.month == -1)
                and (self.day == x.day or self.day == -1 or x.day == -1)
                and (self.hour == x.hour or self.hour == -1 or x.hour == -1)
                and (self.minute == x.minute or self.minute == -1 or x.minute == -1)
                and (self.weekday == x.weekday or self.weekday == -1 or x.weekday == -1))

    def __lt__(self, x):
        if self.year != -1 and x.year != -1 and self.year != x.year:
            return self.year < x.year
        elif self.year == -1 or x.year == -1 or self.year == x.year:
            if self.month != -1 and x.month != -1 and self.month != x.month:
                return self.month < x.month
            elif self.month == -1 or x.month == -1 or self.month == x.month:
                if self.day != -1 and x.day != -1 and self.day != x.day:
                    return self.day < x.day
                elif self.day == -1 or x.day == -1 or self.day == x.day:
                    if self.hour != -1 and x.hour != -1 and self.hour != x.hour:
                        return self.hour < x.hour
                    elif self.hour == -1 or x.hour == -1 or self.hour == x.hour:
                        if self.minute != -1 and x.minute != -1 and self.minute != x.minute:
                            return self.minute < x.minute
        return False

    def __gt__(self, x):
        return not (self < x or self == x)

    def __ge__(self, x):
        return not self < x

    def __str__(self):
        return "%d年%d月%d日%d时%d分" % (self.year, self.month, self.day, self.hour, self.minute)


def get_current_time():
    sys_time = time.localtime()
    return event_time(sys_time[0], sys_time[1], sys_time[2], sys_time[3], sys_time[4])


class event:
    def __init__(self, warn_name, warn_info):
        self.name = warn_name
        self.info = warn_info

    def __str__(self):
        return self.name+'\n'+self.info


class warn_info:
    def __init__(self, event, warnloop, warntime, key):
        self.event = event
        self.warn_loop = warnloop  # 1:once, 2:day, 3:week
        self.warntime = warntime
        self.key = key

    def __str__(self):
        return self.event.name+':'+self.event.info
