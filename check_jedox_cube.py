#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lib.jedox_api import jedox_api
from lib.leanbi_lib import leanbi_script
import datetime
import logging
import sys

class jedox_check_data(leanbi_script):
    def __init__(self):
        self.return_code=0
        leanbi_script.__init__(self,self.__class__.__name__)
        
        self.connection=jedox_api()
        self.set_return_code(self.get_Date())
        self.set_return_code(self.set_Date())
        self.set_return_code(self.get_Date())
        
        sys.exit(self.return_code)
        
    def set_return_code(self,value):
        if value==False and self.return_code==0 :
            self.return_code=1

    
    def set_Date(self):
        try:
            date=datetime.datetime.now()
            self.connection.cell_replace("ETL_Starter","health_check","Last_Executed",date)
            self.logger.info("Value successfully set")
            return True
        except Exception ,e :
            print e
            return False  
        
    def get_Date(self):
        try:
            data=self.connection.cell_area("ETL_Starter","health_check","Last_Executed")
            self.logger.info("Could read value from Cube succesfully : %s" % data)
            return True
        except Exception,e:
            self.logger.error("could not get Date from CUBE")
            self.logger.exception(Exception)
            return False
            
        

if __name__ == '__main__':
    jedox_check_data()
