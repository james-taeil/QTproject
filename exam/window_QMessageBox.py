import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt5.QtGui import QIcon



class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('QMessageBox')
        self.setGeometry(300, 300, 300, 300)
        self.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', 'Are you sure to quit?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()

        else:
            event.innore()


if __name__ =='__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())