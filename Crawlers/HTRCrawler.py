from Crawler import *

class HTRCrawler(Crawler):
	def parse(self,url):
		self.parse_list = []
		self.date_list = []
		soup = BeautifulSoup(self.getPage(url),'html.parser')
		#get the current month's link
		locs = soup.find_all(name='loc',limit=3)
		if not locs:
			return
		link = locs[2].string
		soup = BeautifulSoup(self.getPage(link),'html.parser')
		#if isn't init,first link will be latest article
		if self.last_article:
			for i in soup.find_all('url'):
				if self.last_article==i.loc.string:
					break
				else:
					self.parse_list.append(i.loc.string)
					self.date_list.append(i.lastmod.string.split('T')[0])
		if soup.loc:
			self.last_article = soup.loc.string

	def getDate_Titles(self,lst):
		res=[]
		index = 0
		for url in lst:
			tup = self.__getDate_Title(url,index)
			if tup:
				res.append(tup)
			index = index + 1
		return res


	def __getDate_Title(self,parse_url,index):
		soup = BeautifulSoup(self.getPage(parse_url),'html.parser')
		h1 = soup.find(name = 'h1',attrs={'class':'entry-title'})
		if not h1:
			return ''
		title = h1.string
		date = self.date_list[index].split('-')
		dates = self.get_dates(date)
		date = dates[0]+self.get_format_digit(dates[1])+self.get_format_digit(dates[2])
		return (date,title,parse_url)