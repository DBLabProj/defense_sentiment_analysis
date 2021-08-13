import json, csv
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
        least =10 # 최소 댓글 수 
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

def getSentimentsList(data):
    emotions = []

    for date in data:
        #print(data[date])
        for article in data[date]:
            #print(article)
            #print(data[date][article])
            emotions.extend( data[date][article]['emotions'] )
    return emotions

# for tablelist in tlist:
# for tablename in tablelist:
keyword = "usarmy"
path = "./data/predict-data/tf/"
with open(path+"tf_predict_trump_usarmy.json", encoding="utf-8") as json_file:
    data1 = json.load(json_file)
    
with open(path+"tf_predict_bidden_usarmy.json", encoding="utf-8") as json_file:
    data2 = json.load(json_file)

emo1 = getSentimentsList(data1)
emo2 = getSentimentsList(data2)

_, emo1 = makeValue(data1)
_, emo2 = makeValue(data2)

f = open("./ttest/"+keyword+'-trump2.csv','w', newline='')
wr = csv.writer(f)
for e in (emo1):
    wr.writerow([e])
    
f = open("./ttest/"+keyword+'-bidden2.csv','w', newline='')
wr = csv.writer(f)
for e in (emo2):
    wr.writerow([e])



