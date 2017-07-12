import threading

class TestThread(threading.Thread):
	def __init__(self,queue,lock):
		super(TestThread,self).__init__()
		self.lock = lock
		self.queue = queue

	def run(self):
		while True:
			self.lock.acquire()
			if self.queue.empty():
				self.lock.release()
				break
			print self.queue.get()
			self.lock.release()
		print '-------------------------------end'



