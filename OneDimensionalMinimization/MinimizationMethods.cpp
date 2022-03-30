#include "MinimizationMethods.h"
#include <iostream>

double MinimizationMethods::dichotomyMethod(double epsilon)
{
    double a = targetFunction.getLeftBorder();
    double b = targetFunction.getRightBorder();

    while (b - a > epsilon)
    {   
        double delta = 0.01 * (b - a);
        double x1 = (a + b) / 2 - delta;
        double x2 = (a + b) / 2 + delta;
        double fX1 = targetFunction(x1);
        double fX2 = targetFunction(x2);

        if (fX1 > fX2)
        {
            a = x1;
        }
        else
        {
            b = x2;
        }
    }

    return (a + b) / 2;
}

double MinimizationMethods::goldenSectionMethod(double epsilon)
{

    return 0;
}