from Crawler import *

class MWTCrawler(Crawler):
	def __init__(self,home,last_article):
		Crawler.__init__(self,home,last_article)

	def parse(self,url):
		soup = BeautifulSoup(self.getPage(url),"html.parser")
		#get the current month's link
		link = soup.find_all("loc",limit = 2)[1].string
		soup = BeautifulSoup(self.getPage(link),"html.parser")
		#if isn't init,first link will be latest article
		if self.last_article:
			for i in soup.find_all('loc'):
				if self.last_article==i.string:
					break;
				else:
					self.new_article_list.append(i.string)
		self.last_article = soup.loc.string

	def getTitle(self,article_link):
		soup = BeautifulSoup(self.getPage(article_link,"html.parser"))
		pass

