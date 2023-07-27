*** Settings ***
Library               ../ModelBasedLibrary.py
Suite Setup           Setup model    model.json
Suite Teardown        Teardown model


*** Test Cases ***

My first model based test
    Run model based test    path.json


*** Keywords ***



Keyword 1
    No Operation