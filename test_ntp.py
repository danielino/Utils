#!/usr/bin/env python
from socket import AF_INET, SOCK_DGRAM
import sys
import socket
import struct, time


host = sys.argv[1]
port = 123
buf = 1024
address = (host,port)
msg = '\x1b' + 47 * '\0'

# reference time (in seconds since 1900-01-01 00:00:00)
TIME1970 = 2208988800L # 1970-01-01 00:00:00

try:
    # connect to server
    client = socket.socket( AF_INET, SOCK_DGRAM)
    client.settimeout(10)
    client.sendto(msg, address)
    data, addr = client.recvfrom( buf )

    udp_d_struct = struct.unpack( "!12I", data) #network 12 unsigned int

    # select only reftime
    t = struct.unpack( "!12I", data )[10]
    t -= TIME1970
    print "Time Receive = %s" % time.ctime(t)
except socket.timeout:
    print "connection timeout"
