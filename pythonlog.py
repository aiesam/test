import logging
import getopt
import sys
import time
import random
import os
from pythonjsonlogger import jsonlogger
from  datetime import datetime


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            # this doesn't use record.created, so it is slightly off
            now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            log_record['timestamp'] = now
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname


def main(argv):
    usageInfo = '\nUSAGE:\n\nlogGenerator.py --logFile <targetFile>\n\t[--minSleepMs <int>] [--maxSleepMs <int>] \n\t[--sourceDataFile <fileWithTextData>] [--iterations <long>]\n\t[--minLines <int>] [--maxLines <int>] \n\t[--logPattern <pattern>] [--datePattern <pattern>]'

    iterations = -1  # infinate
    minSleep = 0.1
    maxSleep = 1
    minLines = 1
    maxLines = 1
    logFile = 'logGenerator.log'
    sourceDataFile = 'defaultDataFile.txt'
    sourceData = ''
    logPattern = '%(asctime)s,%(msecs)d %(process)d %(filename)s %(lineno)d %(name)s %(levelname)s %(message)s'
    datePattern = "%Y-%m-%d %H:%M:%S"

    if len(argv) == 0:
        # print(usageInfo)
        sys.exit(2)

    try:
        opts, args = getopt.getopt(argv,"h",["help","logFile=","minSleepMs=","maxSleepMs=","iterations=","sourceDataFile=","minLines=","maxLines="])
    except:
        # print(usageInfo)
        sys.exit(2)


    for opt, arg in opts:

        if opt in ('-h' , "--help"):
            print(usageInfo)
            sys.exit()

        elif opt in ("--logFile"):
            logFile = arg

        elif opt in ("--minSleepMs"):
            minSleep = (0.001 * float(arg))

        elif opt in ("--maxSleepMs"):
            maxSleep = (0.001 * float(arg))

        elif opt in ("--maxLines"):
            maxLines = int(arg)

        elif opt in ("--minLines"):
            minLines = int(arg)

        elif opt in ("--sourceDataFile"):
            sourceDataFile = arg

        elif opt in ("--iterations"):
            iterations = int(arg)

        elif opt in ("--logPattern"):
            logPattern = arg

        elif opt in ("--datePattern"):
            datePattern = arg

    #check if sourcefile exists
    if os.path.exists(sourceDataFile):
        pass
    else:
        print("Please check if file " + sourceDataFile + " exists")
        sys.exit()

    # bring in source data
    with open (sourceDataFile, "r") as fh:
        sourceData=fh.read()
    sourceData = sourceData.splitlines(True)
    totalLines = len(sourceData)-1

    if (maxLines > totalLines):
        maxLines = totalLines

  

    # setup logging
    logging.Formatter.converter = time.gmtime
    # logger = logging.getLogger("log-generator")
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)


    # fileHandler = logging.FileHandler(logFile)
    # fileHandler.setLevel(logging.DEBUG)
    # formatter = logging.Formatter(logPattern,datePattern)
    # fileHandler.setFormatter(formatter)
    # logger.addHandler(fileHandler)

    logHandler = logging.StreamHandler()
    # formatter = jsonlogger.JsonFormatter()
    formatter = CustomJsonFormatter('%(timestamp)s %(level)s %(name)s %(message)s')
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)

    mustIterate = True
    while (mustIterate):

        # sleep
        # time.sleep(random.uniform(minSleep, maxSleep))
        time.sleep(2)
        # get random data
        lineToStart = random.randint(0,totalLines)
        linesToGet = random.randint(minLines, maxLines)

        lastLineToGet = (lineToStart + linesToGet)

        if (lastLineToGet > totalLines):
            lastLineToGet = totalLines

        toLog = ''.join(sourceData[lineToStart:lastLineToGet])

        if (toLog.startswith('\n')):
            toLog = toLog[1:]

        if (toLog == ''):
            continue

        logger.debug(toLog[:-1])
        # print(toLog[:-1])

        if (iterations > 0):
            iterations = iterations - 1
            if (iterations == 0):
                mustIterate = False

    sys.exit(0)


if __name__ == "__main__":
    main(sys.argv[1:])
