#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# required : apt-get install python-psutil

import psutil
import argparse
import sys

class checker():
    def __init__(self,services):
        self.services_to_check=services
        self.check_services(self.services_to_check)
        self.results()

    def check_services(self,services):
        process_list=psutil.process_iter()
        for i in process_list:
            pinfo=i.as_dict(attrs=["name","cmdline"])
            process_name=pinfo["name"]
            process_cmdline=pinfo["cmdline"]
            for tc in services: #loop over services to check
                if process_name in tc["prog"]: #process is in list
                    if "cmdline" in tc:
                        if tc["cmdline"] in process_cmdline:
                            tc["check"]=True
                    else : #no cmdline, prog is enough
                        tc["check"]=True

    def results(self):
        return_code=0
        missing=[]
        for r in self.services_to_check:
            if  "check" not in r :
                missing.append(r["name"])
                return_code+=1



        if return_code==0 :
            print("All OK")
        else :
            print ("Services missing:%s" % missing)
            sys.exit(2)



if __name__=="__main__" :
    parser = argparse.ArgumentParser(description='check if jedox services are running')
    parser.add_argument('--services', action="append", help="indicate which service to check example : java,/my.jar odr myprog",required=True)
    args=vars(parser.parse_args())

    services=[]
    for a in args["services"]:

        sp=a.split(",")
        if len(sp)==2 :#there is no ':' so only program name
            services.append({"name":sp[0], "prog":sp[1]})
        else :
            services.append({"name":sp[0],"prog":sp[1], "cmdline":sp[2]})

    checker(services)

