import os
import sys
import time

import Save
import Event
import Window

def get_warn_queue():
    events=Save.get_events()
    current_time=Event.get_current_time()
    warn_queue=[]
    if 'once' in events:
        for i in events['once']:
            if i.warntime>=current_time:
                warn_queue.append(i)
    if 'week' in events:
        weekday=Event.calc_weekday(current_time.year,current_time.month,current_time.day)
        for i in events['week']:
            if i.warntime.weekday==weekday:
                warn_queue.append(i)
    if 'day' in events:
        warn_queue+=events['day']
    warn_queue.sort(key=lambda x: (x.warntime.hour*60+x.warntime.minute))
    return warn_queue

def calc_wait_time(next_warn_time):
    current_time=Event.get_current_time()
    if current_time>next_warn_time:
        return -1
    if next_warn_time.hour==-1:
        wait_time = 60*(next_warn_time.minute-current_time.minute)-time.localtime()[5]
        return wait_time if wait_time>0 else 0
    if next_warn_time.minute<current_time.minute:
        next_warn_time.minute+=60
        next_warn_time.hour-=1
    wait_time = 60*(next_warn_time.minute-current_time.minute+60*(next_warn_time.hour-current_time.hour))-time.localtime()[5]
    return wait_time if wait_time>0 else 0

def Warn():
    warn_queue=get_warn_queue()
    current_time=Event.get_current_time()
    cnt=len(warn_queue)
    for i in range(cnt):
        if warn_queue[0].warntime<current_time:
            warn_queue.pop(0)
    while len(warn_queue)>0:
        warn=warn_queue.pop(0)
        wait_time=calc_wait_time(warn.warntime)
        if wait_time<0:continue
        time.sleep(wait_time)
        Window.MessageBox(warn.event.info)

if __name__=='__main__':
    Warn()