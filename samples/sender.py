#!/usr/bin/env python

from context import *
from multisock import logfactory
import random

def printResult(parent, evt):
    assert (evt is not None and evt.hasPayload())
    result = evt.get('value')
    parent.logger.info ('Received result: %d' % result)

def loop(component):
    ##########################################
    # NOTIFICATION
    ##########################################
    msg = Notification('/arithm/calc/sum')
    msg.set('/operation', 'SUM')
    msg.set('/p1', random.randint(1,1000))
    msg.set('/p2', random.randint(1,1000))

    #
    component.logger.info('Requiring the SUM of %d %d' % (msg.get('p1'), msg.get('p2')))

    # Ask calculator to apply the operation
    component.notify(msg)
    # Next loop step in 5 seconds
    component.delay(5)

def main():
    # name, mcastIP, mcastPort
    logger = logfactory.LogFactory('c2', 'logs/sender')
    logger.info('Instantiating Sender Sample')
    c=Component('c1', '224.1.1.1', 1234, logger)
    # ACTIVE LOOP
    c.setLoop(loop)
    # REACTIONS
    c.add('/arithm/result', printResult)
    # START COMPONENT
    c.start()

if __name__ == '__main__':
    main()