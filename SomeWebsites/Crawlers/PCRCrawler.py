from Crawler import *

class PCRCrawler(Crawler):
	def parse(self,url):
		self.parse_list=[]
		soup = BeautifulSoup(self.getPage(url),'html.parser')
		links = soup.find_all(name='a',attrs={'class':'contentpagetitle'})
		if self.last_article:
			for link in links:
				url = self.home+'/'+link.get('href').split('/')[2]
				if url == self.last_article:
					break
				else:
					self.parse_list.append(url)
		if links:
			self.last_article = self.home+'/'+links[0].get('href').split('/')[2]
			

	def getDate_Titles(self,lst):
		res = []
		for link in lst:
			soup = BeautifulSoup(self.getPage(link),'html.parser')
			if soup.h1 and soup.time:
				title = soup.h1.string.replace('\n','')
				date = soup.time.string.split(',')[1].split(' ')
				dates = self.get_dates(date)
				date = dates[2]+self.month_dict.get(dates[1].lower()[:3])+self.get_format_digit(dates[0])
				res.append((date,title,link))
		return res