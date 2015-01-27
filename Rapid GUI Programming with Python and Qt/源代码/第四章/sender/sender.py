#coding=utf-8
from  GUI import Ui_Form
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui  import *
class xDialog(QDialog):
    def __init__(self,parent=None):
        super(xDialog,self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.btnOne.clicked.connect(self.anyBtn)
        self.ui.btnTwo.clicked.connect(self.anyBtn)
        self.ui.btnThree.clicked.connect(self.anyBtn)
    def anyBtn(self):
        button = self.sender()
        if button is None or not isinstance(button,QPushButton):
            return
        self.ui.labelInfo.setText("You clicked button %s"%button.text())
app = QApplication(sys.argv)
dialog = xDialog()
dialog.show()
app.exec_()
        