import urllib2
import random
import time
from bs4 import BeautifulSoup
from bs4 import element
from config import *
import Queue
import httplib
import ssl
import socket

httplib.HTTPConnection._http_vsn = 10  
httplib.HTTPConnection._http_vsn_str = 'HTTP/1.0' 

class HTTPSConnectionV3(httplib.HTTPSConnection):
	def __init__(self, *args, **kwargs):
		httplib.HTTPSConnection.__init__(self, *args, **kwargs)
         
	def connect(self):
		sock = socket.create_connection((self.host, self.port), self.timeout)
		if self._tunnel_host:
			self.sock = sock
			self._tunnel()
		try:
			self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file, ssl_version=ssl.PROTOCOL_TLSv1)
		except ssl.SSLError, e:
			self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file, ssl_version=ssl.PROTOCOL_TLSv1)
			print 'do nothing'
			#print("Trying SSLv3.")
			#self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file, ssl_version=ssl.PROTOCOL_SSLv23)
             
class HTTPSHandlerV3(urllib2.HTTPSHandler):
	def https_open(self, req):
		return self.do_open(HTTPSConnectionV3, req)

class Crawler(object):
	def __init__(self):
		ctx = ssl.create_default_context()
		ctx.check_hostname = False
		ctx.verify_mode = ssl.CERT_NONE
		proxy_handler = urllib2.ProxyHandler({
	        "http"  : proxyMeta,
	        "https" : proxyMeta,
		})
		self.opener = urllib2.build_opener(HTTPSHandlerV3(),proxy_handler)
		self.headers={'Referer':'https://www.yelp.com'}
		self.ua_index = random.randint(0,len(USER_AGENTS)-1)

	def getUserAgent(self):
		self.ua_index = (self.ua_index+1)%len(USER_AGENTS)
		return USER_AGENTS[self.ua_index]

		self.headers['user-agent'] = self.getUserAgent()
	def getHeaders(self):
		return self.headers


	def getPage(self,url,except_lock):
		cnt = 8
		for i in range(0,cnt):
			try:
				global request_num
				request_num = request_num+1
				print '**********************************send a request:'+str(request_num)
				req = urllib2.Request(url=url,headers=self.getHeaders())
				res = self.opener.open(req)
				#res=urllib2.urlopen(req)
				page = res.read()
				if not page:
					print 'none88888888888888'
					print page
					continue
				return page
			# except urllib2.HTTPError, e:
			# 	print 'HTTPError:'+url
			# except httplib.IncompleteRead, e:
			# 	time.sleep(1)
			# 	print e
			except Exception,e:
				print e
				time.sleep(0.5)
				if i ==cnt-1:
					print e,'connect fail'
					print 'getpage error'+url
					# except_lock.acquire()
					# except_file = open('./except_url.txt','a')
					# except_file.write(url+'\n')
					# except_file.close()
					# except_lock.release()



