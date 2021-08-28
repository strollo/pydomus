#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Xpath simplified expressions to match tokens through which events are notified to subscribers.
"""

class Pattern:
    def __init__(self, path, caseSensitive=False):
        if path is None or not isinstance(path, str): raise ValueError('Invalid path parameter: null not allowed')
        path=path.strip()
        if len(path) == 0: raise ValueError('Invalid path parameter')
        self.caseSensitive=caseSensitive
        if self.caseSensitive:
            self.path=path.lower()
        else:
            self.path=path
    def __repr__(self):
        return self.path

    def match(self, token):
        """
        Checks the matching between the current pattern path (the type of messages consumed)
        and a given message token (the type of transmitted messages).
        """
        if not isinstance(token, str): return False
        if token is None: return False
        to_match = token.strip()
        if self.caseSensitive:
            to_match = to_match.lower()
        tokens = list(filter(lambda x: x != '', to_match.split('/')))
        patterns = list(filter(lambda x: x != '', self.path.split('/')))

        for i in range(len(tokens)):
            _token = tokens[i]
            _pattern = patterns[0]
            if _token != _pattern:
                if _pattern == '*':
                    continue
            else:
                patterns.pop(0)
            if len(patterns) == 0:
                return (i == len(tokens)-1) and _token == _pattern

        if len(patterns) == 2:
            if patterns[0] == '*' and patterns[1] == _token:
                return True
        return len(patterns) == 0 or (len(patterns) == 1 and patterns[0] == '*')