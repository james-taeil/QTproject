import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt




class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        lbl_Blue = QLabel('Blue')
        lbl_Blue.setStyleSheet("color : blue;"
                               "background-color : #87CEFA;")

        vbox = QVBoxLayout()
        vbox.addWidget(lbl_Blue)

        self.setLayout(vbox)

        self.setWindowTitle('Reimplementing event handler')
        self.setGeometry(300, 300, 300, 300)
        self.show()


    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
        elif e.key() == Qt.Key_F:
            self.showFullScreen()
        elif e.key() == Qt.Key_N:
            self.showNormal()



if __name__ =='__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())