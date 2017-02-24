import urllib2
import os
from bs4 import BeautifulSoup
from Crawlers.Crawler import *
from Crawlers.MWTCrawler import *
from config import *
import smtplib

# message = """From: From Person <from@fromdomain.com>
# 			 To: To Person <to@todomain.com>
# 			 Subject: SMTP e-mail test
# 			 This is a test e-mail message.
# 		  """

# smtp = smtplib.SMTP_SSL("smtp.qq.com", 465)
# smtp.login(sender, pwd)
# smtp.sendmail(sender, sender, message)         
# print "Successfully sent email"


last_title_dict = {}
#record.txt records {home:last_latest_article_link},to judge if an article is new
if not os.path.exists('./record.txt'):
	file = open("./record.txt",'w')
	for i in url_list:
		file.write(i+",\n")
	file.close()

record_file = open("./record.txt",'r')
#read record file to dict
while True:
	line = record_file.readline()
	if line:
		last_title_dict[line.split(',')[0]] = line.split(',')[1].replace("\n", "")
	else:
		break
record_file.close()

b = B()
#b.a1('fuck')
print b.getS()



crawler = MWTCrawler(url_list[0],last_title_dict[url_list[0]])
crawler.parse(url_list[0])

record_file = open("./record.txt",'w+')
print crawler.get_write_content()
record_file.write(crawler.get_write_content())
record_file.close()