import pandas as pd
import os
import Config as const_config
import datetime

class ExcelWriter(object):
    ''' This class is reponsible for writing data into excel'''
    def dumpDataToExcel(self, writer, df, sheet_name):
        retVal = 0
        try:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            retVal = 1
        except Exception as e:
            print "Exception occurred at ExcelWriter.dumpDataToExcel"
            print str(e)
        finally:
            return retVal