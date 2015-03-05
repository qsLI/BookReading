#coding:utf-8
from SimpleXMLRPCServer import SimpleXMLRPCServer
import sys
def add(x,y):
	return x + y
def hello(name):
	print "hello, " + name
def writeMessage(name):
	f = open("123.txt",'a')
	f.write(name+"\n")
	f.close()
	return "Your message is writen to 123.txt"
if __name__ == "__main__":
	reload(sys)   
	sys.setdefaultencoding('utf8')
	print sys.getdefaultencoding()
	s = SimpleXMLRPCServer(('192.168.1.189',8080),encoding="utf8",allow_none=True)
	s.register_function(add)
	s.register_function(hello)
	s.register_function(writeMessage)
	s.serve_forever()