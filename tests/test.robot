*** Settings ***
Resource    OpenTodos.resource
Resource    ShowAllTodos.resource
Metadata    foo                          bar
Metadata    ModelBasedTests              model.json
Metadata    Testing path 1               path.json
Metadata    Testing path 2               path.json


*** Test Cases ***

Testing path 1
    [Documentation]        asdf
    Log    No operation

Testing path 2
    Log    No operation


*** Keywords ***



Keyword 1
    No Operation