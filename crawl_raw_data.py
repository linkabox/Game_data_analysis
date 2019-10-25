# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 09:38:46 2017

@author: tanyu.mobi
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
#r.encoding = r.apparent_encoding


def GetHtmlText(url):
    try:
        ug = {'user-agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=ug, timeout=20)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except:
        return ''

# print a.encode('gb18030')


def timestamp_datetime(value):
    format = '%Y-%m-%d %H:%M:%S'
    # value为传入的值为时间戳(整形)，如：1332888820
    value = time.localtime(value)
    # 经过localtime转换后变成
    ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=0)
    # 最后再经过strftime函数转换为正常日期格式。
    dt = time.strftime(format, value)
    return dt


def datetime_timestamp(dt):
    # dt为字符串
    # 中间过程，一般都需要将字符串转化为时间数组
    time.strptime(dt, '%Y-%m-%d %H:%M:%S')
    ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=-1)
    # 将"2012-03-28 06:53:40"转化为时间戳
    s = time.mktime(time.strptime(dt, '%Y-%m-%d %H:%M:%S'))
    return int(s)


def to_num(s):
    try:
        return int(s)
    except ValueError:
        return s


def parsepage(html):
    list = []
    soup = BeautifulSoup(html, 'html.parser')
    for i in range(len(soup.find_all('li', class_='taptap-review-item collapse in'))):
        a = soup.find_all('li', class_='taptap-review-item collapse in')[i]
        user_id = a.find('span', 'taptap-user')['data-user-id']
        web = a.find('a')['href']
        sex = a.find('a')['class'][-1]
        user_name = a.find('span', 'taptap-user').find('a').string
        child_spans = a.find('a', 'text-header-time')('span')
        for j in range(len(child_spans)):
            if child_spans[j].has_attr('data-dynamic-time'):
                field = to_num(child_spans[j]['data-dynamic-time'])
                if isinstance(field, str):
                    comment_time = field
                else:
                    comment_time = timestamp_datetime(field)
        score = int(a.find('div', 'item-text-score').find('i')
                    ['style'][-4:-2])/14
        if a.find('div', 'item-text-score').find('span') is not None:
            p_time = a.find('div', 'item-text-score').find('span').string
            play_time = p_time[4:len(p_time)]
        else:
            play_time = ''
        comment = ''
        all_p = a.find(name='div', attrs={'class': 'item-text-body'})('p')
        for j in range(len(all_p)):
            if all_p[j].text is not None:
                comment = comment + all_p[j].text
            else:
                comment = comment + str(all_p[j].text)
        if a.find('span', 'text-footer-device') is not None:
            phone = a.find('span', 'text-footer-device').string
        else:
            phone = ''
        happy = a.find(
            'ul', class_='list-unstyled text-footer-btns').find_all('span')[1].string
        like = a.find(
            'ul', class_='list-unstyled text-footer-btns').find_all('span')[2].string
        unlike = a.find(
            'ul', class_='list-unstyled text-footer-btns').find_all('span')[3].string
        user_data = []
        user_data.append(user_name)
        user_data.append(user_id)
        user_data.append(sex)
        user_data.append(comment_time)
        user_data.append(play_time)
        user_data.append(score)
        user_data.append(comment)
        user_data.append(phone)
        user_data.append(happy)
        user_data.append(like)
        user_data.append(unlike)
        user_data.append(web)
        all_data.append(user_data)

def crawl_taptap(appId,maxPage):
    for i in range(0, maxPage):
        i = i+1
        url = 'https://www.taptap.com/app/{0}/review?order=default&page={1}#review-list'.format(appId, i)
        html = GetHtmlText(url)
        parsepage(html)
        print("finish:"+url)
        # time.sleep(5)

### Main
if not os.path.exists('output'):
    os.makedirs('output')

all_data =[]
crawl_taptap(177088,5)
crawl_taptap(176951,2)

realId = 177088
data = pd.DataFrame(all_data, columns=['user_name', 'user_id', 'sex', 'comment_time',
                                        'play_time', 'score', 'comment', 'phone', 'happy', 'like', 'unlike', 'link'])
data.to_csv('./output/taptap_{0}.csv'.format(realId),encoding='utf-8', index=False)
data.to_csv('./output/taptap_{0}_xlsx.csv'.format(realId),encoding='gb18030', index=False)
# data.to_json('./taptap_{0}.json'.format(realId))
print("all done")
