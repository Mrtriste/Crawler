#-*- coding:utf-8 -*-

import urllib2
import time
from bs4 import BeautifulSoup
from config import *
from Crawlers.SearchCrawler import *
from Crawlers.ShopCrawler import *
from Crawlers.CommentCrawler import *
import Queue
import threading
from Crawlers.TestThread import *
from Crawlers.CrawlerThread import *
import os

##############################################
# file_name = './data.txt'
# city_file = './city.txt'
# city_queue = Queue.Queue()
# city_list = []
# city_lock = threading.Lock()
# data_lock = threading.Lock()
# except_lock = threading.Lock()
# global file_cnt
# file_cnt = 0

# city_url_folder = './cityurl/'
# city_url_queue = Queue.Queue()


def delete_city(city):
	city_lock.acquire()
	city_list.remove(city)
	file = open(city_file,'w')
	for i in city_list:
		file.write(i+'\n')
	file.close()
	city_lock.release()

def test_handle_one_city():
	city = 'Dallas, TX'
	city = city.replace(' ','+')
	c = SearchCrawler()
	c.init(city)
	c.begin()



def test_handle_one_city_shop():
	city_url = 'https://www.yelp.com/search?find_loc=Dallas,+TX&cflt=amateursportsteams'
	c = ShopCrawler(city_url,'111.txt')
	c.begin()


def handle_one_city_shop():
	pass

def compact_folder(src_folder,tgt_file):
	file = open(tgt_file,'a')
	for fn in os.listdir(src_folder):
		f = open(src_folder+'\\'+fn,'r')
		file.writelines(f.readlines())
		f.close()
	file.close()

def set_file(filename):
	file = open(filename,'r')
	l = list(set(file.readlines()))
	file.close()
	file = open(filename,'w')
	file.writelines(l)
	file.close()


def send(targetUrl):
	print 'send'
	resp = urllib2.urlopen(targetUrl).read()
	print 'get'
	#print resp 


def unique(src_file,tgt_file):
	src = open(src_file,'r')
	lines = src.readlines()
	src.close()
	print 'src:',str(len(lines))+' lines'
	l = list(set(lines))
	print 'tgt:',str(len(l))+' lines'
	tgt = open(tgt_file,'w')
	tgt.writelines(l)
	tgt.close()

def divide_file(src_file,tgt_file_prefix,tgt_file_postfix,tgt_num):
	src = open(src_file,'r')
	lines = src.readlines()
	src.close()
	length = len(lines)
	one_file_num = length/tgt_num
	remain = length - one_file_num*tgt_num
	for i in range(0,remain):
		tgt_name = tgt_file_prefix+str(i+3)+'.'+tgt_file_postfix
		tgt = open(tgt_name,'w')
		tgt.writelines(lines[i*(one_file_num+1):(i+1)*(one_file_num+1)])
		tgt.close()
	start = remain*(one_file_num+1)
	for i in range(remain,tgt_num):
		tgt_name = tgt_file_prefix+str(i+3)+'.'+tgt_file_postfix
		tgt = open(tgt_name,'w')
		tgt.writelines(lines[start+(i-remain)*one_file_num:start+(i-remain+1)*one_file_num])
		tgt.close()
	
	tgt.close()


def cal_city():
	while True:
		if all_city.empty():
			break
		queue_lock.acquire()
		city = all_city.get().strip(' \r\n')
		queue_lock.release()
		url = search_url.format(city)
		c = Crawler()
		for i in range(0,10):
			page = c.getPage(url,except_lock)
			soup = BeautifulSoup(page,'html.parser')
			num_str = soup.find(name = 'span',attrs={'class':'pagination-results-window'})
			if not num_str:
				continue
			else:
				break
		if not num_str:
			exc_num = exc_num+1
			print 'exception)))))))))))))))))))))))))))))))'
		num = (int)(num_str.string.split('of ')[-1].strip(' \n'))
		s = city+'\t'+str(num)
		list_lock.acquire()
		record[num]=s
		nums.append(num)
		list_lock.release()
	print '---------------thread end---------------'



