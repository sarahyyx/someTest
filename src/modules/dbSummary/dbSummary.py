from logs import logDecorator as lD 
import jsonref, pprint
import json
import numpy as np 
import matplotlib.pyplot as plt
from tqdm import tqdm
import operator

from psycopg2.sql import SQL, Identifier, Literal

from lib.databaseIO import pgIO

from modules.dbSummary import utils
from modules.dbSummary import reportWriter

config = jsonref.load(open('../config/config.json'))
dbSummary_config = jsonref.load(open('../config/modules/dbSummary.json'))
logBase = config['logging']['logBase'] + '.modules.dbSummary.dbSummary'


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

@lD.log(logBase + '.getTopValuesCol')
def getTopValuesCol(logger, d, top_d):

    try:
        for column in d:
            top_d[column] = dict(sorted(d[column].items(), key=operator.itemgetter(1), reverse=True)[:dbSummary_config["params"]["top_number"]])

    except Exception as e:
        logger.error(f'Unable to get data for the column names: {e}')

    return top_d 

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

    tableInfo = {
        'totalNumUser': None,
        'totalNumColumns': None,
        'columnNames': None,
    }

    tableInfo['columnNames'] = getColumnNames()
    tableInfo['totalNumUser'] = getNumRowsCol()[0]
    tableInfo['totalNumColumns'] = getNumRowsCol()[1]

    # #create a columnInfo dictionary with keys as the column name and values as the counts
    # columnInfo = {key: None for key in tableInfo['columnNames']}
    topValuesColumns = {key: None for key in tableInfo['columnNames']}

    # #populating the columnInfo dictionary with column counts 
    # for column in tqdm(columnInfo, total=getNumRowsCol()[1]):
    #     columnInfo[column] = dict(utils.getColDistParallel(column))

    # #save both dictionaries to the data/final folder, run only on first try
    # with open('/home/sarah/Documents/programs/someTest/data/final/tableInfo.json', 'w') as f:
    #     json.dump(tableInfo, f)
    # f.close()

    # with open('/home/sarah/Documents/programs/someTest/data/final/columnInfo.json', 'w') as f:
    #     json.dump(columnInfo, f)
    # f.close()

    #reading from final data json file instead of populating the dict again
    columnInfo = jsonref.load(open('../data/final/columnInfo.json'))
    
    topValuesColumns = getTopValuesCol(columnInfo, topValuesColumns)

    print("Plotting graphs...")
    for columnName in tqdm(tableInfo['columnNames']):
        utils.plotCountGraph(columnName, list(topValuesColumns[columnName].keys()), list(topValuesColumns[columnName].values()))
    print("--- Finished plotting ----")

    reportWriter.generateIntro(tableInfo)

    reportWriter.generateColNames(tableInfo)

    reportWriter.generateTop(topValuesColumns)

    print('Getting out of dbSummary module')
    print('-'*30)

    return

