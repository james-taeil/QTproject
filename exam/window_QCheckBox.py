import sys
from PyQt5.QtWidgets import QApplication, QWidget, QCheckBox
from PyQt5.QtCore import Qt

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        cb = QCheckBox('Show title', self)
        cb.move(20,20)
        cb.toggle()
        cb.stateChanged.connect(self.changeTitle)

        self.setWindowTitle('QCheckbox')
        self.setGeometry(300, 300, 300, 300)
        self.show()

    def changeTitle(self, state):
        if state == Qt.Checked:
            self.setWindowTitle('누르지마')
        else:
            self.setWindowTitle('왜눌럿냐')

if __name__ =='__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())