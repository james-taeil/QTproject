import sys
from PyQt5.QtWidgets import *

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

import smtplib

class MailTrans(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    #UI
    def initUI(self):
        #왼쪽
        self.lbl_id = QLabel("구글 아이디    :", self)
        self.lbl_id.move(20, 20)
        self.edit_id = QLineEdit(self)
        self.edit_id.move(110, 15)
        self.edit_id.textChanged.connect(self.reciver)

        self.lbl_passwd = QLabel("구글 비밀번호 :", self)
        self.lbl_passwd.move(20, 50)
        self.edit_passwd = QLineEdit(self)
        self.edit_passwd.setEchoMode(QLineEdit.Password)
        self.edit_passwd.move(110, 45)

        self.lbl_divisionLine1 = QLabel('-'*40, self)
        self.lbl_divisionLine1.move(20, 75)

        self.lbl_receiver = QLabel("받는 사람", self)
        self.lbl_receiver.move(20, 105)

        self.lbl_receiveAddr = QLabel("메일 주소       :", self)
        self.lbl_receiveAddr.move(20, 140)
        self.edit_receiveAddr = QLineEdit(self)
        self.edit_receiveAddr.move(110, 135)

        self.lbl_divisionLine2 = QLabel('-'*40, self)
        self.lbl_divisionLine2.move(20, 165)

        self.lbl_transmit = QLabel("보내는 사람", self)
        self.lbl_transmit.move(20, 225)

        self.lbl_transmitAddr = QLabel("메일 주소       :", self)
        self.lbl_transmitAddr.move(20, 260)
        self.edit_transmitAddr = QLineEdit(self)
        self.edit_transmitAddr.move(110, 255)
        self.edit_transmitAddr.setReadOnly(True)

        #오른쪽
        self.lbl_title = QLabel('메일 제목', self)
        self.lbl_title.move(300, 20)
        self.edit_title = QLineEdit(self)
        self.edit_title.move(300, 40)
        self.edit_title.setFixedWidth(430)

        self.lbl_attachedFile = QLabel("첨부 파일", self)
        self.lbl_attachedFile.move(300, 80)
        self.edit_attachedFile = QLineEdit(self)
        self.edit_attachedFile.move(370, 75)
        self.edit_attachedFile.setFixedWidth(275)
        self.edit_attachedFile.setReadOnly(True)
        self.btn_attachedFile = QPushButton("파일 선택", self)
        self.btn_attachedFile.move(655, 73)
        self.btn_attachedFile.clicked.connect(self.attachedFile)

        self.lbl_attachedImageFile = QLabel("이미지 파일", self)
        self.lbl_attachedImageFile.move(300, 110)
        self.edit_attachedImageFile = QLineEdit(self)
        self.edit_attachedImageFile.move(370, 105)
        self.edit_attachedImageFile.setFixedWidth(275)
        self.edit_attachedImageFile.setReadOnly(True)
        self.btn_attachedImageFile = QPushButton("파일 선택", self)
        self.btn_attachedImageFile.move(655, 103)
        self.btn_attachedImageFile.clicked.connect(self.attachedImageFile)

        self.lbl_context = QLabel("메일 내용", self)
        self.lbl_context.move(300, 135)

        self.text_context = QTextEdit(self)
        self.text_context.move(300, 160)
        self.text_context.setAcceptRichText(False)
        self.text_context.setFixedSize(430, 180)

        self.btn_transmit = QPushButton("전송", self)
        self.btn_transmit.move(25, 335)
        self.btn_transmit.clicked.connect(self.transmit)

        self.btn_init = QPushButton("초기화", self)
        self.btn_init.move(105, 335)
        self.btn_init.clicked.connect(self.init)

        self.btn_exit = QPushButton("종료", self)
        self.btn_exit.move(185, 335)
        self.btn_exit.clicked.connect(self.exit)

        self.setWindowTitle("메일 전송 프로그램`")
        self.setGeometry(0, 0, 750, 380)
        self.center()
        self.show()

    #메일 주소 쓰면 아래 보내는 메일주소 edit창에 자동입력
    def reciver(self):
        self.edit_transmitAddr.setText(self.edit_id.text())

    #메일 전송
    def transmit(self):
        if(self.edit_id.text() != "") and (self.edit_passwd.text() != "") and (self.edit_transmitAddr != ''):
            try:
                host = "smtp.gmail.com"
                port = "587"
                userid = self.edit_id.text()
                userpw = self.edit_passwd.text()

                senderAddr = self.edit_transmitAddr.text()
                receiveAddr = self.edit_receiveAddr.text()

                mailTitle = self.edit_title.text()
                body = self.text_context.toPlainText()


                mailSend = MIMEMultipart()
                mailSend.add_header("From", senderAddr)
                mailSend.add_header("To", receiveAddr)
                mailSend.add_header("Subject", mailTitle)
                mailSend.attach(MIMEText(body, "plain"))


                if (self.edit_attachedFile.text() != ""):
                    attachedFile = open(self.edit_attachedFile.text(), "rb")
                    file = MIMEApplication(attachedFile.read())
                    attachedFile.close()
                    mailSend.attach(file)


                if (self.edit_attachedImageFile.text() != ""):
                    attachedImageFile = open(self.edit_attachedImageFile.text(), "rb")
                    img = MIMEImage(attachedImageFile.read())
                    attachedImageFile.close()
                    mailSend.attach(img)

                server = smtplib.SMTP(host, port)
                server.starttls()
                server.login(userid, userpw)
                server.send_message(mailSend)
                server.quit()

                self.edit_receiveAddr.clear()
                self.edit_title.clear()
                self.text_context.clear()
                self.edit_attachedFile.clear()
                self.edit_attachedImageFile.clear()

                QMessageBox.information(self, "전송 성공", "메일이 전송되었습니다.",
                                        QMessageBox.Yes, QMessageBox.Yes)
            except Exception as e:
                print(e)
                QMessageBox.information(self, "전송 오류", "메일 전송 오류 입니다.",
                                        QMessageBox.Yes, QMessageBox.Yes)
                return
        else:
            QMessageBox.information(self,"입력 오류", "빈칸 없이 입력하세요.",
                                        QMessageBox.Yes, QMessageBox.Yes)
        return

    #초기화
    def init(self):
        self.edit_id.clear()
        self.edit_passwd.clear()
        self.edit_receiveAddr.clear()
        self.edit_transmitAddr.clear()
        self.edit_title.clear()
        self.edit_attachedFile.clear()
        self.edit_attachedImageFile.clear()
        self.text_context.clear()

    #종료
    def exit(self):
        sys.exit(1)

    #텍스트 첨부 파일
    def attachedFile(self):
        attached_file = QFileDialog.getOpenFileName(self, "텍스트 첨부 파일" './')
        self.edit_attachedFile.setText(attached_file[0])

    #이미지 첨부 파일
    def attachedImageFile(self):
        attached_image_file = QFileDialog.getOpenFileName(self, "이미지 첨부", filter="*.png;*.jpg")
        self.edit_attachedImageFile.setText(attached_image_file[0])




    #중앙배치
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MailTrans()
    sys.exit(app.exec_())