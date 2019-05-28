from logs import logDecorator as lD 
import jsonref, pprint
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt

from psycopg2.sql import SQL, Identifier, Literal
from lib.databaseIO import pgIO
from collections import Counter
from textwrap import wrap

from tqdm import tqdm
from multiprocessing import Pool
from time import sleep

config = jsonref.load(open('../config/config.json'))
dbSummary_config = jsonref.load(open('../config/modules/dbSummary.json'))
logBase = config['logging']['logBase'] + '.modules.dbSummary.utils'

@lD.log(logBase + '.getMaritalDistPP')
def getMaritalDistPP(logger, data):
    
    try:
        data = [d[0] for d in data]
        c = Counter(data)
        return c
    except Exception as e:
        logger.error(f'{e}')
        return Counter([])

    return

#parallel processing, used in conjunction with above
@lD.log(logBase + '.getMaritalDistParallel')
def getMaritalDistParallel(logger):

    p = Pool()
    

    result = Counter([])
    try:
        query = '''
        SELECT marital from raw_data.background
        '''

        dataIter = pgIO.getDataIterator(query, chunks= 1000)
        
        for c in tqdm(p.imap(getMaritalDistPP, dataIter), total=501):
            result.update(c)

        return result

    except Exception as e:
        logger.error(f'Unable to generate result: {e}')


    p.close()

    return result

#How to use the above two functions with SQL Querying
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

@lD.log(logBase + '.getColDistPP')
def getColDistPP(logger, data):
    
    try:
        data = [d[0] for d in data]
        c = Counter(data)
        return c
    except Exception as e:
        logger.error(f'{e}')
        return Counter([])

    return

#parallel processing, used in conjunction with above
@lD.log(logBase + '.getColDistParallel')
def getColDistParallel(logger, column):

    p = Pool()
    
    result = Counter([])
    try:
        query = SQL('''
        SELECT 
            {} 
        FROM 
            raw_data.background
        ''').format(
            Identifier(column)
        )

        dataIter = pgIO.getDataIterator(query, chunks= 1000)
        
        for c in tqdm(p.imap(getMaritalDistPP, dataIter), total=501):
            result.update(c)

        return result

    except Exception as e:
        logger.error(f'Unable to generate result: {e}')


    p.close()

    return result

@lD.log(logBase + '.plotCountGraph')
def plotCountGraph(logger, attribute, valueList, countList):
    
    try:       
        y_pos = np.arange(len(valueList))
        valueList = [ '\n'.join(wrap(v, 5)) for v in valueList ]

        plt.bar(y_pos, countList, align='center', alpha=0.5, color='black')
        plt.xticks(y_pos, valueList)
        plt.ylabel('Value Count')
        plt.title(attribute)
        plt.tight_layout()

        plt.savefig(f'../results/AttributeValueCounts/{attribute}.png', dpi=300)
        plt.close()

    except Exception as e:
        logger.error(f'{e}')

    return

@lD.log(logBase + '.getMaritalDist')
def getMaritalDist(logger):

    result = Counter([])
    try:
        query = '''
        SELECT marital from raw_data.background
        '''

        for data in tqdm(pgIO.getDataIterator(query, chunks= 1000), total=501):
            data = [d[0] for d in data]
            c = Counter(data)
            result.update(c)


        return result

    except Exception as e:
        logger.error(f'Unable to generate result: {e}')

    return result