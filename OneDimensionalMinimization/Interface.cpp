#include "Interface.h"
#include <boost/lexical_cast.hpp>

wxIMPLEMENT_APP(MinimizationApp);

wxBEGIN_EVENT_TABLE(MinimizationFrame, wxFrame)
    EVT_BUTTON(ID_BUTTON_SOLVE, MinimizationFrame::OnButtonSolveClicked)
    EVT_BUTTON(ID_BUTTON_SOLVE_DEFAULT, MinimizationFrame::OnButtonDefaultSolveClicked)
wxEND_EVENT_TABLE()

bool MinimizationApp::OnInit()
{
    m_locale.Init(wxLANGUAGE_RUSSIAN);
    MinimizationFrame *frame = new MinimizationFrame();
    frame->Show(true);
    return true;
}

MinimizationFrame::MinimizationFrame()
    : wxFrame(NULL, wxID_ANY, "Одномерная минимизация", wxPoint(30, 30), wxSize(650, 500))
{
    defaultFunction = Function([](double x)
                               { return sin(x) * x + 2 * cos(x); },
                               -5, -4);
    methods = MinimizationMethods(defaultFunction);

    staticTextEnterFunction = new wxStaticText(this, wxID_ANY, "Введите функцию:", wxPoint(5, 12), wxSize(150, 50));
    editFieldEnterFunction = new wxTextCtrl(this, wxID_ANY, "", wxPoint(150, 0), wxSize(500, 50));

    staticTextFunctionsLeftBorder = new wxStaticText(this, wxID_ANY, "Введите левую границу:", wxPoint(5, 62), wxSize(150, 50));
    staticTextFunctionsRightBorder = new wxStaticText(this, wxID_ANY, "Введите правую границу:", wxPoint(5, 112), wxSize(150, 50));
    editFieldFunctionsLeftBorder = new wxTextCtrl(this, wxID_ANY, "", wxPoint(150, 50), wxSize(500, 50));
    editFieldFunctionsRightBorder = new wxTextCtrl(this, wxID_ANY, "", wxPoint(150, 100), wxSize(500, 50));

    staticTextEnterEpsilon = new wxStaticText(this, wxID_ANY, "Введите требуемую точность:", wxPoint(5, 162), wxSize(150, 50));
    editFieldEnterEpsilon = new wxTextCtrl(this, wxID_ANY, "", wxPoint(150, 150), wxSize(500, 50));

    buttonSolve = new wxButton(this, ID_BUTTON_SOLVE, "Решить", wxPoint(5, 250), wxSize(100, 50));
    buttonSolveDefault = new wxButton(this, ID_BUTTON_SOLVE_DEFAULT, "Решить\nзадачу по\nумолчанию", wxPoint(105, 250), wxSize(100, 100));
}

void MinimizationFrame::OnButtonSolveClicked(wxCommandEvent &event)
{
    try
    {
        std::string epsilonStr = (editFieldEnterEpsilon->GetValue()).ToStdString();
        std::string functionStr = (editFieldEnterFunction->GetValue()).ToStdString();
        std::string leftBorderStr = (editFieldFunctionsLeftBorder->GetValue()).ToStdString();
        std::string rightBorderStr = (editFieldFunctionsRightBorder->GetValue()).ToStdString();

        if (functionStr == "")
            throw std::runtime_error("Введите функцию");

        double epsilon = boost::lexical_cast<double>(epsilonStr);
        double leftBorder = boost::lexical_cast<double>(leftBorderStr);
        double rightBorder = boost::lexical_cast<double>(rightBorderStr);

        ExpressionCalculate calculateFunc = ExpressionCalculate(functionStr);
        Function function = Function([&calculateFunc](double x){ return calculateFunc.calculate(x); }, leftBorder, rightBorder);

        methods.setTargetFunction(function);

        double dichotomyRes = methods.dichotomyMethod(epsilon);
        double goldenRes = methods.goldenSectionMethod(epsilon);

        MinimizationResultFrame* minimizationResultFrame = new MinimizationResultFrame(dichotomyRes, goldenRes);
        minimizationResultFrame->Show(true);
        event.Skip();
    }
    catch(const std::exception& e)
    {
        wxLogMessage(e.what());
        event.Skip();
    }
}

void MinimizationFrame::OnButtonDefaultSolveClicked(wxCommandEvent &event)
{
    try
    {
        methods.setTargetFunction(defaultFunction);

        std::string epsilonStr = (editFieldEnterEpsilon->GetValue()).ToStdString();
        if (epsilonStr == "")
            throw std::runtime_error("Введите точность");

        double epsilon = boost::lexical_cast<double>(epsilonStr);
        double dichotomyRes = methods.dichotomyMethod(epsilon);
        double goldenRes = methods.goldenSectionMethod(epsilon);
        MinimizationResultFrame* minimizationResultFrame = new MinimizationResultFrame(dichotomyRes, goldenRes);
        minimizationResultFrame->Show(true); 
        event.Skip();
    }
    catch (const std::exception &e)
    {
        wxLogMessage(e.what());
        event.Skip();
    }
}

MinimizationResultFrame::MinimizationResultFrame(double dichotomyRes, double goldenRes)
    : wxFrame(NULL, wxID_ANY, "Одномерная минимизация", wxPoint(30, 30), wxSize(650, 500))
{
    wxString dichotomyResStr = wxString::Format(wxT("Метод дихотомии: %lf"), dichotomyRes);
    wxString goldenResStr = wxString::Format(wxT("Метод золотого сечения: %lf"), goldenRes);

    staticTextDichotomyResult = new wxStaticText(this, wxID_ANY, dichotomyResStr, wxPoint(5, 5), wxSize(300, 25));
    staticTextGoldenResult = new wxStaticText(this, wxID_ANY, goldenResStr, wxPoint(5, 30), wxSize(300, 25));
}