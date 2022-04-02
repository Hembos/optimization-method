#include "MinimizationMethods.h"
#include <iostream>
#include <fstream>

double MinimizationMethods::dichotomyMethod(double epsilon)
{
    std::ofstream logs;
    logs.open("../dichotomy.txt");
    logs << "Start didhotomy method" << std::endl;

    double a = targetFunction.getLeftBorder();
    double b = targetFunction.getRightBorder();

    int iterationNum = 0;

    while (b - a > epsilon)
    {
        logs << "\nIteration " << iterationNum << std::endl;
        logs << "Interval " << '[' << a << ", " << b << ']' << std::endl;

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

        iterationNum++;
    }

    logs << "\nSolution " << (a + b) / 2 << std::endl;
    logs << "\nFunction call count " << targetFunction.callCount;

    return (a + b) / 2;
}

double MinimizationMethods::goldenSectionMethod(double epsilon)
{
    std::ofstream logs;
    logs.open("../golden.txt");
    logs << "Start golden section method" << std::endl;

    targetFunction.callCount = 0;
    double a = targetFunction.getLeftBorder();
    double b = targetFunction.getRightBorder();
    double alpha = (3 - sqrt(5)) / 2;

    double lambda = a + alpha * (b - a);
    double mu = a + (1 - alpha) * (b - a);

    int iterationNum = 0;

    while (b - a > epsilon)
    {
        logs << "\nIteration " << iterationNum << std::endl;
        logs << "Interval " << '[' << a << ", " << b << ']' << std::endl;

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

        iterationNum++;
    }

    logs << "\nSolution " << (a + b) / 2 << std::endl;
    logs << "\nFunction call count " << targetFunction.callCount;

    return (a + b) / 2;
}