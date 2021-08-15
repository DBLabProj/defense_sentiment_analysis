'''
21.08.09
특정 json 파일을 특정 날짜 기준으로 2개의 새로운 json 파일 생성
'''
import json

def seperateJson(dirpath, json_name, date_point): # date_point likes "2020/11/05"
    with open(dirpath+json_name+'.json', encoding="utf-8") as json_file:
        data = json.load(json_file)

    # 기준 날짜 년, 월, 일
    point_y, point_m, point_d = [ int(x) for x in date_point.split("/")]
    
    data1, data2 = {}, {} # 분리할 딕셔너리
    for date in data.keys(): # 날짜 리스트
        # 기존 json 파일 날짜
        y, m, d = int(date[:4]), int(date[4:6]), int(date[-2:])
        
        if y < point_y: data1[date] = data[date]
        elif y == point_y and m < point_m: data1[date] = data[date]
        elif y == point_y and m == point_m and d < point_d: data1[date] = data[date]
        else: # 이전 날짜
            data2[date] = data[date]


    return data1, data2



if __name__ == "__main__":
    dirpath = "./predict-data/kobert/"
    json_name = "kobert_predict_volunteer_all"
    check_point = "2020/01/01"
    before, after = seperateJson(dirpath, json_name, check_point)

    result_path = "./predict-data/tf/" #  result save json path
    before_name, after_name = json_name+"_before", json_name+"_after"
    with open(result_path+before_name+".json", "wt", encoding="utf-8") as json_file:
        json.dump(before, json_file, indent="\t", ensure_ascii = False)

    with open(result_path+after_name+".json", "wt", encoding="utf-8") as json_file:
        json.dump(after, json_file, indent="\t", ensure_ascii = False)
