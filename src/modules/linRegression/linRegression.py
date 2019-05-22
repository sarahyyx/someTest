from logs import logDecorator as lD 
import jsonref, pprint
import numpy as np 
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

config = jsonref.load(open('../config/config.json'))
linRegression_config = jsonref.load(open('../config/modules/linRegression.json'))
logBase = config['logging']['logBase'] + '.modules.linRegression.linRegression'


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
        print('We are in test function')

    except Exception as e:
        logger.error('doSomething failed because of {}'.format(e))

    return 


@lD.log(logBase + '.fitModel')
def fitModel(logger, x, y):
    '''print a line
    
    This function simply prints a single line
    
    Parameters
    ----------
    logger : {logging.Logger}
        The logger used for logging error information
    '''

    try:
        print('We are in fitModel function')

        model = LinearRegression()
        model.fit(x,y)

        print("intercept: ", model.intercept_)
        print("slope: ", model.coef_)
        b0 = model.intercept_
        b1 = model.coef_

        fig = plt.figure()
        ax = plt.subplot(111)
        ax.scatter(x,y, marker="x")
        plt.title("LinReg Test")

        y_pred = model.predict(x)
        ax.plot(x, y_pred, 'r')
        plt.savefig('../results/plot.png')


    except Exception as e:
        logger.error('fitModel failed because of {}'.format(e))

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
    print('Main function of linRegression module')
    print('='*30)
    print('We get a copy of the result dictionary over here ...')
    pprint.pprint(resultsDict)

    # x = module1_config["inputs"]["x"].GetInt()
    # y = module1_config["inputs"]["y"].GetInt()


    inputDict = linRegression_config["inputs"]

    doSomething(inputDict)

    x = np.load(linRegression_config["params"]["x"])
    x = np.array(x).reshape((-1,1))
    y = np.load(linRegression_config["params"]["y"])

    fitModel(x,y)

    print('Getting out of linRegression module')
    print('-'*30)

    return

