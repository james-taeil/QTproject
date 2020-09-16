import sys
import mysql.connector
from PyQt5 import QtGui
from PyQt5.QtWidgets import *



class Window(QDialog):
    def __init__(self):
        super().__init__()

        self.title = "PyQt5 Database Connection"
        self.top = 200
        self.left = 500
        self.width = 400
        self.height = 300

        self.InitWindow()


    def InitWindow(self):
        self.button = QPushButton('DB Connection', self)
        self.button.setGeometry(100, 100, 200, 50)
        self.button.clicked.connect(self.DBConnection)

        self.setWindowIcon(QtGui.QIcon("mavel.jpg"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()


    def DBConnection(self):
        try:
            db = mysql.connector.connect(host = "127.0.0.1",
                                         user = "madang",
                                         password = "madang",
                                         database = 'madang',
                                         auth_plugin = 'mysql_native_password')

            QMessageBox.about(self, 'Connection', 'Database Connected Successfully')
        except db.Error as e:
            QMessageBox.about(self, 'Connection', 'Failed To Connect Database')
            sys.exit(1)


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())