#!/usr/bin/env python
# -*- coding: utf-8 -*-


import socket
import argparse
import logging
from sys import exit

class checker:
    def __init__(self,port_list):
        self.return_code=0
        self.missing=[]

        for p in port_list:
            self.check(p)

        self.results()

    def check(self,port_config):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1',int(port_config["port"])))
        if result == 0:
           logging.debug("Port %s:%s is open" %(port_config["description"],port_config["port"]))

        else:
            logging.debug("Port %s:%s is NOT open" %(port_config["description"],port_config["port"]))
            self.return_code+=1
            self.missing.append("%s:%s" % (port_config["port"],port_config["description"]))

    def results(self):
        if self.return_code==0 :
            print("All Ports are open")
            exit(0)
        else :
            print ("Ports are missing : %s" % self.missing)
            exit(2)





if __name__=="__main__" :
    parser = argparse.ArgumentParser(description='check if jedox ports are open')
    parser.add_argument('--ports', action="append", help="indicate which port to monitor : 7777,olap",required=True)
    args=vars(parser.parse_args())

    ports=[]
    for a in args["ports"]:

        sp=a.split(",")
        if len(sp)==1 :#there is no ':' so only program name
            ports.append({"port":a})
        else :
            ports.append({"port":sp[0],"description":sp[1]})

    checker(ports)
