#include <iostream>
#include "function.h"
#include "MinimizationMethods.h"
#include "ExpressionCalculate.h"

int main()
{
    // Function function = Function([](double x){ return sin(x) * x + 2 * cos(x); }, -5, -4);
    try
    {
        ExpressionCalculate calculator = ExpressionCalculate("x*sin(x)+2*cos(x)");
        Function function = Function([&calculator](double x)
                                     { return calculator.calculate(x); },
                                     -5., -4.);

        MinimizationMethods methods = MinimizationMethods(function);

        std::cout << methods.dichotomyMethod(0.00001) << std::endl;
        std::cout << methods.goldenSectionMethod(0.00001) << std::endl;
    }
    catch (const std::exception &e)
    {
        std::cerr << e.what() << '\n';
    }

    return 0;
}