########################################### calulate the shop's num in cities

# all_city = Queue.Queue()
# queue_lock = threading.Lock()
# except_lock = threading.Lock()
# list_lock = threading.Lock()
# record={}
# nums=[]
# exc_num = 0

# if __name__ == "__main__":
# 	print 'main'
# 	file = open('./city.txt','r')
# 	lines = file.readlines()
# 	file.close()
# 	for l in lines:
# 		l = l.replace(' ','+')
# 		all_city.put(l)
# 	threads=[]

# 	for i in range(0,70):
# 		t = threading.Thread(target=cal_city)
# 		threads.append(t)
# 		t.start()
# 		print 'thread',i
# 		time.sleep(0.3)

# 	for t in threads:
# 		t.join()

# 	file = open('./tongji.txt','w')
# 	nums.sort()
# 	length = 0
# 	total = 0
# 	for i in nums:
# 		total = total+i
# 		if i>1000:
# 			length = length+1
# 		l = record[i]
# 		file.write(l+'\n')
# 	file.close()
# 	print exc_num,' city'
# 	print 'total:',len(nums),'city,',length,' city >1000'
# 	print total,' shops'









##############################################crawl shops in catagories' url
# if __name__ == "__main__":
	# queue_lock = threading.Lock()
	# cnt_lock = threading.Lock()
	# tgt_file_lock = threading.Lock()
	# except_lock = threading.Lock()
	# buffer_queue = Queue.Queue()

	# queue = Queue.Queue()
	# file = open(city_data,'r')
	# url_list = file.readlines()
	# print 'total cnt:'+str(len(url_list))
	# for i in url_list:
	# 	queue.put(i)
	# file.close()
	# threads = []
	# for i in range(0,100):
	# 	t = CrawlerThread(buffer_queue,url_list,queue,queue_lock,cnt_lock,tgt_file_lock,except_lock)
	# 	threads.append(t)
	# 	t.start()
	# 	print 'thread',i
	# 	time.sleep(1)

	# for t in threads:
	# 	t.join()

	# shopfile = open(shop_data,'a')
	# while not buffer_queue.empty():
	# 	item = buffer_queue.get()+'\n'
	# 	shopfile.write(item)
	# shopfile.close()

	# if url_list:
	# 	file = open(city_data,'w')
	# 	file.writelines(url_list)
	# 	file.close()



def handleOneCity():
	while True:
		if city_queue.empty():
			break
		city = city_queue.get()
		if not city:
			continue
		#city = 'Richmond, VA'
		temp_city = city.replace(' ','+')
		c = SearchCrawler()
		c.init(temp_city,except_lock)
		c.begin()
		data_lock.acquire()
		# c_name = temp_city.replace(' ','').replace(',','-')
		file = open(file_name,'a')
		while not c.total_queue.empty():
			url = c.total_queue.get()
			file.write(url+'\n')
		file.close()
		global file_cnt
		file_cnt = file_cnt+1
		print file_cnt,'city-------------'
		data_lock.release()

		
		delete_city(city)


######################################################crawl catagory's url in cities
# if __name__ == "__main__":
# 	#unique(file_name,file_name)
# 	#test_handle_one_city()
# 	lst = open('./city.txt','r')
# 	index = 0
# 	while True:
# 		line = lst.readline()
# 		if line:
# 			index = index+1
# 			city_queue.put(line.strip(' \n'))
# 			city_list.append(line.strip(' \n'))
# 		else:
# 			break
# 	lst.close()
# 	print index,' city'

# 	threads = []

# 	for i in range(0,70):
# 		t = threading.Thread(target=handleOneCity)
# 		print '----'
# 		threads.append(t)
# 		t.setDaemon(True)
# 		t.start()
# 		time.sleep(1)
# 	for t in threads:
# 		t.join()
