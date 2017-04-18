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

    def initData(self):
        #default history length is 100
        self.loglength=1000
        self.loadsha1AndInfo()

    def loadsha1AndInfo(self):
        logsha1='git log --pretty=format:\"%H\" -' + str(self.loglength) + " ."
        output = os.popen(logsha1);
        self.sha1=[]
        for line in output:
            line=line.strip('\n')
            self.sha1.append(line)

        loginfo='git log --date=short --pretty=format:\"%ad || %s\" -' + str(self.loglength) + " ."
        output = os.popen(loginfo);
        self.info=[]
        for line in output:
            line=line.strip('\n')
            self.info.append(line)



    def gitLogShow(self, shaindex):
        if not shaindex:
            return

        self.textEdit.clear()
        #self.textEdit.setColor(QtCore.Qt.red)
        cursor = self.textEdit.textCursor()
        cursor.movePosition(QtGui.QTextCursor.Start)

        textFormat = QtGui.QTextCharFormat()
        redFormat = QtGui.QTextCharFormat()
        redFormat.setForeground(QtCore.Qt.red)
        greenFormat = QtGui.QTextCharFormat()
        greenFormat.setForeground(QtCore.Qt.darkGreen)
        blueFormat = QtGui.QTextCharFormat()
        blueFormat.setForeground(QtCore.Qt.blue)
        boldFormat = QtGui.QTextCharFormat()
        boldFormat.setForeground(QtCore.Qt.darkCyan)
        boldFormat.setFontWeight(QtGui.QFont.Bold)
        timeFormat = QtGui.QTextCharFormat()
        #timeFormat.setForeground(QtCore.Qt.darkCyan)
        timeFormat.setFontWeight(QtGui.QFont.Bold)
        infoFormat = QtGui.QTextCharFormat()
        infoFormat.setFontWeight(QtGui.QFont.Bold)

        #print the info
        gitshowinfo='git show -s ' + self.sha1[shaindex]
        output = os.popen(gitshowinfo);
        for line in output:
            line=line.strip('\n')

            cursor.insertText(line, infoFormat)
            cursor.insertBlock()

        #print the file
        gitshow='git show ' + self.sha1[shaindex] + " --pretty=format:\"\""
        output = os.popen(gitshow);
        for line in output:
            line=line.strip('\n')
            length = len(line)
            index = 0
            while index < length:
                if line[index] != ' ':
                    break
                index = index + 1

            if index == length:
                cursor.insertText(line, textFormat)
                cursor.insertBlock()
                continue

            if index < length - 2 and line[index] == '-' and line[index + 1]  == '-' and line[index + 2]  == '-':
                cursor.insertText(line, boldFormat)
            elif index < length - 2 and line[index] == '+' and line[index + 1]  == '+' and line[index + 2]  == '+':
                cursor.insertText(line, boldFormat)
            elif line[index]  == '-':
                cursor.insertText(line, greenFormat)
            elif line[index] == '+':
                cursor.insertText(line, redFormat)
            elif index < length - 1 and line[index] == '@' and line[index] == '@':
                cursor.insertText(line, blueFormat)
            elif line[index] == 'd':
                cursor.insertText(line, boldFormat)
            else:
                cursor.insertText(line, textFormat)
            cursor.insertBlock()




    def about(self):
        QtGui.QMessageBox.about(self, "My Git Gui",
                "This is a Simple git gui, just for myself requirement "
                "If you useing this tools and have any question, pls contract to zhenjun85@qq.com")

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

        dock = QtGui.QDockWidget("Git Log Info", self)
        self.paragraphsList = QtGui.QListWidget(dock)
        self.paragraphsList.addItems(self.info)
        dock.setWidget(self.paragraphsList)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock)

        self.paragraphsList.currentRowChanged.connect(self.gitLogShow)


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
