import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.lb1 = QLabel(self)
        self.lb1.move(60, 40)

        qle = QLineEdit(self)
        qle.move(60,100)


        qle.textChanged[str].connect(self.onChanged)


        self.setWindowTitle('QLineEdit')
        self.setGeometry(300, 300, 300, 300)
        self.show()

    def onChanged(self, text):
        self.lb1.setText(text)
        self.lb1.adjustSize()

if __name__ =='__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())