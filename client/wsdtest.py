#coding:utf-8
# author: edvard

from WindPy import w
import xmlrpclib

# 如下地址不要改为localhost，否则会因为DNS解析导致RPC调用极其缓慢。
proxy=xmlrpclib.ServerProxy('http://127.0.0.1:10000')

def display_info(row):
	print row,',',

def display_time(tm):
	print tm,

def submit_record(stk,row):
	global proxy
	proxy.add_bar(stk,row)

def democb(indata):
	if indata.ErrorCode != 0:
		print 'ErrorCode %s' % indata.ErrorCode
		return

	#f = display_info
	f = submit_record
	row = []
	tm = indata.Times[0].strftime('%H:%M:%S')
	row.append(tm)
	#print indata.Times[0].strftime('%H:%M:%S'),
	for k in xrange(len(indata.Fields)):
		if indata.Fields[k] == u'RT_UPWARD_VOL':
			row.append('B')
			row.append(indata.Data[k][0])
		elif indata.Fields[k] == u'RT_DOWNWARD_VOL':
			row.append('S')
			row.append(indata.Data[k][0])
		else:
			row.append(indata.Data[k][0])
	f('000001',row)

def fetch():
	# rt_time,rt_low,rt_last,rt_last,rt_last_vol,rt_upward_vol,rt_downward_vol
	data = w.wsq('000001.SZ','rt_last,rt_last_vol,rt_upward_vol,rt_downward_vol',func=democb)

if __name__ == '__main__':
	w.start()

	fetch()

	while True:
		try:
		    pass
		except Exception as e:
			print e
			w.stop()

