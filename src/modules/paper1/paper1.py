from logs import logDecorator as lD 
import jsonref, pprint

import matplotlib.pyplot as plt
from tqdm import tqdm
import operator
import csv

from psycopg2.sql import SQL, Identifier, Literal

from lib.databaseIO import pgIO
from modules.paper1 import queryDB

config = jsonref.load(open('../config/config.json'))
paper1_config = jsonref.load(open('../config/modules/paper1.json'))
logBase = config['logging']['logBase'] + '.modules.paper1.paper1'


@lD.log(logBase + '.genRaceDict')
def genRaceDict(logger, inputCSV):
    '''print a line
    
    This function simply prints a single line
    
    Parameters
    ----------
    logger : {logging.Logger}
        The logger used for logging error information
    '''

    try:
        raceDict = {
                'AA': [],
                'NH/PI': [],
                'MR': []
        }

        with open(inputCSV) as f:
            readCSV = csv.reader(f, delimiter=',')
            for row in readCSV:
                for race in paper1_config["inputs"]["races"]:
                    if row[2] == race:
                        raceDict[race].append((row[0], row[1]))

    except Exception as e:
        logger.error('genRaceDict failed because of {}'.format(e))

    return raceDict

@lD.log(logBase + '.countMainRace')
def countMainRace(logger, inputDict):
    '''print a line
    
    This function simply prints a single line
    
    Parameters
    ----------
    logger : {logging.Logger}
        The logger used for logging error information
    '''

    try:
        AAcount = 0
        NHPIcount = 0
        MRcount = 0

        for t in inputDict['AA']:
            AAcount = AAcount + int(t[1])
        for t in inputDict['NH/PI']:
            NHPIcount = NHPIcount + int(t[1])
        for t in inputDict['MR']:
            MRcount = MRcount + int(t[1])

        total = AAcount + NHPIcount + MRcount

        print(f"There are {AAcount} Asian American patients")
        print(f"There are {NHPIcount} Native Hawaiian/Pacific Islander patients")
        print(f"There are {MRcount} Multi-Racial patients")

        print(f"Total: {total} patients")

        return

    except Exception as e:
        logger.error('genRaceDict failed because of {}'.format(e))

    return raceDict

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
    print('Main function of module paper1')
    print('='*30)

    raceCount = queryDB.getRace()

    with open('../data/raw_data/raceCount.csv','w+') as output:
        csv_out=csv.writer(output)
        csv_out.writerow(['race','count'])
        for row in raceCount:
            csv_out.writerow(row)

    raceDict = genRaceDict('../data/intermediate/paperRaceCount.csv')
    countMainRace(raceDict)

    print('Getting out of module paper1')
    print('-'*30)

    return

