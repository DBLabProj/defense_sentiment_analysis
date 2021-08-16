# 
# util.py
# Author : Ji-yong219
# Project Start:: 2020.12.18
# Last Modified from Ji-yong 2021.06.22
#

import calendar, datetime
import json

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)
        
def get_num_month(str_month):
    for month_idx in range(1, 13):
        if str_month == calendar.month_name[month_idx]:
            if month_idx < 10:
                return '0'+str(month_idx)
            else:
                return str(month_idx)

        elif str_month == calendar.month_abbr[month_idx]:
            if month_idx < 10:
                return '0'+str(month_idx)
            else:
                return str(month_idx)
                
def convert_date(original_date):
    data = original_date.split(' ')
    # print(f'data:{data}')
    month = get_num_month(data[0].replace('.', ''))
    dates = data[1].replace(',', '')
    year = data[2].replace(',', '')
    hour = data[4].split(':')[0]
    minute = data[4].split(':')[1]
    
    temp = '-'.join([str(i) for i in [year, month, dates, hour, minute, 0, data[5].replace('.', '').upper()]])
    converted_date = datetime.datetime.strptime(temp, '%Y-%m-%d-%I-%M-%S-%p') - datetime.timedelta(hours=-9)
    return converted_date.strftime('%Y%m%d%H%M')

    
def merge_crawl_data_json(keyword, start_date, end_date):
    dic = {}
    dic2 = {}
    
    for company in ["daum", "naver"]:

        start_date_ = datetime.date(int(start_date[:4]), int(start_date[4:6]), int(start_date[6:]))
        end_date_ = datetime.date(int(end_date[:4]), int(end_date[4:6]), int(end_date[6:])) + datetime.timedelta(days=1)

        date_list = [str(i).replace('-', '')[0:8] for i in daterange(start_date_, end_date_)]


        for date in date_list:
            if date[:6] not in dic2.keys():
                dic2[date[:6]] = []

        json_list = []
        for date in dic2.keys():
            with open(f'result/{company}_news/news_{keyword}_{company}_{start_date}_{end_date}__{date}.json','r', encoding='utf8') as f:
                dic2 = json.load(f)

            dic.update(dic2)

        dic2 = {}
        for date in dic.keys():
            if date[:6] not in dic2.keys():
                dic2[date[:6]] = []

            dic2[date[:6]].append(dic[date])


        all = 0
        for mon in dic2.keys():
            count = 0
            for dic3 in dic2[mon]:
                if dic3 is None: continue
                for url, contain in dic3.items():
                    for comment in contain['comments']:
                        count += 1
            all += count
            print(f'{mon} : {count}')
        print(f'all : {all}')

        with open(f'result/{company}_news/news_{keyword}_{company}_{start_date}_{end_date}.json', 'w', encoding='utf8') as f:
            json.dump(dict(dic), f, indent=4, sort_keys=True, ensure_ascii=False)




    dic = {}
    start_date_ = datetime.date(int(start_date[:4]), int(start_date[4:6]), int(start_date[6:]))
    end_date_ = datetime.date(int(end_date[:4]), int(end_date[4:6]), int(end_date[6:])) + datetime.timedelta(days=1)

    date_list = [str(i).replace('-', '')[0:8] for i in daterange(start_date_, end_date_)]


    for date in date_list:
        if date not in dic.keys():
            dic[date] = {}

    all = 0
    for date in dic.keys():
        for company in ["daum", "naver"]:
            with open(f'result/{company}_news/news_{keyword}_{company}_{start_date}_{end_date}__{date[:6]}.json','r', encoding='utf8') as f:
                dic2 = json.load(f)

            if date in dic2.keys() and dic2[date] != {} and dic2[date] is not None:
                dic[date].update(dic2[date])


    dic2 = {}
    for date in dic.keys():
        if date[:6] not in dic2.keys():
            dic2[date[:6]] = []

        dic2[date[:6]].append(dic[date])

    all = 0
    for mon in dic2.keys():
        count2 = 0
        count = 0
        for dic3 in dic2[mon]:
            for url, contain in dic3.items():
                for comment in contain['comments']:
                    count += 1
                count2 += 1
        all += count
        print(f'{mon} : {count}\t{count2}')
    print(f'all : {all}\t{count2}')

    with open(f'result/news_{keyword}_all_{start_date}_{end_date}.json', 'w', encoding='utf8') as f:
        json.dump(dict(dic), f, indent=4, sort_keys=True, ensure_ascii=False)