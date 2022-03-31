#pragma once
#include <cmath>
#include <functional>

class Function
{
private:
    double a;
    double b;

    std::function<double(double x)> func;

    int callCount = 0;

public:
    Function(std::function<double(double x)> func, double a, double b)
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