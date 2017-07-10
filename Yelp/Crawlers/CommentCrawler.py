from Crawler import *
import json
import traceback

class CommentCrawler(Crawler):
	def __init__(self,url,except_lock,info_lock):
		self.comments_num = 0
		self.comment_url = url.strip(' \r\n')
		self.except_lock = except_lock
		self.info_lock = info_lock
		self.comments=[]
		self.company_data = ''
		self.post_num =''
		super(CommentCrawler,self).__init__()

	def begin(self):
		if not self.comment_url:
			return
		self.first()
		if self.comments_num>20:
			num = self.comments_num/20+1 if self.comments_num%20!=0 else self.comments_num/20
			for index in range(1,num-1):
				self.remain_20(index)
			self.remain(num-1)

				
	def first(self):
		cnt = 5
		header_cnt = 0
		price_cnt = 0
		for iii in range(0,cnt):
			try:
				page = self.getPage(home_url+self.comment_url,self.except_lock)
				soup = BeautifulSoup(page,'html.parser')
				shop_header = soup.find(name = 'div',attrs={'class':'biz-page-header-left claim-status'})
				if not shop_header:
					shop_header = soup.find(name = 'div',attrs={'class':'biz-page-header-left'})
				if not shop_header:
					header_cnt = header_cnt+1
					if header_cnt<3:
						continue
					else:
						print 'no header'
						self.info_lock.acquire()
						except_file = open('./info/header_error.txt','a')
						except_file.write(self.comment_url+'\n')
						except_file.close()
						self.info_lock.release()
						return
				###########
				name_tag = shop_header.find(name='h1',attrs={'class':'biz-page-title embossed-text-white shortenough'})
				if not name_tag:
					name_tag = shop_header.find(name='h1',attrs={'class':'biz-page-title embossed-text-white'})
				if not name_tag:
					print 'no name'
					self.info_lock.acquire()
					except_file = open('./info/name_error.txt','a')
					except_file.write(self.comment_url+'\n')
					except_file.close()
					self.info_lock.release()
					return
				name = name_tag.string.strip(' \r\n')
				###########
				review_num_tag = shop_header.find(name='span',attrs={'class':'review-count rating-qualifier'})
				if not review_num_tag:
					print 'no review tag'
					self.info_lock.acquire()
					except_file = open('./info/no_review.txt','a')
					except_file.write(self.comment_url+'\n')
					except_file.close()
					self.info_lock.release()
					return
				###########
				cate = ''
				cate_tag = shop_header.find(name='span',attrs='category-str-list')
				if cate_tag:
					cate_list = cate_tag.find_all('a')
					if cate_list:
						cate = cate_list[0].string
						for i in cate_list[1:]:
							cate = cate+','+i.string
				###########
				latitude = 0
				longitude =0
				location_tag = soup.find(name='div',attrs='lightbox-map hidden')
				if not location_tag:
					print '***************wrong**************location is null'
				#else:
				location = location_tag['data-map-state']
				
				location_center = json.loads(location)['center']
				latitude = location_center['latitude']
				longitude = location_center['longitude']
				###########
				review_num =  review_num_tag.string.strip(' \r\n')
				price_tag = soup.find(name='dd',attrs={'class':'nowrap price-description'})
				price =''
				if price_tag:
					price = price_tag.string.strip(' \r\n')
				else:
					price_cnt = price_cnt+1
					if price_cnt<2:
						continue

				price_sign_tag = soup.find(name='span',attrs={'class':'business-attribute price-range'})
				price_sign = ''
				if price_sign_tag:
					price_sign =price_sign_tag.string.strip(' \r\n')

				#print type(price_tag),price_tag
				###########
				addr = ''
				city = ''
				region = ''
				code = ''

				addr_tag = soup.find(name='span',attrs={'itemprop':'streetAddress'})
				city_tag = soup.find(name='span',attrs={'itemprop':'addressLocality'})
				region_tag = soup.find(name='span',attrs={'itemprop':'addressRegion'})
				code_tag = soup.find(name='span',attrs={'itemprop':'postalCode'})

				if addr_tag:
					lst = self.get_navistring(addr_tag)
					addr = lst[0]
					for i in lst[1:]:
						addr = addr+' '+i
				
				if city_tag:
					city = city_tag.string.strip(' \r\n')

				if region_tag:
					region = region_tag.string.strip(' \r\n')

				if code_tag:
					code = code_tag.string.strip(' \r\n')


				print addr,'#',city,'#',region,'#',code,'#'
				name = '\"'+name+'\"'
				addr = '\"'+addr+'\"'
				city = '\"'+city+'\"'
				price_sign = '\"'+price_sign+'\"'
				price = '\"'+price+'\"'
				cate = '\"'+cate+'\"'
				
				s = name+','+review_num+','+addr+','+city+','+region+','+code+','+price_sign+','+price+','+cate+','+str(longitude)+','+str(latitude)
				#print s
				###########
				n = int(review_num.split(' ')[0])
				if n >1000:
					self.comments_num = 1000
				else:
					self.comments_num = n
				#print 'comment_num:',self.comments_num


				self.company_data = s
				self.add_comments(soup,self.comment_url)
				return
			except Exception,e:
				print e,'first error'
				if iii ==cnt-1:
					print e,'!!!!!!!!!!!!!!!!!!!!!first error'
					print '###'+self.comment_url
					self.except_lock.acquire()
					f = open('./info/first.txt','a')
					f.write(traceback.format_exc()+'-------------\n'+self.comment_url+'\n')
					f.close()
					except_file = open('./first_url.txt','a')
					except_file.write(self.comment_url+'\n')
					except_file.close()
					self.except_lock.release()

	def remain_20(self,index):
		cnt = 5
		for iii in range(0,cnt):
			try:
				page = self.get_index_page(index)
				soup = BeautifulSoup(page,'html.parser')
				user_list = soup.find_all(name='li',attrs={'class':'user-name'})
				review_list = soup.find_all(name='div',attrs={'class':'review-content'})
				# print len(review_list)
				#date_list = soup.find_all(name='span',attrs={'class':'rating-qualifier'})
				#rating_list = soup.find_all(name='div',attrs={'class':'review-content'})

				len_u = len(user_list)
				len_r = len(review_list)
				if len_u!=20 or len_r!=20:
					if iii != cnt-1:
						print 'retry',index
						continue
					else:
						self.except_lock.acquire()
						f = open('./info/length.txt','a')
						f.write('1')
						f.close()
						except_file = open('./except_url.txt','a')
						except_file.write(self.comment_url+'\n')
						except_file.close()
						self.except_lock.release()
				if len_u!= len_r:
					print 'in remain20, two length is not equal:',len(user_list),len(review_list)
					print self.comment_url
				l = len_u if len_u<=len_r else len_r

				for i in range(0,l):
					#print '---------------'
					user = next(user_list[i].find('a').children).strip(' \r\n')
					#rate = rating_list[i].find('img')['alt']
					rate = review_list[i].find('img')['alt']
					#date = next(date_list[i].children).strip(' \r\n')
					date = next(review_list[i].find(name='span',attrs={'class':'rating-qualifier'}).children).strip(' \r\n')
					user = '\"'+user+'\"'
					s = user+','+date+','+rate
					#print s
					self.comments.append(s)
				return
			except Exception,e:
				#print e,'remain20 error'
				if iii ==cnt-1:
					print 'remain20 error:',e
					print '###'+self.comment_url+' '+str(index)
					self.except_lock.acquire()
					f = open('./info/remain20.txt','a')
					f.write(traceback.format_exc()+'\n-------------\n')
					f.close()
					except_file = open('./remain20_url.txt','a')
					except_file.write(self.get_index_url(index)+'\n')
					except_file.close()
					self.except_lock.release()

	def remain(self,index):
		cnt = 5
		for iii in range(0,cnt):
			try:
				page = self.get_index_page(index)
				url = self.get_index_url(index)
				soup = BeautifulSoup(page,'html.parser')
				self.add_comments(soup,url)
				return
			except Exception,e:
				print e,'remain error'
				if iii ==cnt-1:
					print e,'!!!!!!!!!!!!!!!!!!!!!remain error'
					print '###'+self.comment_url+' '+str(index)
					self.except_lock.acquire()
					f = open('./info/remain.txt','a')
					f.write(traceback.format_exc()+'\n-------------\n')
					f.close()
					except_file = open('./remain_url.txt','a')
					except_file.write(self.get_index_url(index)+'\n')
					except_file.close()
					self.except_lock.release()

	def add_comments(self,soup,url):
		user_list = soup.find_all(name='li',attrs={'class':'user-name'})
		review_list = soup.find_all(name='div',attrs={'class':'review-content'})
		#date_list = soup.find_all(name='span',attrs={'class':'rating-qualifier'})
		#rating_list = soup.find_all(name='div',attrs={'class':'review-content'})

		#print len(user_list),len(review_list)
		if len(user_list)== len(review_list):
			for i in range(0,len(user_list)):
				#print '---------------'
				user = next(user_list[i].find('a').children).strip(' \r\n')
				#rate = rating_list[i].find('img')['alt']
				rate = review_list[i].find('img')['alt']
				#date = next(date_list[i].children).strip(' \r\n')
				date = next(review_list[i].find(name='span',attrs={'class':'rating-qualifier'}).children).strip(' \r\n')
				s = user+','+date+','+rate
				#print s
				self.comments.append(s)
			return

		temp_list = []
		cnt = 5
		for iii in range(0,cnt):
			try:
				page = self.getPage(home_url+url,self.except_lock)
				soup = BeautifulSoup(page,'html.parser')
				user_list = soup.find_all(name='li',attrs={'class':'user-name'})
				review_list = soup.find_all(name='div',attrs={'class':'review-content'})
				#date_list = soup.find_all(name='span',attrs={'class':'rating-qualifier'})
				#rating_list = soup.find_all(name='div',attrs={'class':'review-content'})

				len_u = len(user_list)
				len_r = len(review_list)
				if len_u!= len_r:
					if iii!=cnt-1:
						continue

				l = len_u if len_u<=len_r else len_r
				for i in range(0,l):
					#print '---------------'
					user = next(user_list[i].find('a').children).strip(' \r\n')
					#rate = rating_list[i].find('img')['alt']
					rate = review_list[i].find('img')['alt']
					#date = next(date_list[i].children).strip(' \r\n')
					date = next(review_list[i].find(name='span',attrs={'class':'rating-qualifier'}).children).strip(' \r\n')
					s = user+','+date+','+rate
					#print s
					temp_list.append(s)
				for i in temp_list:
					self.comments.append(i)
				return
			except Exception,e:
				print 'add comments error:',e
				if iii!=cnt-1:
					temp_list = []
				else:
					for i in temp_list:
						self.comments.append(i)
					self.except_lock.acquire()
					f = open('./info/add.txt','a')
					f.write(traceback.format_exc()+'\n-------------\n')
					f.close()
					except_file = open('./add_url.txt','a')
					except_file.write(self.get_index_url(index)+'\n')
					except_file.close()
					self.except_lock.release()


	def get_index_url(self,index):
		return self.comment_url+(comment_url_num.format(index*20))

	def get_index_page(self,index):
		start = index*20
		if start >= self.comments_num:
			print 'start error'
			return
		url_page = home_url+self.comment_url+(comment_url_num.format(start))
		#print '-------------------begin page'
		page = self.getPage(url_page,self.except_lock)
		#print '-------------------end page'
		return page

	def get_navistring(self,tag):
		navi = []
		if not isinstance(tag,element.Tag):
			tag_str = tag.strip(' \r\n')
			if tag_str:
				navi.append(tag_str)
			return navi
		
		for i in tag.children:
			for ii in self.get_navistring(i):
				navi.append(ii)
		return navi

	def get_post_num(self,src):
		s =''
		for i in src[::-1]:
			if i>='0' and i<='9':
				s = i+s
			else:
				break
		if len(s)==5 or len(s)==6:
			self.post_num = s
			return True
		return False
