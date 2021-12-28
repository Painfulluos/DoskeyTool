from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

import os
import winreg


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(543, 249)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.SaveButton = QtWidgets.QPushButton(self.centralwidget)
        self.SaveButton.setGeometry(QtCore.QRect(410, 200, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.SaveButton.setFont(font)
        self.SaveButton.setObjectName("SaveButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 271, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(10, 60, 511, 31))
        self.textEdit.setAutoFillBackground(True)
        self.textEdit.setObjectName("textEdit")
        self.checkBoxRegistry = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBoxRegistry.setGeometry(QtCore.QRect(20, 120, 151, 17))
        self.checkBoxRegistry.setObjectName("checkBoxRegistry")
        self.checkBoxRegistry.setFixedWidth(300)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.add_functions()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "DoskeyTool"))
        self.SaveButton.setText(_translate("MainWindow", "Write to a file"))
        self.label.setText(_translate("MainWindow", "Enter the command to create an alias:"))
        self.checkBoxRegistry.setText(_translate("MainWindow", "Write the path to the register for autorun doskey"))

    def add_functions(self):
        self.SaveButton.clicked.connect(lambda: self.buttonActions(self.checkBoxRegistry.checkState()))

    def buttonActions(self,isSaveRegistry): # 
        message = QMessageBox()
        try:
            self.checkFile()
            self.add_command()
            if isSaveRegistry == 2:
                self.setAutorun()
                message.setText("The command was successfully added. The path to the file doskey.bat was recorded in the registry.")
            else:
                message.setText("The command was successfully added.")
            message.setWindowTitle("Success!")
            
            message.setIcon(QMessageBox.Information)
        except:
            message.setWindowTitle("Error!")
            message.setText("An error occurred while adding the command.")
            message.setIcon(QMessageBox.Critical)
        finally:

            message.setStandardButtons(QMessageBox.Reset|QMessageBox.Ok)
            message.buttonClicked.connect(self.message_action)
            message.exec_()

    def message_action(self,btn):
        if btn.text() == "Reset":
            self.textEdit.setText("")

    def checkFile(self):
        isFileExist = os.path.exists("C:\\doskey\\doskey.bat")
        if not isFileExist:
            if not os.path.exists("C:\\doskey\\"):
                os.mkdir("C:\\doskey\\")
            with open("C:\\doskey\\doskey.bat", "w") as file:
                file.write('@echo off\n\n')

    def add_command(self):
        text = self.textEdit.toPlainText()
        with open("C:\\doskey\\doskey.bat", "a+") as file:
            file.write("doskey "+text+"\n")

    def setAutorun(self):
        keyVal = r'Software\\Microsoft\\Command Processor\\'
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, keyVal, 0, winreg.KEY_ALL_ACCESS)
        except:
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, keyVal)
        winreg.SetValueEx(key,"AutoRun", 0, winreg.REG_SZ, "C:\\doskey\\doskey.bat")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
