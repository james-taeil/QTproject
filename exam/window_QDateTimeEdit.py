import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QDateTimeEdit
from PyQt5.QtCore import QDateTime


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        lbl = QLabel('QDateTimeEdit')

        datetimedit = QDateTimeEdit(self)
        datetimedit.setDateTime(QDateTime.currentDateTime())
        datetimedit.setDateTimeRange(QDateTime(1900, 1, 1, 00, 00, 00),
                              QDateTime(2100, 1, 1, 00, 00, 00))
        datetimedit.setDisplayFormat('yyyy.MM.dd hh:mm:ss')


        vbox = QVBoxLayout()
        vbox.addWidget(lbl)
        vbox.addWidget(datetimedit)
        vbox.addStretch()

        self.setLayout((vbox))


        self.setWindowTitle('QDateTimeEdit')
        self.setGeometry(300, 300, 300, 300)
        self.show()


if __name__ =='__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())