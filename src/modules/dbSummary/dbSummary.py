from logs import logDecorator as lD 
import jsonref, pprint
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from tqdm import tqdm

from psycopg2.sql import SQL, Identifier, Literal

from lib.databaseIO import pgIO

from modules.dbSummary import utils

config = jsonref.load(open('../config/config.json'))
dbSummary_config = jsonref.load(open('../config/modules/dbSummary.json'))
logBase = config['logging']['logBase'] + '.modules.dbSummary.dbSummary'

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

@lD.log(logBase + '.getColumnInfo')
def getColumnMean(logger, column):

    try:

        queryColumnData = '''
        SELECT %s
        FROM raw_data.background
        '''

        columnData = pgIO.getAllData(queryColumnData, values=columnNames)

    except Exception as e:
        logger.error(f'Unable to get data for the column names: {e}')

    return columnData


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

    # for col, n in zip(['marital', 'id'], [10, 20]): #create config file with column names

    #     query = SQL('''
    #         SELECT 
    #             {} 
    #         from 
    #             {}.{}
    #         limit {}
    #         ''').format(
    #             Identifier(col),
    #             Identifier('raw_data'),
    #             Identifier('background'),
    #             Literal(n)
    #         )

    #     data = [d[0] for d in pgIO.getAllData(query)]
    #     print(data)

    # maritalDist = utils.getMaritalDistParallel()
    # print(maritalDist)
    
    tableInfo = {
        'totalNumUser': None,
        'totalNumColumns': None,
        'columnNames': None,
    }

    tableInfo['columnNames'] = getColumnNames()
    tableInfo['totalNumUser'] = getNumRowsCol()[0]
    tableInfo['totalNumColumns'] = getNumRowsCol()[1]

    #create a columnInfo dictionary with keys as the column name and values as the counts
    columnInfo = {key: None for key in tableInfo['columnNames']}

    #iterate through column names 
    for column in tqdm(columnInfo, total=getNumRowsCol()[1]):
        columnInfo[column] = dict(utils.getColDistParallel(column))

    # generateReport(tableInfo)

    print('Getting out of dbSummary module')
    print('-'*30)

    return

