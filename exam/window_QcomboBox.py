import sys
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QLabel


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.lb1 = QLabel('Option1', self)
        self.lb1.move(50, 150)

        cb = QComboBox(self)
        cb.addItem('Option1')
        cb.addItem('Option2')
        cb.addItem('Option3')
        cb.addItem('Option4')
        cb.move(50,50)

        cb.activated[str].connect(self.onAcivated)


        self.setWindowTitle('QCheckbox')
        self.setGeometry(300, 300, 300, 300)
        self.show()

    def onAcivated(self, text):
        self.lb1.setText(text)
        self.lb1.adjustSize()

if __name__ =='__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())