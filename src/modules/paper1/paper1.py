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
                'list': ['M', 'Male'],
                'AAcount': None,
                'NHPIcount': None,
                'MRcount': None
            },
            'Female': {
                'list': ['F', 'Female'],
                'AAcount': None,
                'NHPIcount': None,
                'MRcount': None
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

  
        var = ('M', 'Male')
        query = SQL('''
            SELECT 
                distinct sex, race
            FROM
                raw_data.background
            WHERE 
                sex in {} and
                race in {}

            limit 10
            ''').format(
                Literal(var),
                Literal(('Chinese', 'Asian american', 'Korean', 'Asian', 'Vietnamese', 'Indian', 'asian'))
            )

        data = pgIO.getAllData(query)
        for d in data:
            print(d)
        # for race in raceLists:
        #     for sex in sexDict:  
        #         query = SQL('''
        #             SELECT 
        #                 COUNT(sex)
        #             FROM
        #                 raw_data.background
        #             WHERE 
        #                 sex in ({})
        #             AND
        #                 race in ({})
        #             ''').format(
        #                 Identifier(str(sexDict[sex]['list'])[1:-1]),
        #                 Identifier(str(raceLists['AA'])[1:-1])
        #                 )
        #         data = pgIO.getAllData(query)
        #         data = [d[0] for d in data]
        #         print(data)
        #         break

        # query = '''
        # SELECT
        # COUNT(*)
        # FROM raw_data.background
        # WHERE
        # sex in ('M', 'Male')
        # AND
        # race in ('Chinese', 'Asian american', 'Korean', 'Asian', 'Vietnamese', 'Indian', 'asian');
        # '''
        # data = pgIO.getAllData(query)
        # data = [d[0] for d in data]
        # print(data)

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

    raceCount = queryDB.getRace()

    with open('../data/raw_data/raceCount.csv','w+') as output:
        csv_out=csv.writer(output)
        csv_out.writerow(['race','count'])
        for row in raceCount:
            csv_out.writerow(row)

    raceDict = genRaceDict('../data/intermediate/paperRaceCount.csv')
    countMainRace(raceDict)

    countRaceSex(raceDict)

    print('Getting out of module paper1')
    print('-'*30)

    return

