import pandas as pd
import os
import Config as const_config

class CSVReader(object):
    ''' This class read CSV file and return pandas dataFrame'''

    def findAllCSVFromDirectory(self, path):
        ''' This method find all CSV files from a directory '''
        inputFileList = []
        try:
            directory = os.path.join(const_config.ROOT_DIRECTORY, path)
            for root,dirs,files in os.walk(directory):
                for file in files:
                    if file.endswith(".csv"):
                        inputFileList.append(file)
        except Exception as e:
            print "Exception occurred at CSVReader.findAllCSVFromDirectory"
            print str(e)
        finally:
            return inputFileList

    def getDataFrameFromCSV(self, path, fileName):
        ''' This method will read CSV file and return dataFrame'''
        try:
            print "Reading file : " + str(fileName)
            csvFile = os.path.join(const_config.ROOT_DIRECTORY, path, fileName)
            return pd.read_csv(csvFile, dtype=str)
        except Exception as e:
            print "Exception occurred at CSVReader.getDataFrameFromCSV"