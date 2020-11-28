#include "nb.h"

// global variables - need this to predict
vector<double> meanWin; 
vector<double> stdWin;
vector<double> meanLose;
vector<double> stdLose;


// g(x) = 1/sigma*(sqrt(2*pi))*exp(-1/2*pow((obs - mean)/std),2)
double gaussianFunction(const vector<double> std, const vector<double> mean, const vector<double> obs) {

    const size_t colSize = obs.size();

    double retProb = 1.0; 

    if (colSize != mean.size()) {
        cout << "Size of observations is different from training data" << endl;
        return 909; 
    }

    const double sqrtTwoPi = sqrt(2*M_PI);

    for (size_t col = 0; col < colSize; col++) {
        // partOne = 1/sigma*(sqrt(2*pi))
        // cout << std[col] << endl; 
        double partOne = 1/(std[col]*sqrtTwoPi); 
     
        // partTwo = pow(obs-mean/std, 2)
        double partTwo = pow(((obs[col] - mean[col])/std[col]), 2);
     
        // retProb *= partOne*exp(-0.5*partTwo); 
        // to prevent overflow
        retProb += log(partOne*exp(-0.5*partTwo)); 
        // cout << retProb << endl; 
    }

    return retProb; 

}

vector<double> calcMean(const vector<vector<double>> df) {
    const size_t rowSize = df.size();
    const size_t colSize = df[0].size();

    // have to declare size, otherwise get seg fault
    vector<double> mean((colSize), 0.0); 

    for (size_t i = 0; i < rowSize; i++) {
        vector<double> temp = df[i];
        for (size_t j = 0; j < colSize; j++) {
            mean[j] += temp[j]; 
        }
    }

    for (size_t i = 0; i < colSize; i++) {
        mean[i] /= rowSize; 
        // cout << mean[i] << endl; 
    }

    // cout << "mean size: " << mean.size() << endl; 
    
    return mean;
}

// std dev = sqrt(1/rowSize * sum of pow((val - mean), 2))
vector<double> CalcStdDev(const vector<vector<double>> df, const vector<double> mean) {
    const size_t rowSize = df.size();
    const size_t colSize = df[0].size();

    // have to declare size, otherwise get seg fault
    vector<double> std(colSize); 

    for (size_t row = 0; row < rowSize; row++) {
        vector<double> tempRow = df[row];
        for (size_t colVal = 0; colVal < colSize; colVal++) {
            // cout << tempRow.size() << endl;
            std[colVal] += pow((tempRow[colVal] - mean[colVal]), 2);
        }
        // cout << endl << endl; 
    }

    for (size_t col = 0; col < colSize; col++) {
        std[col] /= rowSize;
        std[col] = sqrt(std[col]);
    }

    // cout << "std size: " << std.size() << endl; 
    return std; 
}

void printVec(const vector<double> & vec) {
    vector<double>::const_iterator it;

    for (it = vec.begin(); it != vec.end(); it++) {
        cout << *it << "\t";
    }
    cout << endl << endl;
}

// removing labels before calculating mean/stddev
vector<double> sliceVector (vector<double> vec) {
    return vector<double>(vec.begin()+1, vec.end());  
}

// to train the model, first sort df by label
// then calculate the mean and std for each label
void trainModel(vector<vector<double>> train_df) {

    // declaring const variables (size of dataframe)
    const size_t rowSize = train_df.size();
    // cout << "rowSize: " << rowSize << endl; 

    // new dataframes for sortting win/lose data
    vector<vector<double>> train_df_win;
    vector<vector<double>> train_df_lose;

    int countWin = 0;
    int countLose = 0;

    // sorting data by labels
    for (size_t i = 0; i < rowSize; i++) {
        if (train_df[i][0] == 1) {
        // if (trainLabels[i] == "W") {
            vector<double> temp = sliceVector(train_df[i]);
            // printVec(temp);
            train_df_win.push_back(temp);
            countWin++;
        } else {
            // cout << train_df[i][0] << endl; 
            vector<double> temp1 = sliceVector(train_df[i]);
            train_df_lose.push_back(temp1);
            countLose++;
        }
    }
    // cout << "win count: " << countWin << endl;
    // cout << "lose count: " << countLose << endl;

    // calculate the mean and std for each label
    meanWin = calcMean(train_df_win);
    stdWin = CalcStdDev(train_df_win, meanWin);

    meanLose = calcMean(train_df_lose); 
    stdLose = CalcStdDev(train_df_lose, meanLose);
}

// to predict labels, use the mean and std & the gaussian formula 
vector<int> predictLabels(vector<vector<double>> test_df) {
    const size_t rowSize = test_df.size();
    
    const int win = 1;
    const int lose = 0;
    
    vector<int> predictedLabels(rowSize);

    for (size_t row = 0; row < rowSize; row++) {
        vector<double> tempRow = test_df[row];
        double winProb = gaussianFunction(stdWin, meanWin, tempRow);
        double loseProb = gaussianFunction(stdLose, meanLose, tempRow); 

        if (winProb == 909 || loseProb == 909) {
            cout << "Error in test dataframe size" << endl;
        }

        // cout << "Win: " << winProb << endl;
        // cout << "Lose: " << loseProb << endl; 

        if (winProb > loseProb) {
            predictedLabels.push_back(win);
        } else {
            predictedLabels.push_back(lose);
        }
    }

    return predictedLabels; 
}
