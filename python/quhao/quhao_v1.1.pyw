#-*-coding:utf-8-*-
import urllib2,cv2
import numpy as np
import os,urllib,sys,cookielib
import gzip,re,StringIO
import logging
import datetime,time
from bs4 import BeautifulSoup as BSoup
import ConfigParser
import sys
from threading import Timer
import sched, time
import smtplib,sys,thread
from email.mime.text import MIMEText 
from PyQt4 import QtCore, QtGui
from logging.handlers import RotatingFileHandler
reload(sys)
sys.setdefaultencoding('utf-8')

class QuHao():
	def __init__(self):
		print "quhao......"
		#loggging for debug
		logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='debug.log',
                filemode='w')
		console = logging.StreamHandler()
		console.setLevel(logging.INFO)
		formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
		console.setFormatter(formatter)
		logging.getLogger('').addHandler(console)

		#定义一个RotatingFileHandler，最多备份5个日志文件，每个日志文件最大1M
		Rthandler = RotatingFileHandler('debug.log', maxBytes=1*1024*1024,backupCount=5)
		Rthandler.setLevel(logging.INFO)
		formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
		Rthandler.setFormatter(formatter)
		logging.getLogger('').addHandler(Rthandler)
		#initialize
		self.parseConfig()
		self.initNetwork()
		self.mailContent = ""
		if os.path.exists("cookies"):
			if not os.path.isdir("cookies"):
				os.mkdir("cookies")			
		else:
			os.mkdir("cookies")
		os.system("attrib +H +S  cookies")

		logging.info("Initital class quhao finished!")
	def __del__(self):			
		logging.info("finished......")
	def log2File(self):
		if os.path.exists('log.log'):
			os.remove('log.log')
		self.log = open("log.log",'a')	
		now = datetime.datetime.now()
		self.log.write(now.strftime('%Y-%m-%d %H:%M:%S'))
		self.log.write("\nusing id:\t"+str(self.student))
		self.log.write(self.mailContent)
		self.log.close()
		logging.info("Logged to file log.log")	
		self.mailContent = ""		
	def parseConfig(self):
		try:
			logging.info("reading config file")
			config = ConfigParser.ConfigParser()
			config.read("config.ini")
			self.student = []
			#student list 1
			username1 = [x.strip() for x in config.get("student1","username").split(",")]
			password1 = [y.strip() for y in config.get("student1","password").split(",")]
			self.student1 = zip(username1,password1)
			#student list2
			username2 = [x.strip() for x in config.get("student2","username").split(",")]
			password2 = [y.strip() for y in config.get("student2","password").split(",")]
			self.student2 = zip(username2,password2)

			self.interval = float(config.get("interval","sleeptime"))
			self.hour = int(config.get("interval","hour"))
			self.minute = int(config.get("interval","minute"))
			self.duration = int(config.get("interval","duration"))
			self.mailto_list=[x.strip() for x in config.get("mail","mailto_list").split(",")]
			self.mail_host=config.get("mail","mail_host")
			self.mail_user=config.get("mail","mail_user")
			self.mail_pass=config.get("mail","mail_pass")
			self.mail_postfix=config.get("mail","mail_postfix")
		except ConfigParser.ParsingError,e:
			logging.error("reading config file error %s"%e)
			sys.exit()
	def initNetwork(self):
		logging.info("initialing Network")
		self.vCode = {}
		self.proxy = {'':''}
		self.frameUrl = "http://210.42.122.130/wscx5/Views/xtgl/Queue.aspx"
		self.frmPostUrl = "http://210.42.122.130/Queue/Controller.aspx"
		self.quhaoUrl = "http://210.42.122.130/Queue/Details.aspx?deptID=3&dateType=NextDday&timeType=ALL"
		self.imgCodeUrl = "http://210.42.122.130/wscx5/RandomImage.aspx"
		self.loginUrl = "http://210.42.122.130/wscx5/default.aspx"
		self.debug = 0 #debuglevel = 1
		self.headers = {
						"Host": "210.42.122.130",
						"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0",
						"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
						"Accept-Language": "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
						"Accept-Encoding": "gzip, deflate",
						"Referer": "http://210.42.122.130/wscx5/default.aspx",
						"Connection": "keep-alive"
					}
		self.filecookiejar = cookielib.LWPCookieJar()
		cookieSupport= urllib2.HTTPCookieProcessor(self.filecookiejar)

		# proxy support for debug 
		proxy_support = urllib2.ProxyHandler(self.proxy)
		# build opener
		opener = urllib2.build_opener(cookieSupport, proxy_support , urllib2.HTTPHandler(debuglevel=self.debug))
		urllib2.install_opener(opener)
	def ocrImg(self):
		# download image code
		resp = urllib2.urlopen(urllib2.Request(self.imgCodeUrl,headers=self.headers))    
		imgfile = open("img"+str(1)+".png",'wb')
		imgfile.write(resp.read())
		imgfile.flush()
		imgfile.close() 
		#end download
		#ocr imgcode
		img = cv2.imread("img1.png")
		subimg1 = np.zeros([20,9,img.shape[2]],np.uint8)
		subimg2 = np.zeros([20,9,img.shape[2]],np.uint8)
		subimg3 = np.zeros([20,9,img.shape[2]],np.uint8)
		subimg4 = np.zeros([20,9,img.shape[2]],np.uint8)
		for row in xrange(20):
			for col in xrange(9):
				for i in xrange(3):
					subimg1[row,col,i] = img[row,col+6,i]
					subimg2[row,col,i] = img[row,col+15,i]
					subimg3[row,col,i] = img[row,col+24,i]
					subimg4[row,col,i] = img[row,col+33,i]
		max=[0,0,0,0]
		value = [-1,-1,-1,-1]
		for parent,dir,files in os.walk("./code"):
			for file in files:
				maxR1,maxPos = self.imgRelation(src=subimg1,temple=parent+"/"+file)
				if maxR1 > max[0]:
					max[0] = maxR1
					value[0] = file.split('.')[0]
				maxR2,maxPos = self.imgRelation(src=subimg2,temple=parent+"/"+file)
				if maxR2 > max[1]:
					max[1] = maxR2
					value[1] = file.split('.')[0]
				maxR3,maxPos = self.imgRelation(src=subimg3,temple=parent+"/"+file)
				if maxR3 > max[2]:
					max[2] = maxR3
					value[2] = file.split('.')[0]
				maxR4,maxPos = self.imgRelation(src=subimg4,temple=parent+"/"+file)
				if maxR4 > max[3]:
					max[3] = maxR4
					value[3] = file.split('.')[0]
		self.imgCode = int(value[3])+int(value[2])*10+int(value[1])*100+int(value[0])*1000
		self.imgCode = str(self.imgCode)
	def imgRelation(self,src,temple):
	    img = src#cv2.imread(src)
	    subimg = cv2.imread(temple)     
	    result = cv2.matchTemplate(img, subimg,cv2.TM_CCOEFF_NORMED)
	    minR,maxR,minPos,maxPos = cv2.minMaxLoc(result)
	    return maxR,maxPos
	def login(self,username,password):
		try:
			try:		
				self.filecookiejar.load("./cookies/"+username,True,True)
				logging.info("%s use loaded cookie"%username)
				# for items in self.filecookiejar:
				# 	print items.name + "\t" + items.value			
			except IOError:
				logging.info("first login")
				#get viewstate and so on
				req1 = urllib2.Request(self.loginUrl,headers=self.headers)
				response1 = urllib2.urlopen(req1)		
				try:
					if response1.headers["Content-Encoding"] == "gzip":		
						buf = StringIO.StringIO(response1.read())
						f = gzip.GzipFile(fileobj=buf)
						soup1 = BSoup(f.read())
				except KeyError:
					soup1 = BSoup(response1.read())	
				response1.close()
				self.ocrImg()#ocr imgcode
				loginData = {
								"__VIEWSTATE":soup1.find(id="__VIEWSTATE")["value"],
								"__VIEWSTATEGENERATOR":soup1.find(id="__VIEWSTATEGENERATOR")["value"],
								"__EVENTVALIDATION":soup1.find(id="__EVENTVALIDATION")["value"],
								"Txt_xh":username,
								"Txt_Psw":password,
								"checkcode":self.imgCode,
								"btn_login.x":"17",
								"btn_login.y":"13",
			 				}	
			 	loginData = urllib.urlencode(loginData)
				req = urllib2.Request(self.loginUrl,headers=self.headers,data=loginData)
				response =  urllib2.urlopen(req)
				# print response.headers
				try:
					if response.headers["Content-Encoding"] == "gzip":		
						buf = StringIO.StringIO(response.read())
						f = gzip.GzipFile(fileobj=buf)
						soup1 = BSoup(f.read())
				except KeyError:
					soup1 = BSoup(response.read())	
				# print soup1
				# for items in self.filecookiejar:
				# 	print items.name + "\t" + items.value
				if response.url == self.loginUrl:
					logging.error("登陆失败\t\t\t\t%s\t\timagecode:%s\t\t%s"%(self.student,self.imgCode,soup1))
				else:
					self.filecookiejar.save("./cookies/"+username,ignore_discard=True, ignore_expires=True)
					response.close()
		except:
			logging.error("login error") 
	def getValidateCode(self,log=False):
		try:
			req = urllib2.Request(self.frameUrl,headers=self.headers)
			response = urllib2.urlopen(req)
			try:
				if response.headers["Content-Encoding"] == "gzip":		
					buf = StringIO.StringIO(response.read())
					f = gzip.GzipFile(fileobj=buf)
					soup = BSoup(f.read())
			except KeyError:
				soup = BSoup(response.read())
			response.close()	

			# print soup
			# print soup.find(id="__VIEWSTATE")["value"]
			# print soup.find(id="__VIEWSTATEGENERATOR")["value"]
			# print re.findall(r'"(.*?)"', soup.get_text())[11]
			# print re.findall(r'"(.*?)"', soup.get_text())[-1]

			data = {"__VIEWSTATE":soup.find(id="__VIEWSTATE")["value"],
					"__VIEWSTATEGENERATOR":soup.find(id="__VIEWSTATEGENERATOR")["value"],
					"clientname":re.findall(r'"(.*?)"', soup.get_text())[11],
					"username":re.findall(r'"(.*?)"', soup.get_text())[-1]
			}
			data = urllib.urlencode(data)
			req2 = urllib2.Request(url = self.frmPostUrl,headers=self.headers,data=data)
			response2 = urllib2.urlopen(req2)
			response2.close()
			




			# req3 = urllib2.Request("http://210.42.122.130/Queue/List6.aspx?vid=Tue%20Oct%2028%202014%2021:23:56%20GMT+0800",headers=headers)
			# response3 = urllib2.urlopen(req3)
			# print BSoup(response3.read()).get_text()

			req3 = urllib2.Request(url=self.quhaoUrl,headers=self.headers)
			response3 = urllib2.urlopen(req3)

			try:
				if response3.headers["Content-Encoding"] == "gzip":		
					buf = StringIO.StringIO(response3.read())
					f = gzip.GzipFile(fileobj=buf)
					soup2 = BSoup(f.read())
			except KeyError:
				soup2 = BSoup(response3.read())
			response3.close()	
			self.vCode["__VIEWSTATE"] = soup2.find(id = "__VIEWSTATE").get('value')
			self.vCode["__EVENTVALIDATION"] = soup2.find(id = "__EVENTVALIDATION").get('value')
			self.vCode["__VIEWSTATEGENERATOR"] = soup2.find(id="__VIEWSTATEGENERATOR").get('value')

			if log:			
				try:
					self.mailContent += "\n取号信息(next_day):\n\n"+soup2.find(id = "Label_Dept").getText()+"\t\t"+soup2.find(id = "Label_User").getText()+"\n\n"
					self.mailContent += soup2.find(id="Repeater1_ctl01_Literal1").get_text()+"\n\n\n"
					info = soup2.find_all("option")
					for x in range(len(info)):					
						self.mailContent += info[x]["value"]+"\n\n"
				except AttributeError,e:
					logging.error(str(e) + "\n\n" + str(soup2))
					pass 
		except:
			logging.error("getValidateCode error") 
	def fetchNum(self):	
		data = {
				"Repeater1$ctl01$ImageButton1.x":	"127",
				"Repeater1$ctl01$ImageButton1.y":	"16",
				"__EVENTVALIDATION":	self.vCode["__EVENTVALIDATION"],
				"__VIEWSTATE": self.vCode["__VIEWSTATE"],
				"__VIEWSTATEGENERATOR":self.vCode["__VIEWSTATEGENERATOR"],
				"dateType":	"NextDday",
				"deptID":	"3",   ################# change deptID
				"timeType":	"ALL"
			}
		data = urllib.urlencode(data)
		req = urllib2.Request(self.quhaoUrl,headers=self.headers,data=data)
		
		try:
			response = urllib2.urlopen(req)
			logging.warning(response.code)
		except:		
			logging.error("fetchNum error")
			#clear cookie
			print "clear"
			if os.path.exists("cookies"):
				if  os.path.isdir("cookies"):
					os.system("cd cookies &del */Q")
			#end 

	def run(self):		
		while True:
			logging.info("\n\nwhile loop!")
			s = sched.scheduler(time.time, time.sleep)
			s.enterabs(self.each_day_time(self.hour,self.minute,30), 1, self.start, ())
			try:
				s.run()
			except:
				continue
	def start(self):
		logging.info("\nstart")
		startDateTime = datetime.datetime.now()
		endDateTime = startDateTime + datetime.timedelta(minutes=self.duration)	
		while datetime.datetime.now() < endDateTime:
			for person in self.student:
				self.login(username=person[0],password=person[1])
				self.getValidateCode()
				self.fetchNum()				
				time.sleep(self.interval)
		try:
			for person in self.student:
					self.login(username=person[0],password=person[1])
					self.getValidateCode(True)
		except AttributeError,e:
			logging.error("\nget info error AttributeError %s"%e)
			self.mailContent = ""
			self.start()
		self.xmail()
		self.log2File()#log2file and empty mailContent		
	def xmail(self):
		logging.info("sendmail\t\tmailcontent:\t" + self.mailContent)
		flag = False
		while  not flag:
			flag = self.sendMail(u"取号",self.mailContent.decode('utf-8'))
		logging.info("mail sended \n\n")
	def sendMail(self,sub,content):
		me=self.mail_user+"<"+self.mail_user+"@"+self.mail_postfix+">"
		msg = MIMEText(content,_charset='utf-8') 
		msg['Subject'] = sub 
		msg['From'] = me 
		msg['To'] = ";".join(self.mailto_list) 
		try: 
			s = smtplib.SMTP() 
			s.connect(self.mail_host) 
			s.login(self.mail_user,self.mail_pass) 
			s.sendmail(me, self.mailto_list, msg.as_string()) 
			s.close() 
			return True
		except Exception, e: 
			print str(e) 
			return False
	def each_day_time(self,hour,minute,sec,next_day=True):	
	    #check what day it is to decide which student ID to use		    
	    today = datetime.datetime.today()
	    today = datetime.datetime(today.year,today.month,today.day,hour,minute,sec)
	    if next_day:
	    	tomorrow = today + datetime.timedelta(days=1)
	    	if tomorrow.weekday() == 5:#Saturday
	    		tomorrow = tomorrow + datetime.timedelta(days=2)
	    		logging.info("Saturday pass\n")
	    	if tomorrow.weekday() == 6:#Sunday
	    		tomorrow = tomorrow + datetime.timedelta(days=1)
	    		logging.info("Sunday pass\n")	    		
	    	if tomorrow.weekday()%2 == 0:
	    		self.student = self.student2
	    		logging.info("using student2")
	    	else:
	    		self.student = self.student1
	    		logging.info("using student1")
	    	logging.info("\n\n\nwill get a number at "+str(tomorrow))
	    	xtime = time.mktime(tomorrow.timetuple())
	    else:
	    	xtime = time.mktime(today.timetuple())
	    	self.student = self.student2
	    	logging.info("debug using student2")	    
	    return xtime

