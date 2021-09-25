# from src.database.GenomaDB import Animal, Mapa, Animal_mapa, Marcador, Mapa_marcador, session
# from src.configuration.config import DATA_FOLDER
# from src.helpers.logger import logger

# import os
import pandas as pd
from random import random, randint
from time import sleep
from math import floor

from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import Dropout
# import sqlalchemy_mixins
# import hashlib
# from tqdm import tqdm


class RNN:

    timeSteps = 500
    samples_count = 0

    def __init__(self):


        print("\n### O que você quer fazer? ")
        print("  # ( 0 ): Voltar")
        print("  # ( 1 ): Gerar dados de treinamento e teste")
        print("  # ( 2 ): Carregar dados de treinamento e teste")
        opt = int(input("# Opção: "))

        if opt == 1:
            self.prep_db()
        if opt == 2:
            self.load_db()

        print(self.DATA_X.shape)

        self.train()

    # region Carregando os dados
    def prep_db(self, missingProb=0.3):
        base = pd.read_pickle(
            'Computed/bases/a509466ad9104985a5bb3f7c686c5e36/chr_1_haplotypes.zip', compression='zip').T.ix[:, :((self.timeSteps*2) - 1)]

        mask = []
        for step in range(0, int(base.shape[1]/2)):
            if step > 10:
                mask.append(random() > missingProb)
            else:
                mask.append(True)

        DATA_X = []
        DATA_Y = []

        for row_idx, row in base.iterrows():
            print(row_idx)
            item0 = 0
            sample_x = []
            sample_y = []
            for item_idx, item in row.items():
                if item_idx % 2 == 0:
                    if not mask[int(item_idx/2)]:
                        sample_x.append([-1, -1])
                    else:
                        sample_x.append([item0, item])

                    sample_y.append([item0, item])
                else:
                    item0 = item

            DATA_X.append(pd.DataFrame(sample_x))
            DATA_Y.append(pd.DataFrame(sample_y))

        self.DATA_X = pd.DataFrame(DATA_X)
        self.DATA_Y = pd.DataFrame(DATA_Y)

        self.DATA_X.drop(self.DATA_X.tail(1).index, inplace=True)
        self.DATA_Y.drop(self.DATA_Y.head(1).index, inplace=True)        

        self.samples_count = self.DATA_X.shape[0]

        self.DATA_X.to_pickle(
            'Computed/imputation/data_x.zip', compression='zip')
        self.DATA_Y.to_pickle(
            'Computed/imputation/data_y.zip', compression='zip')

    def load_db(self):
        self.DATA_X = pd.read_pickle(
            'Computed/imputation/data_x.zip', compression='zip')
        self.DATA_Y = pd.read_pickle(
            'Computed/imputation/data_y.zip', compression='zip')
        self.samples_count = DATA_X.shape[0]
        
    # endregion

    def getData(self, typ='train', train_rel=0.99):
        if typ == 'train':
            minVal = 0
            maxVal = floor(self.samples_count*train_rel) - 1
        else:
            minVal = floor(self.samples_count*train_rel) - 1
            maxVal = self.samples_count - 1

        random_sample = randint(minVal, maxVal)
        # print(minVal, maxVal, random_sample)

        X = self.DATA_X.iloc[random_sample]
        y = self.DATA_Y.iloc[random_sample]

        X = X[0].values
        y = y[0].values        

        X = X.reshape(len(X), 2, 1)
        y = y.reshape(len(y), 2)

        return X, y

    def train(self):
        n_timeSteps = self.timeSteps

        # define model
        model = Sequential()
        model.add(LSTM(128, activation='relu', input_shape=(2, 1), batch_input_shape=(1, 2, 1), return_sequences=True, stateful=True))
        # model.add(LSTM(128, activation='relu', input_shape=(2, 1), stateful=True, batch_input_shape=(1, 2, 1)))
        model.add(Dropout(0.1))
        model.add(LSTM(128, return_sequences=True, activation='relu', stateful=True))
        model.add(Dropout(0.1))
        model.add(LSTM(64, activation='relu', stateful=True))
        model.add(Dropout(0.1))
        model.add(Dense(2, activation='tanh'))
        model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
        # model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
                                                                                
        # fit model                                         
        for i in range(150):
            X, y = self.getData()
            model.fit(X, y, epochs=1, batch_size=1, verbose=2)


        X, y = self.getData('teste')
        yhat = model.predict(X, batch_size=1)
        for i in range(len(X)):
        	print('Expected', y[i], 'Predicted', yhat[i])
