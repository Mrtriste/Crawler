from Crawler import *

class MWTCrawler(Crawler):

	def parse(self,url):
		self.parse_list=[]
		soup = BeautifulSoup(self.getPage(url),'html.parser')
		#get the current month's link
		locs = soup.find_all('loc',limit = 2)
		if not locs:
			return
		link = locs[1].string
		soup = BeautifulSoup(self.getPage(link),'html.parser')
		#if isn't init,first link will be latest article
		if self.last_article:
			for i in soup.find_all('loc'):
				if self.last_article==i.string:
					break
				else:
					self.parse_list.append(i.string)
		if soup.loc:
			self.last_article = soup.loc.string

	def getDate_Titles(self,lst):
		res=[]
		for url in lst:
			tup = self.__getDate_Title(url)
			if tup:
				res.append(tup)
		return res


	def __getDate_Title(self,parse_url):
		soup = BeautifulSoup(self.getPage(parse_url),'html.parser')
		times = soup.find_all(name='time',attrs={'class':'entry-time','itemprop':'datePublished'})
		if times:
			date = times[0].string.replace(',','').split(' ')
			dates = self.get_dates(date)
			date = dates[2]+self.month_dict.get(dates[0].lower()[:3])+self.get_format_digit(dates[1])
			return (date,soup.title.string,parse_url)
		else:
			return ''


