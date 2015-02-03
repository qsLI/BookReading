#coding=utf-8
import os,time
import random
from splinter import Browser

#随机评论
commentsList = [u"不错的资源！！！！！！！",u"谢谢楼主分享！",u"还不错，谢谢",u"还没看,先下载",u"感谢分享，nice",u"很好的东西，非常不错",u"用这个很方便!!",u"这个很不错！"]
print random.choice(commentsList)
browser = Browser('chrome')
# Visit URL
url = "http://passport.csdn.net/account/login"
browser.visit(url)
# browser.fill('f', 'splinter - python acceptance testing for web applications')
# Find and click the 'search' button
btnEmail = browser.find_by_id('username')
btnPasswd = browser.find_by_id('password')
btnEmail.fill('')#用户名
btnPasswd.fill('')#密码
#print dir(browser)
# Interact with elements
btnSubmit = browser.find_by_value("登 录")
btnSubmit.click()#登录
# button.click()
#time.sleep(10)
time.sleep(6)
browser.visit("http://download.csdn.net/my/downloads")
while browser.is_element_not_present_by_css(".pageliststy"):
    time.sleep(0.1)
urls = [ url['href'] for url in  browser.find_link_by_text("立即评价，通过可返分")]
#总页面个数
pages = int(browser.find_by_css(".pageliststy")[-1]['href'].split('/')[-1])
for index in range(2,pages+1):
    browser.visit("http://download.csdn.net/my/downloads/%d"%index)
    urls = urls + [ url['href'] for url in  browser.find_link_by_text("立即评价，通过可返分")]
    time.sleep(1)
print urls
for url in urls:
    print url
    browser.visit(url)
    while browser.is_element_not_present_by_value("5"):
        time.sleep(0.1)
    startControl = browser.find_by_css(".star-rating")[-1]# -1 for 5 stars  -2 for 4 stars  1 for one star  also may  random
    textControl = browser.find_by_id("cc_body")[0]#评论框
    btnComment = browser.find_by_value("发表评论")[0]#提交框
    #print dir(startControl)
    print "loaded"
    startControl.mouse_over()#鼠标到评分栏
    startControl.click()    #鼠标点击
    textControl.fill(random.choice(commentsList))#填写评论
    btnComment.click()#评论提交
    alert = browser.get_alert()#处理 js的alert确认
    alert.accept()#确定
    time.sleep(60)#评论间隔要有一分钟
print "Hello Kitty"