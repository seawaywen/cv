# -*- coding: utf-8 -*-


class ActivationError(Exception):

    def __init__(self, message, code=None, params=None):
        self.message = message
        self.code = code
        self.params = params

