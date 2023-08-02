*** Settings ***
Resource    OpenTodos.resource
Resource    ShowAllTodos.resource
Metadata    ModelBasedTests              model.json
Metadata    Testing path 1               path.json
Metadata    Testing path 2               path_CompletedTodosDisplayed.json
# The following metadata is ignored
Metadata    Kaktus                       Baum
Metadata    asfd sdaf                    something.json
Metadata    oewijf
Metadata    foo                          bar
Metadata


*** Test Cases ***

Testing path 1
    [Documentation]        asdf
    Log    No operation

Testing path 2
    Log    No operation

Testing not model base test
    Log    Not model based test
    e_addTodo
    Keyword 1


*** Keywords ***



Keyword 1
    No Operation