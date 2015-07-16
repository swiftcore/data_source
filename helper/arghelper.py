# coding:utf-8
__author__ = 'edvard'
import os
import sys

class ArgChecker(object):
	def __init__(self,directory,args,usage):
		super(ArgChecker,self).__init__()
		self.directory = directory
		self.args = args
		self.usage = usage

	def check_arg_as_file(self):
		if len(self.args) != 2:
			print 'usage:%s' % self.usage
			sys.exit(1)

		if not os.path.exists(os.path.join(self.directory,self.args[1])):
			print 'argument file %s not found.' % os.path.join(self.directory,self.args[1])
			return False

		return True
