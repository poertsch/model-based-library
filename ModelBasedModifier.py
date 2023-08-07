from robot.api import TestSuite, ResultWriter
from robot.api import SuiteVisitor
from robot.model import TestSuite
from robot.running.model import ResourceFile
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
    
    missingKeywordNames = collectNamesForMissingKeywords(suite, model_list)
        
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
                addKeywordToTestAndResources(suite, missingKeywordNames, curTest, path)




def addKeywordToTestAndResources(suite, missingKeywordNames, curTest, path):
    kw = path['currentElementName']
    dataList = path['data']
    kw_args = []
    kw_argNames = []

            # Add Keyword with Arguments to Test Case
    for data in dataList:
                # each data is a dictionary
                # get the key and value of the dictionary
        for key, value in data.items():
            if key != 'JsonContext':
                        # print(key)
                        # print(value)
                kw_args.append(f'{key}={value}')
                kw_argNames.append(f'${{{key}}}')

    curTest.body.create_keyword(name=kw, args=kw_args)
            
            # If keyword is missing in resource files, also add keyword
    if(missingKeywordNames.count(kw) > 0):
        missingKW = suite.resource.keywords.create(name=kw, args=kw_argNames)
        missingKW.body.create_keyword(name='Log', args=['You called the automatically generated keyword ' + kw 
                                                                + ' which is missing in the resource files', 'WARN'])
        missingKeywordNames.remove(kw)
    


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


def collectNamesForMissingKeywords(suite: TestSuite, model_list):
    missingKeywordNames = []
    foundKeywordNames = []
    for key in suite.resource.keywords:
        foundKeywordNames.append(key.name)

        for suiteImport in suite.resource.imports.to_dicts():
            importedResource: ResourceFile = ResourceFile.from_file_system(suite.source.parent.absolute().name + '/' + suiteImport["name"])
            for importedKeyword in importedResource.keywords:
                foundKeywordNames.append(importedKeyword.name)
            
        print(f'Available keywords: {foundKeywordNames}')

    for model in model_list[0]['models']:

        for vertice in model['vertices']:
            try:
                foundKeywordNames.index(vertice['name'])
            except ValueError:
                missingKeywordNames.append(vertice['name'])
                
                
        for edge in model['edges']:
            try:
                foundKeywordNames.index(edge['name'])
            except ValueError:
                missingKeywordNames.append(edge['name'])
                
                
        
    missingKeywordNames = (list(dict.fromkeys(missingKeywordNames)))
    print(f'Missing keywords: {missingKeywordNames}')

    return missingKeywordNames


############### run the suite #####################

# root = TestSuite.from_file_system('tests/')

# prepareSuite(root)

# for suite in root.suites:

#     prepareSuite(suite)

# print()
# print("Run tests....")
# print()
# print()
# root.run(output='results/output.xml')
# ResultWriter('results/output.xml').write_results(log='results/log.html', report='results/report.html')