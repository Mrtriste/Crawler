import urllib2
import time
from bs4 import BeautifulSoup

class Crawler(object):
	month_dict={
	'jan':'01','feb':'02','mar':'03','apr':'04','may':'05','jun':'06',
	'jul':'07','aug':'08','sep':'09','oct':'10','nov':'11','dec':'12'
	}
	def __init__(self,home,last_article):
		self.headers={
		'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
		}
		self.home = home
		self.last_article = last_article
		self.max_try_time = 1

	def get_dates(self,lst):
		dates = []
		for d in lst:
			if d:
				dates.append(d)
		return dates

	def get_format_digit(self,digit):
		return (digit if len(digit)>1 else '0'+digit)

	def get_write_content(self):
		return self.home+','+self.last_article+'\n'

	def getPage(self,url):
		page = '<html> </html>'
		for i in range(0,self.max_try_time):
			try:
				req = urllib2.Request(url=url,headers=self.headers)
				res=urllib2.urlopen(req)
				page = res.read()
				break
			except urllib2.HTTPError, e:
				print 'HTTPError:'+self.home
				page = '<html> </html>'
			except urllib2.URLError,e:
				if i == 0:
					print 'URLError:'+self.home
				print 'reconnect:'+str(i)
				if i == self.max_try_time-1:
					print 'reconeect fail,return default'
				page = '<html> </html>'
		return page
				



	