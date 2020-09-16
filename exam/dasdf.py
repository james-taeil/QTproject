from PyQt5 import QtGui
from PyQt5.QtWidgets import *
import sys
import mysql.connector

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
