# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 22:56:44 2019

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
import sys
import pandas
start_time = time.time()

def crawl():
    ini_index = 2324
    fin_index = 2758
    
    index = ini_index
    
    #網頁標頭省力
    ptt = 'https://www.ptt.cc'
    
    #架設環境
    r = over18_set()
    
    f1 = open('all_articles.txt','w',encoding = "utf-8")
    f2 = open('all_popular.txt','w',encoding = "utf-8")
    
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
    
    return
    
def Push(start_date,end_date):
    
    start_date = int(start_date)
    end_date = int(end_date)
    
    count_like_dict = {}
    count_boo_dict = {}
    all_like = 0
    all_boo = 0
    
    #架設環境
    r = over18_set()
    time.sleep(0.06)
    
    article_list = read_file('all_articles.txt')
    select = article_list[ (article_list['date']>=start_date) & (article_list['date'] <= end_date) ]
    
    for i in range(len(select)):
        url =  select.iloc[i,1]
        all_like,count_like_dict,all_boo,count_boo_dict = what_push(r,url,all_like,count_like_dict,all_boo,count_boo_dict)
    
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

def what_push(r,url,all_like,count_like_dict,all_boo,count_boo_dict):
    
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
    
    return all_like,count_like_dict,all_boo,count_boo_dict

def Popular(start_date,end_date):
    
    start_date = int(start_date)
    end_date = int(end_date)

    article_list = read_file('all_popular.txt')
    select = article_list[ (article_list['date']>=start_date) & (article_list['date'] <= end_date) ]
        
    image_list = []
    
    #架設環境
    r = over18_set()    
    time.sleep(0.06)
    
    for i in range(len(select)):
        url =  select.iloc[i,1]
        soup = soup_set(r,url)
        a = soup.select('a')
        image_list = get_image(a,image_list)
        time.sleep(0.06)

    file_name = 'popular['+str(start_date)+'-'+str(end_date)+'].txt'
    f = open(file_name,'w')
    f.write('number of popular articles: '+str(len(select))+'\n')
    for image in image_list:
        f.write(image+'\n')
    f.close()

def get_image(a,image_list):

    for words in a:
        if words['href'].endswith(('.jpg','.jpeg','.png','.gif')):
            image_list.append(words['href'])
    return image_list
    
def Keyword(keyword,start_date,end_date):
    
    start_date = int(start_date)
    end_date = int(end_date)
    
    article_list = read_file('all_articles.txt')
    select = article_list[ (article_list['date']>=start_date) & (article_list['date'] <= end_date) ]

    image_list = []
    
    #架設環境
    r = over18_set()    
    time.sleep(0.06)
            
    for i in range(len(select)):
        url = select.iloc[i,1]
        soup = soup_set(r,url)
        main = soup.find_all('div', {'id': 'main-container'})
        main = str(main).split('\n--\n')[0]
        if keyword in main:
            a = soup.select('a')
            image_list = get_image(a,image_list)            
        time.sleep(0.06)
            
    file_name = 'keyword('+keyword+')['+str(start_date)+'-'+str(end_date)+'].txt'
    f = open(file_name,'w')
    for image in image_list:
        f.write(image+'\n')
    f.close()

def read_file(file_name):
    try:
        text = open(file_name,'r',encoding="utf-8")
    except:
        print('Please run scrawler first before using this function')
    else:
        article_list = text.read()
        article_list = article_list.split('\n')
        del article_list[-1]
        article_list = [SPLIT(x) for x in article_list]
        article_list = pd.DataFrame(article_list)
        article_list.columns = ['date','href']
        text.close()
        return article_list

def SPLIT(x):
    s = x.split(',')
    return [int(s[0]),s[-1]]

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

def main():
    if sys.argv[1] == 'crawl':
        crawl()
    elif sys.argv[1] == 'push':
        if len(sys.argv)!= 4:
            print("Please enter start date and end date")
        else:
            Push(sys.argv[2],sys.argv[3])
    elif sys.argv[1] == 'popular':
        if len(sys.argv)!= 4:
            print("Please enter start date and end date")
        else:
            Popular(sys.argv[2],sys.argv[3])
    elif sys.argv[1] == 'keyword':
        if len(sys.argv)!= 5:
            print("Please enter keyword, start date and end date")
        else:
            Popular(sys.argv[2],sys.argv[3],sys.argv[4])
    else:
        print('please check your input')
    print('Time spent: ',(time.time()-start_time())/60,' min')

if '__name__' == '__main__':
    main()