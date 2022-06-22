# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwidget.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import QtCore, QtGui, QtWidgets

import spider

class Ui_MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def setupUi(self, mainwidget):
        mainwidget.setObjectName("mainwidget")
        mainwidget.resize(343, 427)
        self.gridLayout = QtWidgets.QGridLayout(mainwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.textEditInfo = QtWidgets.QTextEdit(mainwidget)
        self.textEditInfo.setObjectName("textEditInfo")
        self.gridLayout.addWidget(self.textEditInfo, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(mainwidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.txtWord = QtWidgets.QLineEdit(mainwidget)
        self.txtWord.setObjectName("txtWord")
        self.horizontalLayout.addWidget(self.txtWord)
        self.btnConfirm = QtWidgets.QPushButton(mainwidget)
        self.btnConfirm.setObjectName("btnConfirm")
        self.horizontalLayout.addWidget(self.btnConfirm)
        self.btnCancel = QtWidgets.QPushButton(mainwidget)
        self.btnCancel.setObjectName("btnCancel")
        self.horizontalLayout.addWidget(self.btnCancel)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(mainwidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(True)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 1, 0, 1, 1)

        self.retranslateUi(mainwidget)
        QtCore.QMetaObject.connectSlotsByName(mainwidget)

        self.initData()

    def retranslateUi(self, mainwidget):
        _translate = QtCore.QCoreApplication.translate
        mainwidget.setWindowTitle(_translate("mainwidget", "wallhaven爬虫"))
        self.label.setText(_translate("mainwidget", "搜索关键字"))
        self.btnConfirm.setText(_translate("mainwidget", "开始"))
        self.btnCancel.setText(_translate("mainwidget", "停止"))

    def addText(self, str):
        self.textEditInfo.append(str)

    def updateProgress(self, val):
        self.progressBar.setValue(int(val))

    def clearText(self):
        self.textEditInfo.clear()

    def initData(self):
        self.btnConfirm.clicked.connect(self.startSpider)
        self.btnCancel.clicked.connect(self.stopSpider)
        self.textEditInfo.textChanged.connect(self.scrollToEnd)
        self.textEditInfo.setReadOnly(True)
        self.txtWord.setFocus()
        self.txtWord.editingFinished.connect(self.startSpider)
        self.btnCancel.setEnabled(False)

    def scrollToEnd(self):
        self.textEditInfo.moveCursor(QtGui.QTextCursor.MoveOperation.End)

    def startSpider(self):
        self.updateProgress(0)
        self.btnConfirm.setEnabled(False)
        self.btnCancel.setEnabled(True)
        word = self.txtWord.text()
        self.sp = spider.Spider()
        self.sp.set_message(self.addText)
        self.sp.set_progress(self.updateProgress)
        self.sp.set_finish(self.stopSpider)
        self.sp.set_word(word)
        self.sp.start()

    def stopSpider(self):
        self.sp.exit = True
        self.updateProgress(0)
        self.btnConfirm.setEnabled(True)
        self.btnCancel.setEnabled(False)
