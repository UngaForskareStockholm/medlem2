#! /usr/bin/env python2.7

import datetime

def typecast_json(o):
	if isinstance(o, datetime.datetime) or isinstance(o, datetime.date):
		return o.isoformat()
	else:
		return o

def split_dict(src, keys):
	result = dict()
	for k in set(src.keys()) & set(keys):
		result[k] = src[k]
	return result
