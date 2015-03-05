# -*- coding: utf-8 -*-
from xmlrpclib import ServerProxy
import sys
if __name__ == '__main__':
	s = ServerProxy("http://192.168.1.189:8080",verbose=0,use_datetime=1,allow_none=True)
	#print s.add(3,4)
	reload(sys)   
	sys.setdefaultencoding('utf8')
	print sys.getdefaultencoding()
	print s.writeMessage(u'你好，世界')
	print s.writeMessage(u'我想和你谈谈')
	print s.writeMessage(u'让我们创造更好的世界')