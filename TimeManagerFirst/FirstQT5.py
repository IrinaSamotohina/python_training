from PyQt5 import QtWidgets, uic, QtGui
import sys
import mysql.connector
from PyQt5.QtWidgets import QTableWidgetItem

conn = mysql.connector.connect(host="localhost", user="user_1", password="password", database="plan")
Form, _ = uic.loadUiType("TimeMangGui1.ui")

class Ui(QtWidgets.QDialog, Form):
    def __init__(self):
        super(Ui, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon("icon_time.png"))
        self.pushButton_2.clicked.connect(self.SavePlan)
        self.calendarWidget.clicked.connect(self.showDate)
        self.pushButton.clicked.connect(self.ButtonExit)

    def showDate(self):
        cursor = conn.cursor()
        d = self.calendarWidget.selectedDate().toString('dd.MM.yyyy')
        self.label_2.setText(d)
        print(d)
        #try:
        _SQL = """SELECT * FROM user_plan WHERE data = '8.10.2020'"""
        cursor.execute(_SQL, d)
        contents = cursor.fetchall()
        print(contents)
        #self.tableWidget.setItem(0, 0, QTableWidgetItem(contents))
        #except FileNotFoundError:
            #self.textEdit_2.clear()
            #self.textEdit.clear()
            #self.timeEdit.clear()
            #self.label.setText("Планов ещё нет!")
        print("Yes!")

        # try:
        # plan = open(date + ".txt").read()
        # self.textEdit_2.setText(plan)
        # self.label.clear()

    def SavePlan(self):
        cursor = conn.cursor()
        d = self.calendarWidget.selectedDate().toString('dd.MM.yyyy')
        t = self.timeEdit.time().toString('hh:mm')
        events = self.textEdit.toPlainText()
        print(d, t, events)
        _SQL = """INSERT INTO user_plan (data, time, events) VALUES (%s, %s, %s)"""
        paramms = (d, t, events)
        cursor.execute(_SQL, paramms)
        conn.commit()
        conn.close()
        self.label.setText("План сохранен!")

    def ButtonExit(self):
        sys.exit()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = Ui()
    w.show()
    sys.exit(app.exec_())
    conn.close()
