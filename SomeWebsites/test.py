#-*- coding:utf-8 -*-

s = '中文'
s1 = s.decode('utf-8')
s2 = s.encode('gbk')
s3 = s.decode('utf-8').encode('gbk')
s4 = s.decode('utf-8').encode('ascii')
s5 = s.encode('utf-8')
s6 = s.decode('utf-8').encode('utf-8')


# def test(s1):
# 	s2 = s1.encode('utf-8')
# 	s3 = s1.encode('gbk')
# 	s4 = s3.encode('utf-8')
# 	s5 = s2.decode('gbk')
# 	s6 = s1.decode('ascii')
# 	s7 = s1.encode('ascii')
# 	print s2
# 	print s3
# 	print s4
# 	print s5
# 	print s6
# 	print s7

# s = 'test'
# test(s)




# print type(s3)
# print s3.decode('utf-8').encode('gbk')
# #s4 = s3.encode('ascii')
# print s3.decode('utf-8').encode('gb2312')



# from slackclient import SlackClient

# token = 'xoxp-40029613668-40029615492-147293486659-680e593def36ef83e170408a62dd7d97'
# channel = 'C1615DQK1'
# ts = '1488270989.000004'
# response = 'hello world'
# slack_client = SlackClient(token)
# slack_client.api_call("chat.postMessage", channel=channel,text=response, as_user=True)

# print '-----'
# slack_client.api_call("chat.postMessage", channel=channel,
#                           text=response, as_user=True)

# https://www.sdk.cn/news/4180
# pip install slackclient==1.0.0

#https://slack.com/api/chat.postMessage?token=xoxp-40029613668-40029615492-147293486659-680e593def36ef83e170408a62dd7d97&channel=C1615DQK1&text=test&pretty=1
# {
#     "ok": true,
#     "channel": "C1615DQK1",
#     "ts": "1488270989.000004",
#     "message": {
#         "text": "test",
#         "username": "Slack API Tester",
#         "bot_id": "B4BAMVCKU",
#         "type": "message",
#         "subtype": "bot_message",
#         "ts": "1488270989.000004"
#     }
# }