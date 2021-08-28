#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Notification():
    def __init__(self, token, payload={}):
        if token is None or not isinstance(token, str):
            raise ValueError('Invalid token parameter')
        self.token = token.strip()
        self.payload = payload

    def hasPayload(self):
        return self.payload is not None

    def getToken(self):
        return self.token


    ########################################################################
    # SET PARAMETER
    ########################################################################
    def __set(self, container, subpaths, value):
        if container is None or not isinstance(container, dict):
            return
        if subpaths is None or not isinstance(subpaths, list) or len(subpaths) == 0:
            return
        # The leaf
        if len(subpaths) == 1:
            container[subpaths[0]] = value
        currkey = subpaths.pop(0)
        if currkey in container:
            if not isinstance(container[currkey], dict):
                return
        else:
            container[currkey] = {}
        container = container[currkey]
        self.__set(container, subpaths, value)

    def set(self, path, value):
        if path is None or value is None:
            return
        if self.payload is None:
            self.payload = {}
        if not isinstance(self.payload, dict):
            return
        paths = list(filter(lambda x: x != '', path.split('/')))
        self.__set(self.payload, paths, value)

    ########################################################################
    # GET PARAMATER
    ########################################################################
    def __get(self, subpaths, container):
        if subpaths is None:
            return None
        if not isinstance(container, dict):
            return None
        if not isinstance(subpaths, list):
            return None
        if len(subpaths) == 1:
            try:
                return container[subpaths[0]]
            except:
                return None
        currkey = subpaths.pop(0)
        try:
            return self.__get(subpaths, container[currkey])
        except:
            return None

    def get(self, path):
        if not self.hasPayload():
            return None
        if path is None:
            return None
        try:
            paths = list(filter(lambda x: x != '', path.split('/')))
            return self.__get(paths, self.payload)
        except:
            return None
