#coding:utf-8
from bs4 import BeautifulSoup as bs
import mechanize

br = mechanize.Browser()
#to behave more like a browser
br.set_debug_http(False)
br.set_handle_robots(False)
#br.set_proxies({"http":"127.0.0.1:8080"})
br.set_handle_equiv(True)
br.set_handle_referer(True)
br.set_handle_gzip(True)
br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'),("Referer","http://www.baidu.com")]

#open page
resp = br.open("http://renren.com/")
forms = [ form for form in  br.forms()]
loginForm = forms[0]
print loginForm
loginForm['email'] = '1063891223@qq.com'
loginForm['password'] = '741015616'
res = loginForm.click()
content = mechanize.urlopen(res).read()
print content

#soup = bs(resp.read())
#print soup.prettify().encode("utf-8") #ecoding
#print soup.

print "Hello Kitty"