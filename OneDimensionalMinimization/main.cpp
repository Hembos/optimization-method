#include <iostream>
#include "function.h"

int main()
{
    Function function = Function([](double x){ return sin(x) * x + 2 * cos(x); }, -5, -4);

    std::cout << function.getFuncValue(3) << std::endl;

    return 0;
}