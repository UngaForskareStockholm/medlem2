#! /usr/bin/env python2.7

import json

class APIError(object):
	def __init__(self, error):
		self.response=dict()
		self.response['error'] = error

	def __iter__(self):
		yield self.__str__()

	def __str__(self):
		return json.dumps(self.response) + "\n"
