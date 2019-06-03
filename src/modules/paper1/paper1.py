from logs import logDecorator as lD 
import jsonref, pprint

import matplotlib.pyplot as plt
from tqdm import tqdm
import operator
import csv

from psycopg2.sql import SQL, Identifier, Literal

from lib.databaseIO import pgIO
from modules.paper1 import queryDB
from modules.paper1 import reportWriter

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

    countDict = {
        "AA": [],
        "NH/PI":[],
        "MR":[]
    }

    raceCounts = queryDB.countMainRace()
    countDict["AA"].append(raceCounts[0])
    countDict["NH/PI"].append(raceCounts[1])
    countDict["MR"].append(raceCounts[2])

    raceAgeCounts = queryDB.countRaceAge()
    countDict["AA"].append(raceAgeCounts[0])
    countDict["NH/PI"].append(raceAgeCounts[1])
    countDict["MR"].append(raceAgeCounts[2])

    raceSexCounts = queryDB.countRaceSex()
    countDict["AA"].append(raceSexCounts[0])
    countDict["NH/PI"].append(raceSexCounts[1])
    countDict["MR"].append(raceSexCounts[2])

    raceSettingCounts = queryDB.countRaceSetting()
    countDict["AA"].append(raceSettingCounts[0])
    countDict["NH/PI"].append(raceSettingCounts[1])
    countDict["MR"].append(raceSettingCounts[2])

    print(countDict)

    reportWriter.genIntro()
    reportWriter.genRace(countDict)
    reportWriter.genRaceAge(countDict)
    reportWriter.genRaceSex(countDict)
    reportWriter.genRaceSetting(countDict)

    # queryDB.pushData(('1', 'Inpatient', 'M', 'Asian', '11111', '11111'))

    print('Getting out of module paper1')
    print('-'*30)

    return

