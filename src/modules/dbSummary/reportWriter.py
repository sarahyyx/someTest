from logs import logDecorator as lD 
import jsonref, pprint

from psycopg2.sql import SQL, Identifier, Literal
from lib.databaseIO import pgIO
from collections import Counter

from tqdm import tqdm
from multiprocessing import Pool
from time import sleep

config = jsonref.load(open('../config/config.json'))
dbSummary_config = jsonref.load(open('../config/modules/dbSummary.json'))
logBase = config['logging']['logBase'] + '.modules.dbSummary.reportWriter'

@lD.log(logBase + '.generateIntro')
def generateIntro(logger, r):
    
    report = f'''

# Report on Table Summariser Module

## Abstract: 
This report will give a summary of the target table: raw_data.background of the MindLinc database.

## Summary of Table:

This table has information on {r['totalNumUser']} users, with {r['totalNumColumns']} attribute columns. 

These columns are {r['columnNames']}.

## Description of Table:
        '''

    with open('../report/summariserReport.md', 'w+') as f:
        f.write( report )

    return

@lD.log(logBase + '.generateBody')
def generateBody(logger, r):

    for columnName in r:
        report = f'''
    The top 10 most commonly occurring values of the column {columnName} is: \n{r[columnName]}.
        '''

        with open('../report/summariserReport.md', 'a+') as f:
            f.write( report )

    return

#Sankha's Example
# @lD.log(logBase + '.generateReport')
# def generateReport(logger, r):
    
#     report = f'''

# # Table Summary

# # Abstract: 
# This report will give a summary of the target table: raw_data.background of the MindLinc database.

# # Summary Results

# This table has information on {r['totalNumUser']} users, 
# with {r['totalNumColumns']} attribute columns. These columns are {r['columnNames']}.


# | variable | median | mean | std |
# |----------|--------|------|-----|
# | $x$      | {r['totalNumUser']} | 25 | 1 |
# | $y$      | {r['totalNumUser']} | 25 | 1 |

#         '''

#     with open('../report/report2.md', 'w') as f:
#         f.write( report )

#     return