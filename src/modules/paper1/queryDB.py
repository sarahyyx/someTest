from logs import logDecorator as lD 
import jsonref, pprint
import numpy as np  
import matplotlib.pyplot as plt

from psycopg2.sql import SQL, Identifier, Literal
from lib.databaseIO import pgIO
from collections import Counter
from textwrap import wrap

from tqdm import tqdm
from multiprocessing import Pool

config = jsonref.load(open('../config/config.json'))
paper1_config = jsonref.load(open('../config/modules/paper1.json'))
logBase = config['logging']['logBase'] + '.modules.paper1.paper1'

@lD.log(logBase + '.getRace')
def getRace(logger):
    '''print a line
    
    This function simply prints a single line
    
    Parameters
    ----------
    logger : {logging.Logger}
        The logger used for logging error information
    '''

    try:
        
        query = '''
        SELECT 
        race,
        COUNT(race)
        FROM raw_data.background
        GROUP BY race
        '''

        data = pgIO.getAllData(query)
        # data = [d[0] for d in data]

    except Exception as e:
        logger.error('getRace failed because of {}'.format(e))

    return data

@lD.log(logBase + '.pushData')
def pushData(logger, dataTuple):
    '''print a line
    
    This function simply prints a single line
    
    Parameters
    ----------
    logger : {logging.Logger}
        The logger used for logging error information
    '''

    try:
        
        query = SQL('''
        INSERT INTO test (age, visit_type, sex, race, siteid, backgroundid)
        VALUES {};
        ''').format(
            Literal(dataTuple)
        )

        status = pgIO.commitData(query)
        print(status)

    except Exception as e:
        logger.error('doSomething failed because of {}'.format(e))

    return

@lD.log(logBase + '.getTable1data')
def getTable1data(logger):
    '''print a line
    
    This function simply prints a single line
    
    Parameters
    ----------
    logger : {logging.Logger}
        The logger used for logging error information
    '''
    p = Pool()

    try:
        
        query = SQL('''
        SELECT 
            t1.age,
            t1.visit_type, 
            t2.sex,
            t2.race
        FROM 
            raw_data.typepatient t1
        INNER JOIN 
            raw_data.background t2
        ON
            t1.backgroundid = t2.id
        AND
            t1.siteid = t2.siteid
        WHERE 
            CAST (t1.age AS INTEGER) < 100
        AND
            t1.visit_type in {}
        AND
            t2.sex in {}
        AND
            t2.race in {}
        ''').format(
            Literal(tuple(paper1_config["params"]["setting"]["all"])),
            Literal(tuple(paper1_config["params"]["sexes"]["all"])),
            Literal(tuple(paper1_config["params"]["races"]["all"]))
            )

        dataIter = pgIO.getDataIterator(query, chunks= 1000)


    except Exception as e:
        logger.error('createTable1data failed because of {}'.format(e))

    return
