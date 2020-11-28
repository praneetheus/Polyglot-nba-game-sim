#include "loadfiles.h"
#include "nb.h"
// g++ -O3 -Wall main.cpp loadfiles.cpp nb.cpp -o gnb

// load data
// train the model
// predict

void printVector(const vector<vector<double>> & vec) { 

    vector< vector<double> >::const_iterator row; 
    vector<double>::const_iterator col; 

    for (row = vec.begin(); row != vec.end(); ++row) { 
         for (col = row->begin(); col != row->end(); ++col) { 
            cout << *col << "\t"; 
         } 
         cout << endl;
    } 

} 

void printVec(const vector<string> & vec) {
    vector<string>::const_iterator it;

    for (it = vec.begin(); it != vec.end(); it++) {
        cout << *it << endl;
    }
}

int main() {
    // loading training data
    vector<vector<double>> df = loadData("./train_df.csv");
    // vector<string> labels = loadLables("./train_labels.csv");

    // loading test data 
    vector<vector<double>> test_df = loadData("./test_df.csv");
    const double toteGames = test_df.size();

    // training model
    trainModel(df);

    // // predicting 
    vector<int> preds = predictLabels(test_df); 

    int score = 0;
    
    for (size_t i = 0; i < preds.size(); i++) {
        if (preds[i] == 1) {
            score++;
        }
        // cout << preds[i] << endl;
    }

    // cout << "Won " << score << "/" << toteGames <<  " games; win percent is: " << double(score)/toteGames << endl; 
    cout << toteGames << endl;
    cout << score << endl;
    cout << double(score)/toteGames << endl;
 
    return 0;
}
