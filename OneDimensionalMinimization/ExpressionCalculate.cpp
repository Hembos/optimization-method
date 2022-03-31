#include "ExpressionCalculate.h"
#include <iostream>
#include <string.h>
#include <stack>

ExpressionCalculate::ExpressionCalculate(std::string expr)
{
    this->expr = expr;

    operations["+"] = [](double x, double y) -> double
    { return x + y; };
    operations["-"] = [](double x, double y) -> double
    { return x - y; };
    operations["/"] = [](double x, double y) -> double
    { return x / y; };
    operations["*"] = [](double x, double y) -> double
    { return x * y; };
    operations["^"] = [](double x, double y) -> double
    { return pow(x, y); };
    operations["~"] = [](double x, double y) -> double
    { return -x; };

    unaryFunctions["sin"] = [](double x) -> double
    { return sin(x); };
    unaryFunctions["cos"] = [](double x) -> double
    { return cos(x); };
    unaryFunctions["ln"] = [](double x) -> double
    { return log(x); };
    unaryFunctions["lg"] = [](double x) -> double
    { return log10(x); };
}

double ExpressionCalculate::calculate(double x)
{
    std::queue<Token> tokens = createTokensFromExpr();
    createPostfixNotation(tokens);

    return calcExpression(x);
}

double getNumber(std::stack<double> &numbers)
{
    double number = numbers.top();
    numbers.pop();
    return number;
}

double ExpressionCalculate::calcExpression(double x)
{
    std::queue<Token> tmpPostfixNotation = postfixNotation;

    std::stack<double> numbers;

    while (!tmpPostfixNotation.empty())
    {
        Token t = tmpPostfixNotation.front();
        tmpPostfixNotation.pop();
        if (t.name == ",")
            continue;

        if (t.type == TokenType::number)
        {
            numbers.push(std::stod(t.name));
            continue;
        }

        if (t.type == TokenType::variable)
        {
            numbers.push(x);
            continue;
        }

        if (t.type == TokenType::operation)
        {
            if (t.name == "~")
            {
                if (numbers.size() < 1)
                    throw std::runtime_error("Not correct expression");

                double a = getNumber(numbers);

                double opRes = operations[t.name](a, 0);

                numbers.push(opRes);
                continue;
            }

            if (numbers.size() < 2)
                throw std::runtime_error("Not correct expression");

            double b = getNumber(numbers);
            double a = getNumber(numbers);

            double opRes = operations[t.name](a, b);

            numbers.push(opRes);
            continue;
        }

        if (t.type == TokenType::function)
        {
            double funcRes = 0;
            if (numbers.size() < 1)
                throw std::runtime_error("Not correct expression");
            if (unaryFunctions.find(t.name) == unaryFunctions.end())
                throw std::runtime_error("Not correct function");

            double a = getNumber(numbers);

            funcRes = (unaryFunctions.at(t.name)(a));

            numbers.push(funcRes);
            continue;
        }
    }

    // if (numbers.size() != 1)
    //     throw std::runtime_error("Not correct expression");

    return numbers.top();
}

ExpressionCalculate::TokenType ExpressionCalculate::getType(std::string const &name) const
{
    if (name == "(")
        return TokenType::openBracket;
    if (name == ")")
        return TokenType::closeBracket;
    if (name == "+" || name == "-" || name == "*" || name == "/" || name == "," || name == "~")
        return TokenType::operation;
    if (strspn(name.c_str(), ".0123456789") == name.size())
        return TokenType::number;
    if (name.size() == 1)
        return TokenType::variable;

    return TokenType::function;
}

std::queue<ExpressionCalculate::Token> ExpressionCalculate::createTokensFromExpr()
{
    std::queue<Token> tokens;

    auto isDelimetr =
        [](char c)
    {
        std::string delimetrs = " ()+-/*,^";
        if (delimetrs.find(c) != std::string::npos)
            return true;
        return false;
    };

    int expSize = expr.size();

    for (int i = 0; i < expSize;)
    {
        std::string name;

        if (isDelimetr(expr[i]))
        {
            if (expr[i] == ' ')
            {
                i++;
                continue;
            }

            if (expr[i] == '-' &&
                (i != 0 && isDelimetr(expr[i - 1]) && expr[i - 1] != ')' || i == 0))
            {
                name = '~';
            }
            else
            {
                name = expr[i];
            }
            i++;
        }
        else
        {
            while (!isDelimetr(expr[i]) && i < expr.size())
            {
                name += expr[i];
                i++;
            }
        }

        Token t(name, getType(name));
        tokens.push(t);
    }

    return tokens;
}

void ExpressionCalculate::createPostfixNotation(std::queue<Token> &tokens)
{
    std::stack<Token> tmpTokenStack;
    int numBracket = 0;

    while (!tokens.empty())
    {
        Token t = tokens.front();
        tokens.pop();

        switch (t.type)
        {
        case TokenType::operation:
            if (!tmpTokenStack.empty())
            {
                int curPriority = getPriority(t.name);
                while (!tmpTokenStack.empty() &&
                       (tmpTokenStack.top().type == TokenType::operation && curPriority <= getPriority(tmpTokenStack.top().name) || tmpTokenStack.top().type == TokenType::function))
                {
                    postfixNotation.push(tmpTokenStack.top());
                    tmpTokenStack.pop();
                }
            }
            tmpTokenStack.push(t);
            break;

        case TokenType::function:
            while (!tmpTokenStack.empty() && tmpTokenStack.top().type == TokenType::function)
            {
                postfixNotation.push(tmpTokenStack.top());
                tmpTokenStack.pop();
            }
            tmpTokenStack.push(t);
            break;

        case TokenType::variable:
        case TokenType::number:
            postfixNotation.push(t);
            break;

        case TokenType::openBracket:
            tmpTokenStack.push(t);
            numBracket++;
            break;

        case TokenType::closeBracket:
            while (tmpTokenStack.top().type != TokenType::openBracket)
            {
                if (tmpTokenStack.size() == 1)
                    throw std::runtime_error("Not correct expression");

                postfixNotation.push(tmpTokenStack.top());
                tmpTokenStack.pop();
            }
            tmpTokenStack.pop();
            numBracket--;
            break;

        default:
            break;
        }
    }

    if (numBracket != 0)
        throw std::runtime_error("Not correct expression");

    while (!tmpTokenStack.empty())
    {
        postfixNotation.push(tmpTokenStack.top());
        tmpTokenStack.pop();
    }
}

int ExpressionCalculate::getPriority(std::string const &operation) const
{
    if (operation == "+" || operation == "-")
        return 2;
    if (operation == "*" || operation == "/")
        return 3;
    if (operation == "^")
        return 4;
    if (operation == "~")
        return 5;

    return 0;
}