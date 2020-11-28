import pandas as pd
import numpy as np
import requests
import random as rnd
import os.path
import sys
import subprocess

from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamelog

# get df from nba api and save it and return it
# if df is already saved, return it
def get_df():
    if not (os.path.isfile('./full_df.csv')):
        # print("I run in If")
        gameLog = leaguegamelog.LeagueGameLog(season=2019)
        df = gameLog.get_data_frames()[0]
        df.to_csv("full_df.csv", index=False)
    else:
        # print("I run in else")
        df = pd.read_csv("./full_df.csv")
    return df 

# gets team id by the given team abbreviation
def getTeamByAbb(teamAbbrev):
    return teams.find_team_by_abbreviation(teamAbbrev)['id']

# returns a filtered df - only contains the specified team info
def returnTeamDf(df, teamId):
    return df.loc[df.TEAM_ID == teamId]

# takes team df, and merges all the team's opponent's stats
def returnTeamAndOppStats(df, teamId):
    ret_df = returnTeamDf(df, teamId)

    # get all the game id played by the team
    gid = [gid for gid in ret_df['GAME_ID']]
    
    # finding teams that played TOR
    temp_df = df.loc[df.TEAM_ID != teamId]
    temp_df = temp_df[temp_df.GAME_ID.isin(gid)]
    
    ret_df = ret_df[['WL', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'GAME_ID']]
    temp_df = temp_df[['GAME_ID','FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF' ]]

    new_df = pd.merge(ret_df, temp_df, on='GAME_ID', suffixes=['_t1', '_t2'])

    return new_df

# uses random.gaussian to estimate advanced stats - this is the "simulating" game stats
def generateRandomTeamStats(df, teamId, simNum):
    ret_df = returnTeamDf(df, teamId)
    ret_df = ret_df[['FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF']]

    # Generate hypothetical stats based on team in season stats 
    est_df = pd.DataFrame(columns=ret_df.columns)
    for i in range(simNum):
        est_df.loc[i, 'FGM'] = rnd.gauss(ret_df.FGM.mean(), ret_df.FGM.std())
        est_df.loc[i, 'FGA'] = rnd.gauss(ret_df.FGA.mean(), ret_df.FGA.std())
        est_df.loc[i, 'FG_PCT'] = rnd.gauss(ret_df.FG_PCT.mean(), ret_df.FG_PCT.std())
        est_df.loc[i, 'FG3M'] = rnd.gauss(ret_df.FG3M.mean(), ret_df.FG3M.std())
        est_df.loc[i, 'FG3A'] = rnd.gauss(ret_df.FG3A.mean(), ret_df.FG3A.std())
        est_df.loc[i, 'FG3_PCT'] = rnd.gauss(ret_df.FG3_PCT.mean(), ret_df.FG3_PCT.std())
        est_df.loc[i, 'FTM'] = rnd.gauss(ret_df.FTM.mean(), ret_df.FTM.std())
        est_df.loc[i, 'FTA'] = rnd.gauss(ret_df.FTA.mean(), ret_df.FTA.std())
        est_df.loc[i, 'FT_PCT'] = rnd.gauss(ret_df.FT_PCT.mean(), ret_df.FT_PCT.std())
        est_df.loc[i, 'OREB'] = rnd.gauss(ret_df.OREB.mean(), ret_df.OREB.std())
        est_df.loc[i, 'DREB'] = rnd.gauss(ret_df.DREB.mean(), ret_df.DREB.std())
        est_df.loc[i, 'REB'] = rnd.gauss(ret_df.REB.mean(), ret_df.REB.std())
        est_df.loc[i, 'AST'] = rnd.gauss(ret_df.AST.mean(), ret_df.AST.std())
        est_df.loc[i, 'STL'] = rnd.gauss(ret_df.STL.mean(), ret_df.STL.std())
        est_df.loc[i, 'BLK'] = rnd.gauss(ret_df.BLK.mean(), ret_df.BLK.std())
        est_df.loc[i, 'TOV'] = rnd.gauss(ret_df.TOV.mean(), ret_df.TOV.std())
        est_df.loc[i, 'PF'] = rnd.gauss(ret_df.PF.mean(), ret_df.PF.std())
    return est_df

# merge the estimated team stats & save it as file
def mergeRandomStats(df1, df2):
    if (df1.shape != df2.shape):
        raise Exception

    test_data = df1.join(df2, lsuffix='_t1', rsuffix='_t2')
    test_data.to_csv("test_df.csv", header=False, index=False)


# Need labels for training data
# def saveLabels(df):
#     labels = df.loc[:, 'WL']
#     labels.to_csv("train_labels.csv", header=False, index=False)

def saveData(df):
    train_data = df.iloc[:,[0,1,2,3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]]
    train_data.to_csv("train_df.csv", header=False, index=False)

if __name__ == "__main__":
    teamAarg = sys.argv[1]
    teamBarg = sys.argv[2]

    train_df = returnTeamAndOppStats(get_df(), getTeamByAbb(teamAarg))
    saveData(train_df)
    # saveLabels(train_df)

    est_df1 = generateRandomTeamStats(get_df(), getTeamByAbb(teamAarg), 200)
    est_df2 = generateRandomTeamStats(get_df(), getTeamByAbb(teamBarg), 200)
    mergeRandomStats(est_df1, est_df2)

    proc = subprocess.Popen(["./gnb"])
    proc.wait()