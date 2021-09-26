# from src.database.GenomaDB import Animal, Mapa, Animal_mapa, Marcador, Mapa_marcador, session
# from src.configuration.config import DATA_FOLDER
# from src.helpers.logger import logger

# import os
import math
import pandas as pd
import numpy as np
import pickle
from random import random, randint
from time import sleep
from math import floor
from sklearn.model_selection import train_test_split

from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import Dropout
from sklearn.metrics import mean_squared_error
# import sqlalchemy_mixins
# import hashlib
# from tqdm import tqdm


class RNN:

    data_files = ('Computed/imputation/data_x.zip',
                  'Computed/imputation/data_y.zip')
    look_back = 100
    samples_count = 0

    mafArr = []
    accArr = []

    def __init__(self):

        print("\n### O que você quer fazer? ")
        print("  # ( 0 ): Voltar")
        print("  # ( 1 ): Gerar dados de treinamento e teste")
        print("  # ( 2 ): Carregar dados de treinamento e teste")
        opt = int(input("# Opção: "))

        if opt == 1:
            self.create_dataset()
        if opt == 2:
            self.load_db()

        # print(self.DATA_X.shape)

        self.create_dataset()
        self.train()

        # self.train()

    def create_dataset(self, current_allele):
        look_back = self.look_back

        dataset = pd.read_pickle('Computed/bases/a509466ad9104985a5bb3f7c686c5e36/chr_1_haplotypes.zip',
                                 compression='zip').T.iloc[:, (current_allele - look_back):current_allele]
        dataX, dataY = [], []

        a = dataset.iloc[:, :look_back-2]
        dataX.append(a)
        dataY.append(dataset.iloc[:, look_back-2:])

        dataX = np.array(dataX).reshape(217, look_back-2)
        dataY = np.array(dataY).reshape(217, 2)

        with open(self.data_files[0], 'wb') as f:
            pickle.dump(dataX, f)
        with open(self.data_files[1], 'wb') as f:
            pickle.dump(dataY, f)

        self.data_X = dataX
        self.data_Y = dataY

    def load_db(self):
        with open(self.data_files[0], 'rb') as f:
            self.data_X = pickle.load(f)
        with open(self.data_files[1], 'rb') as f:
            self.data_Y = pickle.load(f)
    # endregion

    def train(self, current_allele):
        self.create_dataset(current_allele)

        x_train, x_test, y_train, y_test = train_test_split(
            self.data_X, self.data_Y, test_size=0.3, random_state=4)
        print('Original: ', self.data_X.shape, self.data_Y.shape)

        x_train = np.reshape(x_train, (x_train.shape[0], 1, x_train.shape[1]))
        x_test = np.reshape(x_test, (x_test.shape[0], 1, x_test.shape[1]))
        print('Treino: ', x_train.shape, y_train.shape)
        print('Teste: ', x_test.shape, y_test.shape)

        # define model
        model = Sequential()
        model.add(LSTM(128, activation='relu', input_shape=(
            1, self.look_back-2), return_sequences=True))
        # model.add(LSTM(128, activation='relu', input_shape=(1, self.look_back-2)))
        model.add(Dropout(0.2))
        model.add(LSTM(128, activation='relu', return_sequences=True))
        model.add(Dropout(0.2))
        model.add(LSTM(64, activation='relu'))
        # model.add(Dropout(0.2))

        # model.add(Dense(32, activation='relu'))
        model.add(Dense(2, activation='relu'))
        model.compile(loss='mean_squared_error',
                      optimizer='adam', metrics=['accuracy'])
        # model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

        alleles, zeros = 0, 0
        for y in y_train:
            alleles += 2
            if y[0] == 0:
                zeros += 1
            if y[1] == 0:
                zeros += 1
        for y in y_test:
            alleles += 2
            if y[0] == 0:
                zeros += 1
            if y[1] == 0:
                zeros += 1

        maf = (alleles - zeros)/alleles
        print(f"MAF: {maf}")
        self.mafArr.append(maf)

        for i in range(200):
            model.fit(x_train, y_train, epochs=1, batch_size=1, verbose=0)

            testPredict = model.predict(x_test)
            total, err = 0, 0
            for idx, predict in enumerate(testPredict):
                if predict[0] < 0:
                    predict[0] = 0
                if predict[0] > 1:
                    predict[0] = 1
                if predict[1] < 0:
                    predict[1] = 0
                if predict[1] > 1:
                    predict[1] = 1
                predict[0] = round(predict[0], 0)
                predict[1] = round(predict[1], 0)

                total += 2
                if predict[0] != y_test[idx][0]:
                    err += 1
                if predict[1] != y_test[idx][1]:
                    err += 1

            acc = 1 - err/total
            print("Taxa de acerto: ", round(acc, 5))
        self.accArr.append(acc)
