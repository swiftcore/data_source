# coding:utf-8
__author__ = 'edvard'

# 以Redis为后端的(待加入)，twisted异步服务器

import sys
import os

sys.path.append(os.path.join(os.getcwd(),'..'))

from twisted.web import xmlrpc, server
import logging
from helper import arghelper

class FetchServer(xmlrpc.XMLRPC):
	def __init__(self):
		xmlrpc.XMLRPC.__init__(self,allowNone=True)
		self.db = {}

	def xmlrpc_add_bar(self,stk,row):
		if not stk in self.db:
			self.db[stk] = [tuple(row)]
			return

		self.db[stk].append(tuple(row))
		logging.info('add %s' % row)

	def xmlrpc_get_latest_bar(self,stk):
		if not stk in self.db:
			return []

		return self.db[stk][-1:]

	def xmlrpc_get_n_bars(self,stk,n):
		if not stk in self.db:
			return []

		return self.db[stk][-n:] if n <= len(self.db[stk]) else self.db[stk]

	def xmlrpc_get_till_bars(self,stk,tm_str):
		raise xmlrpc.Fault(120,'not implemented')

	def xmlrpc_get_all_bars(self,stk):
		if not stk in self.db:
			return []

		return self.db[stk]

def main():
	from twisted.internet import reactor
	r = FetchServer()
	reactor.listenTCP(10000,server.Site(r))
	print 'listen at port 10000'
	try:
		reactor.run()
	except:
		reactor.stop()

def test():
	print 'in test'

if __name__ == '__main__':
	arg_checker = arghelper.ArgChecker(os.path.join(os.getcwd(),'log'),sys.argv,'python server.py <log_file>')
	if not arg_checker.check_arg_as_file():
		# create dirs and files
		if not os.path.exists('log'):
			os.mkdir('log')
		logging.basicConfig(filename=os.path.join(os.getcwd(),'log/log.txt'), 
			level=logging.DEBUG,
			filemode='a',
			format='%(asctime)s - %(levelname)s:%(message)s')
		print 'create the log/log.txt'
	else:
		logging.basicConfig(filename=os.path.join(os.getcwd(),'log/%s' % sys.argv[1]), 
			level=logging.DEBUG,
			filemode='a',
			format='%(asctime)s - %(levelname)s:%(message)s')
	main()
