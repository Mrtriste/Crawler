# -*- coding:utf-8 -*-

from config import *
import requests
import time
import json
import random
import threading
from bs4 import BeautifulSoup
from bs4 import element
import traceback  

global finish_cnt
finish_cnt = 0

class BaseCrawler(object):
	def post(self,city,job,page):
		print city,job,page
		index = random.randint(0,15)
		url = base_url.format(city)
		data = {
			'first':'false',
			'pn':page,
			'kd':job
		}
		headers = {
			'Host': 'www.lagou.com',
			'Referer': 'https://www.lagou.com/jobs/list_{0}?px=default&city={1}'.format(job,city),
			'User-Agent': USER_AGENTS[index]
		}

		for i in range(0,try_num):
			try:
				response = requests.post(url,headers=headers,data=data, proxies=proxies,verify=False) #
				data = response.text
				d = json.loads(data)
				if d['success'] != True:
					print '------post error------'
					print data
					continue
				return d
			except Exception,e:
				print e
				time.sleep(0.5)
				if i == try_num-1:
					print e,'connect fail'
					print 'post error'+url
					return None

	def get_page(self,pos_id):		
		index = random.randint(0,15)
		url = base_url1.format(pos_id)
		headers = {
			'Host': 'www.lagou.com',
			# 'Referer': 'https://www.lagou.com/jobs/list_{0}?px=default&city={1}'.format(job,city),
			'Referer': 'https://www.lagou.com',
			'User-Agent': USER_AGENTS[index]
		}
		for i in range(0,try_num):
			try:
				response = requests.get(url,headers=headers,proxies=proxies,verify=False) # 
				data = response.text
				return data
			except Exception,e:
				print e
				time.sleep(0.5)
				if i == try_num-1:
					print e,'connect fail'
					print 'getpage error'+url
					return None

	def handle_except(self,except_lock,name):
			# except_lock.acquire()
			file = open('../except/'+except_info_filename,'a')
			file.write('********'+self.pos_id+'---'+name+'\n')
			# traceback.print_exc(file=file)
			file.write('\n')
			# except_lock.release()
			# print '*******nodata:',self.pos_id,name
			return ''

	def get_data(self,pos_id,except_lock):
		self.pos_id = pos_id
		def get_navistring(tag):
			navi = []
			if not isinstance(tag,element.Tag):
				tag_str = tag.strip(' \r\n')
				if tag_str:
					navi.append(tag_str)
				return navi
			
			for i in tag.children:
				for ii in get_navistring(i):
					navi.append(ii)
			return navi
		print '************',pos_id,'***********'
		page = self.get_page(pos_id)
		# 
		soup = BeautifulSoup(page,'html.parser')
		pos_content = soup.find(name='div',attrs={'class':'position-content'})
		if pos_content is None:
			except_lock.acquire()
			file = open('../except/'+pos_except_filename,'ab')
			file.write(pos_id+'\n')
			except_lock.release()
			return None
		try:
			pos_name = pos_content.find(name='span',attrs={'class':'name'}).string.strip()
		except Exception,e:
			pos_name = self.handle_except(except_lock,'pos_name')

		# 
		try:
			job_request = pos_content.find(name='dd',attrs={'class':'job_request'})
			req_spans = job_request.find_all(name='span')
			req_info = ''
			for req_span in req_spans:
				req_info += req_span.string.strip()
		except Exception,e:
			req_info = self.handle_except(except_lock,'req_info')

		# 
		try:
			job_detail = soup.find(name='dl',attrs={'class':'job_detail'})
			job_bt = job_detail.find(name='dd',attrs={'class':'job_bt'})
			pos_des_lst = get_navistring(job_bt)
			pos_des = ''
			for iii in pos_des_lst:
				pos_des += iii
		# pos_des_lst = pos_des.split('职位要求：')
		# pos_des1 = pos_des_lst[0].replace('岗位职责：','')
		# pos_des2 = pos_des_lst[1]
		except Exception,e:
			pos_des = self.handle_except(except_lock,'pos_des')

		try:
			# -----------------------
			c_feature = soup.find(name='ul',attrs={'class':'c_feature'})
			field = c_feature.find(name='i',attrs={'class':'icon-glyph-fourSquare'}).next_sibling.strip()
		except Exception,e:
			field = self.handle_except(except_lock,'field')

		# 
		try:
			dev_step = c_feature.find(name='i',attrs={'class':'icon-glyph-trend'}).next_sibling.strip()
		except Exception,e:
			dev_step = self.handle_except(except_lock,'dev_step')

		# 
		try:
			invest = c_feature.find(name='p',attrs={'class':'financeOrg'}).string.strip()
		except Exception,e:
			invest = self.handle_except(except_lock,'invest')

		# 
		try:
			scale = c_feature.find(name='i',attrs={'class':'icon-glyph-figure'}).next_sibling.strip()
		except Exception,e:
			scale = self.handle_except(except_lock,'scale')

		# 
		try:
			home_page = c_feature.find(name='a',attrs={'target':'_blank'})['href'].strip()
		except Exception,e:
			home_page = self.handle_except(except_lock,'home_page')

		# ------------------------
		try:
			content_r = soup.find(name='div',attrs={'class':'content_r'})
			img_link = content_r.find(name='img',attrs={'class':'b2'})['src'].strip()
		except Exception,e:
			img_link = self.handle_except(except_lock,'img_link')

		# 
		try:
			h2 = content_r.find(name='h2',attrs={'class':'fl'}) 
			img_title = ''
			for child in h2:
				if isinstance(child,element.NavigableString):
					img_title += child
			img_title = img_title.replace(' ','').strip()
		except Exception,e:
			img_title = self.handle_except(except_lock,'img_title')


		# -----------------------
		try:
			work_addr_div = soup.find(name='div',attrs={'class':'work_addr'})
			work_addr = ''
			for child in work_addr_div:
				if isinstance(child,element.NavigableString):
					work_addr += child
				else:
					work_addr += child.string 
			work_addr = work_addr.replace('查看地图','').replace(' ','').replace('\n','').strip()
		except Exception,e:
			work_addr = self.handle_except(except_lock,'work_addr')

		# -----------------------
		try:
			jd_publisher = soup.find(name='dd',attrs={'class':'jd_publisher'})
			HR_name = jd_publisher.find(name='span',attrs={'class':'name'}).string
			divs = jd_publisher.find(name='div',attrs={'publisher_data'}).find_all(name='div')
			# ----div0
			div = divs[0]
			light_tip = div.find(name='i',attrs={'class':'light_tip'})
			num = light_tip.string.strip()
			time1 = num+light_tip.next_sibling.strip()
		except Exception,e:
			time1 = self.handle_except(except_lock,'time1')

		# ----div1
		try:
			div = divs[1]
			speed = div.find(name='span',attrs={'class':'data'}).string
			reply = div.find_all(name='i',attrs={'class':'light_tip'})
			rate = reply[0].string.strip()
			time2 = reply[1].string.strip() + reply[1].next_sibling.strip()
		except Exception,e:
			rate = ''
			time2 = self.handle_except(except_lock,'time2')

		# ----div2
		try:
			div = divs[2]
			time31 = div.find(name='span',attrs={'class':'data'}).string.strip()
			span = div.find(name='span',attrs={'class':'tip'})
			time32 = ''
			for c in get_navistring(span):
				time32 += c 
			time32 = time32.strip()
		except Exception,e:
			time31 = ''
			time32 = self.handle_except(except_lock,'time32')

		this_page = 'https://www.lagou.com/jobs/%s.html'%pos_id
		ret_lst = [this_page,pos_name,req_info,field,dev_step,invest,scale,home_page,img_link,img_title,
		work_addr,time1,rate,time2,time31,time32,pos_des]

		# file = open('file.txt','ab')
		# for item in ret_lst[:-1]:
		# 	file.write(item+separator)
		# file.write(ret_lst[-1]+'\n')
		# file.close()

		return ret_lst


