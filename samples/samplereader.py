
from channel import UDPChannel
from logfactory import LogFactory

if __name__ == '__main__':
    logger = LogFactory('reader', 'logs/sample')
    udpchan = UDPChannel('224.1.1.1', 1234, 1024, logger)
    print 'Reading from %s' % udpchan

    while True:
        (data, addr) = udpchan.recv(False)
        print 'received %s' % data