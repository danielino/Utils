__author__ = 'Daniele Marcocci <daniele.marcocci@par-tec.it'
__version__ = 0.1

import os
import sys

from optparse import OptionParser

# Scoreboard Class
class ModStatusScoreboard:

    @staticmethod
    def parse(scoreboard):
        if len(scoreboard) < 1:
            return False

        res = {
            "_" : { "name" : "WaitingForConnection",         "value" : 0 },
            "S" : { "name" : "StartingUp",                   "value" : 0 },
            "R" : { "name" : "ReadingRequest",               "value" : 0 },
            "W" : { "name" : "SendingReply",                 "value" : 0 },
            "K" : { "name" : "KeepAlive",                    "value" : 0 },
            "D" : { "name" : "DNSLookup",                    "value" : 0 },
            "C" : { "name" : "ClosingConnection",            "value" : 0 },
            "L" : { "name" : "Logging",                      "value" : 0 },
            "G" : { "name" : "GracefullyFinishing",          "value" : 0 },
            "I" : { "name" : "IdleCleanupOfWorker",          "value" : 0 },
            "." : { "name" : "OpenSlotWithNoCurrentProcess", "value" : 0 },
        }

        for i in scoreboard:
            if i:
                res[i]['value'] += 1

        return res

# ModStatus
class ModStatus:

    # this class use requests (default) or urllib2.

    __data = {}

    def __init__(self, host = "127.0.0.1", port=80, ssl=False):

        self.host = host
        self.port = port
        self.ssl = ssl
        self.__parseData()


    def __parseData(self):
        if self.port == 443:
            self.ssl = True
            self.proto = "https://"

        if self.ssl:
            self.proto = "https://"
        else:
            self.proto = "http://"

        self.mod_status_url = "%s%s:%s/server-status?auto" % (self.proto, self.host, self.port)

        try:
            modUsed = "requests"
            import requests
            text = requests.get(self.mod_status_url).text

        except ImportError:
            try:
                modUsed="urllib2"
                import urllib2
                text = "".join(urllib2.urlopen(self.mod_status_url).readlines())
            except ImportError:
                print "this class need requests or urllib2 module to get information from mod_status"
                sys.exit()

        for i in text.split('\n'):
            if ':' in i:
                s = i.split(':')
                key = str(s[0].lstrip()).replace(' ','')
                value = str(s[1].lstrip())
                self.__data[key] = value

        return True

    def __get_data_value(self, key):
        if self.__data.has_key(key):
            return self.__data[key]
        return None


    def getData(self, json=False):
        tmp = {
            "mod_status_url"        : self.mod_status_url,
            "server" : {
                "built"             : self.__get_data_value('ServerBuilt'),
                "MPM"               : self.__get_data_value('ServerMPM'),
                "uptime"            : self.__get_data_value('ServerUptime'),
                "uptimeSeconds"     : self.__get_data_value('ServerUptimeSeconds'),
                "version"           : self.__get_data_value('ServerVersion')
            },
            "cpu" : {
                 'ChildrenSystem'   : self.__get_data_value('CPUChildrenSystem'),
                 'ChildrenUser'     : self.__get_data_value('CPUChildrenUser'),
                 'Load'             : self.__get_data_value('CPULoad'),
                 'LoadM' : {
                     "1m"           : self.__get_data_value('Load1'),
                     "5m"           : self.__get_data_value('Load5'),
                     "15m"          : self.__get_data_value('Load15')
                 },
                 'System'           : self.__get_data_value('CPUSystem'),
                 'User'             : self.__get_data_value('CPUUser'),
            },
            "worker" : {
                "busy"              : self.__get_data_value('BusyWorkers'),
                "idle"              : self.__get_data_value('IdleWorkers')
            },
            "request" : {
                "ReqPerSec"         : self.__get_data_value('ReqPerSec'),
                "BytesPerReq"       : self.__get_data_value('BytesPerReq'),
                "BytesPerSec"       : self.__get_data_value('BytesPerSec'),
                "TotalAccesses"     : self.__get_data_value('TotalAccesses'),
                "TotalkBytes"       : self.__get_data_value('TotalkBytes')
            },
            "scoreboard"            : ModStatusScoreboard.parse(self.__get_data_value('Scoreboard'))
        }
        if json:
            import json
            return json.dumps(tmp)
        return tmp


def main():
    parser = OptionParser(usage="usage: %prog [options] filename",
                          version="%User Manager 1.0")
    parser.add_option("-i", "--hostname",
                      dest="hostname",
                      default='127.0.0.1')
    parser.add_option("-p", "--port",
                      dest="port",
                      default=80,)
    parser.add_option("-j", "--json",
                      dest="json",
                      action="store_true",
                      help="return data in json")
    (options, args) = parser.parse_args()

    m = ModStatus(host=options.hostname, port=options.port)
    if options.json:
        print m.getData(json=True)
    else:
        res = m.getData()
        """
            res = {
                "scoreboard" : {
                    "W" : { "name" : "SendingReply", "value" : 0 }
                }
            }
        """
        for i in res['scoreboard'].keys():
            score = res['scoreboard']
            head = "%s %s:" % ( i, score[i]['name'])
            print "%-35s%-5s" % ( head, score[i]['value'])




if __name__ == "__main__":
    main()
