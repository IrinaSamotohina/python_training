import sys
import mysql.connector
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *

conn = mysql.connector.connect(host="localhost", user="user_1", password="password", database="plan")

class WindowUi(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(654, 330)
        self.calendarWidget = QtWidgets.QCalendarWidget(Dialog)
        self.calendarWidget.setGeometry(QtCore.QRect(1, 10, 311, 183))
        self.calendarWidget.setObjectName("calendarWidget")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(560, 300, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(240, 200, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.textEdit = QtWidgets.QTextEdit(Dialog)
        self.textEdit.setGeometry(QtCore.QRect(10, 230, 301, 61))
        self.textEdit.setObjectName("textEdit")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 300, 101, 16))
        self.label.setText("")
        self.label.setObjectName("label")
        self.timeEdit = QtWidgets.QTimeEdit(Dialog)
        self.timeEdit.setGeometry(QtCore.QRect(110, 200, 118, 22))
        self.timeEdit.setObjectName("timeEdit")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(50, 200, 61, 21))
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.listWidget = QtWidgets.QListWidget(Dialog)
        self.listWidget.setGeometry(QtCore.QRect(320, 10, 321, 161))
        self.listWidget.setObjectName("listWidget")
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(560, 180, 75, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setWindowTitle("TimeManager")
        self.pushButton.setText("Выход")
        self.pushButton_2.setText("Записать")
        self.pushButton_3.setText("Обновить")

class Ui(QtWidgets.QDialog, WindowUi):
    contents = []
    def __init__(self):
        super(Ui, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon("icon_time.png"))
        self.pushButton.clicked.connect(self.ButtonExit)
        self.pushButton_2.clicked.connect(self.SavePlan)
        self.pushButton_3.clicked.connect(self.showPlan)
        self.calendarWidget.clicked.connect(self.showPlan)
        self.listWidget.clicked.connect(self.EditPlan)

    def EditPlan(self):
        self.w2 = EditWin()
        self.contents.sort()
        c = self.calendarWidget.selectedDate()
        pln = self.contents[self.listWidget.currentRow()]
        b = str(pln[2])
        self.w2.getRex(b)
        self.w2.getRex_2(c)
        self.w2.pushButton.clicked.connect(self.updatePlan)
        self.w2.show()

    def updatePlan(self):
        self.contents.sort()
        data_old = self.calendarWidget.selectedDate().toString('dd.MM.yyyy')
        data_new = self.w2.dateEdit.dateTime().toString('dd.MM.yyyy')
        pln = self.contents[self.listWidget.currentRow()]
        old_time = pln[1]
        new_time = self.w2.timeEdit.time().toString('hh:mm')
        new_events = self.w2.textEdit.toPlainText()
        cursor = conn.cursor()
        paramms = (new_events, data_new, new_time, data_old, old_time)
        _SQL = """UPDATE user_plan SET events=%s, data=%s, time=%s WHERE data=%s and time=%s"""
        cursor.execute(_SQL, paramms)
        conn.commit()
        self.w2.close()
        self.showPlan()

    def showPlan(self):
        data = []
        cursor = conn.cursor()
        data.append(self.calendarWidget.selectedDate().toString('dd.MM.yyyy'))
        p = tuple(data)
        self.label_2.setText(str(data[0]))
        _SQL = """SELECT * FROM user_plan WHERE data = %s"""
        self.listWidget.clear()
        cursor.execute(_SQL, p)
        self.contents = cursor.fetchall()
        if not self.contents:
            self.listWidget.clear()
            self.textEdit.clear()
            self.timeEdit.clear()
            self.listWidget.clear()
            self.label.setText("Планов ещё нет!")
        else:
            for i in self.contents:
                text = str(i[1] + " - " + i[2])
                self.listWidget.setSortingEnabled(True)
                self.listWidget.addItem(text)
                self.label.setText("У вас есть планы!")
                self.textEdit.clear()
                self.timeEdit.clear()

    def SavePlan(self):
        cursor = conn.cursor()
        d = self.calendarWidget.selectedDate().toString('dd.MM.yyyy')
        t = self.timeEdit.time().toString('hh:mm')
        events = self.textEdit.toPlainText()
        _SQL = """INSERT INTO user_plan (data, time, events) VALUES (%s, %s, %s)"""
        paramms = (d, t, events)
        cursor.execute(_SQL, paramms)
        conn.commit()
        self.label.setText("План сохранен!")

    def ButtonExit(self):
        conn.close()
        sys.exit()


class Ui_Dialog(QWidget):
    q = []
    date = QtCore.QDate(2020, 1, 1)
    def setupUi(self, Dialog):
        self.setWindowTitle("Изменение записи")
        self.setMinimumWidth(340)
        self.setMinimumHeight(144)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(220, 110, 111, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("Записать")
        self.textEdit = QtWidgets.QTextEdit(Dialog)
        self.textEdit.setGeometry(QtCore.QRect(10, 40, 321, 61))
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setText(self.q)
        self.timeEdit = QtWidgets.QTimeEdit(Dialog)
        self.timeEdit.setGeometry(QtCore.QRect(130, 10, 118, 22))
        self.timeEdit.setObjectName("timeEdit")
        self.dateEdit = QtWidgets.QDateEdit(Dialog)
        self.dateEdit.setGeometry(QtCore.QRect(10, 10, 110, 22))
        self.dateEdit.setObjectName("dateEdit")
        self.dateEdit.setDisplayFormat('dd.MM.yyyy')
        self.dateEdit.setDate(self.date)
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(260, 10, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setText("Отмена")
        self.pushButton_2.clicked.connect(self.ButtonExit)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 110, 150, 16))
        self.label.setObjectName("label")
        self.label.setText("Укажите новое время и план")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(50, 10, 61, 21))
        self.label_2.setObjectName("label_2")


class EditWin(Ui_Dialog):
    def __init__(self):
        super(EditWin, self).__init__()

    def getRex(self, b):
        self.q = b
        self.setupUi(self)

    def getRex_2(self, c):
        self.date = c
        self.dateEdit.setDisplayFormat('dd.MM.yyyy')
        self.dateEdit.setDate(c)
        self.setupUi(self)

    def ButtonExit(self):
        self.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = Ui()
    w.show()
    sys.exit(app.exec_())
