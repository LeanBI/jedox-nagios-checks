#!/usr/bin/env python
# -*- coding: utf-8 -*-


import argparse
import logging
from sys import exit
from string import Template
from datetime import datetime,timedelta
from fnmatch import fnmatch
import os

class checker:
    def __init__(self,args):
        self.results=[]
        self.return_code=None
        self.file_name=self.get_file_name(args["file_template"],args["date_format"],args["backup_time"])
        self.check(args["backup_dir"],self.file_name,int(args["backup_file_size"]))
        self.output()

    def get_file_name(self,file_template,date_format,backup_time):

        now=datetime.now()
        backup_time_str=backup_time.split(":")
        backup_time=now.replace(hour=int(backup_time_str[0]), minute=int(backup_time_str[1]))

        if now > backup_time :
            #backup already shoud have be done
            file_date=backup_time.strftime(date_format)
        else :
            #need to take the backup_time from yeasterday
            file_date=backup_time - timedelta(days=1)
            file_date=file_date.strftime(date_format)

        return (file_template % file_date)

    def check(self,backup_dir,file_name,file_size):
        for d in os.listdir(backup_dir):
            if fnmatch(d,file_name):
                size_in_mb=int(os.stat(os.path.join(backup_dir,d)).st_size / 1000000)
                if size_in_mb >  file_size:
                    self.return_code=0
                else :
                    self.results.append("%s(%s)" % (d,size_in_mb))

    def output(self):
        if self.return_code==0:
            print ("All Ok")
            exit(0)
        elif len(self.results)==0 :
            print ("No file found")
            exit(2)
        else:
            print ("Backup has not reached minimum size:%s" % self.results)








if __name__=="__main__" :
    parser = argparse.ArgumentParser(description='check if backup has been done')
    parser.add_argument('--file-template', help="how does the backup file looks like ? :  backup-jedox_leanbi_ch-%s_*.tgz",required=True)
    parser.add_argument('--date-format', help="how does the backup file looks like ? : %Y-%m-%d",required=True)
    parser.add_argument('--backup-time', help="Time when the backup of the day should be finished (%H:%M) : 04:10",required=True)
    parser.add_argument('--backup-dir', help="directory where backups are stored",required=True)
    parser.add_argument('--backup-file-size', help="minimum size the backup should have in MB : 30",required=True)
    args=vars(parser.parse_args())

    checker(args)
