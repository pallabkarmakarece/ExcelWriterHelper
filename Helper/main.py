import threading
from Reader import CSVReader
from Writer import ExcelWriter
import Config as const_config
import datetime
import os
import pandas as pd

class ReadWriteEngine(object):
    ''' Entry point for this project '''
    def __init__(self):
        self.inputPath = const_config.INPUT_DIRECTORY
        self.outputPath = const_config.OUTPUT_DIRECTORY
        self.readerObj = CSVReader()
        self.writerObj = ExcelWriter()
        self.listOfCSVFile = self.readerObj.findAllCSVFromDirectory(self.inputPath)

    def worker(self, fileName, writer):
        try:
            print "Executing thread : " + threading.currentThread().getName()
            df = self.readerObj.getDataFrameFromCSV(self.inputPath, fileName)
            #Slicing sheet name as microsoft excel has 30 character limit for sheetname
            sheet_name = fileName.split(".")[0] if len(fileName) <= 30 else fileName[:30]
            if self.writerObj.dumpDataToExcel(writer, df, sheet_name):
                print "Success : " + threading.currentThread().getName() + ' finished its work'
            else:
                print "Failed : " + threading.currentThread().getName() + ' failed to write data'
        except Exception as e:
            print "Exception occurred at ReadWriteEngine.worker during execution of thread " + threading.currentThread().getName()
            print str(e)

    def Executor(self):
        '''This method is spawing thread. No of thread is equal to number of CSV files'''
        try:
            startTime = datetime.datetime.now()
            outputFileName = const_config.OUTPUT_FILE_NAME + datetime.datetime.now().strftime("%Y_%b_%d_%H%M%S") + '.xlsx'
            excelFile = os.path.join(const_config.ROOT_DIRECTORY, self.outputPath, outputFileName)
            writer = pd.ExcelWriter(excelFile, engine='xlsxwriter')
            threadPool = [threading.Thread(target=self.worker, args=(each, writer)) for each in self.listOfCSVFile]

            for each_thread in threadPool:
                each_thread.start()
            for each_thread in threadPool:
                each_thread.join()
            writer.save()
            endTime = datetime.datetime.now()
            delta = endTime - startTime
            print "Total Time taken : " + str(delta.total_seconds()) + ' Seconds.'
        except Exception as e:
            print "Exception occurred at ReadWriteEngine.Executor"
            print str(e)

def main():
    ReadWriteEngine().Executor()

if __name__ == "__main__":
    main()