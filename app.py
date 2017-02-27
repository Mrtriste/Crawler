import urllib2
import os
from bs4 import BeautifulSoup
from Crawlers.Crawler import *
from Crawlers.MWTCrawler import *
from Crawlers.MWFCrawler import *
from Crawlers.PCRCrawler import *
from Crawlers.FYBCrawler import *
from Crawlers.MRCrawler import *
from Crawlers.MSCrawler import*
from Crawlers.HTRCrawler import*
from config import *
import smtplib
from email.mime.text import MIMEText
import time


def send_to_mail(smtp,date,title,link):
	for i in receivers:
		msg = MIMEText(link)
		msg['From'] = sender
		msg['To'] = i
		msg['Subject'] = '[%s][%s]%s'%(home.split('/')[2],date,title)
		for cnt in range(0,try_conn_mail_cnt):
			try:
				smtp.sendmail(sender, i, msg.as_string())
				print 'send a mail:'+msg['Subject']
				break
			except SMTPDataError,e:
				print "SMTPDataError:"+e.
			except SMTPServerDisconnected,e:
				print 'Disconnected,try reconnect:'+str(cnt)
				smtp = smtplib.SMTP_SSL('smtp.qq.com', 465)
				smtp.login(sender, pwd)

if __name__ == "__main__":
	#record.txt records {home:last_latest_article_link},to judge if an article is new
	if not os.path.exists('./record.txt'):
		file = open('./record.txt','w')
		for i in url_list:
			file.write(i+',\n')
		file.close()
	while True:
		last_title_dict = {}
		record_file = open('./record.txt','r')
		#read record file to dict
		while True:
			line = record_file.readline()
			if line:
				last_title_dict[line.split(',')[0]] = line.split(',')[1].replace("\n", "")
			else:
				break
		record_file.close()

		crawler_list=[]
		crawler = MWTCrawler(url_list[0],last_title_dict[url_list[0]])
		crawler_list.append(crawler)
		crawler = MWFCrawler(url_list[1],last_title_dict[url_list[1]])
		crawler_list.append(crawler)
		crawler = PCRCrawler(url_list[2],last_title_dict[url_list[2]])
		crawler_list.append(crawler)
		crawler = FYBCrawler(url_list[3],last_title_dict[url_list[3]])
		crawler_list.append(crawler)
		crawler = MRCrawler(url_list[4],last_title_dict[url_list[4]])
		crawler_list.append(crawler)
		crawler = MSCrawler(url_list[5],last_title_dict[url_list[5]])
		crawler_list.append(crawler)
		crawler = HTRCrawler(url_list[6],last_title_dict[url_list[6]])
		crawler_list.append(crawler)
		
		index = 0
		tuples = []
		for c in crawler_list:
			c.parse(url_list[index])
			tuples = tuples + c.getDate_Titles(c.parse_list)[::-1]
			index = index+1

		if tuples:
			smtp = smtplib.SMTP_SSL('smtp.qq.com', 465)
			smtp.login(sender, pwd)
			for date_title in tuples:
			 	#print 'date:'+date_title[0]+' title:'+date_title[1]+' link:'+date_title[2]
			 	send_to_mail(smtp,date_title[0],date_title[1],date_title[2])

		record_file = open('./record.txt','w+')
		for c in crawler_list:	
			record_file.write(c.get_write_content())
		record_file.close()
		print '----------------end------------------'
		time.sleep(1800)