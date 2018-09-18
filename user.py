import os
import sys

if __name__ == '__main__':
    sys.path.append(sys.path[0]+'\\modules')

import Save
import Event


def create():
    name = input("输入事件名称:")
    info = input("输入事件信息:")
    loop = int(input("选择提醒周期  1:一次  2:每天  3:每周\n:"))
    time = Event.event_time(-1, -1, -1, -1, -1)
    print('设置提醒时间')
    if loop == 1:
        time.year = int(input('输入年份:'))
        time.month = int(input('输入月份:'))
        time.day = int(input('输入天数:'))
        time.hour = int(input('输入小时:'))
        time.minute = int(input('输入分钟:'))
    elif loop == 2:
        time.hour = int(input('输入小时:'))
        time.minute = int(input('输入分钟:'))
    elif loop == 3:
        time.week = int(input('输入周几:'))
        time.hour = int(input('输入小时:'))
        time.minute = int(input('输入分钟:'))
    else:
        print("无效值")
        return
    Save.add_warn(Event.warn_info(Event.event(
        name, info), loop, time, Save.get_count()))


def show():
    events_list = Save.get_events()
    for events in events_list.values():
        for e in events:
            print('编号:'+str(e.key)+'  事件名:'+e.event.name+'  提示信息:'+e.event.info)


def remove():
    print('事件列表')
    show()
    key = int(input('输入想删除的事件的编号:'))
    Save.remove_warn(key)


while True:
    print('输入选项选定功能')
    print('1:设置居住城市\n2:创建新提醒\n3:删除提醒\n4:显示提醒\n其他值:退出')
    op = int(input(':'))
    if op == 1:
        city = input('输入居住城市中文名:')
        citys = Save.query_city(city)
        if citys == None:
            print('没有找到你输入的城市  换个大地名试试')
        else:
            print('找到这些城市:')
            cnt = 1
            for i in citys:
                print(str(cnt)+':'+i[0]+'-'+city)
                cnt += 1
            n = int(input('输入你所在城市的编号:'))
            Save.set_city((city, citys[n-1][1]))
    elif op == 2:
        create()
    elif op == 3:
        remove()
    elif op == 4:
        show()
    else:
        break
