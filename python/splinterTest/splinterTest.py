#coding=utf-8
import os,time
from splinter import Browser
try:
	browser = Browser('chrome')
	# Visit URL
	url = "http://passport.csdn.net/account/login"
	browser.visit(url)
	# browser.fill('f', 'splinter - python acceptance testing for web applications')
	# Find and click the 'search' button
	btnEmail = browser.find_by_id('username')
	btnPasswd = browser.find_by_id('password')
	btnEmail.fill('1063891223@qq.com')
	btnPasswd.fill('741015616')
	#print dir(browser)
	# Interact with elements
	btnSubmit = browser.find_by_value("登 录")
	btnSubmit.click()
	# button.click()
	#time.sleep(10)
	time.sleep(30)
	browser.visit("http://download.csdn.net/my/downloads")
	print browser.find_link_by_partial_href("download.csdn.net/detail")
except:
	pass
	print "Hello Kitty"
print "Hello Kitty"