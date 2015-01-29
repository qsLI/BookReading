from buddyUi import Ui_Dialog
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
class xDialog(QDialog):
	def __init__(self,parent=None):
		super(QDialog,self).__init__(parent)
		self.ui = Ui_Dialog()
		self.ui.setupUi(self)
app = QApplication(sys.argv)
dialog = xDialog()
dialog.show()
app.exec_()
print "Hello Kitty!"
