#include <vector>

int singleGameSim(double teamA_ptsMn, double teamA_ptsStd,
                double teamA_oppPtsMn, double teamA_oppPtsStd, double teamB_ptsMn, 
                double teamB_ptsStd, double teamB_oppPtsMn, double teamB_oppPtsStd);

std::vector<double> gameSimulation(int numGames, double teamA_ptsMn, double teamA_ptsStd,
                double teamA_oppPtsMn, double teamA_oppPtsStd, double teamB_ptsMn, 
                double teamB_ptsStd, double teamB_oppPtsMn, double teamB_oppPtsStd);