from robot.api.deco import library
from robot.api.deco import keyword
from robot.api.interfaces import ListenerV3
from robot.running import TestSuite


@library(scope='SUITE', version='0.1.0')
class ModelBasedLibrary(ListenerV3):

    def __init__(self, model: str = None, *args: str):
        print('Instance created')

        

    def start_suite(self, data, result):
        print('Start suite ' + data.longname)
        missingKW = data.resource.keywords.create(name='keyword 2', args=['${arg1}, ${arg2}'])
        missingKW.body.create_keyword(name='Log', args=['You called the automatically generated keyword ' + 'keyword 1' 
                                                        + ' which is missing in the resource files', 'WARN'])
        

    def start_test(self, data, result):
        print('Starting test ' + data.longname)

        

    @keyword('Run model based test')
    def runModel(self, path: str):
        print('*CONSOLE* Running Model')



    def end_suite(self, data, result):
        pass