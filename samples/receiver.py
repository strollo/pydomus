#!/usr/bin/env python

from context import *
from multisock import logfactory

# Sample function that applies an operation (SUM/SUB/DIV/MUL) to
# two given numbers.
def calc(operation, a, b):
    if operation == 'SUM':
        return a+b
    if operation == 'SUB':
        return a-b
    if operation == 'DIV':
        return a/b
    if operation == 'MUL':
        return a*b
    raise ValueError('Invalid operation')

# Entry point to handle the entering messages
def doStuff(parent, evt):
    assert(evt is not None and evt.hasPayload())
    # Gets parameters from the payload
    operation=evt.get('/operation')
    a = evt.get('/p1')
    b = evt.get('/p2')
    print 'Executing task %s (%d, %d)' % (operation, a, b)
    result=calc(operation, a, b)
    response=Notification('/arithm/result')
    response.set('value', result)
    print 'Sending back result %d via %s' % (result, response.getToken())

    parent.notify(response)

def main():
    # name, mcastIP, mcastPort
    logger = logfactory.LogFactory('c1', 'logs/receiver')
    logger.info('Instantiating Receiver Sample')
    c=Component('c1', '224.1.1.1', 1234, logger)
    ##########################################
    # REACTION
    ##########################################
    c.add('/arithm/calc/*', doStuff)
    c.start()

if __name__ == '__main__':
    main()