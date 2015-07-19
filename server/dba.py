# coding:utf-8
__author__ = 'edvard'

import redis

class DB(object):
	def __init__(self,host='127.0.0.1',port=6379,db=1):
		self.db = redis.Redis(host=host,port=port,db=db)
		try:
			self.db.ping()
		except:
			raise Exception('db not connected')

	def add_record(self,key,rec):
		self.db.rpush(key,rec)

	def get_latest_record(self,key):
		return self.db.lindex(key,-1)

	def get_n_records(self,key,n):
		return self.db.lrange(key,-n,-1)

	def get_till_record(self,key,tm_stamp):
		pass

	def get_all_records(self,key):
		return self.db.lrange(key,0,-1)
