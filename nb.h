#include <iostream>
#include <vector>
#include <string>
#include <math.h>

using namespace std; 

// to train the model, first sort df by label
// then calculate the mean and std for each label
void trainModel(vector<vector<double>> train_df);

// vector<double> calcMean(const vector<vector<double>> df);
// vector<double> CalcStdDev(const vector<vector<double>> df, const vector<double> mean);

// to predict labels, use the mean and std & the gaussian func. 
vector<int> predictLabels(vector<vector<double>> test_df);

// g(x) = 1/sigma*(sqrt(2*pi))*exp(-1/2*pow((obs - mean)/std),2)
// void gaussianFunction(double std, double mean, double obs);
