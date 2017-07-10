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
from Crawlers.CommentCrawlerThread import *
import os
import sys


if __name__ == "__main__":
	# comment_url = '/biz/c6-performance-skills-training-grand-prairie'
	# comment_url = '/biz/la-contenta-new-york'
	# comment_url = '/biz/bon-crawfish-hut-grand-prairie-12'
	# comment_url = '/biz/dunkin-donuts-arlington-27'


	reload(sys)
	sys.setdefaultencoding('utf-8')
	except_lock = threading.Lock()
	info_lock = threading.Lock()

	# c = CommentCrawler(comment_url,except_lock,info_lock)
	# c.begin()

	queue_lock = threading.Lock()
	cnt_lock = threading.Lock()
	tgt_file_lock = threading.Lock()
	buffer_queue = Queue.Queue()

	queue = Queue.Queue()
	file = open(comment_src_file,'r')
	url_list = file.readlines()
	print 'total cnt:'+str(len(url_list))
	for i in url_list:
		queue.put(i)
	file.close()
	threads = []
	for i in range(0,thread_num):
		t = CommentCrawlerThread(buffer_queue,url_list,queue,queue_lock,tgt_file_lock,except_lock,info_lock)
		threads.append(t)
		t.start()
		print 'thread'+str(i)
		time.sleep(1)

	for t in threads:
		t.join()

	shopfile = open(comment_tgt_file,'a')
	while not buffer_queue.empty():
		item = buffer_queue.get()+'\n'
		shopfile.write(item)
	shopfile.close()

















	# if url_list:
	# 	file = open(comment_src_file,'w')
	# 	file.writelines(url_list)
	# 	file.close()