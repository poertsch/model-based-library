# License https://github.com/poertsch/model-based-library?tab=GPL-3.0-1-ov-file#readme
# See https://github.com/poertsch/model-based-library

from robot.api import TestSuite, ResultWriter
from robot.api import SuiteVisitor
from robot.model import TestSuite
from robot.running.model import TestSuite as RunningTestSuite
import json

class ModelBasedModifier(SuiteVisitor):
    def start_suite(self, suite: TestSuite) -> bool | None:
        prepareSuite(suite)

def prepareSuite(suite: TestSuite):
    print()
    print(f'Prepare Suite: {suite.longname}')
    print()
    isModelBased = False
    model = ''
    testNames = {}

    # Extract test names and path
    for key, fileName in suite.metadata.items():
        if(key == 'ModelBasedTests'):
            isModelBased = True
            model = fileName
    for key, fileName in suite.metadata.items():
        if(isModelBased):
            testNames[key] = fileName
    if(isModelBased):
        print('Suite is model based')
        print()
        processModelBasedSuite(suite, testNames, model)




def processModelBasedSuite(suite: TestSuite, testNames, model):
    # read the json file model.json
    with open(str(suite.source.parent.absolute()) + '/' + model) as f:
        # read the file line by line
        # read each line as a json object
        # append the json object to the list
        model_list = [json.loads(line) for line in f]

    # missingKeywordNames = collectNamesForMissingKeywords(suite, model_list)

    for testName, pathName in testNames.items():
        parentPathName = str(suite.source.parent.absolute())

        curTest = findTestByName(suite, testName)

        if(curTest != None):
            print(f'Processing path from {pathName} for test "{testName}"')

            # extract the path from the path json file
            path_list = extractPathList(pathName, parentPathName)

            #for each element in the path call the keyword
            #if the keyword does not exist, generate one and log a WARNING
            for path in path_list:
                addKeywordToTestAndResources(suite, [], curTest, path)




def addKeywordToTestAndResources(suite, missingKeywordNames, curTest, path):
    kw = path['currentElementName']

    # curTest.body.create_keyword(name=kw, args=kw_args)
    curTest.body.create_keyword(name=kw)
    print(f'Keyword added: {kw}')




def extractPathList(pathName, parentPathName):
    with open(parentPathName + '/' + pathName) as f:
            # read the file line by line
            # read each line as a json object
            # append the json object to the list
        path_list = [json.loads(line) for line in f]
    return path_list


def findTestByName(suite, testName):
    curTest = None
    for test in suite.tests:
        if(test.name == testName):
            curTest = test
    return curTest


