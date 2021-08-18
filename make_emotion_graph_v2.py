# 종교별로 시간 흐름에 따른 감성 수치 변화 그래프
# sentiment flow graph by time per religion

from matplotlib import font_manager, rc
import matplotlib.pyplot as plt
import numpy as np
import math, csv, json

dirname = "tf"
keyword = "모병제-전체-try2"
ystick_value = 1.1

def append_dict(d1, d2): # dictionary + dictionary
    for d in d1.keys():
        if d in d2.keys(): 
            for i in d1[d]: d2[d][i] = d1[d][i]
        else: d2[d] = d1[d]
    return d2

# csv 파일 생성
def makeCSV(tablename, y):
    global dirname
    f = open("./ttest/"+dirname+"/"+tablename+'.csv','w', newline='')
    wr = csv.writer(f)
    for e in y:
        wr.writerow([e])

# 시간 흐름에 따른 감성 지수 그래프
def make_graph_flow(tablename, x, y, fig, graph_title = "Sentiment Graph"):
    global dirname
    plt.figure(fig, figsize=(18, 5))
    font_name = font_manager.FontProperties(fname='./font/KoPubDotumMedium.ttf', size=20).get_name()
    rc('font', family=font_name)
    
    plt.title(graph_title, fontsize=22)
    a =0
    nx=[]
    for s in range(len(x)):
        nx.append(s)
        a+=1
    # nx = np.array(nx)
    ny = np.array(y)
    # m, bb = np.polyfit(nx, ny, 1) # calculate trend line
    # plt.plot(nx, m*nx + bb, 'r--', color='#819FF7' , label="Trend Line")
    print(nx[:3])
    print(y[:3])
    plt.plot(nx, y, 'bo', color='#BF00FF', label="Sentiments" )

    # make month x label
    month_list, temp, year_temp = [], "", ''
    for month in x:
        month, year = month[4:6],  month[2:4]
        if temp != month : 
            temp = month
            month_list.append(month)
            if  year_temp != year: 
                month_list[-1] = year+"/"+ month_list[-1]
                year_temp = year
        else: month_list.append("")
        
    plt.ylim([0.0, ystick_value]) 
    plt.xlabel('Date',fontsize=18)
    plt.ylabel('Sentiment',fontsize=18)
    plt.xticks(rotation=60,fontsize=10)
    plt.yticks(fontsize=16)
    plt.xticks(range(0,len(month_list)), month_list)
    plt.legend()
    plt.savefig("./graph/"+dirname+"/"+tablename+'-emotion-flow.png', dpi=400)
    return 0

# json 파일 읽어서 자료구조 생성
def makeValue(data):
    result = {}

    for date in data.keys():
        emotions_ = []
        for article in data[date]:
            emotions_.extend( data[date][article]['emotions'] )
        #긍정률 계산
        if not emotions_: continue
        # print( sum(emotions_),'//', len(emotions_) )
        result[date] = sum(emotions_) / len(emotions_)
        val = sum(emotions_) / len(emotions_)
        if val > 0.2:
            print('>>',date, val)
    

    x, y = [], []
    for d in result.keys():
        x.append(d)
        y.append(result[d])
    
    return x, y

def calc_mean_std(data):
    import numpy as np
    return round(np.mean(data), 4), round(np.std(data), 4)


fig = 0
avg_x, avg_y = [], []
# for tableList in tlist:
data = []

# 댓글 데이터 json 파일 저장 경로
path = "./data/predict-data/" 
json_name = "tf_volunteer_all_try_2"
# json_name = "kobert_predict_volunteer_comment_data"
with open(path+json_name+'.json', encoding="utf-8") as json_file:
    data_ = json.load(json_file)

x, y = makeValue(data_)

print(x[:10], y[:10])

import time
time.sleep(1)

# 그래프 생성
make_graph_flow(json_name+"3", x, y,  fig, graph_title = "Keras Sentiments Flow Graph (Positive rate)")
# 감성 평균, 표준편차 text 파일 생성
with open( "./graph/"+dirname+"/"+json_name+"_stats.txt", "at", encoding="utf-8" ) as f:
    title = keyword+" 감성 통계"
    f.write(title+"\n")
    mean, std = calc_mean_std(y)
    f.write("avg: "+str(mean)+" std: "+str(std)+"\n")
    
    f.write("--"*10+"\n")

with open( "./graph/"+dirname+"/"+json_name+"year_stats.txt", "at", encoding="utf-8" ) as f:
    title = keyword+" 구간별 감성 통계"
    f.write(title+"\n")
    year_dict = {2018:[], 2019:[], 2020:[]}
    # 년도 구분
    for year, sents in zip(x, y):
        y, m = int(year[:4]), int(year[4:6])
        if y == 2018 :
            year_dict[2018].append( sents )
        elif y == 2019 and m <= 6:
            year_dict[2018].append( sents )
        elif y==2019 and m > 6:
            year_dict[2019].append( sents )
        elif y==2020 and m <= 6:
            year_dict[2019].append( sents )
        elif y==2020 and m > 6:
            year_dict[2020].append( sents )
        else: year_dict[2020].append( sents )

    for years in year_dict.keys(): #년도별 평균 및 표준편차 계산
        mean, std = calc_mean_std( year_dict[years] )
        f.write(str(years)+" : avg: "+str(mean)+" std: "+str(std)+"\n")

# CSV 파일 생성
# makeCSV(keyword, y)

