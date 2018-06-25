
import ConfigParser
from Component import Component
from multisock import channel
from multisock import DataCrypto
from multisock import logfactory
import logging
import os

class ConfigLoader:
    def __init__(self, fname):
        assert (fname is not None and len(fname.strip()) > 0)
        self.inifile=fname.strip()
        self._ini_reader = ConfigParser.ConfigParser()
        self._ini_reader.read(self.inifile)

    def buildComponent(self):
        assert (self._ini_reader.has_option('Component', 'name'))
        ch=self.buildChannel()
        compName=self._ini_reader.get('Component', 'name').strip()
        retval=Component(compName, ch)

    def buildChannel(self):
        retval=None
        assert (self._ini_reader.has_option('Channel', 'mcast_ip'))
        assert (self._ini_reader.has_option('Channel', 'mcast_port'))
        mcast_ip=self._ini_reader.get('Channel', 'mcast_ip')
        mcast_port = int(self._ini_reader.get('Channel', 'mcast_port'))
        logger=self.buildLogger()
        if self._ini_reader.has_option('Channel', 'key1') and self._ini_reader.has_option('Channel', 'key2'):
            retval = channel.Channel(mcast_ip, mcast_port, logger=logger, crypto=DataCrypto(self._ini_reader.get('Channel', 'key1'), self._ini_reader.get('Channel', 'key2')))
        else:
            retval = channel.Channel(mcast_ip, mcast_port, logger=logger)
        assert (retval is not None)
        return retval

    def buildLogger(self):
        assert (self._ini_reader.has_option('Component', 'name'))
        compName = self._ini_reader.get('Component', 'name').strip()
        assert (compName is not None)
        logger=None

        if not self._ini_reader.has_section('Logger'):
            logger = logging.getLogger(compName)
            logger.setLevel(logging.DEBUG)
            ch = logging.StreamHandler()
            ch.setLevel(logging.NOTSET)
            formatter = logging.Formatter('%(asctime)-15s|%(name)-5s|%(levelname).3s|%(message)s')
            ch.setFormatter(formatter)
            logger.addHandler(ch)
            assert(logger is not None)
            return logger


        log_path='logs'
        log_fname=None
        if (self._ini_reader.has_option('Logger', 'path')):
            log_path=self._ini_reader.get('Logger', 'path').strip()
        if (self._ini_reader.has_option('Logger', 'filename')):
            log_fname = self._ini_reader.get('Logger', 'filename').strip()
        if log_fname is not None:
            log_path=os.path.join(log_path, log_fname)

        logger = logfactory.LogFactory(compName, log_path)
        if (self._ini_reader.has_option('Logger', 'level')):
            log_level = self._ini_reader.get('Logger', 'level').strip()
            logger.setLevel(log_level)

        assert (logger is not None)
        return logger
