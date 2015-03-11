# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'proxy.ui'
#
# Created: Sat Jan 24 22:22:26 2015
#      by: PyQt4 UI code generator 4.11.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import sys
import struct,random
import _winreg
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
	def setupUi(self, Form):
		Form.setObjectName(_fromUtf8("切换代理"))
		Form.resize(404, 197)
		self.btnProxy = QtGui.QPushButton(Form)
		self.btnProxy.setGeometry(QtCore.QRect(70, 60, 101, 81))
		self.btnProxy.setObjectName(_fromUtf8("proxy"))
		self.btnReset = QtGui.QPushButton(Form)
		self.btnReset.setGeometry(QtCore.QRect(210, 60, 101, 81))
		self.btnReset.setObjectName(_fromUtf8("reset"))

		self.retranslateUi(Form)
		QtCore.QMetaObject.connectSlotsByName(Form)

	def retranslateUi(self, Form):
		Form.setWindowTitle(_translate("Form", "切换代理", None))
		self.btnProxy.setText(_translate("Form", "changeProxy", None))
		self.btnReset.setText(_translate("Form", "reset", None))
class myDialog(QtGui.QDialog):
	def __init__(self):
		QtGui.QDialog.__init__(self)
		self.ui = Ui_Form()
		self.ui.setupUi(self)
		self.ui.btnProxy.clicked.connect(self.changeProxy)
		self.ui.btnReset.clicked.connect(self.Reset)
		self.proxyers = []
		for line in open("proxy.txt"):    		
			ip,port = line.strip().split("\t")
			self.proxyers.append(ip+":"+port) 
	def changeProxy(self):  
		print "change"
		proxy = random.choice(self.proxyers)
		print proxy
		root = _winreg.HKEY_CURRENT_USER    
		proxy_path = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
		kv_Enable = [
			(proxy_path, "ProxyEnable", 1, _winreg.REG_DWORD),
			(proxy_path, "ProxyServer", proxy, _winreg.REG_SZ),
		]                
		#set proxyer
		for keypath, value_name, value, value_type in kv_Enable:
			hKey = _winreg.CreateKey (root, keypath)
			_winreg.SetValueEx (hKey, value_name, 0, value_type, value) 
	def Reset(self):
		print "reset"
		root = _winreg.HKEY_CURRENT_USER    
		proxy_path = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
		kv_Disable = [
          (proxy_path, "ProxyEnable", 0, _winreg.REG_DWORD),
          (proxy_path, "ProxyServer", "127.0.0.1:8080", _winreg.REG_SZ),
        ]              
		#set proxyer
		for keypath, value_name, value, value_type in kv_Disable:
			hKey = _winreg.CreateKey (root, keypath)
			_winreg.SetValueEx (hKey, value_name, 0, value_type, value) 
if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	window = myDialog()
	window.show()
	sys.exit(app.exec_())
