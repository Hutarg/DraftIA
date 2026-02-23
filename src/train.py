import random
import time
import numpy as np
from model import Model
from stats import *
from utils import *

model = Model()
model.save(f"../models/v0.h5")  # test de sauvegarde

currentPlayerPuuid = getAccount("europe", "Hutarg", "EUW")["puuid"]

roleInputs = []
bansInputs = []
picksInputs = []
statsInputs = []
championOutputs = []

version = 1

while True:
    t = time.time()
    while time.time() - t < 100:
        for id in getMatchesIds("europe", currentPlayerPuuid):
            match = getMatch("europe", id)

            if match["info"]["gameMode"] != 'CLASSIC':
                continue

            if match["info"]["teams"][0]["win"]:
                winningTeam = match["info"]["teams"][0]
                losingTeam = match["info"]["teams"][1]
            else:
                winningTeam = match["info"]["teams"][1]
                losingTeam = match["info"]["teams"][0]

            winningParticipants = []
            losingParticipants = []
            for participant in match["info"]["participants"]:
                if participant["teamId"] == winningTeam["teamId"]:
                    winningParticipants.append(participant)
                else:
                    losingParticipants.append(participant)

            targetIndex = random.randint(0, len(winningParticipants) - 1)
            target = winningParticipants[targetIndex]

            championOutputs.append([1 if i == championsIndices[riotChampionsNames[target["championId"]]]
                                    else 0 for i in range(len(championsIndices) - 1)])

            if target["teamPosition"] == "TOP":
                role = 1
            elif target["teamPosition"] == "JUNGLE":
                role = 2
            elif target["teamPosition"] == "MIDDLE":
                role = 3
            elif target["teamPosition"] == "BOTTOM":
                role = 4
            elif target["teamPosition"] == "UTILITY":
                role = 5
            else:
                continue

            roleInputs.append(role)

            bans = []
            for ban in match["info"]["teams"][0]["bans"]:
                bans.append(championsIndices[riotChampionsNames[ban["championId"]]])
            for ban in match["info"]["teams"][1]["bans"]:
                bans.append(championsIndices[riotChampionsNames[ban["championId"]]])

            bansInputs.append(bans)

            turn = random.randint(0, 1)
            pickCount = random.randint(0, 5)

            winningPickCount = clamp(pickCount + turn, 0, 4)
            losingPickCount = clamp(pickCount, 0, 5)

            losingPicks = [
                championsIndices[riotChampionsNames[losingParticipants[i]["championId"]]] if i < losingPickCount else -1
                for
                i in range(5)]

            winningPicks = []

            for i, participant in enumerate(winningParticipants):
                if i == targetIndex:
                    continue

                if len(winningPicks) >= winningPickCount:
                    break

                winningPicks.append(championsIndices[riotChampionsNames[participant["championId"]]])

            while len(winningPicks) < 4:
                winningPicks.append(-1)

            picksInputs.append(losingPicks + winningPicks)

            statsInputs.append(getStats("europe", currentPlayerPuuid))

        currentPlayerPuuid = target["puuid"]

    model.train(np.array(roleInputs), np.array(bansInputs), np.array(picksInputs), np.array(statsInputs),
                np.array(championOutputs), len(roleInputs), 20)
    model.save(f"../models/v{version}.h5")
    version += 1
