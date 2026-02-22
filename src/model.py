import numpy as np
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Dense, Flatten, Concatenate, Dropout, TimeDistributed
from tensorflow.keras import Model as KerasModel
import tensorflow as tf


# Entrée :
# - role
# - bans (les champions bannis devront avoir une sortie d'environ 0) -> 10
# - picks (de même pour les champions picks) -> 9 (au max 9 si tout les autres joueurs ont picks)
# - données sur chaque champions de
#   l'utilisateur (winrate, pickrate, kda moyen) -> dans le cas où il n'y pas de donnée prendre 50 % wr, 0% pr et kda
#   moyen du joueur peut être rajouter un algorithme knn ou autre pour estimer les stats avec des champions qu'il n'a
#   pas joué avec les données d'autre joueur ? -> 172


class Model:
    def __init__(self, championsCount, ):
        roleInput = Input(shape=(1,), name="roleInput")
        bansInput = Input(shape=(10,), name="bansInput")
        picksInput = Input(shape=(9,), name="picksInput")
        statsInput = Input(shape=(championsCount, 3), name="playerStatsInput")

        # Transforme les données de chaque champion en vecteur en 8 dimension pour que le modèle apprenne mieux
        emdeddedStatsInput = TimeDistributed(Dense(8, activation='relu'))(statsInput)
        emdeddedStatsInput = Flatten()(emdeddedStatsInput)

        inputs = Concatenate()([roleInput, bansInput, picksInput, emdeddedStatsInput])

        layers = Dense(256, activation='relu')(inputs)
        layers = Dropout(0.3)(layers)
        layers = Dense(128, activation='relu')(layers)
        layers = Dropout(0.3)(layers)
        layers = Dense(64, activation='relu')(layers)

        output = Dense(championsCount, activation='softmax')(layers)

        self.model = KerasModel(inputs=[roleInput, bansInput, picksInput, statsInput], outputs=output)
        self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    def train(self, roleInputs, bansInputs, picksInputs, statsInputs, championOutputs, batchSize, epochs):
        self.model.fit(
            x={"roleInput": roleInputs, "bansInput": bansInputs, "picksInput": picksInputs,
               "playerStatsInput": statsInputs},
            y=championOutputs,
            batch_size=batchSize,
            epochs=epochs,
            validation_split=0.1,
            shuffle=True)

    def predict(self, roleInputs, bansInputs, picksInputs, statsInputs):
        self.model.predict({"roleInput": roleInputs, "bansInput": bansInputs, "picksInput": picksInputs,
                            "playerStatsInput": statsInputs})

    def save(self, filePath):
        self.model.save(filePath)