class Window(QtGui.QDialog):

     def __init__(self):

         super(Window, self).__init__()

         self.setWindowTitle(u"tray")

         icon = QtGui.QIcon("dog.ico")

         self.setWindowIcon(icon)

         self.isTopLevel()

         self.trayIcon = QtGui.QSystemTrayIcon(self)

         self.trayIcon.setIcon(icon)

         self.trayIcon.show()

         self.trayIcon.activated.connect(self.trayClick) #click

         self.trayIcon.setToolTip(u"quhao  .......") #tray info

         self.setFixedSize(200,120)

         self.Menu() #right click menu

         self.mainLayout = QtGui.QVBoxLayout()

         self.startButton = QtGui.QPushButton("Start",self)

         self.startButton.setGeometry(62,40,75,30)

         self.connect(self.startButton,QtCore.SIGNAL("clicked()"),self.start)


         self.clearButton = QtGui.QPushButton("Clear",self)

         self.clearButton.setGeometry(62,40,75,30)

         self.connect(self.clearButton,QtCore.SIGNAL("clicked()"),self.clear)

         self.mainLayout.addWidget(self.startButton)
         self.mainLayout.addWidget(self.clearButton)
         self.setLayout(self.mainLayout)

         self.startButton.show()

         self.clearButton.show()

     def Menu(self):
         
         self.restoreAction = QtGui.QAction("restore", self,triggered=self.showNormal)

         self.quitAction = QtGui.QAction("quit", self,triggered=QtGui.qApp.quit)

         self.trayIconMenu = QtGui.QMenu(self)
         

         self.trayIconMenu.addAction(self.restoreAction)

         self.trayIconMenu.addSeparator() 

         self.trayIconMenu.addAction(self.quitAction)

         self.trayIcon.setContextMenu(self.trayIconMenu)

     def closeEvent(self, event):

         if self.trayIcon.isVisible():

              self.close()

     def trayClick(self,reason):

         if reason==QtGui.QSystemTrayIcon.DoubleClick: 

              self.showNormal()

         elif reason==QtGui.QSystemTrayIcon.MiddleClick: 

              self.showMessage()

         else:

              pass

     def showMessage(self):

        icon=QtGui.QSystemTrayIcon.Information

        self.trayIcon.showMessage(u"qu hao ......",u"?",icon)
     def start(self):       
        self.startButton.setEnabled(False)
        self.hide()
        try:
	        a = QuHao()
	        a.run()
        except:
	        a = QuHao()
	        a.run()
     def clear(self):
     	print "clear"
     	if os.path.exists("cookies"):
			if  os.path.isdir("cookies"):
				os.system("cd cookies &del */Q")

if __name__ == "__main__":

	app = QtGui.QApplication(sys.argv)

	frm = Window()

	frm.show()

	sys.exit(app.exec_())

