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

    ''' 
    Since the paper specifies 3 major races: AA, NH/PI and MR, there are many minor 
    races belonging to each in the database. This counts all the minor races under each 
    race and prints the value.

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
        logger.error('countMainRace failed because of {}'.format(e))

    return raceDict

@lD.log(logBase + '.countRaceSex')
def countRaceSex(logger, inputDict):

    '''print a line
    
    This function simply prints a single line
    
    Parameters
    ----------
    logger : {logging.Logger}
        The logger used for logging error information
    '''

    try:

        sexDict = {
            'Male': {
                'tuple': ('M', 'Male'),
                'AA': None,
                'NH/PI': None,
                'MR': None
            },
            'Female': {
                'tuple': ('F', 'Female'),
                'AA': None,
                'NH/PI': None,
                'MR': None
            }
        }

        raceLists = {
            'AA': [],
            'NH/PI': [],
            'MR': []
        }

        for t in inputDict['AA']:
            raceLists['AA'].append(t[0])
        for t in inputDict['NH/PI']:
            raceLists['NH/PI'].append(t[0])
        for t in inputDict['MR']:
            raceLists['MR'].append(t[0])

        for race in raceLists:
            query = SQL('''
            SELECT 
                COUNT(*)
            FROM
                raw_data.background
            WHERE 
                sex in {} and
                race in {}

            limit 10
            ''').format(
                Literal(sexDict['Male']['tuple']),
                Literal(tuple(raceLists[race]))
            )

            data = pgIO.getAllData(query)
            data = [d[0] for d in data]
            sexDict['Male'][race] = data

        for race in raceLists:
            query = SQL('''
            SELECT 
                COUNT(*)
            FROM
                raw_data.background
            WHERE 
                sex in {} and
                race in {}

            limit 10
            ''').format(
                Literal(sexDict['Female']['tuple']),
                Literal(tuple(raceLists[race]))
            )

            data = pgIO.getAllData(query)
            data = [d[0] for d in data]
            sexDict['Female'][race] = data

        print(sexDict)

        print(raceLists)

        return

    except Exception as e:
        logger.error('countRaceSex failed because of {}'.format(e))

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
    print('Main function of module paper1')
    print('='*30)

    # #Generating csv file with the count of all the races, for the purpose of manually marking each to classify them under the paper's races
    # raceCount = queryDB.getRace()

    # with open('../data/raw_data/raceCount.csv','w+') as output:
    #     csv_out=csv.writer(output)
    #     csv_out.writerow(['race','count'])
    #     for row in raceCount:
    #         csv_out.writerow(row)

    raceDict = genRaceDict('../data/intermediate/paperRaceCount.csv')

    # countMainRace(raceDict)

    # countRaceSex(raceDict)

    queryDB.pushData(('1', 'Inpatient', 'M', 'Asian', '11111', '11111'))

    print('Getting out of module paper1')
    print('-'*30)

    return

