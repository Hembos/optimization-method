#include "MinimizationMethods.h"
#include <iostream>
#include <fstream>

double MinimizationMethods::dichotomyMethod(double epsilon)
{
    std::ofstream logs;
    logs.open("../dichotomy" + std::to_string(epsilon) + ".txt");
    logs << "Start didhotomy method" << std::endl;

    double a = targetFunction.getLeftBorder();
    double b = targetFunction.getRightBorder();

    int iterationNum = 0;

    while (b - a > epsilon)
    {
        logs << "\nIteration " << iterationNum << std::endl;
        logs << "Interval " << '[' << a << ", " << b << ']' << std::endl;

        double delta = 0.001 * (b - a);
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
    logs << "\nFunction call count " << targetFunction.callCount << std::endl;
    logs << "\nTheoretic function call count " << 2 * log((targetFunction.getRightBorder() - targetFunction.getLeftBorder()) / epsilon) / log(2 / 1.002) + 1;

    return (a + b) / 2;
}

double MinimizationMethods::goldenSectionMethod(double epsilon)
{
    std::ofstream logs;
    logs.open("../golden" + std::to_string(epsilon) + ".txt");
    logs << "Start golden section method" << std::endl;

    targetFunction.callCount = 0;
    double a = targetFunction.getLeftBorder();
    double b = targetFunction.getRightBorder();
    double alpha = (3 - sqrt(5)) / 2;

    double lambda = a + alpha * (b - a);
    double mu = a + (1 - alpha) * (b - a);

    double fLambda = targetFunction(lambda);
    double fMu = targetFunction(mu);

    logs << "\nlambda " << lambda << std::endl;
    logs << "\nmu " << mu << std::endl;
    logs << "\nf_lambda " << fLambda << std::endl;
    logs << "\nf_mu " << fMu << std::endl;

    int iterationNum = 0;

    while (true)
    {
        logs << "\nIteration " << iterationNum << std::endl;
        logs << "Interval " << '[' << a << ", " << b << ']' << std::endl;

        if (fLambda <= fMu)
        {
            b = mu;
            mu = lambda;
            lambda = a + alpha * (b - a);
            fMu = fLambda;

            if (b - a <= epsilon)
                break;

            fLambda = targetFunction(lambda);
        }
        else
        {
            a = lambda;
            lambda = mu;
            fLambda = fMu;
            mu = a + (1 - alpha) * (b - a);

            if (b - a <= epsilon)
                break;

            fMu = targetFunction(mu);
        }

        iterationNum++;
    }

    logs << "\nSolution " << (a + b) / 2 << std::endl;
    logs << "\nFunction call count " << targetFunction.callCount << std::endl;
    logs << "\nTheoretic function call count " << log((targetFunction.getRightBorder() - targetFunction.getLeftBorder()) / epsilon) / log(1 / (1 - alpha)) + 1 << std::endl;

    return (a + b) / 2;
}