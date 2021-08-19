
# json 읽어서 학습된 모델에 입력해서 댓글당 감성수치 받아서 딕셔너리 완성 > json file
# read json >input RNN model > predict comment sentiment > make dictionary > write json file

from tensorflow.keras import models
from tensorflow.keras.layers.experimental.preprocessing import TextVectorization
import tensorflow as tf
import json, os
from tqdm import tqdm
from text_preprocessing.text_preprocessing import *

os.environ['TF_CPP_MIN_LOG_LEVEL'] ='2'


# load RNN model
model_name = "volunteer_model_try_3"
rnn_model = tf.keras.models.load_model(
    "./model_save/tf_model/"+ model_name, 
    custom_objects={"TextVectorization":TextVectorization}
    )

path = "./data/mecab/comment_json/" # comment  json file directory path
jsonfile = "volunteer_all_mecab"
with open(path+jsonfile+'.json', encoding="utf-8") as json_file:
    data = json.load(json_file) # load json file

all = len( data )
for idx, date in  enumerate( data.keys() ): 
    if idx % 30 ==0: print(idx ,"/", all)
    day_article = data[date]
    for article in day_article.keys():
        for comment in day_article[article]['comments']:
            if comment=="": # if comment is not include text
                continue
            # if preprocessed data
            preprocessedData = comment.replace('\n',' ').replace('\r',' ')
            '''
            # if not preprocessed
            preprocessedData = textPreprocessing(comment.replace('\n',' ').replace('\r',' '),
                                                  method="mecab", stopword=[])
            '''
            emotion = float(rnn_model.predict([preprocessedData])) # predict comment sentiment
            emotion = 0 if emotion<0.5 else 1
            data[date][article]['emotions'].append( emotion )

result_path = "./data/predict-data/" #  result save json path
result_json = "tf_volunteer_all_try_3"
with open(result_path+result_json+".json", "wt", encoding="utf-8") as json_file:
    json.dump(data, json_file, indent="\t", ensure_ascii = False)
