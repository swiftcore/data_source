#coding:utf-8
# author: edvard

from WindPy import w
import xmlrpclib
import ConfigParser
import os
import sys

# 如下地址不要改为localhost，否则会因为DNS解析导致RPC调用极其缓慢。

def context(config,dataname):
	host = config.get('host','127.0.0.1')
	port = config.get('port','10000')
	proxy = xmlrpclib.ServerProxy('http://%s:%s' % (host,port))

	def submit_record(stk,row):
		proxy.add_bar(stk,row)

	def tick(indata):
		if indata.ErrorCode != 0:
			print 'ErrorCode %s' % indata.ErrorCode
			return

		for ix in xrange(len(indata.Codes)):
			row = []
			tm = indata.Times[0].strftime('%H:%M:%S')
			row.append(tm)
			for k in xrange(len(indata.Fields)):
				if indata.Fields[k] == u'RT_UPWARD_VOL':
					row.append('B')
					row.append(indata.Data[k][ix])
				elif indata.Fields[k] == u'RT_DOWNWARD_VOL':
					row.append('S')
					row.append(indata.Data[k][ix])
				else:
					row.append(indata.Data[k][ix])

			stk = indata.Codes[ix]
			submit_record(stk,row)

	calls = {}
	calls['tick'] = tick

	return calls[dataname] if dataname in calls else None

def get_fetch_config(conf_filename):
	section = 'fetch'
	conf = ConfigParser.ConfigParser()
	conf.readfp(open(conf_filename))
	codes_str = conf.get(section,'codes')
	fields_str = conf.get(section,'fields')
	codes = codes_str.split(',')
	fields = fields_str.split(',')

	section = 'server'
	host = conf.get(section,'host')
	port = conf.get(section,'port')

	return {'codes':codes, 'fields':fields, 'host':host, 'port':port}

def fetch(conf_file):
	config = get_fetch_config(conf_file)
	# rt_time,rt_low,rt_last,rt_last,rt_last_vol,rt_upward_vol,rt_downward_vol
	#data = w.wsq('000001.SZ','rt_last,rt_last_vol,rt_upward_vol,rt_downward_vol',func=democb)
	data = w.wsq(config['codes'],config['fields'],func=context(config,'tick'))
	return data

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print 'usage: python fetch.py <conf_file>'
		sys.exit(1)

	if not os.path.exists(sys.argv[1]):
		print 'config file %s cannot be found' % sys.argv[1]
		sys.exit(2)

	w.start()

	data = fetch(sys.argv[1])

	while True:
		try:
		    pass
		except Exception as e:
			print e
			w.cancelRequest(data.RequestID)
			w.stop()

