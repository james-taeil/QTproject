import ast
import mysql.connector
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox


def MyConverter(mydata):
    def cvt(data):
        try:
            return ast.literal_eval(data)

        except Exception:
            return str(data)

    return tuple(map(cvt, mydata))


class UI_MainWindow(object):

    def LoadData(self):
        try:
            db = mysql.connector.connect(host="127.0.0.1",
                                         user="madang",
                                         password="madang",
                                         database='madang',
                                         auth_plugin='mysql_native_password')
        except db.Error as e:
            QMessageBox.about(self, 'Connection', 'Failed To Connect Database')
            sys.exit(1)

        cur = db.cursor()
        rows = cur.execute("select * from book")
        data = cur.fetchall()

        for row in data:
            print(row)
            self.addTable(MyConverter(row))

        cur.close()


    def addTable(self, columns):
        rowPosition = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPosition)


        for i, columns in enumerate(columns):
            self.tableWidget.setItem(rowPosition, i, QtWidgets.QTableWidgetItem(str(columns)))



    def setupUI(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(432, 365)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setRowCount(0)

        column_headers = ['도서번호', '도서이름', '출판사', '정가']
        self.tableWidget.setHorizontalHeaderLabels(column_headers)
        self.verticalLayout.addWidget(self.tableWidget)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.clicked.connect(self.LoadData)
        self.pushButton.setObjectName("pushButton")

        self.verticalLayout.addWidget(self.pushButton)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retarnslateUI(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retarnslateUI(self, Mainwindow):
        _translate = QtCore.QCoreApplication.translate
        Mainwindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Load Data"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UI_MainWindow()
    ui.setupUI(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())