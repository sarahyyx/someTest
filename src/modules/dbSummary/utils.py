from logs import logDecorator as lD 
import jsonref, pprint
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt

from lib.databaseIO import pgIO
from collections import Counter

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