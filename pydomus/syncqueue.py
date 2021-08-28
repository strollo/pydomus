#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Nothing more than a queue where readers/writers concurrently produce/consume messages and receivers passively
wait at least a message is present in it before continuing their computation.
"""

import threading

class SyncQueue:
    def __init__(self):
        self.buff=[]
        self.syncSem=threading.Semaphore(0)
    def push(self, elem):
        if elem is None: return
        self.buff.append(elem)
        self.syncSem.release()
    def size(self):
        return len(self.buff)
    def isEmpty(self):
        return self.size() <= 0
    def pop(self):
        self.syncSem.acquire()
        if self.isEmpty(): return None
        return self.buff.pop(0)