#pragma once
#include <wx/wxprec.h>

#ifndef WX_PRECOMP
#include <wx/wx.h>
#endif

#include "MinimizationMethods.h"
#include "ExpressionCalculate.h"
#include "function.h"

class MinimizationApp : public wxApp
{
public:
    virtual bool OnInit();

private:
    wxLocale m_locale;
};

class MinimizationFrame : public wxFrame
{
public:
    wxStaticText* staticTextEnterFunction;
    wxTextCtrl* editFieldEnterFunction;

    wxStaticText* staticTextFunctionsLeftBorder;
    wxStaticText* staticTextFunctionsRightBorder;
    wxTextCtrl* editFieldFunctionsLeftBorder;
    wxTextCtrl* editFieldFunctionsRightBorder;

    wxStaticText* staticTextEnterEpsilon;
    wxTextCtrl* editFieldEnterEpsilon;

    wxButton* buttonSolve;
    wxButton* buttonSolveDefault;

    Function defaultFunction;
    Function nonDefaultFuntion;
    MinimizationMethods methods;

public:
    MinimizationFrame();

    wxDECLARE_EVENT_TABLE();
private:
    void OnExit(wxCommandEvent &event);

    void OnButtonSolveClicked(wxCommandEvent &event);

    void OnButtonDefaultSolveClicked(wxCommandEvent &event);
};

class MinimizationResultFrame : public wxFrame
{
public:
    wxStaticText* staticTextDichotomyResult;
    wxStaticText* staticTextGoldenResult;

    MinimizationResultFrame(double dichotomyRes, double goldenRes);
};

enum
{
    ID_BUTTON_SOLVE = 10001,
    ID_BUTTON_SOLVE_DEFAULT
};
