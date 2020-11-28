#include "loadfiles.h"

vector<vector<double>> loadData (string fname) {
    vector<vector<double>> df;
    ifstream file(fname);
    string line; 
    char delimiter = ',';
    string val; 

    while(getline(file, line)) {
        vector<double> valArray; 

        istringstream ss(line);
    
        while (getline(ss, val, delimiter)) {
            double v;
            if (val == "W") {
                v = 1; 
            } else if (val == "L") {
                v = 0;
            } else {
                v = stod(val);
            }
            valArray.push_back(v);
        }
        df.push_back(valArray);
    }
    
    return df; 
}