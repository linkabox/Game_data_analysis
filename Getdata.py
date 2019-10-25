# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 09:38:46 2017

@author: tanyu.mobi
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
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


def parsepage(html):
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
                comment_time = child_spans[j]['data-dynamic-time']
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
        list = []
        list.append(user_name)
        list.append(user_id)
        list.append(sex)
        list.append(comment_time)
        list.append(play_time)
        list.append(score)
        list.append(comment)
        list.append(phone)
        list.append(happy)
        list.append(like)
        list.append(unlike)
        list.append(web)
        all_data.append(list)


all_data = []
maxPage = 5
appId = 177088
for i in range(0, maxPage):
    i = i+1
    url = 'https://www.taptap.com/app/{0}/review?order=default&page={1}#review-list'.format(appId, i)
    html = GetHtmlText(url)
    parsepage(html)
    print("finish:"+url)
    # time.sleep(5)
data = pd.DataFrame(all_data, columns=['user_name', 'user_id', 'sex', 'comment_time',
                                       'play_time', 'score', 'comment', 'phone', 'happy', 'like', 'unlike','link'])
data.to_csv('./taptap_{0}.csv'.format(appId), encoding='gb18030', index=False)
# data.to_json('./taptap_{0}.json'.format(appId))
print("all done")
