import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip
from PyQt5.QtCore import QCoreApplication
from  PyQt5.QtGui import QIcon
from PyQt5.QtGui import QFont


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        QToolTip.setFont(QFont('SansSerif',8))
        self.setToolTip('This is a <b>QWidget</b> widget')

        btn = QPushButton('Quit', self)
        btn.setToolTip('<b>닫기</b>')
        btn.move(100, 100)
        btn.resize(btn.sizeHint())
        btn.clicked.connect(QCoreApplication.instance().quit)

        self.setWindowTitle('Quit Butten')
        self.setWindowTitle('Mavel End-Game')
        self.setWindowIcon(QIcon('mavel'))
        self.setGeometry(300, 300, 300, 300)
        self.show()


if __name__ =='__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())