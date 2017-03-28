from Crawler import *

class MWFCrawler(Crawler):
	def parse(self,url):
		self.parse_list = url
		
	def getDate_Titles(self,lst):
		soup = BeautifulSoup(self.getPage(lst),'html.parser')
		res = []
		if self.last_article:
			for i in soup.find_all('article'):
				a = i.header.h2.a
				if self.last_article == a['href']:
					break
				else:
					children = i.footer.div.div.children #find_all(name='span',attrs={'class':'meta-sep date updated'})
					for child in children:
						pass
					date = child.string.replace('\n','').replace(',','').split(' ')
					dates = self.get_dates(date)
					date = dates[2]+self.month_dict.get(dates[0].lower()[:3])+self.get_format_digit(dates[1])
					res.append((date,a.string,a['href']))
		if soup.article:
			self.last_article = soup.article.header.h2.a['href']
		return res