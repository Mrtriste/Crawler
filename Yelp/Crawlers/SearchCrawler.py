from Crawler import *

class SearchCrawler(Crawler):
	def init(self,city,except_lock):
		self.city = city
		self.all_city = ''
		self.big_cata_queue = Queue.Queue()
		self.total_queue = Queue.Queue()
		self.except_lock = except_lock
		print search_url.format(city)

	def begin(self):
		url = search_url.format(self.city)
		#url = self.city
		self.base_url = url
		print '----------------------------------------url:'+url
		for cnt in range(0,10):
			page = self.getPage(url,self.except_lock)
			soup = BeautifulSoup(page,'html.parser')
			num_str_tag = soup.find(name = 'span',attrs={'class':'pagination-results-window'})
			if not num_str_tag:
				continue
			else:
				break
		if not num_str_tag:
			self.except_lock.acquire()
			file = open('city_except.txt','a')
			file.write(url+'\n')
			file.close()
			self.except_lock.release()
		num_str = num_str_tag.string
		num = (int)(num_str.split('of ')[-1].strip(' \n'))
		if num<=1000:
			print '#'+self.city,num,':less than 1000'
			self.all_city = self.getOutData('')#all the city
			self.total_queue.put(self.all_city)
			print 'add to total:'+self.all_city
		else:
			print '#'+self.city,num,':more than 1000'
			self.distribute_catarory(soup,num)

	def distribute_catarory(self,s,fa_num):
		exc = ''
		try:
			ss1 = s.find(name='div',attrs={'class':'all-category-browse-links'})
			if not ss1:
				ss1 = s.find(name='div',attrs={'class':'top-category-browse-links'})
			if not ss1:
				self.except_lock.acquire()
				file = open('city_except.txt','a')
				file.write(self.base_url+'\n')
				file.close()
				self.except_lock.release()

			catarory_list = ss1.find_all('li')
			for i in catarory_list:#every big cata
				filt = i.a['href']#.string.strip(' \n')
				url = home_url+filt
				exc = url
				#print 'uuu:'+url
				if fa_num<2000:
					self.total_queue.put(url)
				else:
					page = self.getPage(url)
					soup = BeautifulSoup(page,'html.parser')
					num_str = soup.find(name = 'span',attrs={'class':'pagination-results-window'}).string
					num = (int)(num_str.split('of ')[-1].strip(' \n'))
					if num<=1000:
						u = self.getOutData(filt)
						#print 'add to total:'+'less->'+'1 depth:'+u
						self.total_queue.put(u)
					else:
						catarory_list1 = []
						ss = soup.find(name='div',attrs={'class':'all-category-browse-links'})
						if not ss:
							ss = soup.find(name='div',attrs={'class':'top-category-browse-links'})
						if not ss:
							print '************************'+url
							f_name = 'log'+self.city.replace(' ','').replace(',','-')+'.txt'
							f = open(f_name,'w')
							f.write(page)
							f.close()
							continue
						catarory_list1=ss.find_all('li')
						for i1 in catarory_list1:
							filt1 = i1.a['href']#.string.strip(' \n')
							u = self.getOutData(filt1)
							#print 'add to total:'+'less->'+'2 depth:'+u
							self.total_queue.put(u)
		except Exception,e:
			print 'catch exception:',e
			print exc


	def getOutData(self,cflt):
		if cflt:
			return home_url+cflt
		return self.base_url

	def writeToFile(self,file):
		while not self.total_queue.empty():
			file.write(self.total_queue.get()+'\n')
