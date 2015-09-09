from dnsupdater.godaddydnsupdater import GodaddyDnsUpdater
from sys import argv as commandlineargs
from os import path as configfilepath

def main():
    if len(commandlineargs) == 2:
        configfile = commandlineargs[1]
        if configfilepath.isfile(configfile):
            dnsupdater = GodaddyDnsUpdater(configfile)
            dnsupdater.updatedns()
        else:
            print('Error: The config file is not valid!')
    else:
        print('Usage: dnsupdater <configfile>')
