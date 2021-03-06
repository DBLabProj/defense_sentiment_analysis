
# 학습 데이터를 통해 RNN 딥러닝 모델 생성
# build RNN model from train data
# 21.08.11

import json
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] ='2'
from text_preprocessing.text_preprocessing import *
import numpy as np
from tensorflow.keras import models, layers, optimizers, losses, metrics
import tensorflow as tf
from keras.preprocessing.sequence import pad_sequences
import csv
import pandas as pd

from tensorflow.keras.layers import Dense, Embedding, Flatten, Dropout
from tensorflow.keras import Input, Model, regularizers

from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers.experimental.preprocessing import TextVectorization
import matplotlib.pyplot as plt

# 훈련 결과 그래프 시각화
def showModelTrain(history):
    # 훈련 과정 시각화 (acc)
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('Model accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend(['Train', 'Test'], loc='upper left')
    plt.show()

    # 훈련 과정 시각화 (loss)
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('Model loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend(['Train', 'Test'], loc='upper left')
    plt.show()

#   csv 파일 읽어서 x y 리스트 저장
# read csv and make list

# 수작업 데이터
x, y = [],[]
path = "./data/mecab/labeling/"
filename = "non_mecab_dataset.tsv" # train data 
with open(path +filename, "rt", encoding="utf-8") as f:
    for idx, l in enumerate( f.readlines() ):
        line = l.strip("\n")
        try:
            data, value = line.strip('\t').split("\t")
        except:
            print(idx, line)
        
        value = float(value)
        preprocessedData = textPreprocessing(
                                    data.replace('\n',' ').replace('\r',' '), 
                                    method="mecab", 
                                    stopword=[])
        x.append(preprocessedData)
        y.append(value)

test_percent = 0.1 # test data percent
# make train and test data usin train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_percent)

def build_model_origin(train_data): # to make rnn model
    train_data = tf.data.Dataset.from_tensor_slices(train_data)
    model = Sequential()
    model.add(Input(shape=(1,), dtype="string")) # input one string data (comment)
    max_tokens = 100000 # dictionary size
    max_len = 64 # comment to vectorize size
    
    vectorize_layer = TextVectorization( # make textvectorization 
      max_tokens=max_tokens,
      output_mode="int",
      output_sequence_length=max_len,
    )
    dropout_val = 0.5 # dropout percent
    vectorize_layer.adapt(train_data.batch(64))
    model.add(vectorize_layer)
    model.add(layers.Embedding(max_tokens + 1, output_dim= 200))
    model.add(Flatten())

    # apply dropout
    for _ in range(8):
        model.add(Dense(32, activation="relu"  ))#, kernel_regularizer= regularizers.l2(0.001)))  #
        model.add(Dropout(dropout_val))
    
    model.add(Dense(32, activation="relu"))
    model.add(Dense(1, activation="sigmoid"))
    return model

def build_model(train_data): # to make rnn model
    train_data = tf.data.Dataset.from_tensor_slices(train_data)
    model = Sequential()
    model.add(Input(shape=(1,), dtype="string")) # input one string data (comment)
    max_tokens = 100000 # dictionary size
    max_len = 64 # comment to vectorize size
    
    vectorize_layer = TextVectorization( # make textvectorization 
      max_tokens=max_tokens,
      output_mode="int",
      output_sequence_length=max_len,
    )
    dropout_val = 0.5 # dropout percent
    vectorize_layer.adapt(train_data.batch(64))
    model.add(vectorize_layer)
    model.add(layers.Embedding(max_tokens + 1, output_dim= 200))
    model.add(Flatten())

    # apply dropout
    # 2**8 ~ 2**1
    for unit in range(8):
        units = 2 ** (8-unit)
        print("Number of units:", units)
        model.add(Dense(units, activation="relu"  )) #, kernel_regularizer= regularizers.l2(0.001)))  #
        if unit!=7:
            model.add(Dropout(dropout_val))
    
    #model.add(Dense(32, activation="relu"))
    model.add(Dense(1, activation="sigmoid"))
    return model


rnn_model =build_model(x_train)
rnn_model.compile( # rnn model compile
        optimizer=  "adam",
        loss='binary_crossentropy',
        metrics=['accuracy']
    )

# model training
history = rnn_model.fit(x_train, y_train, 
                   epochs = 10,
                   batch_size = 32 ,
                   validation_data = (x_test, y_test) 
                   )
rnn_model.summary()

model_save_path = "./model_save/tf_model/" # model save path
model_name ="volunteer_model_try_3" #model save file name
tf.saved_model.save(rnn_model, model_save_path+model_name)

showModelTrain(history)

'''
[volunteer_model_5] model performance
loss: 0.0476 - accuracy: 0.9765 - val_loss: 0.1429 - val_accuracy: 0.9553

[volunteer_model_try_1]
loss: 0.1431 - accuracy: 0.9583 - val_loss: 0.1504 - val_accuracy: 0.9558

[volunteer_model_try_2]
loss: 0.1340 - accuracy: 0.9643 - val_loss: 0.1228 - val_accuracy: 0.9649

[volunteer_model_try_3]
loss: 0.1336 - accuracy: 0.9598 - val_loss: 0.2068 - val_accuracy: 0.9583
'''
