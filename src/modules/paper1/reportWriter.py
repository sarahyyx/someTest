from logs import logDecorator as lD 
import jsonref, pprint

from psycopg2.sql import SQL, Identifier, Literal
from lib.databaseIO import pgIO
from collections import Counter

from tqdm import tqdm
from multiprocessing import Pool
from time import sleep

config = jsonref.load(open('../config/config.json'))
dbSummary_config = jsonref.load(open('../config/modules/paper1.json'))
logBase = config['logging']['logBase'] + '.modules.paper1.reportWriter'

@lD.log(logBase + '.generateIntro')
def generateIntro(logger, r):
    
    report = f'''

# Report on Table Summariser Module

## Abstract: 
This report will give a summary of the target table: raw_data.background of the MindLinc database.

## Summary of Table:

This table has information on {r['totalNumUser']} users, with {r['totalNumColumns']} attribute columns. 

## Description of Table:

        '''
    with open('../report/summariserReport.md', 'w+') as f:
        f.write( report )

    return