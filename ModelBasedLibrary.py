from robot.api.deco import library
from robot.api.deco import keyword
from robot.api.interfaces import ListenerV3
from robot.running import TestSuite


@library(scope='SUITE', version='0.1.0')
class ModelBasedLibrary(ListenerV3):

    def __init__(self):
        print('Instance created')

    ALL_SUITES = {'...': TestSuite()}
    MODEL: str = None
        

    def start_suite(self, data, result):
        print('Start suite ' + data.longname)
        ModelBasedLibrary.ALL_SUITES[data.longname] = data
        print(ModelBasedLibrary.ALL_SUITES)
        

    def start_test(self, data, result):
        if(ModelBasedLibrary.MODEL != None):
            print('Starting test ' + data.longname)
            print('Available keywords:')
            for keyword in ModelBasedLibrary.ALL_SUITES[data.parent.longname].resource.keywords:
                print(keyword)
        
        

    @keyword('Setup model')
    def setupModel(self, model: str):
        print('*CONSOLE* Model: ' + model)
        ModelBasedLibrary.MODEL = model

    @keyword('Teardown model')
    def teardwonModel(self):
        ModelBasedLibrary.MODEL = None

    @keyword('Run model based test')
    def runModel(self, path: str):
        print('*CONSOLE* Running Model')



    def end_suite(self, data, result):
        ModelBasedLibrary.ALL_SUITES.pop(data.longname)
        print(ModelBasedLibrary.ALL_SUITES)