import threading
from ShopCrawler import *

class CrawlerThread(threading.Thread):
	def __init__(self,buffer_queue,url_list,queue,queue_lock,cnt_lock,tgt_file_lock,except_lock):
		super(CrawlerThread,self).__init__()
		self.url_list = url_list
		self.queue_lock = queue_lock
		self.cnt_lock = cnt_lock
		self.tgt_file_lock = tgt_file_lock
		self.except_lock = except_lock
		self.queue = queue
		self.buffer_queue = buffer_queue

	def run(self):
		while True:
			#---------------
			self.queue_lock.acquire()
			if self.queue.empty():
				self.queue_lock.release()
				break
			url = self.queue.get()
			self.queue_lock.release()
			################

			c = ShopCrawler(url,shop_data,self.except_lock)
			# if 'start' in url:
			# 	c.remain_start(url)
			# else:
			# 	c.begin()

			c.begin()

			#---------------
			self.tgt_file_lock.acquire()

			for u in c.get_shopurl_list():
				self.buffer_queue.put(u)
			self.url_list.remove(url)
			global crawl_shop_cnt
			crawl_shop_cnt = crawl_shop_cnt+1
			#c.write2(crawl_shop_cnt)
			mod =50
			if len(self.url_list)<10:
				mod = 1
			if crawl_shop_cnt%mod==0 and crawl_shop_cnt>0:
				shopfile = open(shop_data,'a')
				while not self.buffer_queue.empty():
					item = self.buffer_queue.get()+'\n'
					shopfile.write(item)
				shopfile.close()

				file = open(city_data,'w')
				file.writelines(self.url_list)
				file.close()
				print '--------------------update file--------------------'
			print 'remain:'+str(len(self.url_list))+'    the '+str(crawl_shop_cnt)+' url:'+url


			self.tgt_file_lock.release()
			################

			#---------------
			# self.cnt_lock.acquire()
			
			# self.cnt_lock.release()
			################

		print '-------------------------------end-------------------------------'
