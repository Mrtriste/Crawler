from Crawler import *
class ShopCrawler(Crawler):
	def __init__(self,url,filename,except_lock):
		self.url = url.strip(' \r\n')
		self.filename = filename
		self.shop_url = []
		self.page_index = 0
		self.shop_num = 0
		self.except_lock = except_lock
		super(ShopCrawler,self).__init__()

	def begin(self):
		#print 'crawl:---'+self.url+'---'
		self.first_page()
		if self.shop_num>10:
			num = self.shop_num/10+1 if self.shop_num%10!=0 else self.shop_num/10
			for i in range(1,num):
				self.remain_page(i)

	def first_page(self):
		cnt =5
		first_cnt = 0
		for iii in range(0,cnt):
			try:
				page = self.getPage(self.url,self.except_lock)
				soup = BeautifulSoup(page,'html.parser')
				side = soup.find(name = 'span',attrs={'class':'pagination-results-window'})
				if not side:
					first_cnt = first_cnt+1
					if first_cnt<2:
						continue
					else:
						return
				num_str = side.string
				num = (int)(num_str.split('of ')[-1].strip(' \r\n'))
				if num==0:
					return
				if num>1000:
					self.shop_num = 1000
				else:
					self.shop_num = num
				self.add_shop_urls(soup)
				return
			except Exception,e:
				print '#############'
				print e
				if iii == cnt-1:
					print 'except url:'+self.url
					self.except_lock.acquire()
					except_file = open('./except_url.txt','a')
					except_file.write(self.url+'\n')
					except_file.close()
					self.except_lock.release()

		
	def remain_page(self,index):
		cnt = 5
		for iii in range(0,cnt):
			try:
				start = 10*index
				url = self.url+search_url_num.format(start)
				page = self.getPage(url,self.except_lock)
				soup = BeautifulSoup(page,'html.parser')
				self.add_shop_urls(soup)
				return
			except Exception,e:
				print '#############'
				print e
				if iii ==cnt-1:
					print 'except url:'+self.url
					self.except_lock.acquire()
					except_file = open('./except_url.txt','a')
					except_file.write(self.url+'\n')
					except_file.close()
					self.except_lock.release()

	def remain_start(self,url):
		cnt=5
		for iii in range(0,cnt):
			try:
				page = self.getPage(url,self.except_lock)
				soup = BeautifulSoup(page,'html.parser')
				self.add_shop_urls(soup)
				return
			except Exception,e:
				print '#############'
				print e
				if iii==cnt-1:
					print 'except url:'+self.url
					self.except_lock.acquire()
					except_file = open('./except_url.txt','a')
					except_file.write(self.url+'\n')
					except_file.close()
					self.except_lock.release()

	def add_shop_urls(self,soup):
		results = soup.find_all(name='h3',attrs={'class':'search-result-title'})
		for result in results:
			href = result.find('a')['href']
			if len(href)<4:
				continue
			if not (href[0]=='/' and href[1]=='b' and href[2]=='i' and href[3]=='z' and href[4]=='/'):
				#print 'not href:'+href
				continue
			self.shop_url.append(href)


			#print href
		#print '---------------------------------'

	def write_to_file(self):
		file = open(self.filename,'a')
		for i in self.shop_url:
			file.write(i+'\r\n')
		file.close()

	def write2(self,n):
		filename = './test/'+str(n)+'.txt'
		file = open(filename,'a')
		for i in self.shop_url:
			file.write(i+'\r\n')
		file.close()

	def get_shopurl_list(self):
		return self.shop_url