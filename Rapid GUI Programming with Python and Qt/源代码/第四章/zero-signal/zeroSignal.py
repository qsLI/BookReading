#coding=utf-8
from PyQt4.QtCore import *
from PyQt4.QtGui import *
class ZeroSpinBox(QSpinBox):
	zeros = 0
	def __init__(self,parent=None):
		super(QSpinBox,self).__init__(parent)
		self.connect(self,SIGNAL("valueChanged(int)"),self.checkZero)
	def checkZero(self):
		if self.value() == 0:
			self.zeros += 1
			self.emit(SIGNAL("atzero"),self.zeros)
	def annouce(self):
		print "ZeroSpinBox has been at zero %d times"%zeros
		
zerospinbox = ZeroSpinBox()
zerospinbox.setValue(1)
zerospinbox.setValue(0)
raw_input("Hello Kitty")
print "Hello Kitty!"