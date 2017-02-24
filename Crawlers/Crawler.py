import urllib2
from bs4 import BeautifulSoup

class A:
	def __init__(self):
		self.ss = 'A'
	def getS(self):
		return self.ss
	
class B(A):

	def __init__(self):
		A.__init__(self)
		#self.ss = 'B'
		pass
	def a1(self,a):
		self.ss = a

class Crawler(object):
	def __init__(self,home,last_article):
		self.headers={
		'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
		}
		self.home = home
		self.last_article = last_article
		self.new_article_list=[]

	def getTitles(self):
		pass

	def get_write_content(self):
		return self.home+','+self.last_article+'\n'

	def getPage(self,url):
		try:
			req = urllib2.Request(url=url,headers=self.headers)
			res=urllib2.urlopen(req)
			return res.read()
		except urllib2.HTTPError, e:
			print 'error:'+self.home
	