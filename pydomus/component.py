#!/usr/bin/env python
# -*- coding: utf-8 -*-

from multisock import channel as multiChannel
from multisock import logfactory
from pydomus.syncqueue import SyncQueue
from pydomus.reactions import ReactiveIntf
from pydomus.notification import Notification
import threading
import time
import sys


###################################################################################################
# THREADS
###################################################################################################

def thNetToQueue(component):
    '''
    Reads from the multicast channel all the incoming messages and enqueue them to a queue
    inside the managed component.
    '''
    component.logger.info('Instantiated [thNetToQueue]')
    while True:
        data = component.channel.recv_object()
        component.msgQueue.push(data)

def thQueueToComponent(component):
    '''
    Consumes messages from the queue and activates (if token matched) the callback of
    managed component.
    '''
    component.logger.info('Instantiated [thQueueToComponent]')
    while True:
        data = component.msgQueue.pop()
        try:
            component.handleMsg(data[0], data[1])
        except Exception as e:
            component.logger.error('Failed to handleMsg: %s' % str(e))

def thMainLoop(component):
    if component._loop is not None:
        while True:
            component._loop(component)


###################################################################################################
# COMPONENT
###################################################################################################

class Component(ReactiveIntf):
    def __init__(self, name, ch):
        '''
        Create a component with a label (name) and multicast connection parameters.
        :param name: a short name identifying the component (uniqueness not guaranteed)
        :param mcastIP: the multicast cannel IP to bind
        :param mcastPort: the multicast port
        :param logger: the custom logger to use
        '''

        # Parameters
        if name is None:
            raise ValueError('Invalid name parameter')
        if ch is None:
            raise ValueError('Invalid channel parameter')
        if not isinstance(ch, multiChannel.Channel):
            raise ValueError('Invalid channel type')
        self.msgQueue = SyncQueue()
        self.channel = ch
        self.name = name.strip()
        if ch.logger is not None:
            self.logger = ch.logger
        else:
            self.logger = logfactory.LogFactory(self.name)
        self._loop = None
        # Super instantiation
        ReactiveIntf.__init__(self)

    #####################################################
    # The active part
    #####################################################
    def delay(self, secs):
        time.sleep(secs)

    def setLoop(self, loop):
        self._loop = loop

    #####################################################
    # THREADS ON NET
    #####################################################
    def start(self):
        """
        The component starts.
        :return:
        """
        # Receiver threads
        self.__init_TH_()

        # Main process loop
        try:
            while True:
                self.th_receiver.join(600)
                self.th_consumer.join(600)
                self.th_loop.join(600)
                if not self.th_receiver.isAlive():
                    break
                if not self.th_consumer.isAlive():
                    break
        except KeyboardInterrupt:
            print("Ctrl-c pressed ...")
            print("Closing connections")
            sys.exit(1)

    def __init_TH_(self):
        self.logger.info('Creating threads')
        self.th_receiver = threading.Thread(target=thNetToQueue, args=(self,))
        self.th_receiver.daemon = True
        self.th_receiver.start()
        self.th_consumer = threading.Thread(target=thQueueToComponent, args=(self,))
        self.th_consumer.daemon = True
        self.th_consumer.start()
        self.th_loop = threading.Thread(target=thMainLoop, args=(self,))
        self.th_loop.daemon = True
        self.th_loop.start()

    #####################################################
    # THE INTERACTIVE PART
    #####################################################
    def handleMsg(self, msg, sender=None):
        """
        The ReactiveIntf implementation automatically will resolve the compatible
        reactions bound to this component and trigger them.
        """
        if msg is None or not isinstance(msg, Notification):
            raise ValueError('Invalid msg parameter')
        notification = msg
        if sender is not None:
            self.logger.info('Checking token [%s] from [%s]' % (notification.getToken(), str(sender)))
        else:
            self.logger.info('Checking token [%s]' % notification.getToken())
        self.handle(notification)

    def notify(self, msg):
        '''
        Send a message on the multicast channel so it can be (eventually) consumed by subscribed components that
        can react to the given token.
        :param token: a token expressed in the form of MessageToken instance
        :param msg: the message to send
        '''
        if msg is None or not isinstance(msg, Notification):
            raise ValueError('Invalid msg parameter')
        self.channel.send_object(msg)
