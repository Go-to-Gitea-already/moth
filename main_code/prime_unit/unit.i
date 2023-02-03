%module "unit"

%{
#include "unit.h"
%}

%include stl.i
/* instantiate the required template specializations */
namespace std {
    %template(IntVector)    vector<int>;
    %template(DoubleVector) vector<double>;
    %template(PrimeUnitVector) vector<PrimeUnit>;
}

%include "unit.h"

