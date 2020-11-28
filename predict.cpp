#include "predict.h"
#include <iostream>
#include <string>
#include <random>
#include <cmath>
// #include <tuple>
#include <vector>

int singleGameSim(double teamA_ptsMn, double teamA_ptsStd,
                double teamA_oppPtsMn, double teamA_oppPtsStd, double teamB_ptsMn, 
                double teamB_ptsStd, double teamB_oppPtsMn, double teamB_oppPtsStd)
{
    std::random_device rd;
    std::mt19937 e2(rd());

    std::default_random_engine generator;
    std::normal_distribution<double> teamA_pts_dist(teamA_ptsMn, teamA_ptsStd);
    std::normal_distribution<double> teamA_oppPts_dist(teamA_oppPtsMn, teamA_oppPtsStd);

    std::normal_distribution<double> teamB_pts_dist(teamB_ptsMn, teamB_ptsStd);
    std::normal_distribution<double> teamB_oppPts_dist(teamB_oppPtsMn, teamB_oppPtsStd);

    auto teamAscore = teamA_pts_dist(e2) + teamB_oppPts_dist(e2);
    auto teamBscore = teamB_pts_dist(e2) + teamA_oppPts_dist(e2);

    // std::cout << teamAscore << std::endl;
    // std::cout << teamBscore << std::endl;

    if (round(teamAscore) > round(teamBscore)) {
        return 1;
    } else if (round(teamAscore) < round(teamBscore)) {
        return -1;
    }
    return 0;
}

std::vector<double> gameSimulation(int numGames, double teamA_ptsMn, double teamA_ptsStd,
                double teamA_oppPtsMn, double teamA_oppPtsStd, double teamB_ptsMn, 
                double teamB_ptsStd, double teamB_oppPtsMn, double teamB_oppPtsStd) 
{

    double teamAwin = 0;
    double teamBwin = 0;
    double tie = 0; 

    for (auto i = 0; i < numGames; i++) {
        int singleGameResult = singleGameSim(teamA_ptsMn, teamA_ptsStd, teamA_oppPtsMn,
         teamA_oppPtsStd, teamB_ptsMn, teamB_ptsStd, teamB_oppPtsMn, teamB_oppPtsStd);
         if (singleGameResult == 1) {
             teamAwin++;
         } else if (singleGameResult == -1) {
             teamBwin++;
         } else {
             tie++;
         }
    }

    double teamAwinRate = teamAwin/(teamAwin+teamBwin+tie);
    double teamBwinRate = teamBwin/(teamAwin+teamBwin+tie);
    double tieRate = tie/(teamAwin+teamBwin+tie);
    std::vector<double> ret;
    ret.push_back(teamAwinRate);
    ret.push_back(teamBwinRate);
    ret.push_back(tieRate);

    return ret;
}

