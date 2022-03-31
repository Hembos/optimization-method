#pragma once
#include <string>
#include <string>
#include <queue>
#include <map>
#include <cmath>
#include <functional>

class ExpressionCalculate
{
private:
    enum TokenType
    {
        operation,
        function,
        number,
        openBracket,
        closeBracket,
        variable
    };

    struct Token
    {
        std::string name;
        TokenType type;
        Token(std::string name, TokenType type)
            : name(name), type(type) {}
    };

    std::string expr;

    using binary = std::function<double(double, double)>;
    std::map<std::string, binary> operations;
    using unary = std::function<double(double)>;
    std::map<std::string, unary> unaryFunctions;

    std::queue<Token> postfixNotation;

    std::queue<Token> createTokensFromExpr();
    TokenType getType(std::string const& name) const;
    void createPostfixNotation(std::queue<Token>& tokens);
    int getPriority(std::string const& operation) const;
    double calcExpression(double x);

public:
    ExpressionCalculate(std::string expr);
    
    double calculate(double x);
};