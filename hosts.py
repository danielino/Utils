import os
import re

HOSTS_FILE="/etc/hosts"

def getAll():
    with open(HOSTS_FILE) as fp:
        rl = fp.readlines()
    tmp = []
    for i in rl:
        i = re.sub('#\w.+', '', i)
        it = i.split()
        tmp.append({
            "ip" : it[0],
            "hostname" : it[1],
            "alias" : it[1:]
        })


def checkEntry(needle):
    r = getAll()
    tmp = []
    for i in r:
        if needle in i:
            tmp.append(i)

    return tmp


def addEntry(ip, hostname, alias = []):
    if not os.access(HOSTS_FILE, os.W_OK):
        raise Exception("file is not writeable by current user")

    if checkEntry(hostname):
        raise Exception("hostname %s already exists" % hostname)

    if checkEntry(ip):
        raise Exception("ip %s already exists" % ip)

    # format record
    t = "%s\t%s" % ( ip, hostname )
    if alias:
        for i in alias:
            t += "\t%s" % i
    # get file
    with open(HOSTS_FILE, 'r') as fp:
        rl = fp.readlines()

    if not rl[-1].endswith('\n'):
        t = "\n%s" % t

    with open(HOSTS_FILE, 'a+') as fp:
        fp.write(t)

