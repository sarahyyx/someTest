from logs import logDecorator as lD 
import jsonref, pprint

config = jsonref.load(open('../config/config.json'))
module1_config = jsonref.load(open('../config/modules/module1.json'))
logBase = config['logging']['logBase'] + '.modules.module1.module1'


@lD.log(logBase + '.doSomething')
def doSomething(logger, inputDict):
    '''print a line
    
    This function simply prints a single line
    
    Parameters
    ----------
    logger : {logging.Logger}
        The logger used for logging error information
    '''

    try:
        print('We are in module 1')

        x = inputDict['x']
        y = inputDict['y']
        sum_xy = x+y
        print(sum_xy)
    except Exception as e:
        logger.error('doSomething failed because of {}'.format(e))

    return 

@lD.log(logBase + '.main')
def main(logger, resultsDict):
    '''main function for module1
    
    This function finishes all the tasks for the
    main function. This is a way in which a 
    particular module is going to be executed. 
    
    Parameters
    ----------
    logger : {logging.Logger}
        The logger used for logging error information
    resultsDict: {dict}
        A dintionary containing information about the 
        command line arguments. These can be used for
        overwriting command line arguments as needed.
    '''

    print('='*30)
    print('Main function of module 1')
    print('='*30)
    print('We get a copy of the result dictionary over here ...')
    pprint.pprint(resultsDict)

    # x = module1_config["inputs"]["x"].GetInt()
    # y = module1_config["inputs"]["y"].GetInt()

    inputDict = module1_config["inputs"]

    doSomething(inputDict)

    print('Getting out of Module 1')
    print('-'*30)

    return

