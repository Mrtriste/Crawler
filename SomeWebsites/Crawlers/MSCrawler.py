from Crawler import *

class MSCrawler(Crawler):
	def parse(self,url):
		self.parse_list = url
		
	def getDate_Titles(self,lst):
		soup = BeautifulSoup(self.getPage(lst),'html.parser')
		res = []
		if self.last_article:
			for i in soup.find_all(name='div',attrs={'class':'blockDescNews'}):
				a = i.h1.a
				if self.last_article == self.home+a['href']:
					break
				else:
					date = i.time.string.split(' ')[1].split('/')
					dates = self.get_dates(date)
					date = dates[2]+self.get_format_digit(dates[0])+self.get_format_digit(dates[1])
					res.append((date,a.string,self.home+a['href']))
		blockDesc = soup.find(name='div',attrs={'class':'blockDescNews'})
		if blockDesc:
			self.last_article = self.home+blockDesc.h1.a.get('href')
		return res