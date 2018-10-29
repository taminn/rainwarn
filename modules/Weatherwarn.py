import sys
import os
import time

import Save
import weather
import Window

def Warn():
    city=Save.get_city()
    if city==None:
        return
    msg = []
    weather_info = weather.get_weather_info(city[1])

    if weather_info == None:
        return []
    if weather_info.today_rain and weather_info.tomorrow_rain:
        msg.append("今明两天的天气是{weather}  出门留心天气".format(
            weather=weather_info.tomorrow_wearther))
    elif weather_info.today_rain:
        msg.append("今天的天气是{weather}  出门留心天气".format(
            weather=weather_info.today_weather))
    elif weather_info.tomorrow_rain:
        msg.append("明天的天气是{weather}  出门留心天气".format(
            weather=weather_info.tomorrow_wearther))
    if int(weather_info.today_max_tmp)-int(weather_info.tomorrow_max_tmp) >= 10:
        msg.append("明天的最高气温是{tmp}℃\n  降温较强记得增添衣物\n".format(
            tmp=weather_info.tomorrow_max_tmp))
    elif int(weather_info.tomorrow_max_tmp) >= 37:
        msg.append("明天的最高气温是:{tmp}℃\n气温过高  注意防暑\n".format(
            tmp=weather_info.tomorrow_max_tmp))
    if len(msg) > 0:
        Window.MessageBox(msg)

if __name__=='__main__':
    Warn()