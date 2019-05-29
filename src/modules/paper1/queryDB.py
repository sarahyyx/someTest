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
        logger.error('doSomething failed because of {}'.format(e))

    return data

