#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The Reactive interface of a component.
"""

from pydomus.pattern import Pattern
from pydomus.notification import Notification

class ReactiveIntf:
    def __init__(self):
        self.reactions = {}

    def add(self, pattern, reaction):
        assert (pattern is not None)
        assert (reaction is not None)
        _pattern = None
        # 1 - PATTERN
        if isinstance(pattern, str):
            _pattern = Pattern(pattern)
        elif isinstance(pattern, Pattern):
            _pattern = pattern
        else:
            raise ValueError('Invalid pattern parameter')
        # 2 - REACTION
        if not callable(reaction):
            raise ValueError('Invalid reaction parameter')
        self.reactions[_pattern] = reaction

    def getReactions(self, token):
        """
        Returns the list of all reactions having a compatible pattern
        """
        if token is None or not isinstance(token, str):
            return []

        return list(filter(lambda entry: entry[0].match(token), list(self.reactions.items())))

    def handle(self, notification):
        if notification is None or not isinstance(notification, Notification):
            return
        token = notification.getToken()
        reactions = self.getReactions(token)
        for reaction in reactions:
            self.logger.info('Reacting to token %s' % token)
            try:
                reaction[1](self, notification)
            except Exception as e:
                self.logger.error('Failed to react: %s' % str(e))

if __name__ == '__main__':
    ri = ReactiveIntf()
    ri.add('/test/*', lambda x: x)
    ri.add('/test/params/*', lambda x: x)
    p = ri.getReactions('/test')

    n = Notification('/test')
    ri.handle(n)
