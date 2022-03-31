#pragma once
#include "function.h"

class MinimizationMethods
{
private:
    Function targetFunction;

public:
    MinimizationMethods() {}

    MinimizationMethods(Function targetFunction)
        : targetFunction(targetFunction) {}

    double dichotomyMethod(double epsilon);

    double goldenSectionMethod(double epsilon);

    void setTargetFunction(Function function)
    {
        targetFunction = function;
    }    
};