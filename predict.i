%module predict
%{
#include "predict.h"
%}

%include "std_vector.i"

namespace std {
    %template(vectord) vector<double>;
}


%include "predict.h"