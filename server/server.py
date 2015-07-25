# coding:utf-8
__author__ = 'edvard'

# 以Redis为后端的(待加入)，twisted异步服务器

import sys
import os

sys.path.append(os.path.join(os.getcwd(),'..'))

from twisted.web import xmlrpc, server
import logging
import ConfigParser
from helper import arghelper
import dba 

class FetchServer(xmlrpc.XMLRPC):
	def __init__(self):
		xmlrpc.XMLRPC.__init__(self,allowNone=True)

		conf = ConfigParser.ConfigParser()
		conf.readfp(open('db_conf.cfg'))
		section = 'connection'
		db_host = conf.get(section,'host')
		db_port = conf.getint(section,'port')
		db_id = conf.getint(section,'db')
		
		self.db = dba.DB(host=db_host,port=db_port,db=db_id)

	def xmlrpc_add_bar(self,stk,row):
		if len(row) == 5:
			row_str = '%s,%.2f,%.2f,%s,%.2f' % tuple(row)
		elif len(row) == 7:
			row_str = '%s,%.2f,%.2f,%s,%.2f,%s,%.2f' % tuple(row)
		elif len(row) == 2:
			row_str = '%s,%.2f' % tuple(row)
		else:
			row_str = '%s' % row
			logging.info('unknown format row:%s' % row)

		self.db.add_record(stk,row_str)
		logging.info('add %s' % row_str)

	def xmlrpc_get_latest_bar(self,stk):
		return self.db.get_latest_record(stk)

	def xmlrpc_get_n_bars(self,stk,n):
		return self.db.get_n_records(stk,n)

	def xmlrpc_get_till_bars(self,stk,tm_str):
		raise xmlrpc.Fault(120,'not implemented')

	def xmlrpc_get_all_bars(self,stk):
		return self.db.get_all_records(stk)

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
