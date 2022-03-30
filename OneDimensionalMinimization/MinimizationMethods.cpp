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
    double a = targetFunction.getLeftBorder();
    double b = targetFunction.getRightBorder();
    double alpha = (3 - sqrt(5)) / 2;

    double lambda = a + alpha * (b - a);
    double mu = a + (1 - alpha) * (b - a);

    while (b - a > epsilon)
    {
        double fLambda = targetFunction(lambda);
        double fMu = targetFunction(mu);

        if (fLambda <= fMu)
        {
            b = mu;
            mu = lambda;
            lambda = a + alpha * (b - a);
        }
        else
        {
            a = lambda;
            lambda = mu;
            mu = a + (1 - alpha) * (b - a);
        }
    }

    return (a + b) / 2;
}