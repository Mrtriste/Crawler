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
import sys
import json
from slackclient import SlackClient
#import sqlite3
import string

def save_to_db(tuples):
	try:
		conn = sqlite3.connect('blog.db')
		sql = "CREATE TABLE IF NOT EXISTS blog (ID integer PRIMARY KEY,domain varchar,title varchar,url varchar,blog_date TEXT,insert_date TEXT)"
		conn.execute(sql)  
		cs = conn.cursor()
		try:
			for i in tuples:
				local_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
				cs.execute("insert into blog values(null,?,?,?,?,?)",(i[2].split('/')[2],i[1],i[2],i[3],local_time))
		except sqlite3.OperationalError,e:
			print 'OperationalError:'+e

		conn.commit()
		cs.close()
		conn.close()
	except Exception,e:
		print 'catch exception:'+e

def send_slack(slack_client,date,title,link):
	try:
		text = '[howto][%s][%s]%s'%(link.split('/')[2],date,title)+'\n'+link
		print 'slack:'+filter(lambda x: x in string.printable, text)
		slack_client.api_call("chat.postMessage", channel=channel,text=text, as_user=True)
	except Exception,e:
		print e

def send_to_mail(smtp,date,title,link):
	for i in receivers:
		msg = MIMEText(link)
		msg['From'] = sender
		msg['To'] = i
		msg['Subject'] = '[howto][%s][%s]%s'%(link.split('/')[2],date,title)
		for cnt in range(0,try_conn_mail_cnt):
			try:
				print 'send a mail:'+filter(lambda x: x in string.printable,msg['Subject']+' to '+i)
				smtp.sendmail(sender, i, msg.as_string())
				time.sleep(send_mail_interval)
				break
			except smtplib.SMTPDataError,e:
				print "SMTPDataError:"+e
			except smtplib.SMTPServerDisconnected,e:
				print 'Disconnected,try reconnect:'+str(cnt)
				smtp = smtplib.SMTP_SSL(server, port)
				smtp.login(sender, pwd)
			except Exception,e:
				print e


if __name__ == "__main__":
	reload(sys)
	sys.setdefaultencoding('utf-8')
	#record.txt records {home:last_latest_article_link},to judge if an article is new
	if not os.path.exists('./record.txt'):
		file = open('./record.txt','w')
		for i in url_list:
			file.write(i+',\n')
		file.close()
	while True:
		print '-----------------start------------------'
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
			####################login mail
			smtp = smtplib.SMTP_SSL(server, port)
			smtp.login(sender, pwd)
			####################get slack client
			slack_client = SlackClient(token)
			for date_title in tuples:
				print date_title[0]+' '+date_title[1]+' '+date_title[2]#+' '+date_title[3]
				#############################send by mail
			 	send_to_mail(smtp,date_title[0],date_title[1],date_title[2])
			 	#############################send by slack
			 	send_slack(slack_client,date_title[0],date_title[1],date_title[2])
			###################logout mail
			smtp.close()
			save_to_db(tuples)



		record_file = open('./record.txt','w+')
		for c in crawler_list:	
			record_file.write(c.get_write_content())
		record_file.close()
		print '-----------------end------------------'
		time.sleep(refresh_time)