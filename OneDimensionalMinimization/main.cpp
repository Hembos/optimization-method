#include <iostream>
#include "function.h"
#include "MinimizationMethods.h"

int main()
{
    Function function = Function([](double x){ return sin(x) * x + 2 * cos(x); }, -5, -4);
    MinimizationMethods methods = MinimizationMethods(function);
    
    std::cout << methods.dichotomyMethod(0.00001) << std::endl;
    std::cout << methods.goldenSectionMethod(0.00001) << std::endl;

    return 0;
}