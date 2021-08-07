
# json 읽어서 학습된 모델에 입력해서 댓글당 감성수치 받아서 딕셔너리 완성 > json file
# read json >input RNN model > predict comment sentiment > make dictionary > write json file

from tensorflow.keras import models
from tensorflow.keras.layers.experimental.preprocessing import TextVectorization
import tensorflow as tf
import json, os
from tqdm import tqdm
from preprocessing.text_preprocessing import *

os.environ['TF_CPP_MIN_LOG_LEVEL'] ='2'

'''
tlist = [] # database table name list
for i in range(1,6):
    t = "daum"
    tlist.append(t+"after"+str(i))
    tlist.append(t+"before"+str(i))
for i in range(1,6):
    t = "naver"
    tlist.append(t+"after"+str(i))
    tlist.append(t+"before"+str(i))
'''

# load RNN model
model_name = "model+labeling+nave+case5"
rnn_model = tf.keras.models.load_model(
    "./model_save/tf_model/"+ model_name, 
    custom_objects={"TextVectorization":TextVectorization}
    )

path = "./data/" # comment  json file directory path
jsonfile = "news_usarmy_all_20200601_20210601"

with open(path+jsonfile+'.json', encoding="utf-8") as json_file:
    data = json.load(json_file) # load json file

all = len( data )
for idx, date in  enumerate( data.keys() ): 
    if idx % 50 ==0: print(idx ,"/", all)
    day_article = data[date]
    for article in day_article.keys():
        for comment in day_article[article]['comments']:
            if comment=="": # if comment is not include text
                continue
            #print(comment.replace('\n',' ').replace('\r',' '))
            preprocessedData = textPreprocessing(comment.replace('\n',' ').replace('\r',' '), method="mecab", stopword=[])
            #print(preprocessedData)
            emotion = float(rnn_model.predict([preprocessedData])) # predict comment sentiment
            data[date][article]['emotions'].append(round(emotion, 3)) # dictionary value append sentiment

result_path = "./predict-data/tf/" #  result save json path
result_json = "tf_predict_data"
with open(result_path+result_json+".json", "wt", encoding="utf-8") as json_file:
    json.dump(data, json_file, indent="\t", ensure_ascii = False)
