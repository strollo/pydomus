###############################################################################
# A simple builder of loggers.
###############################################################################
# @author: daniele strollo (daniele.strollo@gmail.com)
###############################################################################

import logging
import datetime
import os


######################################################
# SINGLETON LOGGER
######################################################
class LogFactory:
    '''
    A general purpose logger builder.
    Usage:
        logger = LogHandler('compname', 'logs/samplelog')    # logs to a file samplelog_DATE.log
        logger.info('Hello world')                       # direct access to logger lib methods
    '''

    def __init__(self, compname, fname):
        self.__init_logger__(compname, fname)

    def __check_log_dir(self, logfile):
        '''
        checks if the log dir exists otherwise tries to create it.
        '''
        _dir=os.path.dirname(logfile)
        if _dir is None or len(_dir.strip()) == 0:
            return
        # directory does not exists
        if not os.path.exists(_dir):
            os.makedirs(_dir)

    def __init_logger__(self, compname, fname):
        self.__check_log_dir(fname)

        # create logger with 'spam_application'
        self.logger = logging.getLogger(compname)
        self.logger.setLevel(logging.DEBUG)
        # create file handler which logs even debug messages

        _date = datetime.date.strftime(datetime.date.today(), '%Y%m%d')
        _fname = '%s_%s.log' % (fname, _date)
        fh = logging.FileHandler(_fname)
        fh.setLevel(logging.DEBUG)
        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(logging.WARN)
        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)-15s|%(name)-5s|%(levelname)-8s| %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # add the handlers to the logger
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def __getattr__(self, item):
        '''
        Allows direct access to encapsulated logger instance.
        '''
        return getattr(self.logger, item)



if __name__ == '__main__':
    logger = LogFactory('test', 'logs/samplelog')
    logger.info('hello')
    logger.warn('test warn')