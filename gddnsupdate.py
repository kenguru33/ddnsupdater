from ddnsupdater.godaddy import GodaddyDynamicDnsUpdater
import sys
import os.path

configfile = sys.argv[1]
if os.path.isfile(configfile):
    dnsupdater = GodaddyDynamicDnsUpdater(configfile)
    dnsupdater.updatedns()
else:
    print('No valid config file.')
