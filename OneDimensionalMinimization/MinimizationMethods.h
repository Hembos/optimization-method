#pragma once
#include "function.h"

class MinimizationMethods
{
private:
    Function targetFunction;

public:
    MinimizationMethods(Function targetFunction)
        : targetFunction(targetFunction) {}

    double dichotomyMethod(double epsilon);

    double goldenSectionMethod(double epsilon);
};