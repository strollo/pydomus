
from channel import UDPChannel
from logfactory import LogFactory


if __name__ == '__main__':
    logger = LogFactory('writer', 'logs/sample')
    udpchan = UDPChannel('224.1.1.1', 1234, 1024, logger)

    for i in range(10):
        print 'Sending to %s' % udpchan
        udpchan.send("Test %d" % i)
