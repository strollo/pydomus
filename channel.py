#!/usr/bin/env python

"""
Channel.py
Implements a very small and easy to use channel for connecting UDP multicast channels with
simple operations for sending and receiving data.
"""
__name__        = "channel.py"
__author__      = "Daniele Strollo (daniele.strollo@gmail.com)"
__copyright__   = "Copyright 2018, The PyMultiComm Project"
__license__     = "GPL"
__version__     = "1.0.1"
__maintainer__  = "Daniele Strollo"
__status__      = "Production"

import socket
import struct
from logfactory import LogFactory

class UDPChannel:

    def __init__(self, mcast_ip, mcast_port, bufsize=4096, logger=None):
        self.mcast_ip = mcast_ip
        self.mcast_port = mcast_port
        self.bufsize = bufsize
        self.writer = None
        self.reader = None
        if logger is None:
            self.logger = LogFactory('pymulticomm', 'logs/pymulticomm')
            self.logger.info('Creating UDP Channel on %s %d' % (self.mcast_ip, self.mcast_port))
        else:
            self.logger = logger
        self.__init_protocol__()

    def __init_protocol__(self):
        # UDP socket writer
        self.writer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.writer.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
        self.writer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        _mreq = struct.pack("4sI", socket.inet_aton(self.mcast_ip), socket.INADDR_ANY)
        self.writer.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, _mreq)
        self.writer.bind(('', self.mcast_port))
        # UDP socket reader
        self.reader = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.reader.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        _mreq = struct.pack("4sI", socket.inet_aton(self.mcast_ip), socket.INADDR_ANY)
        self.reader.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, _mreq)
        # setblocking(0) is equiv to settimeout(0.0) which means we poll the socket.
        # But this will raise an error if recv() or send() can't immediately find or send data.
        self.reader.setblocking(0)
        self.reader.bind(('', self.mcast_port))
        self.logger.info('UDPChannel on %s %d connected' % (self.mcast_ip, self.mcast_port))

    def __repr__(self):
        return 'MulticastCh<%s:%d>' % (self.mcast_ip, self.mcast_port)

    def set_read_blocking(self, blocking=True):
        if blocking:
            self.reader.setblocking(1)
        else:
            self.reader.setblocking(0)

    def close(self):
        try:
            if self.reader is not None:
                self.reader.close()
        except:
            pass
        try:
            if self.writer is not None:
                self.writer.close()
        except:
            pass

    def send(self, data):
        self.logger.debug('(%s:%d) >>> %s' % (self.mcast_ip, self.mcast_port, data))
        self.writer.sendto(data, (self.mcast_ip, self.mcast_port))

    def recv(self, blocking=True):
        self.set_read_blocking(blocking)

        # buf = bytearray(self.bufsize)
        # nbytes,addr = self.reader.recvfrom_into(buf)
        # data = buf[:nbytes]
        data, addr = self.reader.recvfrom(self.bufsize)
        if (data is None or len(data) == 0):
            return None
        self.logger.debug('(%s:%d)/%s <<< %s' % (self.mcast_ip, self.mcast_port, addr, data))
        return data, addr


if __name__ == '__main__':
    udpchan = UDPChannel('232.232.117.27', 15997)
    udpchan.send("Test")
    buff = udpchan.recv()
    print 'received %s' % buff