# coding:utf-8

# author: edvard

# 测试客户端，可以连接任意后端的server

import xmlrpclib
import random
from datetime import datetime 
import logging
import os 
import time

class Tester(object):
	def __init__(self,round):
		self.proxy = xmlrpclib.ServerProxy('http://localhost:10000')
		self.stk = '000001'
		self.round = round

	def run(self):
		for i in xrange(self.round):
			self.run_once()

	def run_once(self):
		sig = random.choice([1,1,1,1,2,3,4])
		if sig == 1:
			self.add_random_bar(self.stk)
		elif sig == 2:
			self.display_latest(self.stk)
		elif sig == 3:
			n = random.randint(1,6)
			self.display_n(self.stk,n)
		else:
			self.display(self.stk)

	def add_random_bar(self,stk):
		vol = random.randint(100,3000)
		vol = vol - vol%100
		tm = datetime.now()
		bar = (tm.strftime('%H:%M:%S'),random.random()*10,vol)
		self.proxy.add_bar(stk,bar)
		logging.info('add bar (%s,%.3f,%d)' % tuple(bar))
		time.sleep(1)

	def display(self,stk):
		logging.info('*** all bars ***')
		bars = self.proxy.get_all_bars(stk)
		if len(bars) == 0:
			return

		for bar in bars:
			logging.info('(%s,%.3f,%d)' % tuple(bar))

	def display_latest(self,stk):
		logging.info('*** latest bar ***')
		bars = self.proxy.get_latest_bar(stk)
		if len(bars) == 0:
			return

		logging.info('(%s,%.3f,%d)' % tuple(bars[0]))

	def display_n(self,stk,n):
		logging.info('*** %d bars ***' % n)
		bars = self.proxy.get_n_bars(stk,n)
		if len(bars) == 0:
			return 

		for bar in bars:
			logging.info('(%s,%.3f,%d)' % tuple(bar))

if __name__ == '__main__':
	logging.basicConfig(filename=os.path.join(os.getcwd(),'log.txt'),
		level=logging.DEBUG,
		filemode='a',
		format='%(asctime)s - %(levelname)s: %(message)s')
	t = Tester(20)
	t.run()
