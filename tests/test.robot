*** Settings ***
Library               ../ModelBasedLibrary.py    tests/model.json    tests/path.json


*** Test Cases ***

My first model based test
    Run model based test    path.json


*** Keywords ***



Keyword 1
    No Operation