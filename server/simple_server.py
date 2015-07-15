# coding:utf-8
# author: edvard

# 用dict作为数据库的服务器

import xmlrpclib

from SimpleXMLRPCServer import SimpleXMLRPCServer

db = {}

def add_bar(stk,row):
	if stk in db:
		db[stk].append(tuple(row))
	else:
		db[stk] = [row]

def get_latest_bar(stk):
	if stk in db:
		return db[stk][-1:]
	else:
		return []

def get_n_bars(stk,n):
	if stk in db:
		return db[stk][-n:] if n <= len(db[stk]) else db[stk]
	else:
		return []

def get_till_bars(stk,tm_str):
	if not stk in db:
		return [] 

	cnt = 0
	while cnt < len(db):
		break

def get_all_bars(stk):
	if not stk in db:
		return []

	return db[stk]

server = SimpleXMLRPCServer(('0.0.0.0',10000),allow_none=True)
print 'Listening on port 10000'

server.register_function(add_bar,'add_bar')
server.register_function(get_latest_bar,'get_latest_bar')
server.register_function(get_n_bars,'get_n_bars')
server.register_function(get_all_bars,'get_all_bars')

server.serve_forever()



