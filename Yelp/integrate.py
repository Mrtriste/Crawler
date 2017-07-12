from main import *
import csv

def func(filename,tgt):
	file = open(filename,'r')	
	reader = csv.reader(file)
	lst = []
	for row in reader:
		temp=[]
		for i in row[0:8]:
			temp.append(i)
		for i in row[9:]:
			temp.append(i)
		cate_list = row[8].split(',')
		for i in cate_list:
			temp.append(i)
		lst.append(temp)
		# for i in temp:
		# 	print i
		
	file.close()

	file = open(tgt,'ab')
	writer = csv.writer(file)
	writer.writerows(lst)
	file.close()

def compact(src_folder,tgt):
	for fn in os.listdir(src_folder):
		print fn,'begin'
		func(src_folder+'\\'+fn,tgt)
		print '---------------end'

if __name__ == "__main__":
	#compact('F:\step1\comment','./allcomment.csv')
	#compact('F:\step4','./allcomment.csv')
	count=0  
	fp=open("./allcomment.csv","r")  
	while 1:
		buffer=fp.read(8*1024*1024)  
		if not buffer:  
			break  
		count+=buffer.count('\n')  
		#print count  
	print count  
	print 'over'  
	fp.close()