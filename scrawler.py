# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 18:46:14 2019

@author: USER
"""

import re
import datetime
import requests
from bs4 import BeautifulSoup
import time
import operator
import pandas as pd
import os



def crawl():
    ini_index = 2324
    fin_index = 2758
    
    index = ini_index
    
    #網頁標頭省力
    ptt = 'https://www.ptt.cc'
    
    #架設環境
    r = over18_set()
    
    f1 = open('text.txt','w',encoding = "utf-8")
    f2 = open('text2.txt','w',encoding = "utf-8")
    
    for idx in range(fin_index-ini_index+1):
    #for idx in range(10):        
        
        #起始頁
        url = "https://www.ptt.cc/bbs/Beauty/index{}.html".format(index+idx)
        
        soup = soup_set(r,url)
                
        date = soup.select('div.r-ent div.date')
        title = soup.select('div.r-ent div.title')
        regrex = re.compile('([ ]*[0-9]*)/([0-9]*)')
        num = soup.select('div.r-ent div.nrec')

        for i in range(len(date)):
            try:
                if title[i].a.text.find('公告') != -1:
                    continue
            except:
                continue
            else:
                z = regrex.match(date[i].text)
                date_tr = z.group(1) + z.group(2)
                if (index+idx) == ini_index and date_tr == '1231':
                    continue
                if (index+idx) == fin_index and date_tr == ' 101':
                    continue
                
                txt = date_tr+','+title[i].a.text+','+ptt+title[i].a['href']
                f1.write(txt)
                f1.write('\n')
                try:
                    if num[i].span.text == '爆':
                        f2.write(txt)
                        f2.write('\n')
                except:
                    continue
        time.sleep(0.06)
    f1.close()
    f2.close()

def Push(start_date,end_date):
    
    start_date = int(start_date)
    end_date = int(end_date)
    
    ini_index = 2324
    fin_index = 2758
    
    count_like_dict = {}
    count_boo_dict = {}
    all_like = 0
    all_boo = 0
    
    #網頁標頭省力
    ptt = 'https://www.ptt.cc'
    
    #架設環境
    r = over18_set()
    
    time.sleep(0.06)
    
    if start_date == 101 :

        start = ini_index+1
        url = "https://www.ptt.cc/bbs/Beauty/index{}.html".format(ini_index)
        soup = soup_set(r,url)
        date = soup.select("div.r-ent div.date")
        title = soup.select("div.r-ent div.title")
        
        for j in range(len(title)):
        
            if date_trans(date[j].text) == 1231:
                continue
                        
            try:
                url = ptt+title[j].a['href']
            except:
                continue
            else:
                soup = soup_set(r,url)
                push = soup.select("div.push span.hl.push-tag")
                user_id = soup.select("div.push span.f3.hl.push-userid")
                for k in range(len(push)):
                    if push[k].text == '推 ':
                        all_like += 1
                        if user_id[k].text in count_like_dict:
                            count_like_dict[user_id[k].text] += 1
                        else:
                            count_like_dict[user_id[k].text] = 1
                    elif push[k].text == '噓 ':
                        all_boo += 1
                        if user_id[k].text in count_boo_dict:
                            count_boo_dict[user_id[k].text] += 1
                        else:
                            count_boo_dict[user_id[k].text] =1
                time.sleep(0.06)        
        time.sleep(0.06)
        
    else:
        for i in range(ini_index+1,fin_index):
            url = "https://www.ptt.cc/bbs/Beauty/index{}.html".format(i)
            soup = soup_set(r,url)
            date = soup.select("div.r-ent div.date")
            if date_trans(date[0].text) == start_date:
                start = i
                break
            elif date_trans(date[-1].text) == start_date:
                start = i
                break
            time.sleep(0.06)

    for i in range(start,fin_index):
        
        url = "https://www.ptt.cc/bbs/Beauty/index{}.html".format(i)
        soup = soup_set(r,url)
        date = soup.select("div.r-ent div.date")
        
        if date_trans(date[0].text) > end_date:
            break
        
        title = soup.select("div.r-ent div.title")
        
        for j in range(len(title)):
        
            if date_trans(date[j].text) > end_date:
                break

            try:
                url = ptt+title[j].a['href']
            except:
                continue
            else:
                soup = soup_set(r,url)
                push = soup.select("div.push span.hl.push-tag")
                user_id = soup.select("div.push span.f3.hl.push-userid")
                for k in range(len(push)):
                    if push[k].text == '推 ':
                        all_like += 1
                        if user_id[k].text in count_like_dict:
                            count_like_dict[user_id[k].text] += 1
                        else:
                            count_like_dict[user_id[k].text] = 1
                    elif push[k].text == '噓 ':
                        all_boo += 1
                        if user_id[k].text in count_boo_dict:
                            count_boo_dict[user_id[k].text] += 1
                        else:
                            count_boo_dict[user_id[k].text] =1
                time.sleep(0.06)        
        time.sleep(0.06)
    
    if end_date == 1231:
        
        soup = soup_set(r,url)
        date = soup.select("div.r-ent div.date")
        title = soup.select("div.r-ent div.title")
        
        for j in range(len(title)):
        
            if date_trans(date[j].text) == 101:
                break

            try:
                url = ptt+title[j].a['href']
            except:
                continue
            else:
                soup = soup_set(r.url)
                push = soup.select("div.push span.hl.push-tag")
                user_id = soup.select("div.push span.f3.hl.push-userid")
                for k in range(len(push)):
                    if push[k].text == '推':
                        all_like += 1
                        if user_id[k].text in count_like_dict:
                            count_like_dict[user_id[k].text] += 1
                        else:
                            count_like_dict[user_id[k].text] = 1
                    elif push[k].text == '噓':
                        all_boo += 1
                        if user_id[k].text in count_boo_dict:
                            count_boo_dict[user_id[k].text] += 1
                        else:
                            count_boo_dict[user_id[k].text] =1
                time.sleep(0.06)        
        time.sleep(0.06)
    
    sorted_like = pd.DataFrame(list(count_like_dict.items()))
    sorted_like = sorted_like.sort_values([1,0],ascending=[False,True])
    sorted_like = sorted_like.reset_index(drop = True)
    
    sorted_boo = pd.DataFrame(list(count_boo_dict.items()))
    sorted_boo = sorted_boo.sort_values([1,0],ascending=[False,True])
    sorted_boo = sorted_boo.reset_index(drop = True)
    
    file_name = 'push['+str(start_date)+'-'+str(end_date)+'].txt'
    f = open(file_name,'w')
    f.write('all like: ' + str(all_like) + '\n')
    f.write('all boo: ' + str(all_boo) + '\n')
    for i in range(10):
        f.write('like #'+str(i+1)+': '+sorted_like.iloc[i,0]+' '+str(sorted_like.iloc[i,1])+'\n')
    for i in range(10):
        f.write('like #'+str(i+1)+': '+sorted_boo.iloc[i,0]+' '+str(sorted_boo.iloc[i,1])+'\n')
    f.close()
        
def Popular(start_date,end_date):
    
    start_date = int(start_date)
    end_date = int(end_date)
    
    ini_index = 2324
    fin_index = 2758
    
    image_list = []
    count = 0
    #網頁標頭省力
    ptt = 'https://www.ptt.cc'
    
    #架設環境
    r = over18_set()
    
    time.sleep(0.06)
    
    if start_date == 101 :

        start = ini_index+1
        url = "https://www.ptt.cc/bbs/Beauty/index{}.html".format(ini_index)
        soup = soup_set(r,url)
        date = soup.select("div.r-ent div.date")
        title = soup.select("div.r-ent div.title")
        num = soup.select('div.r-ent div.nrec')
        
        for j in range(len(title)):
        
            if date_trans(date[j].text) == 1231:
                continue
            try:
                lable = num[j].span.text
            except:
                continue
            else:
                if lable == '爆':
                    count += 1
                    try:
                        url = ptt+title[j].a['href']
                    except:
                        continue
                    else:
                        soup = soup_set(r,url)
                        a = soup.select('a')
                        for words in a:
                            if words['href'].endswith(('.jpg','.jpeg','.png','.gif')):
                                image_list.append(words['href'])
        time.sleep(0.06)
        
    else:
        
        for i in range(ini_index+1,fin_index):
            
            url = "https://www.ptt.cc/bbs/Beauty/index{}.html".format(i)
            soup = soup_set(r,url)
            date = soup.select("div.r-ent div.date")
            if date_trans(date[0].text) == start_date:
                start = i
                break
            elif date_trans(date[-1].text) == start_date:
                start = i
                break
            time.sleep(0.06)
            
    for i in range(start,fin_index):
        
        url = "https://www.ptt.cc/bbs/Beauty/index{}.html".format(i)
        soup = soup_set(r,url)
        date = soup.select("div.r-ent div.date")
        num = soup.select('div.r-ent div.nrec')
        
        if date_trans(date[0].text) > end_date:
            break
        
        title = soup.select("div.r-ent div.title")
        
        for j in range(len(title)):
        
            if date_trans(date[j].text) > end_date:
                break

            try:
                lable = num[j].span.text
            except:
                continue
            else:
                if lable == '爆':
                    count += 1
                    try:
                        url = ptt+title[j].a['href']
                    except:
                        continue
                    else:
                        soup = soup_set(r,url)
                        a = soup.select('a')
                        for words in a:
                            if words['href'].endswith(('.jpg','.jpeg','.png','.gif')):
                                image_list.append(words['href'])
        time.sleep(0.06)
    
    if end_date == 1231:
        
        soup = soup_set(r,url)
        date = soup.select("div.r-ent div.date")
        title = soup.select("div.r-ent div.title")
        num = soup.select('div.r-ent div.nrec')
        
        for j in range(len(title)):
        
            if date_trans(date[j].text) == 101:
                break
            try:
                lable = num[j].span.text
            except:
                continue
            else:
                if lable == '爆':
                    count += 1
                    try:
                        url = ptt+title[j].a['href']
                    except:
                        continue
                    else:
                        soup = soup_set(r,url)
                        a = soup.select('a')
                        for words in a:
                            if words['href'].endswith(('.jpg','.jpeg','.png','.gif')):
                                image_list.append(words['href'])
        time.sleep(0.06)
    
    file_name = 'popular['+str(start_date)+'-'+str(end_date)+'].txt'
    f = open(file_name,'w')
    f.write('number of popular articles: '+str(count)+'\n')
    for image in image_list:
        f.write(image+'\n')
    f.close()

def Keyword(keyword,start_date,end_date):
    
    start_date = int(start_date)
    end_date = int(end_date)
    
    ini_index = 2324
    fin_index = 2758
    
    image_list = []
    #網頁標頭省力
    ptt = 'https://www.ptt.cc'
    
    #架設環境
    r = over18_set()
    
    time.sleep(0.06)
    if start_date == 101 :

        start = ini_index+1
        url = "https://www.ptt.cc/bbs/Beauty/index{}.html".format(ini_index)
        soup = soup_set(r,url)
        date = soup.select("div.r-ent div.date")
        title = soup.select("div.r-ent div.title")
        
        for j in range(len(title)):
        
            if date_trans(date[j].text) == 1231:
                continue
                        
            try:
                url = ptt+title[j].a['href']
            except:
                continue
            else:
                soup = soup_set(r,url)
                main = soup.find_all('div', {'id': 'main-container'})
                main = str(main).split('\n--\n')[0]
                if keyword in main:
                    a = soup.select('a')
                    for words in a:
                        if words['href'].endswith(('.jpg','.jpeg','.png','.gif')):
                            image_list.append(words['href'])
                time.sleep(0.06)        
        time.sleep(0.06)
        
    else:
        for i in range(ini_index+1,fin_index):
            url = "https://www.ptt.cc/bbs/Beauty/index{}.html".format(i)
            soup = soup_set(r,url)
            date = soup.select("div.r-ent div.date")
            if date_trans(date[0].text) == start_date:
                start = i
                break
            elif date_trans(date[-1].text) == start_date:
                start = i
                break
            time.sleep(0.06)

    for i in range(start,fin_index):
        
        url = "https://www.ptt.cc/bbs/Beauty/index{}.html".format(i)
        soup = soup_set(r,url)
        date = soup.select("div.r-ent div.date")
        
        if date_trans(date[0].text) > end_date:
            break
        
        title = soup.select("div.r-ent div.title")
        
        for j in range(len(title)):
        
            if date_trans(date[j].text) > end_date:
                break

            try:
                url = ptt+title[j].a['href']
            except:
                continue
            else:
                soup = soup_set(r,url)
                main = soup.find_all('div', {'id': 'main-container'})
                main = str(main).split('\n--\n')[0]
                if keyword in main:
                    a = soup.select('a')
                    for words in a:
                        if words['href'].endswith(('.jpg','.jpeg','.png','.gif')):
                            image_list.append(words['href'])
                time.sleep(0.06)        
        time.sleep(0.06)
    
    if end_date == 1231:
        
        soup = soup_set(r,url)
        date = soup.select("div.r-ent div.date")
        title = soup.select("div.r-ent div.title")
        
        for j in range(len(title)):
        
            if date_trans(date[j].text) == 101:
                break

            try:
                url = ptt+title[j].a['href']
            except:
                continue
            else:
                soup = soup_set(r.url)
                main = soup.find_all('div', {'id': 'main-container'})
                main = str(main).split('\n--\n')[0]
                if keyword in main:
                    a = soup.select('a')
                    for words in a:
                        if words['href'].endswith(('.jpg','.jpeg','.png','.gif')):
                            image_list.append(words['href'])
                time.sleep(0.06)        
        time.sleep(0.06)
    
    file_name = 'keyword('+keyword+')['+str(start_date)+'-'+str(end_date)+'].txt'
    f = open(file_name,'w')
    for image in image_list:
        f.write(image+'\n')
    f.close()
    
def over18_set():

    #架設環境
    r = requests.Session() 
    
    payload = {
            "from":"/bbs/Beauty/index.html",
            "yes":"yes"
            }
    
    #發yes,no的cookies
    over18 = r.post("https://www.ptt.cc/ask/over18?from=%2Fbbs%2FBeauty%2Findex.html",data = payload)
    
    return r

def soup_set(r,url):

    text_list = r.get(url)
    text_list.encoding = 'utf_8'
    context = text_list.text
    soup = BeautifulSoup(context, 'html.parser')

    return soup

def date_trans(date):
    return int(date.replace('/',''))
        