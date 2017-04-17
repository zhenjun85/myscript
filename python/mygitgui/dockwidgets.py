#!/usr/bin/env python


# This is only needed for Python v2 but is harmless for Python v3.
import sip
sip.setapi('QString', 2)

import os
from PyQt4 import QtCore, QtGui

try:
    import dockwidgets_rc3
except ImportError:
    import dockwidgets_rc2


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.textEdit = QtGui.QTextEdit()
        self.setCentralWidget(self.textEdit)

        self.initData()
        self.createActions()
        self.createMenus()
        self.createDockWindows()

        self.setWindowTitle("My Git Gui")

        self.newLetter()

    def initData(self):
        #default history length is 100
        self.loglength=1000
        self.loadsha1AndInfo()

    def loadsha1AndInfo(self):
        logsha1='git log --pretty=format:\"%H\" -' + str(self.loglength)
        output = os.popen(logsha1);
        self.sha1=[]
        for line in output:
            line=line.strip('\n')
            self.sha1.append(line)

        loginfo='git log --pretty=format:\"%s\" -' + str(self.loglength)
        output = os.popen(loginfo);
        self.info=[]
        for line in output:
            line=line.strip('\n')
            self.info.append(line)



    def newLetter(self):
        self.textEdit.clear()

        cursor = self.textEdit.textCursor()
        cursor.movePosition(QtGui.QTextCursor.Start)
        topFrame = cursor.currentFrame()
        topFrameFormat = topFrame.frameFormat()
        topFrameFormat.setPadding(16)
        topFrame.setFrameFormat(topFrameFormat)

        textFormat = QtGui.QTextCharFormat()
        boldFormat = QtGui.QTextCharFormat()
        boldFormat.setFontWeight(QtGui.QFont.Bold)
        italicFormat = QtGui.QTextCharFormat()
        italicFormat.setFontItalic(True)

        tableFormat = QtGui.QTextTableFormat()
        tableFormat.setBorder(1)
        tableFormat.setCellPadding(16)
        tableFormat.setAlignment(QtCore.Qt.AlignRight)
        cursor.insertTable(1, 1, tableFormat)
        cursor.insertText("The Firm", boldFormat)
        cursor.insertBlock()
        cursor.insertText("321 City Street", textFormat)
        cursor.insertBlock()
        cursor.insertText("Industry Park")
        cursor.insertBlock()
        cursor.insertText("Some Country")
        cursor.setPosition(topFrame.lastPosition())
        cursor.insertText(QtCore.QDate.currentDate().toString("d MMMM yyyy"),
                textFormat)
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertText("Dear ", textFormat)
        cursor.insertText("NAME", italicFormat)
        cursor.insertText(",", textFormat)
        for i in range(3):
            cursor.insertBlock()
        cursor.insertText("Yours sincerely,", textFormat)
        for i in range(3):
            cursor.insertBlock()
        cursor.insertText("The Boss", textFormat)
        cursor.insertBlock()
        cursor.insertText("ADDRESS", italicFormat)

    def insertCustomer(self, customer):
        if not customer:
            return
        customerList = customer.split(', ')
        document = self.textEdit.document()
        cursor = document.find('NAME')
        if not cursor.isNull():
            cursor.beginEditBlock()
            cursor.insertText(customerList[0])
            oldcursor = cursor
            cursor = document.find('ADDRESS')
            if not cursor.isNull():
                for i in customerList[1:]:
                    cursor.insertBlock()
                    cursor.insertText(i)
                cursor.endEditBlock()
            else:
                oldcursor.endEditBlock()


    def gitLogShow(self, index):
        if not index:
            return
        document = self.textEdit.document()
        cursor = document.find("Yours sincerely,")
        if cursor.isNull():
            return
        cursor.beginEditBlock()
        cursor.movePosition(QtGui.QTextCursor.PreviousBlock,
                QtGui.QTextCursor.MoveAnchor, 2)
        cursor.insertBlock()
        cursor.insertText(self.sha1[index])
        cursor.insertBlock()
        cursor.endEditBlock()



    def about(self):
        QtGui.QMessageBox.about(self, "My Git Gui",
                "This is a Simple git gui, just for myself requirement")

    def createActions(self):

        self.quitAct = QtGui.QAction("&Quit", self, shortcut="Ctrl+Q",
                statusTip="Quit the application", triggered=self.close)

        self.aboutAct = QtGui.QAction("&About", self,
                statusTip="Show the application's About box",
                triggered=self.about)

        self.aboutQtAct = QtGui.QAction("About &Qt", self,
                statusTip="Show the Qt library's About box",
                triggered=QtGui.qApp.aboutQt)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.quitAct)

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)


    def createDockWindows(self):

        dock = QtGui.QDockWidget("Paragraphs", self)
        self.paragraphsList = QtGui.QListWidget(dock)
        self.paragraphsList.addItems(self.info)
        dock.setWidget(self.paragraphsList)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock)

        #self.paragraphsList.currentTextChanged.connect(self.addParagraph)
        self.paragraphsList.currentRowChanged.connect(self.gitLogShow)


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
