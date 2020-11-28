import pandas as pd
import requests
import sys

import predict

# to get team ID (needed to get advanced stats)
from nba_api.stats.static import teams
# for advanced stats
from nba_api.stats.endpoints import teamgamelog
from nba_api.stats.endpoints import leaguegamelog

gameLog = leaguegamelog.LeagueGameLog(season=2019)
gameLog_df = gameLog.get_data_frames()[0]

def getAdvStats(teamAbbrev, Season="2019-20"):
    teamId = teams.find_team_by_abbreviation(teamAbbrev)['id']
    advStats = teamgamelog.TeamGameLog(team_id = teamId, season=Season)
    return advStats.get_data_frames()[0]

# df1 = teamGameLog, df2 = leagueGameLog
def addOppScore(df1, df2):
    rowSize, _ = df1.shape
    for i in range(rowSize):
        s = df1.loc[i, 'MATCHUP']
        df1.loc[i, 'oppTeam'] = s[-3:]

    # return pd.merge(df1, df2[['GAME_ID', 'TEAM_ABBREVIATION','PTS']], how='left', left_on=['Game_ID', 'oppTeam'], right_on=['GAME_ID', 'TEAM_ABBREVIATION'], suffixes=['_t1', '_t2'])
    return pd.merge(df1[['Game_ID', 'MATCHUP', 'FGA', 'FG_PCT', 'FG3A', 'FG3_PCT', 'FTA', 'FT_PCT', 'OREB', 'TOV', 'oppTeam']], df2[['GAME_ID', 'TEAM_ABBREVIATION','PTS', 'FGA', 'FG_PCT', 'FG3A', 'FG3_PCT', 'FTA', 'FT_PCT', 'OREB', 'TOV']], how='left', left_on=['Game_ID', 'oppTeam'], right_on=['GAME_ID', 'TEAM_ABBREVIATION'], suffixes=['_t1', '_t2'])

# returns mean and std of team's pts 
def calcScoreByAdvStats(df):
    rowSize, _ = df.shape
    for i in range(rowSize):
        fga_t1 = df.loc[i, 'FGA_t1']
        fgpct_t1 = df.loc[i, 'FG_PCT_t1']
        fga_t2 = df.loc[i, 'FGA_t2']
        fgpct_t2 = df.loc[i, 'FG_PCT_t2']


        fg3a_t1 = df.loc[i, 'FG3A_t1']
        fg3pct_t1 = df.loc[i, 'FG3_PCT_t1']
        fg3a_t2 = df.loc[i, 'FG3A_t2']
        fg3pct_t2 = df.loc[i, 'FG3_PCT_t2']

        fta_t1 = df.loc[i, 'FTA_t1']
        ftapct_t1 = df.loc[i, 'FT_PCT_t1']
        fta_t2 = df.loc[i, 'FTA_t2']
        ftapct_t2 = df.loc[i, 'FT_PCT_t2']

        oreb_t1 = df.loc[i, 'OREB_t1']
        tov_t1 = df.loc[i, 'TOV_t1']
        oreb_t2 = df.loc[i, 'OREB_t2']
        tov_t2 = df.loc[i, 'TOV_t2']
        # adds a new coloum to the DF
        
        df.loc[i, 'estPTS_t1'] = 2*(fga_t1*fgpct_t1) + 3*(fg3a_t1 * fg3pct_t1) + (fta_t1*ftapct_t1) + (oreb_t1/2) - (2*tov_t1)
        df.loc[i, 'estPTS_t2'] = 2*(fga_t2*fgpct_t2) + 3*(fg3a_t2 * fg3pct_t2) + (fta_t2*ftapct_t2) + (oreb_t2/2) - (2*tov_t2)

    return df.estPTS_t1.mean(), df.estPTS_t1.std(), df.estPTS_t2.mean(), df.estPTS_t2.std()


def main(teamA, teamB, numGames):
    teamA_df = getAdvStats(teamA)
    teamB_df = getAdvStats(teamB)

    tA_df = addOppScore(teamA_df, gameLog_df)
    tB_df = addOppScore(teamB_df, gameLog_df)

    teamAMeanPts, teamASTD, teamAOppoMeanPts, teamAOppoSTD = calcScoreByAdvStats(tA_df)
    teamBMeanPts, teamBSTD, teamBOppoMeanPts, teamBOppoSTD = calcScoreByAdvStats(tB_df)

    # print(teamAMeanPts, teamASTD, teamAOppoMeanPts, teamAOppoSTD)
    # print(teamBMeanPts, teamBSTD, teamBOppoMeanPts, teamBOppoSTD)
    returnVals = predict.gameSimulation(numGames, teamAMeanPts, teamASTD, teamAOppoMeanPts, teamAOppoSTD,
    teamBMeanPts, teamBSTD, teamBOppoMeanPts, teamBOppoSTD)

    for val in returnVals:
        print(val) 


if __name__ == "__main__":
    # game teamGameLog first
    teamAarg = sys.argv[1]
    teamBarg = sys.argv[2]

    main(teamAarg, teamBarg, 10000)