class IdCrawlerThread(threading.Thread):
	def __init__(self,queue,id_dict,queue_lock,dict_lock,except_lock):
		super(IdCrawlerThread,self).__init__()
		self.queue = queue
		self.id_dict = id_dict
		self.queue_lock = queue_lock
		self.dict_lock = dict_lock
		self.except_lock = except_lock

	def run(self):
		c = BaseCrawler()
		while True:
			# get one duty
			self.queue_lock.acquire()
			if self.queue.empty():
				self.queue_lock.release()
				break
			items = self.queue.get()
			self.queue_lock.release()
			
			# get id 
			d = c.post(items[0],items[1],items[2])
			lst = []
			try:
				result = d['content']['positionResult']['result']
				for item in result:
					lst.append(item['positionId'])
			except Exception,e:
				print '--------json error-------'
				print e
				self.except_lock.acquire()
				file = open('../except/'+id_except_filename,'a')
				file.write(item[0]+'\t'+item[1]+'\t'+str(item[2])+'\n')
				self.except_lock.release()

			# append to lst
			self.dict_lock.acquire()
			self.id_dict[items[0]+'_'+items[1]] += lst
			self.dict_lock.release()

class PosCrawlerThread(threading.Thread):
	def __init__(self,queue,duty_lst,res,queue_lock,except_lock,cnt_lock,filename,id_file):
		super(PosCrawlerThread,self).__init__()
		self.queue = queue
		self.duty_lst = duty_lst
		self.res = res
		self.queue_lock = queue_lock
		self.except_lock = except_lock
		self.cnt_lock = cnt_lock
		self.filename = filename
		self.id_file = id_file


	def run(self):
		c = BaseCrawler()
		while True:
			# get one duty
			self.queue_lock.acquire()
			if self.queue.empty():
				self.queue_lock.release()
				break
			item = self.queue.get()
			self.queue_lock.release()

			ret_lst = c.get_data(item,self.except_lock)

			self.cnt_lock.acquire()
			global finish_cnt
			finish_cnt += 1
			self.duty_lst.remove(item)
			if ret_lst is not None:
				self.res.append(ret_lst)
			if finish_cnt%per_save_num==0 and finish_cnt>0:
				finish_cnt = 0
				print '-------------------------------save to file'
				file = open(self.filename,'ab')
				for lll in self.res:
					for item in lll[:-1]:
						file.write(item+separator)
					file.write(lll[-1]+'\n')
				file.close()

				file = open(self.id_file,'wb')
				for item in self.duty_lst:
					file.write(item+'\n')
				file.close()

				del self.res[:]
			self.cnt_lock.release()
