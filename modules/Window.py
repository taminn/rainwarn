import tkinter
import sys
import os
import threading
import time

import Save
import weather

def format_msg(msg):
    if type(msg) is type(''):
        if msg=='':return ''
        msg = [msg,]
    res = ""
    word_len = 0
    for i in msg:
        for ch in i:
            if '\u4e00' <= ch <= '\u9fff':
                word_len += 3
            elif ch == '\n':
                word_len = 0
            elif 'A'<=ch<='Z':
                word_len+=2
            elif 'a'<=ch<='z':
                word_len+=1.6
            else:
                word_len+=1.8
            res += ch
            if word_len > 51:
                res += '\n'
                word_len = 0
        if res[-1] != '\n':
            res += '\n'
        res += '\n'
    return res

def get_date():
    current_date=time.localtime()[:3]
    def chinses_number(x):
        arr=['零','一','二','三','四','五','六','七','八','九','十']
        if x<=10:return arr[x]
        elif x<20:return '十'+chinses_number(x%10)
        elif x%10==0:return chinses_number(x//10)+'十'
        else: return chinses_number(x//10)+'十'+chinses_number(x%10)
    return chinses_number(current_date[1])+'月'+chinses_number(current_date[2])+'日'

def get_weather(city_id):
    info=weather.get_weather_info(city_id)
    if info==None:return ''
    return '雨' if info.today_rain else '晴'

def show(msg,weather,city):
    msg = format_msg(msg)
    window = tkinter.Tk()
    window.wm_attributes('-topmost',1)
    window.bind("<Double-Button-1>", lambda x,ob=window:ob.destroy())
    window.title('')
    window.overrideredirect(True)  # 取消边框
    window.attributes("-alpha", 1)  # 背景色
    window.geometry("450x300+1070+510")
    os.chdir(sys.path[0])
    #这里的路径需要注意
    try:
        photo = tkinter.PhotoImage(file="./modules/backimage/backimage.gif")
    except:
        photo = tkinter.PhotoImage(file='./backimage/backimage.gif')
    canvas = tkinter.Canvas(window, bg='white', height=300,
                            width=450, highlightthickness=0)
    canvas.create_image(0, 0, anchor='nw', image=photo)
    canvas.create_text(30, 25, text=msg, font=(
        '华文新魏', '17'), anchor='nw', fill='#FFFFFF')
    canvas.create_text(405,250,text=get_date()+'  '+weather,font=(
        '华文新魏', '17'), anchor='se', fill='#FFFFFF')
    canvas.pack()
    canvas.create_text(420,275,text='﹏ '+city+' ﹏',font=(
        '华文新魏', '16'), anchor='se', fill='#FFFFFF')
    canvas.pack()
    window.mainloop()


class MessageBox():
    last_thread=None  #链式的线程队列
    user_city=Save.get_city()
    if user_city==None:
        user_city=('未设置居住城市','')
        today_weather=''
    else:
        today_weather=get_weather(user_city[1])

    def __init__(self,msg):
        self.last_thread=MessageBox.last_thread
        self.current_thread=threading.Thread(target=show,args=(msg,MessageBox.today_weather,MessageBox.user_city[0]))
        MessageBox.last_thread=self.current_thread
        if self.last_thread!=None:
            self.last_thread.join()
        self.current_thread.start()


if __name__=='__main__':
    MessageBox("")