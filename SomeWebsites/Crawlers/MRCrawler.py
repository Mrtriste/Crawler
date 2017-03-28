from Crawler import *
import re

class MRCrawler(Crawler):
	def parse(self,url):
		self.parse_list=[]
		soup = BeautifulSoup(self.getPage(url),'html.parser')
		links = soup.find_all(name='a',attrs={'rel':'bookmark'})
		if self.last_article:
			for link in links:
				if link.get('href') == self.last_article:
					break
				else:
					self.parse_list.append(link.get('href'))
		if links:
			self.last_article = links[0].get('href')
			

	def getDate_Titles(self,lst):
		res = []
		for link in lst:
			soup = BeautifulSoup(self.getPage(link),'html.parser')
			title = soup.find(name='h1',attrs={'class':'entry-title site-title'}).string
			date = soup.find(name='div',attrs={'class':'entry-meta'})
			for child in date.children:
				break
			date = child.string.replace('\n','').replace('\t','').replace(',','').split(' ')
			dates = self.get_dates(date)
			date = dates[3]+self.month_dict.get(dates[1].lower()[:3])+self.get_format_digit(str(re.findall(r'\d+',dates[2])[0]))
			res.append((date,title,link))
		return res