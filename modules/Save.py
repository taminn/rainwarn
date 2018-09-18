import pickle
import os
import sys
import time

import Event

def get_current_date():
    return time.localtime()[:3]

def read_file(file_name,mode='rb'):
    os.chdir(sys.path[0])
    if sys.path[0].find('modules')!=-1:
        path='./data/'+file_name
    else:
        path='./modules/data/'+file_name
    try:
        file = open(path, mode)
        date= file.read()
        file.close()
        return date
    except:
        return None


def write_file(file_name,data,mode='wb'):
    os.chdir(sys.path[0])
    if sys.path[0].find('modules')!=-1:
        path='./data/'+file_name
    else:
        path='./modules/data/'+file_name
    try:
        file = open(path, mode)
        file.write(data)
        file.close()
        return True
    except:
        return False

                
def Load_info():
    file=read_file('user.data')
    if file==None:
        return {'city': None, 'count':0, 'once': [], 'week': [], 'day': []}
    info = pickle.loads(file, encoding='GBK')
    return info


def Save_info(info):
    data=pickle.dumps(info)
    return write_file('user.data',data)

class record:
    info=None
    def __init__(self):
        if record.info==None:
            date=get_current_date()
            file=read_file('warn.record')
            if file==None:
                records=set()
            else:
                old_record = pickle.loads(file,encoding='GBK')
                if old_record['date'] != date:
                    records=set()
                else:records=old_record['records']  # warn 应该是一个set
            record.info={'date':date,'records':records}
    def have(self,data):
        return data in record.info['records']
    
    def add(self,data):
        if data not in record.info['records']:
            record.info['records'].add(data)
            new_record=pickle.dumps(record.info)
            write_file('warn.record',new_record)

def get_city():
    return Load_info()['city']

def get_events():
    info=Load_info()
    del info['city']
    del info['count']
    return info

def add_warn(warn):
    info=Load_info()
    current_time=Event.get_current_time()
    for i in info['once']:
        if i.warntime<current_time:
            info['once'].remove(i)
    if warn.warn_loop==1:
        info['once'].append(warn)
    elif warn.warn_loop==2:
        info['day'].append(warn)
    elif warn.warn_loop==3:
        info['week'].append(warn)
    info['count']+=1
    Save_info(info)

def set_city(city):
    info=Load_info()
    info['city']=city
    Save_info(info)

def get_count():
    info=Load_info()
    return info['count']

def remove_warn(key):
    info=Load_info()
    p=0
    for i in info['once']:
        if i.key==key:
            del info['once'][p]
            Save_info(info)
            return True
        else:
            p+=1
    p=0
    for i in info['day']:
        if i.key==key:
            del info['day'][p]
            Save_info(info)
            return True
        else:
            p+=1
    p=0
    for i in info['week']:
        if i.key==key:
            del info['week'][p]
            Save_info(info)
            return True
        else:
            p+=1
    return False


def query_city(city_name):
    data=read_file('citys.data')
    citys=pickle.loads(data)
    if city_name in citys:
        return citys[city_name]
    else:
        return None

