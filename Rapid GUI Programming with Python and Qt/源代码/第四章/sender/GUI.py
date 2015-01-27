# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sender.ui'
#
# Created: Tue Jan 27 13:33:01 2015
#      by: PyQt4 UI code generator 4.11.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(612, 86)
        self.horizontalLayoutWidget = QtGui.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 611, 81))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.btnOne = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.btnOne.setMinimumSize(QtCore.QSize(25, 50))
        self.btnOne.setObjectName(_fromUtf8("btnOne"))
        self.horizontalLayout.addWidget(self.btnOne)
        self.btnTwo = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.btnTwo.setMinimumSize(QtCore.QSize(25, 50))
        self.btnTwo.setObjectName(_fromUtf8("btnTwo"))
        self.horizontalLayout.addWidget(self.btnTwo)
        self.btnThree = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.btnThree.setMinimumSize(QtCore.QSize(25, 50))
        self.btnThree.setObjectName(_fromUtf8("btnThree"))
        self.horizontalLayout.addWidget(self.btnThree)
        self.labelInfo = QtGui.QLabel(self.horizontalLayoutWidget)
        self.labelInfo.setObjectName(_fromUtf8("labelInfo"))
        self.horizontalLayout.addWidget(self.labelInfo)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.btnOne.setText(_translate("Form", "按钮一", None))
        self.btnTwo.setText(_translate("Form", "按钮二", None))
        self.btnThree.setText(_translate("Form", "按钮三", None))
        self.labelInfo.setText(_translate("Form", "TextLabel", None))

