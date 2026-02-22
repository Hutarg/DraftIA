import requests
import time
from utils import *

API_KEY = "RGAPI-d4b466b8-e4a3-435c-98f9-a5091c049d9b"
headers = {"X-Riot-Token": API_KEY}


def getAccount(continent: str, name: str, tag: str):
    url = f"https://{continent}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tag}"
    response = requests.get(url, headers=headers)
    return response.json()


def getSummoner(region: str, puuid: str):
    url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"
    response = requests.get(url, headers=headers)
    return response.json()


def getChampionsStats(region: str, puuid: str):
    url = f"https://{region}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}"
    response = requests.get(url, headers=headers)
    return response.json()


def getMatchesIds(continent: str, puuid: str):
    url = f"https://{continent}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
    response = requests.get(url, headers=headers)
    return response.json()


def getMatch(continent: str, matchId: str):
    url = f"https://{continent}.api.riotgames.com/lol/match/v5/matches/{matchId}"
    response = requests.get(url, headers=headers)
    return response.json()


def getStats(continent: str, puuid: str):
    matchesIds = getMatchesIds(continent, puuid)

    winrate = 0
    kda = 0

    stats = [[0, 0, 0] for i in range(len(championsIndices) - 1)]
    counts = [0 for i in range(len(championsIndices) - 1)]

    for matchId in matchesIds[:50]:
        time.sleep(10)
        match = getMatch(continent, matchId)

        for participant in match["info"]["participants"]:
            if participant["puuid"] == puuid:
                team = match["info"]["teams"][0] if participant["teamId"] == match["info"]["teams"][0]["teamId"] \
                    else match["info"]["teams"][1]

                wr = wr + 1 if team["win"] else 0
                kda = kda + (participant["kills"] + participant["assists"])/(participant["deaths"] + 1)

                championIndex = championsIndices[riotChampionsNames[participant["championId"]]]-1
                stats[championIndex] = [stats[championIndex][0] + 1 if team["win"] else 0,
                                        stats[championIndex][1] + 1,
                                        stats[championIndex][2] + (participant["kills"] + participant["assists"])/(participant["deaths"] + 1)]

                counts[championIndex] = counts[championIndex] + 1

    winrate = winrate/50
    kda = kda/50

    for i in range(len(stats)):
        count = counts[i] if counts[i] > 0 else 1
        stats[i] = [stats[i][0]/count, stats[i][1]/len(stats), stats[i][2]/count]

    return stats


if __name__ == "__main__":
    puuid = getAccount("europe", "Hutarg", "EUW")["puuid"]
    print(getSummoner("EUW1", puuid))
    for id in getMatchesIds("europe", puuid):
        print(getMatch("europe", id))
