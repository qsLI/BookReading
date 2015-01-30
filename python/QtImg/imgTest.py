#coding=utf-8
from imgUi import Ui_MainWindow
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
class xMainWindow(QMainWindow):
	def __init__(self):
		super(QMainWindow, self).__init__(parent=None)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.img = QImage("C:\\Users\\Public\\Pictures\\Sample Pictures\\1.jpg")
		self.ui.imgLabel.setPixmap(QPixmap.fromImage(self.img))
app = QApplication(sys.argv)
window = xMainWindow()
window.show()
app.exec_()