import pandas as pd
import numpy as np
import requests
# import random as rnd
import sys

import predict
# using swig
# swig -c++ -python predict.i
# g++ -c -fpic predict.cpp predict_wrap.cxx -I/usr/include/python3.8
# g++ -shared predict.o predict_wrap.o -o _predict.so -lstdc++
# https://stackoverflow.com/questions/51466189/swig-c-to-python-vector-problems

# NBA api making endpoint calls
from nba_api.stats.endpoints import leaguegamelog

# leage game log
gameLog = leaguegamelog.LeagueGameLog(season=2019)

# gamelog has dataframe
'''
dataframe has the following fields
['SEASON_ID', 'TEAM_ID', 'TEAM_ABBREVIATION', 'TEAM_NAME', 'GAME_ID', 
'GAME_DATE', 'MATCHUP', 'WL', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M',
'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 
'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'PLUS_MINUS', 'VIDEO_AVAILABLE']
'''
df = gameLog.get_data_frames()[0]


def mergeOpponentPts(full_df, team1Abb):
    '''
    This function finds all the teams that played the specific team, and merges
    their pts of opponents into their dataframe
    '''
    # filter for specific team
    specificTeam_df = df.loc[df['TEAM_ABBREVIATION'] == team1Abb]
    # get game ID of all the games they have played so far
    game_id = [gid for gid in specificTeam_df['GAME_ID']]
    # will need to refactor this later
    temp_df = full_df[full_df.GAME_ID.isin(game_id)]
    temp_df = temp_df.loc[temp_df['TEAM_ABBREVIATION'] != team1Abb]

    return specificTeam_df.merge(temp_df[['GAME_ID', 'TEAM_ABBREVIATION', 'PTS']], on='GAME_ID', how='left', suffixes=['_t1', '_t2'])

def meanAndStd(team_df):
    team_mean_teamPts = team_df.PTS_t1.mean()
    team_std_teamPts = team_df.PTS_t1.std()

    team_mean_oppPts = team_df.PTS_t2.mean()
    team_std_oppPts = team_df.PTS_t2.std()

    return team_mean_teamPts, team_std_teamPts, team_mean_oppPts, team_std_oppPts


# teamA = mergeOpponentPts(df, 'TOR')
# teamB = mergeOpponentPts(df, 'MIL')

def gameSimCallC(numGames, teamA, teamB):
    teamAMeanPts, teamASTD, teamAOppoMeanPts, teamAOppoSTD = meanAndStd(teamA)
    teamBMeanPts, teamBSTD, teamBOppoMeanPts, teamBOppoSTD = meanAndStd(teamB)

    # print("I get here")

    returnVals = predict.gameSimulation(numGames, teamAMeanPts, teamASTD, teamAOppoMeanPts, teamAOppoSTD,
    teamBMeanPts, teamBSTD, teamBOppoMeanPts, teamBOppoSTD)

    # print(returnVals)
    for val in returnVals:
        print(val) 

# gameSimCallC(100, teamA, teamB)
if __name__ == "__main__":
    teamAarg = sys.argv[1]
    teamBarg = sys.argv[2]
    teamA = mergeOpponentPts(df, teamAarg)
    teamB = mergeOpponentPts(df, teamBarg)
    gameSimCallC(10000, teamA, teamB)