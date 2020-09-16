import sys, pymysql
from email import charset

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtCore import Qt


#회원 정보 추가 GUI
from Tools.scripts.make_ctype import values


class insert(QWidget):
    global w    #sql() 시작 메소드 객체


    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(500, 330, 250, 250)
        self.setWindowTitle("회원 정보 추가")

        self.lbl_name = QLabel("회원 정보 추가", self)
        self.lbl_name.move(80, 25)

        self.lbl_name = QLabel('이름', self)
        self.lbl_name.move(25, 60)
        self.txt_name = QLineEdit(self)
        self.txt_name.move(25 + 49, 60)

        self.lbl_age = QLabel("나이", self)
        self.lbl_age.move(25, 95)
        self.txt_age = QLineEdit(self)
        self.txt_age.move(25 + 49, 95)

        self.lbl_phone = QLabel('연락처', self)
        self.lbl_phone.move(25, 130)
        self.txt_phone = QLineEdit(self)
        self.txt_phone.move(25 + 49, 130)

        self.lbl_address = QLabel("주소", self)
        self.lbl_address.move(25, 165)
        self.txt_address = QLineEdit(self)
        self.txt_address.move(25 + 49, 165)

        self.btn_insert = QPushButton('저장', self)
        self.btn_insert.move(85, 200)
        self.btn_insert.clicked.connect(self.into)

        self.center()


    #회원 정보 추가
    def into(self):
        if(self.txt_name.text() != '') and (self.txt_age.text() != '') and (self.txt_phone.text() != '') and (self.txt_address.text() != ''):
            try:
                self.cmd = "insert into membership(name, age, phone, address) values('{}','{}','{}','{}')".format(self.txt_name.text(),self.txt_age(),self.txt_phone(),self.txt_address())

                print(self.cmd)
                self.cur.execute(self.cmd)
                self.conn.commit()




                self.txt_name.setText(self.txt_name.text())
                self.txt_age.setText(self.txt_age.text())
                self.txt_phone.setText(self.txt_phone.text())
                self.txt_address.setText(self.txt_address.text())

            except:
                QMessageBox.information(self, "삽입 오류", "올바른 형식으로 입력하세요.",
                                        QMessageBox.Yes, QMessageBox.Yes)
                return
        else:
            QMessageBox.information(self, "입력 오류", "빈칸 없이 입력하세요.",
                                    QMessageBox.Yes, QMessageBox.Yes)
            return

        self.close()


    # 회원 추가 후 내용 지운다.
    def showEvent(self, QShowEvent):
        self.txt_name.clear()
        self.txt_age.clear()
        self.txt_phone.clear()
        self.txt_address.clear()
        print('# 회원 추가 후 내용을 지운다.')


    # 중앙 배치치
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    # 회원 정보 관리 GUI
class sql(QWidget):
    global k


    def __init__(self):
        super().__init__()      #상위 객체 생성
        self.sqlConnect()
        self.initUI()           #클래스 안의 메소드 호출


    def sqlConnect(self):
        try:
            self.conn = pymysql.connect(
                host = "127.0.0.1",
                user = "user1",
                password = "user1",
                database = 'bookdb',
                port = 3306,
                charset = "utf8"
            )
        except:
            print('잘못 입력했음!')
            exit(1)

        print("연결 성공!")
        self.cur = self.conn.cursor()


    def initUI(self):
        self.w = 500
        self.h = 550
        self.btnSize = 40
        self.setGeometry(300, 300, self.w, self.h)
        self.setWindowTitle("회원 정보 관리 시스템")


        # 개인 정보 입력
        self.lbl_title = QLabel("개인 회원 정보 관리", self)
        self.lbl_title.move(200, 20)

        self.lbl_number = QLabel("번호", self)
        self.lbl_number.move(25, 50)
        self.txt_number = QLineEdit(self)
        self.txt_number.move(25 + 49, 45)
        self.txt_number.setReadOnly(True)       # 변경하지 못하도록 ReadOnly 속성 지정

        self.lbl_name = QLabel("이름", self)
        self.lbl_name.move(25, 85)
        self.txt_name = QLineEdit(self)
        self.txt_name.move(25 + 49, 80)

        self.lbl_age = QLabel("나이", self)
        self.lbl_age.move(25, 120)
        self.txt_age = QLineEdit(self)
        self.txt_age.move(25 + 49, 115)

        self.lbl_phone = QLabel('연락처', self)
        self.lbl_phone.move(25, 155)
        self.txt_phone = QLineEdit(self)
        self.txt_phone.move(25 + 49, 150)

        self.lbl_address = QLabel("주소", self)
        self.lbl_address.move(25, 190)
        self.txt_address = QLineEdit(self)
        self.txt_address.move(25 + 49, 185)

        self.lineedit_true()


        #트리 뷰
        self.list = QTreeView(self)
        self.list.setRootIsDecorated(False)
        self.list.setAlternatingRowColors(True)
        self.list.resize(450, 260)
        self.list.move(25, 230)


        # 목록 리스트
        self.item_list = QStandardItemModel(0, 5, self)
        self.item_list.setHeaderData(0, Qt.Horizontal, "번호")
        self.item_list.setHeaderData(1, Qt.Horizontal, "이름")
        self.item_list.setHeaderData(2, Qt.Horizontal, "나이")
        self.item_list.setHeaderData(3, Qt.Horizontal, "연락처")
        self.item_list.setHeaderData(4, Qt.Horizontal, "주소")

        # 테이블 회원 목록 클릭 이벤트 연결
        self.list.clicked.connect(self.slt)

        # 목록 리스트 트리뷰 리스트에 추가
        self.list.setModel(self.item_list)

        # 버튼
        self.btn_new = QPushButton("신규", self)
        self.btn_new.clicked.connect(self.newlist)      #newlist 연결(추가?)
        self.btn_new.resize(self.btnSize, self.btnSize)

        self.btn_update = QPushButton("수정", self)
        self.btn_update.resize(self.btnSize, self.btnSize)
        self.btn_update.clicked.connect(self.edit)      #edit 연결

        self.btn_delete = QPushButton("삭제", self)
        self.btn_delete.resize(self.btnSize, self.btnSize)
        self.btn_delete.clicked.connect(self.dlt)      # dlt 연결

        self.btn_end = QPushButton("종료", self)
        self.btn_end.resize(self.btnSize, self.btnSize)
        self.btn_end.clicked.connect(self.end)          # end 연결


        self.btn_update.setDisabled(True)
        self.btn_delete.setDisabled(True)

        self.center()
        self.show()


    # 종료
    def end(self):
        exit(1)


    # 중앙 배치
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    # 회원 삭제
    def dlt(self):
        if (self.txt_number.text() != ""):
            try:
                agree = QMessageBox.question(self, "삭제 확인", "정말로 삭제 하시겠습니까?",
                                             QMessageBox.Yes|QMessageBox.No, QMessageBox.No)

                if agree == QMessageBox.Yes:
                    self.cmd = "Delet from membership where no = '{}'".format(self.txt_number.text())
                    print(self.cmd)
                    self.cur.execute(self.cmd)
                    self.conn.commit()
                    self.slt()

            except:
                QMessageBox.information(self, "삭제 오류", "잘못 선택된 회원입니다.",
                                        QMessageBox.Yes, QMessageBox.Yes)
                return
        else:
            QMessageBox.information(self, "삭제 오류", "회원 번호가 없습니다.",
                                    QMessageBox.Yes, QMessageBox.Yes)
            return
        QMessageBox.information(self, "삭제 성공", "삭제되었습니다.",
                                QMessageBox.Yes, QMessageBox.Yes)

        self.lineedit_true()
        self.btn_update.setDisabled(True)
        self.btn_delete.setDisabled(True)



    # 회원 수정
    def edit(self):
        if (self.txt_name.text() != "") and (self.txt_age.text() != "") and (self.txt_phone.text() != "") and (self.txt_address.text() != ""):
            try:
                self.cmd = "Update membership set name = '{}', age = '{}', phone = '{}', address = '{}' where no = '{]'".format(self.txt_name.text(), self.txt_age.text(), self.txt_phone.text(), self.txt_address.text(), self.txt_number.text())
                print(self.cmd)
                w.cur.execute(self.cmd)
                w.conn.commit()
            except:
                QMessageBox.information(self, "삽입 오류", "올바른 형식으로 입력하세요.",
                                        QMessageBox.Yes, QMessageBox.Yes)
                return

        else:
            QMessageBox.information(self, "입력 오류", "빈칸 없이 입력하세요.",
                                    QMessageBox.Yes, QMessageBox.Yes)
            return
        QMessageBox.information(self, "수정 성공", "수정되었습니다.",
                                QMessageBox.Yes, QMessageBox.Yes)

        self.lineedit_true()
        self.btn_update.setDisabled(True)
        self.btn_delete.setDisabled(True)


    # 테이블 회원 목록 클릭 이벤트
    def slt(self):
        self.txt_number.setText(str(self.item_list.index(self.list.currentIndex().row(), 0).data()))
        self.txt_name.setText(str(self.item_list.index(self.list.currentIndex().row(), 1).data()))
        self.txt_age.setText(str(self.item_list.index(self.list.currentIndex().row(), 2).data()))
        self.txt_phone.setText(str(self.item_list.index(self.list.currentIndex().row(), 3).data()))
        self.txt_address.setText(str(self.item_list.index(self.list.currentIndex().row(), 4).data()))

        self.btn_update.setDisabled(False)
        self.btn_delete.setDisabled(False)

        self.txt_name.setReadOnly(False)
        self.txt_age.setReadOnly(False)
        self.txt_phone.setReadOnly(False)
        self.txt_address.setReadOnly(False)

        print('slt(self)')


    # QLineEdit 설정 변경
    def lineedit_true(self):
        self.txt_number.clear()
        self.txt_name.clear()
        self.txt_age.clear()
        self.txt_phone.clear()
        self.txt_address.clear()
        self.txt_name.setReadOnly(True)
        self.txt_age.setReadOnly(True)
        self.txt_phone.setReadOnly(True)
        self.txt_address.setReadOnly(True)


    # 회원 목록 새로 고침
    def newlist(self):
        self.cur.execute("select max(no) from membership") #행 갯수 가져오기
        self.conn.commit()
        self.cnt = self.cur.fetchone()
        k.show()            #신규창 보여주기
        print('newlist(self)')

    #프로그램 시작시 self.list.resize(450, 260)로 인한 이벤트 핸들러
    def resizeEvent(self, QResizeEvent):
        self.btnX = self.width() - 185
        self.btnY = self.height() - 50

        self.btn_new.move(self.btnX, self.btnY)
        self.btn_update.move(self.btnX + self.btnSize * 1, self.btnY)
        self.btn_delete.move(self.btnX + self.btnSize * 2, self.btnY)
        self.btn_end.move(self.btnX + self.btnSize * 3, self.btnY)
        print('resizeEvent(self, QResizeEvent)')


    #윈도우 닫기 이벤트
    def closeEvent(self, QCloseEvent):
        self.conn.close()


    #목록 테이블에 마우스가 들어오면 발생하는 이벤트 : 회원 목록 다시 보여주기
    def enterEvent(self, QEvent):
        self.cmd = "select * from membership"
        self.cur.execute(self.cmd)
        self.conn.commit()
        ar = self.cur.fetchall()

        self.item_list.removeRow(len(ar))

        for i in range(len(ar)):
            self.item_list.removeRow(i)
            self.item_list.insertRow(i)
            self.item_list.setData(self.item_list.index(i, 0), ar[i][0])
            self.item_list.setData(self.item_list.index(i, 1), ar[i][1])
            self.item_list.setData(self.item_list.index(i, 2), ar[i][2])
            self.item_list.setData(self.item_list.index(i, 3), ar[i][3])
            self.item_list.setData(self.item_list.index(i, 4), ar[i][4])


        self.txt_number.clear()
        self.txt_name.clear()
        self.txt_age.clear()
        self.txt_phone.clear()
        self.txt_address.clear()

        print('enterEvent(self, QEvent)')


    #프로그램 시작 시 self.show() 이벤트에 대한 핸들러
    def showEvent(self, QShowEvent):
        self.cmd = "select * from membership"
        self.cur.execute(self.cmd)
        self.conn.commit()
        ar = self.cur.fetchall()

        self.item_list.removeRow(len(ar))

        for i in range(len(ar)):
            self.item_list.removeRow(i)
            self.item_list.insertRow(i)
            self.item_list.setData(self.item_list.index(i, 0), ar[i][0])
            self.item_list.setData(self.item_list.index(i, 1), ar[i][1])
            self.item_list.setData(self.item_list.index(i, 2), ar[i][2])
            self.item_list.setData(self.item_list.index(i, 3), ar[i][3])
            self.item_list.setData(self.item_list.index(i, 4), ar[i][4])

        self.txt_number.clear()
        self.txt_name.clear()
        self.txt_age.clear()
        self.txt_phone.clear()
        self.txt_address.clear()

        print('showEvent(self, QShowEvent)')


#Application 오브젝트 생성 - 쉘스크립트에서 실행할 때 명령줄로 인수를 받을수 있음
app = QApplication(sys.argv)

#객체 생성 - 메인 GUI에 생성되는 창
w = sql() #객체 생성
k = insert() #신규창 등록 삽입
sys.exit(app.exec_()) #실행 창 닫을때