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
    %template(DoubleMap) map<std::string,double>;
    %template(IntMap) map<int,int>;
    %template() map<std::string,int>;
}


/*
%typemap(out) std::map<int, int> (PyObject* obj) %{
  obj = PyDict_New();
  for (const auto& n : $1) {
    PyObject* A = n.first.c_str();
    PyObject* B = n.second.c_str();
    PyDict_SetItem(obj, A, B);
    Py_XDECREF(A);
    Py_XDECREF(B);
  }
  $result = SWIG_Python_AppendOutput($result, obj);
%}
*/

%include "unit.h"

%template() std::pair<swig::SwigPtr_PyObject, swig::SwigPtr_PyObject>;
%template(pymap) std::map<swig::SwigPtr_PyObject, swig::SwigPtr_PyObject>;
