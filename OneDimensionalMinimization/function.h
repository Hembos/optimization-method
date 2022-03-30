#pragma once
#include <cmath>

class Function
{
private:
    double a;
    double b;

    double (*func)(double x);

public:
    Function(double (*func)(double x), double a, double b)
        : a(a), b(b), func(func) {}

    double getFuncValue(double x)
    {
        return func(x);
    }
};