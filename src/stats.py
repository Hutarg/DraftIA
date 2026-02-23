import requests
import time
from src.utils import *
from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path(__file__).resolve().parent.parent / "riot" / ".env"
load_dotenv(env_path)

API_KEY = os.getenv("RIOT_API_KEY")
headers = {"X-Riot-Token": API_KEY}

apiRequestsCount = 0
firstRequestTime = time.time()


def wait():
    global apiRequestsCount, firstRequestTime
    time.sleep(0.1)

    current_time = time.time()
    dt = current_time - firstRequestTime

    if dt >= 120:
        firstRequestTime = current_time
        apiRequestsCount = 0
        elapsed = 0

    if apiRequestsCount >= 100:
        sleep_time = 140 - dt
        if sleep_time > 0:
            print(f"Rate limit reached. Sleeping for {sleep_time:.2f} seconds.")
            time.sleep(sleep_time)

        firstRequestTime = time.time()
        apiRequestsCount = 0

    apiRequestsCount += 1
    print(f"API calls: {apiRequestsCount}")


def getAccount(continent: str, name: str, tag: str):
    wait()
    url = f"https://{continent}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tag}"
    response = requests.get(url, headers=headers)

    if response.status_code == 429:
        time.sleep(60)
        print("Rate limit exceeded. Sleeping for 1 minutes")
        return getAccount(continent, name, tag)
    elif response.status_code != 200:
        print("API Error:", response.status_code, response.text)
        return None

    return response.json()


def getSummoner(region: str, puuid: str):
    wait()
    url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"
    response = requests.get(url, headers=headers)

    if response.status_code == 429:
        time.sleep(60)
        print("Rate limit exceeded. Sleeping for 1 minutes")
        return getSummoner(region, puuid)
    elif response.status_code != 200:
        print("API Error:", response.status_code, response.text)
        return None

    return response.json()


def getChampionsStats(region: str, puuid: str):
    wait()
    url = f"https://{region}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}"
    response = requests.get(url, headers=headers)

    if response.status_code == 429:
        time.sleep(60)
        print("Rate limit exceeded. Sleeping for 1 minutes")
        return getChampionsStats(region, puuid)
    elif response.status_code != 200:
        print("API Error:", response.status_code, response.text)
        return None

    return response.json()


def getMatchesIds(continent: str, puuid: str):
    wait()
    url = f"https://{continent}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
    response = requests.get(url, headers=headers)

    if response.status_code == 429:
        time.sleep(60)
        print("Rate limit exceeded. Sleeping for 1 minutes")
        return getMatchesIds(continent, puuid)
    elif response.status_code != 200:
        print("API Error:", response.status_code, response.text)
        return None

    return response.json()


def getMatch(continent: str, matchId: str):
    wait()
    url = f"https://{continent}.api.riotgames.com/lol/match/v5/matches/{matchId}"
    response = requests.get(url, headers=headers)

    if response.status_code == 429:
        time.sleep(60)
        print("Rate limit exceeded. Sleeping for 1 minutes")
        return getMatch(continent, matchId)
    elif response.status_code != 200:
        print("API Error:", response.status_code, response.text)
        return None

    return response.json()


def getStats(continent: str, puuid: str):
    matchesIds = getMatchesIds(continent, puuid)

    winrate = 0
    kda = 0

    stats = [[0, 0, 0] for i in range(len(championsIndices) - 1)]
    counts = [0 for i in range(len(championsIndices) - 1)]

    for matchId in matchesIds[:50]:
        match = getMatch(continent, matchId)

        if match["info"]["gameMode"] != 'CLASSIC':
            continue

        for participant in match["info"]["participants"]:
            if participant["puuid"] == puuid:
                team = match["info"]["teams"][0] if participant["teamId"] == match["info"]["teams"][0]["teamId"] \
                    else match["info"]["teams"][1]

                winrate += + 1 if team["win"] else 0
                kda = kda + (participant["kills"] + participant["assists"])/(participant["deaths"] + 1)

                championIndex = championsIndices[riotChampionsNames[participant["championId"]]]-1
                win = 1 if team["win"] else 0
                stats[championIndex] = [stats[championIndex][0] + win,
                                        stats[championIndex][1] + 1,
                                        stats[championIndex][2] + (participant["kills"] + participant["assists"])/(participant["deaths"] + 1)]

                counts[championIndex] = counts[championIndex] + 1

    winrate = winrate/50
    kda = kda/50

    for i in range(len(stats)):
        if counts[i] == 0:
            stats[i] = [winrate, stats[i][1]/len(stats), kda]
        else:
            stats[i] = [stats[i][0]/counts[i], stats[i][1]/len(stats), stats[i][2]/counts[i]]

    return stats


if __name__ == "__main__":
    puuid = getAccount("europe", "Hutarg", "EUW")["puuid"]
    print(getSummoner("EUW1", puuid))
    for id in getMatchesIds("europe", puuid):
        print(getMatch("europe", id))
