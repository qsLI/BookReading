#coding=utf-8
import os,time
from splinter import Browser
from threading import *
# class closeWindow(Thread):
#     def __init__(self,browser):
#         super(closeWindow, self).__init__()
#         self.browser = browser
#     def run(self):
#         time.sleep(50)
#         print "time out kill window 0"
#         self.browser.windows[1].close()
#         self.stop()
#     def stop(self):
#         thread.exit_thread()

def login(browser,username="",passwd=""):
    """登录csdn"""

    url = "http://passport.csdn.net/account/login"
    browser.visit(url)
    # browser.fill('f', 'splinter - python acceptance testing for web applications')
    # Find and click the 'search' button
    btnEmail = browser.find_by_id('username')
    btnPasswd = browser.find_by_id('password')
    btnRemember = browser.find_by_name('rememberMe')


    btnEmail.fill(username)#用户名
    btnPasswd.fill(passwd)#密码
    btnRemember.check()#
    #print dir(browser)
    # Interact with elements
    btnSubmit = browser.find_by_value("登 录")
    btnSubmit.click()#登录
    time.sleep(8)
    # button.click()


def searchFree(browser):
    """用百度搜索免费的资源，返回资源的列表"""

    url = "http://www.baidu.com"
    browser.visit(url)
    btnKeyWord = browser.find_by_id('kw')[0]
    btnKeyWord.fill(u'"资源积分:0分"  联通下载 qt  site:download.csdn.net')#密码
    btnSubmit = browser.find_by_id("su")[0]
    btnSubmit.click()#提交搜素

    base = 0
    time.sleep(4)    
    for page in range(1,90):        
        # timerThread = closeWindow(browser)
        # timerThread.start()
        print base," base"
        print page," page"
        for x in range(base+1,base+11):
            print x
            time.sleep(6)
            urlTmp = browser.find_by_xpath('//*[@id="%d"]/h3/a'%x)[0]
            # time.sleep(10)
            urlTmp.click()
            browser.windows.current = browser.windows[1]
   
            try:
                print "try to clcik"
                # browser.execute_script('window.scrollTo(0, 400);')
                browser.execute_script('window.scrollTo(0, 200);')
                time.sleep(15)                     
                browser.execute_script('window.scrollTo(0, 400);')
                btnDownload = browser.find_by_css(r'#wrap > div.bd.clearfix > div.article > div.information.mb-bg.clearfix > div.info > a.btn.btn-primary.btn-lg.WCDMA.btndownload')[0]
                btnDownload.click()    
                time.sleep(10)      
                btnDownload = browser.find_by_css(r'#download_btn2')[0]
                btnDownload.click()    
                # btnDownload = browser.find_by_xpath(r'//*[@id="download_btn2"]')[0]
                # btnDownload.click()  
                time.sleep(10)
                btnConfirm = browser.find_by_xpath(r'//*[@id="user_score_btn"]')[0]
                btnConfirm.click()
                print "done"
            except:
                try:
                    btnConfirm = browser.find_by_xpath(r'//*[@id="user_score_btn"]')[0]
                    btnConfirm.click()
                    time.sleep(5)
                    print "done"
                except:
                    print "error"        
            browser.windows.current = browser.windows[0]
            browser.windows.current.close_others() #关闭窗口
            # timerThread.stop()
        base = base + 10    
        nextPage = browser.find_link_by_text(u"下一页>")[0] 
        nextPage.click()


if __name__ == "__main__":
    browser = Browser('chrome')
    login(browser)
    searchFree(browser)
    print "Hello Kitty"