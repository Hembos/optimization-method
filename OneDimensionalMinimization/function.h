#pragma once
#include <cmath>

class Function
{
private:
    double a;
    double b;

    double (*func)(double x);

    int callCount = 0;

public:
    Function(double (*func)(double x), double a, double b)
        : a(a), b(b), func(func) {}

    double getFuncValue(double x)
    {
        callCount++;
        return func(x);
    }

    double getLeftBorder()
    {
        return a;
    }

    double getRightBorder()
    {
        return b;
    }

    double operator ()(double x)
    {
        callCount++;
        return func(x);
    }
};