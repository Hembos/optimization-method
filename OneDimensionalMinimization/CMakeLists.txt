cmake_minimum_required(VERSION 3.0.0)
project(Minimization VERSION 0.1.0)

find_package(wxWidgets REQUIRED COMPONENTS net core base)
include(${wxWidgets_USE_FILE})

add_executable(Minimization MinimizationMethods.cpp 
                            function.h MinimizationMethods.h 
                            ExpressionCalculate.cpp ExpressionCalculate.h
                            Interface.cpp Interface.h)

target_link_libraries(Minimization ${wxWidgets_LIBRARIES})
set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
include(CPack)
