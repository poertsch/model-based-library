# model-based-library
Model based testing with Robot Framework based on GraphWalker models

# Status of this repository

Initial development is currently going on here. This Project is far away from being usable for anybody.

# User Guide

You have to complete the following steps to run a model base test.

1. Draw a model with GraphWalker
1. Generate one or multiple paths with GraphWalker CLI
1. Create a model based test suite
1. Run the tests

## Draw a model with GraphWalker

In order to run a model based test you need to draw a model. Model based Library supports GraphWalker models.
See https://graphwalker.github.io/ for details how to draw a model.

## Generate one or multiple paths with GraphWalker CLI

For the model you created you need to generate one or multiple paths. You can generate a path with the GraphWalker CLI (see https://graphwalker.github.io/). Use the command `java -jar graphwalker-cli-4.3.1.jar GLOBAL_OPTIONS offline OPTIONS -m <model-file> "GENERATOR(STOP_CONDITION)" >> path.json`. See the GraphWalker Wiki for details: https://github.com/GraphWalker/graphwalker-project/wiki/Offline.

## Create a model based test suite

A Model based test suite can be created like a normal test suite in robot framework. The only difference is that each test for a given path needs 
additional configuration. Lets assume that you have a GraphWalker model
defined in the file `model.json` and that you have a path for that model
defined in `path.json`.

To create a model base test suite you first need to mark a test suite as
model base. In the Settings section you need to add the following Metadata:

```
Metadata    ModelBasedTests    model.json
```

Based on this metadata the test suite is marked as model based and the
graph in `model.json`. Each edge and vertex in the model
needs to have a keyword with the same name as the edge or vertex. You 
can define the keywords in the Keywords section or in resource files.
If you use resource files you need to import them in the Settings section
like you do with normal test suites. If during test execution a keyword is
missing for a vertex or edge, you will get a runtime error.

To test a given path for the defined model you need to add the following
metadata:

```
Metadata    Testing path 1    path.json
```

Within the metadata you define a test name and the path for the test. In the example above the test name is `Testing path 1` and the path is defined in `path.json`. Additional you need to create the test in the Test Cases section of the suite. Since a test case cannot be empty you need to add at least one keyword to the test:

```
*** Test Cases ***

Testing path 1
    [Documentation]        You can also define a documentation, tags, etc...
    Log    This is a model based test.
```

The following example shows a complete test suite:

```
*** Settings ***
# You can import resoutces, add documentation etc.
Resource    OpenTodos.resource
Resource    ShowAllTodos.resource
# Metdata for the model based tests
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
    Log    This is a model based test.


Testing path 2
    Log    This is another model based test.


A normal test case
    [Documentation]     You can also add testcases which are not model based.
    Log    Not a model based test
    e_addTodo
    Keyword 1


*** Keywords ***



Keyword 1
    No Operation
```

## Run the tests

Copy the file `ModelBasedModifier.py` in the root folder of your test suites and run robot framework with `--prerunModifier ./ModelBasedModifier.py`.

