# -*- coding:utf-8 -*-

from config import *
from crawler import *
import requests
import sys 
import json
import math
import Queue
import os
import threading
from bs4 import BeautifulSoup
from bs4 import element
import string
import traceback
import ssl

# str转bytes叫encode，bytes转str叫decode str就是unicode字符
# http://blog.csdn.net/jim7424994/article/details/22675759

reload(sys)
sys.setdefaultencoding('utf-8') 
ssl._create_default_https_context = ssl._create_unverified_context
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def crawl_id():
	c = BaseCrawler()
	queue = Queue.Queue()
	id_dict = dict() # {job_city:id_lst}
	for city in city_lst:
		for job in job_lst:
			city = city.decode('utf-8')
			job = job.decode('utf-8')
			if os.path.exists('../cache/'+city+'_'+job+'_'+id_filename):
				continue
			else:
				id_dict[city+'_'+job] = []
				d = c.post(city,job,1)
				try:
					pageSize = d['content']['pageSize']
					totalCount = d['content']['positionResult']['totalCount']
					max_page_num = int(math.ceil(float(totalCount)/pageSize))

					print city,job,totalCount,pageSize,max_page_num
					for i in range(2,max_page_num+1):
						queue.put([city,job,i])

					result = d['content']['positionResult']['result']
					for item in result:
						id_dict[city+'_'+job].append(item['positionId'])
				except Exception,e:
					print e

	# handle duty in queue
	if queue.empty():
		return 
	threads=[]
	queue_lock = threading.Lock();
	dict_lock = threading.Lock()
	except_lock = threading.Lock()
	for i in range(0,thread_num):
		t = IdCrawlerThread(queue,id_dict,queue_lock,dict_lock,except_lock)
		threads.append(t)
		t.start()
		print 'thread',i
		time.sleep(1)

	for t in threads:
		t.join()

	for key,value in id_dict.items():
		file = open('../cache/'+key+'_'+id_filename,'a')
		for i in value:
			file.write(str(i)+'\n')
		file.close()


def crawl_posinfo():
	cache_folder = '../cache/'
	all_file_list=os.listdir(cache_folder)
	print all_file_list

	for id_file in all_file_list:
		if not 'txt' in id_file:
			continue
		global finish_cnt
		finish_cnt = 0

		queue = Queue.Queue()
		duty_lst = []
		file = open(cache_folder+id_file)
		for line in file.readlines():
			queue.put(line.strip())
			duty_lst.append(line.strip())
		if queue.empty():
			continue

		# handle duty in queue
		threads=[]
		res = []
		l = id_file.split('_')
		filename = '../result/'+l[0]+'_'+l[1]+'_'+pos_filename
		queue_lock = threading.Lock();
		dict_lock = threading.Lock()
		except_lock = threading.Lock()
		cnt_lock = threading.Lock()
		for i in range(0,thread_num):
			t = PosCrawlerThread(queue,duty_lst,res,queue_lock,except_lock,cnt_lock,filename,cache_folder+id_file)
			threads.append(t)
			t.start()
			print 'thread',i
			time.sleep(1)

		for t in threads:
			t.join()

		# write remained data
		file = open(filename,'ab')
		for lll in res:
			for item in lll[:-1]:
				file.write(item+separator)
			file.write(lll[-1]+'\n')
		file.close()

		file = open(cache_folder+id_file,'wb')
		for item in duty_lst:
			file.write(item+'\n')
		file.close()


if __name__ == '__main__':
	for folder in ['../cache','../except','../result']:
		if not os.path.exists(folder):
			os.makedirs(folder)

	crawl_id()
	crawl_posinfo()
	