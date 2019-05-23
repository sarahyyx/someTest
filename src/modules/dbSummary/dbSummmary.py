from logs import logDecorator as lD 
import jsonref, pprint
import numpy as np 
import matplotlib.pyplot as plt

from lib.databaseIO import pgIO

config = jsonref.load(open('../config/config.json'))
dbSummary_config = jsonref.load(open('../config/modules/dbSummary.json'))
logBase = config['logging']['logBase'] + '.modules.dbSummary.dbSummary'


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
def generateReport(logger, r):
    
    report = f'''

# Title of the Report

# Abstract: Some text for the Abstract ...

# Description

$$ y = m x + c $$

$x$ and $y$ are  ...

The calucalted values for $m$ and $c$ are ...

Details of the input ...

| variable | median | mean | std |
|----------|--------|------|-----|
| $x$      | {r['x-median']} | 25 | 1 |
| $y$      | {r['y-median']} | 25 | 1 |

# Results

This is the value of m: 

# Conclusion

Some conclusion

        '''

    with open('../report/report1.md', 'w') as f:
        f.write( report )

    return

@lD.log(logBase + '.getUserMSE')
def getUserMSE(logger, user):

    data = []

    try:
        query = '''
        select * from raw_data.mse where siteid = %s and backgroundid=%s limit 10;
        '''

        data = pgIO.getAllData(query, user)

    except Exception as e:
        logger.error(f'Unable to get data for user: {user}: {e}')

    return data 


@lD.log(logBase + '.generatePlot')
def generatePlot(logger, x, y, m):
    '''print a line
    
    This function simply prints a single line
    
    Parameters
    ----------
    logger : {logging.Logger}
        The logger used for logging error information
    '''

    try:
        print('We are in generatePlot function')

        fig = plt.figure(figsize=(4,3))
        ax = plt.axes([0.15, 0.22, 0.84, 0.77])
        ax.plot(x,y, "s", mfc='None', mec='black', alpha=0.4)
        # plt.title("LinReg Test")

        y_pred = m.predict(x)
        ax.plot(x, y_pred, color='black', lw=2)

        plt.xlabel(r'$x$')
        plt.ylabel(r'$y$')

        plt.savefig('../results/plot_1.png', dpi=300)


    except Exception as e:
        logger.error('generatePlot failed because of {}'.format(e))

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

    fittedModel = fitModel(x,y)

    generatePlot(x, y, fittedModel)

    results = {
        'x-median': 20,
        'y-median': 20,
    }
    generateReport( results)

    user = ('CenterPointe', '18425')
    data = getUserMSE(user)
    print(data) #data type is a list

    print('Getting out of linRegression module')
    print('-'*30)

    return

