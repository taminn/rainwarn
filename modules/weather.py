from urllib import request
import json
import sys
import os
import time

import Save

class weather:
    def __init__(self):
        self.today_weather=''
        self.tomorrow_wearther=''
        self.today_min_tmp=''
        self.today_max_tmp=''
        self.tomorrow_min_tmp=''
        self.tomorrow_max_tmp=''

def get_weather_info(city_id):
    url = "https://free-api.heweather.com/s6/weather/forecast?location={city_id}&key=8d1050f774c04190a70c7e62aa088a22".format(city_id=city_id)
    time_cnt=0
    while time_cnt<600:
        try:
            html = request.urlopen(url)
            text = html.read().decode('utf-8')
            break
        except:
            time_cnt+=10
            time.sleep(10)
    else:
        return None
    try:
        info = json.loads(text)
        info = info["HeWeather6"][0]
        weather_info = weather()
        weather_info.today_weather = info['daily_forecast'][0]['cond_txt_d']
        weather_info.tomorrow_wearther = info['daily_forecast'][1]['cond_txt_d']
        weather_info.today_min_tmp = info['daily_forecast'][0]['tmp_min']
        weather_info.today_max_tmp = info['daily_forecast'][0]['tmp_max']
        weather_info.tomorrow_min_tmp = info['daily_forecast'][1]['tmp_max']
        weather_info.tomorrow_max_tmp = info['daily_forecast'][1]['tmp_max']
        for i in weather_info.today_weather:
            if i == '雨' or i == '雪':
                weather_info.today_rain = True
                break
        else:
            weather_info.today_rain = False
        for i in weather_info.tomorrow_wearther:
            if i == '雨' or i == '雪':
                weather_info.tomorrow_rain = True
                break
        else:
            weather_info.tomorrow_rain = False
        return weather_info
    except:
        return None
