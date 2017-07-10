import threading
from CommentCrawler import *

class CommentCrawlerThread(threading.Thread):
	def __init__(self,buffer_queue,url_list,queue,queue_lock,tgt_file_lock,except_lock,info_lock):
		super(CommentCrawlerThread,self).__init__()
		self.url_list = url_list
		self.queue_lock = queue_lock
		self.tgt_file_lock = tgt_file_lock
		self.except_lock = except_lock
		self.queue = queue
		self.buffer_queue = buffer_queue
		self.info_lock =info_lock

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

			c = CommentCrawler(url,self.except_lock,self.info_lock)
			c.begin()

			#---------------
			self.tgt_file_lock.acquire()
			print len(c.comments),c.comments_num
			for u in c.comments:
				if not c.company_data:
					break
				self.buffer_queue.put(c.company_data+','+u)
			self.url_list.remove(url)

			global crawl_shop_cnt
			crawl_shop_cnt = crawl_shop_cnt+1
			#c.write2(crawl_shop_cnt)
			mod =1000
			if len(self.url_list)<1000:
				mod = 100
			if len(self.url_list)<500:
				mod = 10
			if len(self.url_list)<100:
				mod = 1
			if crawl_shop_cnt%mod==0 and crawl_shop_cnt>0:
				shopfile = open(comment_tgt_file,'a')
				while not self.buffer_queue.empty():
					item = self.buffer_queue.get()+'\n'
					shopfile.write(item)
				shopfile.close()

				file = open(comment_src_file,'w')
				file.writelines(self.url_list)
				file.close()
				print '--------------------update file--------------------'
			print 'remain:'+str(len(self.url_list))+'    the '+str(crawl_shop_cnt)+' url:'+url
			self.tgt_file_lock.release()
			################

		print '-------------------------------end-------------------------------'
