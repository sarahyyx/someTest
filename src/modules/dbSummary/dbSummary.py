from logs import logDecorator as lD 
import jsonref, pprint
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt

from psycopg2.sql import SQL, Identifier, Literal

from lib.databaseIO import pgIO

from modules.dbSummary import utils

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

@lD.log(logBase + '.generateReport')
def generateReport(logger, r):
    
    report = f'''

# Table Summary

# Abstract: 
This report will give a summary of the target table: raw_data.background of the MindLinc database.

# Summary Results

This table has information on {r['totalNumUser']} users, 
with {r['totalNumColumns']} attribute columns. These columns are {r['columnNames']}.


| variable | median | mean | std |
|----------|--------|------|-----|
| $x$      | {r['totalNumUser']} | 25 | 1 |
| $y$      | {r['totalNumUser']} | 25 | 1 |

        '''

    with open('../report/report2.md', 'w') as f:
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

@lD.log(logBase + '.getNumRowsCol')
def getNumRowsCol(logger):

    try:

        queryNumColumn = '''
        SELECT COUNT (*) column_name 
        FROM information_schema.columns 
        WHERE table_schema = 'raw_data'
        AND table_name =  'background'
        '''

        queryNumRows = '''
        SELECT COUNT (*)
        FROM raw_data.background
        '''

        #extracting the column name elements from the tuple
        numRowsCol = []
        for tuple in pgIO.getAllData(queryNumRows):
            numRowsCol.append(tuple[0])
        for tuple in pgIO.getAllData(queryNumColumn):
            numRowsCol.append(tuple[0])

    except Exception as e:
        logger.error(f'Unable to get data: {e}')

    return numRowsCol 

@lD.log(logBase + '.getColumnNames')
def getColumnNames(logger):

    try:

        queryColumnNames = '''
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_schema = 'raw_data'
        AND table_name =  'background'
        '''

        #extracting the column name elements from the tuple
        columnNames = []
        for tuple in pgIO.getAllData(queryColumnNames):
            columnNames.append(tuple[0])


    except Exception as e:
        logger.error(f'Unable to get data for the column names: {e}')

    return columnNames 

@lD.log(logBase + '.getColumnMean')
def getColumnMean(logger, columnNames):

    try:

        queryColumnData = '''
        SELECT %s
        FROM raw_data.background
        '''

        columnData = pgIO.getAllData(queryColumnData, values=columnNames)

    except Exception as e:
        logger.error(f'Unable to get data for the column names: {e}')

    return columnData

# @lD.log(logBase + '.getSigCols')
# def getSigCols(logger, columnNames):

#     try:

#         queryColumnNullCount = '''
#         SELECT COUNT(%s)
#         FROM raw_data.background
#         '''

#         columnNullCount = []
#         for tuple in pgIO.getAllData(queryColumnNullCount, values=columnNames):
#             columnNullCount.append(tuple[0])

#     except Exception as e:
#         logger.error(f'Unable to get data for the column names: {e}')

#     return columnNullCount 

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
    print('Main function of dbSummary module')
    print('='*30)
    # print('We get a copy of the result dictionary over here ...')
    # pprint.pprint(resultsDict)



    for col, n in zip(['marital', 'id'], [10, 20]):

        query = SQL('''
            SELECT 
                {} 
            from 
                {}.{}
            limit {}
            ''').format(
                Identifier(col),
                Identifier('raw_data'),
                Identifier('background'),
                Literal(n)
            )

        data = [d[0] for d in pgIO.getAllData(query)]
        print(data)

    # maritalDist = utils.getMaritalDist()
    # maritalDist = utils.getMaritalDistParallel()
    # print(maritalDist)

    # tableInfo = {
    #     'totalNumUser': None,
    #     'totalNumColumns': None,
    #     'columns': {
    #                 'names': None,
    #                 'type': None,
    #                 'numEntries': None,
    #                 'means': None,
    #                 'mins': None,
    #                 'maxs': None,
    #                 },
    # }

    # tableInfo['columns']['names'] = getColumnNames()
    # tableInfo['totalNumUser'] = getNumRowsCol()[0]
    # tableInfo['totalNumColumns'] = getNumRowsCol()[1]

    # print(tableInfo)

    # print(getColumnMean())

    #generateReport(tableInfo)


    print('Getting out of dbSummary module')
    print('-'*30)

    return

