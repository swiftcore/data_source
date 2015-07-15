# coding:utf-8
# author: edvard

# 以Redis为后端的，twisted异步服务器

from twisted.web import xmlrpc, server

class DB(object):
	def __init__(self):
		pass

class TkServer(xmlrpc.XMLRPC):
	def __init__(self):
		xmlrpc.XMLRPC.__init__(self,allowNone=True)
		self.db = DB()

	def closeDB(self):
		self.db.close()

	def xmlrpc_add_bar(self,stk,bar):
		pass

	def xmlrpc_get_latest_bar(self,stk):
		pass

	def xmlrpc_get_n_bars(self,stk,n):
		pass

	def xmlrpc_get_till_bars(self,stk,tm_str):
		pass

	def xmlrpc_get_all_bars(self,stk):
		pass

if __name__ == '__main__':
	from twisted.internet import reactor
	r = TkServer()
	reactor.listenTCP(10000,server.Site(r))
	try:
		reactor.run()
	except Exception as e:
		print e
		r.closeDB()
		reactor.stop()

