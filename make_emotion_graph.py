# 종교별로 시간 흐름에 따른 감성 수치 변화 그래프
# sentiment flow graph by time per religion

from matplotlib import font_manager, rc
import matplotlib.pyplot as plt
import numpy as np
import math, csv, json

dirname = "tf"
keyword = "모병제-전체"

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
def make_graph_flow(tablename, x, y,fig, graph_title = "Sentiment Graph"):
    global dirname
    plt.figure(fig, figsize=(18, 5))
    font_name = font_manager.FontProperties(fname='./font/KoPubDotumMedium.ttf', size=20).get_name()
    rc('font', family=font_name)
    
    plt.title(graph_title,fontsize=22)
    a =0
    nx=[]
    for s in range(len(x)):
        nx.append(s)
        a+=1
    nx = np.array(nx)
    ny = np.array(y)
    m, bb = np.polyfit(nx, ny, 1) # calculate trend line
    plt.plot(nx, m*nx + bb, 'r--', color='#819FF7' , label="Trend Line")
    plt.plot(nx, y, 'bo', color='#2E2EFE', label="Sentiments" )

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
        
    plt.ylim([0.0, 0.3]) 
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
    result = []
    table_emo_count, table_emo_avg= 0, 0.0 # 감성 개수, 감성 총 합
    for date in data.keys():
        for art in data[date].keys():
            table_emo_count += len(data[date][art]['emotions'])
    
    for data_date in data.keys():
        table_emo_avg += sum([ (sum(data[data_date][art]['emotions'])/(len(data[data_date][art]['emotions'])+1))\
                                *(len(data[data_date][art]['emotions'])/ table_emo_count) \
                                for art in data[data_date].keys() ]) #날짜당 감성 평균, 가중 평균
    
    for date in data.keys(): #모든 날짜
        day_emo_count = sum([len(data[date][artc]['emotions']) for artc in data[date].keys()]) #날짜당 총 댓글 수 / all comment per day
        if day_emo_count ==0: continue
        
        emotion, isInput = 0, True
        day_emo_count = sum([ len(data[date][art]['emotions']) for art in data[date].keys() ]) #날짜당 총 댓글 수
        for article in data[date].keys(): #모든 기사
            if len(data[date])==1 and len(data[date][article]['emotions']) <1: # 기사가 1개 and 댓글이 0개인 경우 > 입력 안함
                isInput=False
                break
                
            emotionList= data[date][article]['emotions']
            if emotionList == []: continue
            
            emotion_avg  =sum(emotionList) / len(emotionList) #기사당 감성 평균 / emotion average per article
            emotion += (len(emotionList)/day_emo_count) * emotion_avg # 날짜당 기사 가중 평균 / article emotion weighted average per day
        least = 30 # 최소 댓글 수 
        # 공식 참고 : https://www.quora.com/How-does-IMDbs-rating-system-work
        emotion_ = (day_emo_count/(day_emo_count+least))*emotion +  (least/(day_emo_count+least))*table_emo_avg 
        
        d_y, d_m, d_d = int(date[:4]), int(date[4:6]), int(date[6:])
        
        if isInput: result.append([date, round(emotion_, 6), d_y, d_m, d_d ])
        
    result_sort_day = sorted(result, key = lambda x: (x[2], x[3], x[-1])) # 정렬 : 1순위 년도, 2순위 월, 3순위 일
    
    x,y = [],[]
    for val in result_sort_day:
        x.append(val[0])
        y.append(val[1])
    
    return x, y

def calc_mean_std(data):
    import numpy as np
    return round(np.mean(data), 4), round(np.std(data), 4)


fig = 0
avg_x, avg_y = [], []
# for tableList in tlist:
data = []

# 댓글 데이터 json 파일 저장 경로
path = "./data/predict-data/" + dirname + "/"
json_name = "tf_predict_volunteer_all_3"

with open(path+json_name+'.json', encoding="utf-8") as json_file:
    data_ = json.load(json_file)

data = makeValue(data_)
x, y = data[0], data[1]

print(x[:10], y[:10])

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

# 그래프 생성
make_graph_flow(json_name, x, y,  fig, graph_title = "Keras Sentiments Flow Graph")
# CSV 파일 생성
makeCSV(keyword, y)

