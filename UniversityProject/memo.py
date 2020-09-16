import  sys, pymysql
from builtins import super, set
from itertools import starmap

from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import *

class MyApp(QDialog):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        tabs = QTabWidget()
        tabs.addTab(SubjectTab(), '학과 등록')
        tabs.addTab(StudentTab(), '학생 등록')
        tabs.addTab(LessonTab(), '과목 등록')
        tabs.addTab(TraineeTab(), '수강 등록')

        buttonbox = QDialogButtonBox(QDialogButtonBox.Ok)
        buttonbox.accepted.connect(self.accept)

        vbox = QVBoxLayout()
        vbox.addWidget(tabs)
        vbox.addWidget(buttonbox)

        self.setWindowTitle("미래 대학교 수강 신청")
        self.setLayout(vbox)
        self.setGeometry(0, 0, 1200, 600)
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()                           # 창의 위치&크기 정도 가져옴
        cp = QDesktopWidget().availableGeometry().center()  #사용하는 모니터 화면의 가운데 위치를 파악
        qr.moveCenter(cp)                                   #직사각형 위치를 화면의 중심의 위치로 이동
        self.move(qr.topLeft())                             #화면 중심으로 이동 했던 직사각형 qr의 위치로 이동 시킴
                                                            #결과적으로 현재 창의 중심이 화면의 중심과 일치하게 되면서 창이 가운데 나타남


class SubjectTab(QWidget):
    def __init__(self):
        super().__init__()
        self.dbConnect()
        self.initUI()
        self.subjectlist(self)


    def dbConnect(self):
        #DB 연동 pymysql.connect() 메소드 사용 // 예외처리
        try:
            self.conn = pymysql.connect(
                host = "127.0.0.1",
                user = "manager",
                password = "manager",
                db = "universitydb",
                port = 3306,
                charset = "utf8"
            )
        except:
            print("접속 실패!")
            exit(1)
        print("접속 성공!")

        self.uni_cur = self.conn.cursor() #연결된 DB에 커서 두기


    def initUI(self):
        #최상위 '학과 등록' 제목
        self.lbl_subject_title_name = QLabel('학과 등록', self)
        self.lbl_subject_title_name.move(30, 25)

        #학과 일련 번호
        self.lbl_subject_no = QLabel('일련 번호 :', self)
        self.lbl_subject_no.move(50, 55)
        self.ledit_subject_no = QLineEdit(self)             #일련번호 빈칸만들기
        self.ledit_subject_no.move(120, 50)
        self.ledit_subject_no.setReadOnly(True)

        #학과 학과 번호
        self.lbl_subject_num = QLabel('학과 번호 :', self)
        self.lbl_subject_num.move(50, 85)
        self.ledit_subject_num = QLineEdit(self)            #학과번호 빈칸만들기
        self.ledit_subject_num.move(120, 80)

        #학과 학과명
        self.lbl_subject_name = QLabel('학 과 명 :', self)
        self.lbl_subject_name.move(50, 115)
        self.ledit_subject_name = QLineEdit(self)           #학과명 빈칸만들기
        self.ledit_subject_name.move(120, 110)

        #학과 학과 목록
        self.lbl_subject_list = QLabel('학과 목록', self)
        self.lbl_subject_list.move(400, 25)

        ##버튼 만들기 - 등록 수정 삭제 \ 초기화 수정 아래 위치 // 버튼간 x 간격 10 // 버튼 x 길이 70 // 버튼 y 길이 20
        #등록 버튼
        self.btn_subject_insert = QPushButton('등 록', self) #입력 버튼만들기
        self.btn_subject_insert.move(50, 150)
        # clicked.connect()는 클릭 이벤트시 특정 함수로 연결 하기 위함 // subject_insert 함수로 연결
        self.btn_subject_insert.clicked.connect(self.subject_insert)

        #수정 버튼
        self.btn_subject_update = QPushButton('수 정', self) #수정 버튼만들기
        self.btn_subject_update.move(130, 150)
        self.btn_subject_update.clicked.connect(self.subject_edit)      #버튼 subject_edit 메소드로 연결


        #삭제 버튼
        self.btn_subject_delete = QPushButton('삭 제', self) #삭제 버튼만들기
        self.btn_subject_delete.move(210, 150)
        self.btn_subject_delete.clicked.connect(self.subject_delete)    #버튼 subject_delete 메소드로 연결

        #초기화 버튼
        self.btn_subject_reset = QPushButton('초기화', self) #초기화 버튼만들기
        self.btn_subject_reset.move(130, 180)
        self.btn_subject_reset.clicked.connect(self.subject_clear) #subject_clear 함수로 연결

        self.btn_subject_update.setDisabled(True)
        self.btn_subject_delete.setDisabled(True)


        #트리 뷰
        self.subject_TreeView_list = QTreeView(self)                 #행과 열의 표를 만들 수 있는 메소드
        self.subject_TreeView_list.setRootIsDecorated(False)         # 펼치기/접기 아이콘을 나타낼지를 결정
        self.subject_TreeView_list.setAlternatingRowColors(True)     #행마다 색깔 변경하는 메소드
        self.subject_TreeView_list.resize(500, 450)
        self.subject_TreeView_list.move(400, 50)


        #학과 목록 리스트 헤더 // 트리뷰 상단에 일련번호/학과번호/학과명 헤더 만들기
        self.subject_list_Headitem = QStandardItemModel(0, 3, self)             #3개 값 할당
        self.subject_list_Headitem.setHeaderData(0, Qt.Horizontal, "일련 번호")
        self.subject_list_Headitem.setHeaderData(1, Qt.Horizontal, "학과 번호")
        self.subject_list_Headitem.setHeaderData(2, Qt.Horizontal, "학 과 명")


        #학과 목록 테이블 클릭 이벤트 연결
        self.subject_TreeView_list.clicked.connect(self.subject_list_select)

        #학과 목록 리스트를 트리뷰 리스트에 추가
        self.subject_TreeView_list.setModel(self.subject_list_Headitem)


    # 학과 등록 메소드
    def subject_insert(self):
        if ((self.ledit_subject_num.text() != "") and (self.ledit_subject_name.text() != "")): #빈칸입력시 오류 출력 경우
            try:
                # 사용자에게 입력 받은 값 SQL에 insert 해주기

                # insert문 만들기
                self.subject_insert_sql = "insert into subject(s_num, s_name) values('{}','{}')"\
                .format(self.ledit_subject_num.text(), self.ledit_subject_name.text())
                print(self.subject_insert_sql)

                # sql에서 insert 실행
                self.uni_cur.execute(self.subject_insert_sql)
                self.conn.commit()

            except:
                QMessageBox.information(self, "삽입 실행 오류!", "올바른 형식으로 입력하세요.",
                                        QMessageBox.Yes, QMessageBox.Yes)
                return
        else:
            QMessageBox.information(self, "입력 오류!", "빈칸 없이 입력하세요.",
                                    QMessageBox.Yes, QMessageBox.Yes)
            return

        self.subject_clear()
        self.subjectlist(self)


    #수정 메소드
    def subject_edit(self):
        if ((self.ledit_subject_num != "") and (self.ledit_subject_name != "")):
            try:
                self.subject_update_sql = "update subject set s_num = '{}', s_name = '{}' where s_no = '{}'"\
                .format(self.ledit_subject_num.text(), self.ledit_subject_name.text(), self.ledit_subject_no.text())
                print(self.subject_update_sql)

                self.uni_cur.execute(self.subject_update_sql)
                self.conn.commit()

            except:
                QMessageBox.information(self, "삽입 실행 오류!", "올바른 형식으로 입력하세요.",
                                        QMessageBox.Yes, QMessageBox.Yes)
                return
        else:
            QMessageBox.information(self, "입력오류!", "빈칸 없이 입력하세요.",
                                    QMessageBox.Yes, QMessageBox.Yes)
            return

        QMessageBox.information(self, "수정 성공!", "수정되었습니다.",
                                QMessageBox.Yes, QMessageBox.Yes)

        self.subject_clear()
        self.subjectlist(self)


    #삭제 메소드
    def subject_delete(self):
        if (self.ledit_subject_no.text() != ""):
            try:
                agree = QMessageBox.question(self, "삭제 확인", "정말로 삭제 하시겠습니까?",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if agree == QMessageBox.Yes:
                    self.delete_sql = "delete from subject where s_no = '{}'"\
                    .format(self.ledit_subject_no.text())
                    print(self.delete_sql)

                    self.uni_cur.execute(self.delete_sql)
                    self.conn.commit()

                    self.subject_clear()
                    self.subjectlist(self)

            except:
                QMessageBox.information(self, "삭제 오류", "잘못 선택된 회원입니다.",
                                        QMessageBox.Yes,QMessageBox.Yes)
                return
        else:
            QMessageBox.information(self, "삭제 오류", "회원 번호가 없습니다.",
                                    QMessageBox.Yes, QMessageBox.Yes)
            return

        QMessageBox.information(self, "삭제 성공", "삭제되었습니다.",
                                 QMessageBox.Yes, QMessageBox.Yes)




    # 학과 테이블 목록 클릭 이벤트
    def subject_list_select(self):
        self.ledit_subject_no.setText(str(str(self.subject_list_Headitem.index(self.subject_TreeView_list.currentIndex().row(), 0).data())))
        self.ledit_subject_num.setText(self.subject_list_Headitem.index(self.subject_TreeView_list.currentIndex().row(), 1).data())
        self.ledit_subject_name.setText(str(self.subject_list_Headitem.index(self.subject_TreeView_list.currentIndex().row(), 2).data()))

        self.btn_subject_update.setDisabled(False)
        self.btn_subject_delete.setDisabled(False)
        self.btn_subject_insert.setDisabled(True)


    #학과 목록에 값 입력시 마다 전체 목록 보여주기 // 등록 수정 삭제 시 사용
    def subjectlist(self, QShowEvent):
        self.subject_total_list = "select * from subject"   #select 질의문 등록
        self.uni_cur.execute(self.subject_total_list)       #selcet 질의문 실행 // uni_cur는 데이터 창에 커서를 옮기기 위함
        self.conn.commit()

        rs = self.uni_cur.fetchall() #데이터 자료를 한번에 모든 로우 데이터 읽기

        self.subject_list_Headitem.removeRow(len(rs))

        for i in range(len(rs)):
            self.subject_list_Headitem.removeRow(i)
            self.subject_list_Headitem.insertRow(i)

            self.subject_list_Headitem.setData(self.subject_list_Headitem.index(i, 0), rs[i][0])
            self.subject_list_Headitem.setData(self.subject_list_Headitem.index(i, 1), rs[i][1])
            self.subject_list_Headitem.setData(self.subject_list_Headitem.index(i, 2), rs[i][2])

        self.ledit_subject_no.clear()
        self.ledit_subject_num.clear()
        self.ledit_subject_name.clear()


    #학과 목록 테이블에 마우스가 들어오면 발생하는 이벤트
    def enterEvent(self, QEvent):
        self.subject_list = "select * from subject"
        self.uni_cur.execute(self.subject_list)
        self.conn.commit()

        rs = self.uni_cur.fetchall()

        self.subject_list_Headitem.removeRow(len(rs))

        for i in range(len(rs)):
            self.subject_list_Headitem.removeRow(i)
            self.subject_list_Headitem.insertRow(i)

            self.subject_list_Headitem.setData(self.subject_list_Headitem.index(i, 0), rs[i][0])
            self.subject_list_Headitem.setData(self.subject_list_Headitem.index(i, 1), rs[i][1])
            self.subject_list_Headitem.setData(self.subject_list_Headitem.index(i, 2), rs[i][2])

        self.ledit_subject_no.clear()
        self.ledit_subject_num.clear()
        self.ledit_subject_name.clear()

    # lineEdit 창 클리어 메소드
    def subject_clear(self):
        self.ledit_subject_no.clear()
        self.ledit_subject_num.clear()
        self.ledit_subject_name.clear()

        #버튼 비활성화 기본 값 False
        self.btn_subject_insert.setDisabled(False) #등록 버튼 활성화
        self.btn_subject_update.setDisabled(True) #수정 버튼 비활성화
        self.btn_subject_delete.setDisabled(True) #삭제 버튼 비활성화


class StudentTab(QWidget):
    def __init__(self):
        super().__init__()
        self.dbConnect()
        self.initUI()
        self.studentList(self)

    #DB연동
    def dbConnect(self):
        #DB 연동 pymysql.connect() 메소드 사용 // 예외처리
        try:
            self.conn = pymysql.connect(
                host = "127.0.0.1",
                user = "manager",
                password = "manager",
                db = "universitydb",
                port = 3306,
                charset = "utf8"
            )
        except:
            print("접속 실패!")
            exit(1)
        print("접속 성공!")

        self.uni_cur = self.conn.cursor() #연결된 DB에 커서 두기

    #UI
    def initUI(self):
        self.lbl_student_register = QLabel("학생 등록", self)
        self.lbl_student_register.move(30, 25)

        self.btn_studentName_load = QPushButton("학과명 로드", self)
        self.btn_studentName_load.move(90, 20)
        self.btn_studentName_load.clicked.connect(self.subjectName_load)

        self.lbl_sd_no = QLabel("일련번호 :", self)
        self.lbl_sd_no.move(30, 55)
        self.edit_sd_no = QLineEdit(self)
        self.edit_sd_no.move(90, 50)
        self.edit_sd_no.setDisabled(True)

        self.lbl_s_num = QLabel("학 과 명 : ", self)
        self.lbl_s_num.move(30, 85)

        #학과 등록에서 등록된 학과명 불러오기 (self 사용 하지 않음)
        self.subjectNamelist = []
        self.subjectNamecombo = QComboBox(self)
        self.subjectNamecombo.move(90, 80)
        self.subjectNamecombo.activated[str].connect(self.onActivated)

        self.subjectName = QLabel("학과명을 선택하세요.", self)
        self.subjectName.move(190, 85)

        self.lbl_sd_num = QLabel('학   번 :', self)
        self.lbl_sd_num.move(30, 115)
        self.edit_sd_num = QLineEdit(self)
        self.edit_sd_num.move(90, 110)
        self.edit_sd_num.setDisabled(True)


        self.lbl_sd_name = QLabel("이   름 :", self)
        self.lbl_sd_name.move(30, 145)
        self.edit_sd_name = QLineEdit(self)
        self.edit_sd_name.move(90, 140)

        self.lbl_sd_id = QLabel("아 이 디 :", self)
        self.lbl_sd_id.move(30, 175)
        self.edit_sd_id = QLineEdit(self)
        self.edit_sd_id.move(90, 170)

        self.btn_id_check = QPushButton("중복 확인",self)
        self.btn_id_check.move(245, 168)
        self.btn_id_check.clicked.connect(self.id_check)

        self.lbl_sd_passwd = QLabel("비밀번호 :", self)
        self.lbl_sd_passwd.move(30, 205)
        self.edit_sd_passwd = QLineEdit(self)
        self.edit_sd_passwd.move(90, 200)

        self.lbl_sd_pw = QLabel('12 자 이하', self)
        self.lbl_sd_pw.move(245, 205)

        self.lbl_sd_birthday = QLabel("생년월일 :", self)
        self.lbl_sd_birthday.move(30, 235)
        self.date_sd_birthday = QDateEdit(self)
        self.date_sd_birthday.setDate(QDate.currentDate())
        self.date_sd_birthday.move(90, 230)

        self.lbl_sd_phone = QLabel("연 락 처 :", self)
        self.lbl_sd_phone.move(30, 265)
        self.edit_sd_phone = QLineEdit(self)
        self.edit_sd_phone.move(90, 260)

        self.lbl_sd_address = QLabel("주   소 :", self)
        self.lbl_sd_address.move(30, 295)
        self.edit_sd_address = QLineEdit(self)
        self.edit_sd_address.move(90, 290)

        self.lbl_sd_email = QLabel("이 메 일 :", self)
        self.lbl_sd_email.move(30, 325)
        self.edit_sd_email = QLineEdit(self)
        self.edit_sd_email.move(90, 320)

        self.btn_student_insert = QPushButton("등 록", self)
        self.btn_student_insert.move(30, 360)
        self.btn_student_insert.clicked.connect(self.student_insert)

        self.btn_student_update = QPushButton("수 정", self)
        self.btn_student_update.move(110, 360)
        self.btn_student_update.clicked.connect(self.student_edit)

        self.btn_student_delete = QPushButton("삭 제", self)
        self.btn_student_delete.move(190, 360)
        self.btn_student_delete.clicked.connect(self.student_delete)

        self.btn_student_init = QPushButton("초 기 화", self)
        self.btn_student_init.move(110, 390)
        self.btn_student_init.clicked.connect(self.student_init)

        self.lbl_student = QLabel("학생 목록", self)
        self.lbl_student.move(350, 25)

        self.btn_student_update.setDisabled(True)
        self.btn_student_delete.setDisabled(True)


        #트리뷰
        self.studentlist = QTreeView(self)
        self.studentlist.setRootIsDecorated(False)
        self.studentlist.setAlternatingRowColors(True)
        self.studentlist.resize(800, 450)
        self.studentlist.move(350, 50)

        #학생 목록 트리뷰 into 헤더
        self.student_item_list = QStandardItemModel(0, 11, self)
        self.student_item_list.setHeaderData(0, Qt.Horizontal, "일련 번호")
        self.student_item_list.setHeaderData(1, Qt.Horizontal, "학번")
        self.student_item_list.setHeaderData(2, Qt.Horizontal, "이름")
        self.student_item_list.setHeaderData(3, Qt.Horizontal, "아이디")
        self.student_item_list.setHeaderData(4, Qt.Horizontal, "비밀번호")
        self.student_item_list.setHeaderData(5, Qt.Horizontal, "학과번호")
        self.student_item_list.setHeaderData(6, Qt.Horizontal, "생년월일")
        self.student_item_list.setHeaderData(7, Qt.Horizontal, "핸드폰번호")
        self.student_item_list.setHeaderData(8, Qt.Horizontal, "주소")
        self.student_item_list.setHeaderData(9, Qt.Horizontal, "이메일")
        self.student_item_list.setHeaderData(10, Qt.Horizontal, "등록일")

        #학생 목록 테이블 클릭 이벤트 연결
        self.studentlist.clicked.connect(self.item_select)

        #학생 목록 리스트를 트리뷰 리스트에 추가
        self.studentlist.setModel(self.student_item_list)

    #학과 테이블에서 학과명 불러오기
    def subjectName_load(self):
        subjectNamelist = self.subject_nameList()
        self.subjectNamecombo.clear()
        for i in range(len(subjectNamelist)):
            s_name = subjectNamelist[i]
            self.subjectNamecombo.addItems(s_name)

        self.btn_studentName_load.setDisabled(True)
        self.btn_student_insert.setDisabled(False)

    #학생 정보 등록
    def student_insert(self):
        if ((self.edit_sd_num.text() != "") and (self.edit_sd_name.text() != "") and (self.edit_sd_id.text() != "")
            and (self.edit_sd_passwd.text() != "") and (self.edit_sd_phone.text() != "") and (self.edit_sd_address.text() != "")
            and (self.edit_sd_email.text() != "")):

            try:
                self.subject_list = "select s_num from subject where s_name = '{}'"\
                .format(self.subjectName.text())
                self.uni_cur.execute(self.subject_list)
                self.conn.commit()
                s_num = self.uni_cur.fetchone()

                self.student_insert_sql = "insert into student(sd_num, sd_name, sd_id, sd_passwd, s_num, sd_birth, sd_phone, sd_address, sd_email) values('{}','{}','{}','{}','{}','{}','{}','{}','{}')"\
                .format(self.edit_sd_num.text(), self.edit_sd_name.text(), self.edit_sd_id.text(), self.edit_sd_passwd.text(), s_num[0], self.date_sd_birthday.text(), self.edit_sd_phone.text(), self.edit_sd_address.text(), self.edit_sd_email.text())

                print(self.student_insert_sql)

                self.uni_cur.execute(self.student_insert_sql)
                self.conn.commit()

            except:
                QMessageBox.information(self, "삽입 오류", "올바른 형식으로 입력하세요.",
                                        QMessageBox.Yes, QMessageBox.Yes)
                return
        else:
            QMessageBox.information(self, "입력 오류", "빈칸 없이 입력하세요.",
                                    QMessageBox.Yes, QMessageBox.Yes)
            return

        self.student_init()
        self.studentList(self)

    #학생 정보 수정
    def student_edit(self):
        if ((self.edit_sd_passwd.text() != "") and (self.edit_sd_phone.text() != "") and (self.edit_sd_address.text() != "") and (self.edit_sd_email.text() != "")):
            try:
                self.student_update_sql = "update student set sd_passwd = '{}', sd_phone = '{}', sd_address = '{}', sd_email = '{}' where sd_no = '{}'"\
                .format(self.edit_sd_passwd.text(), self.edit_sd_phone.text(), self.edit_sd_address.text(), self.edit_sd_email.text(), self.edit_sd_no.text())

                self.uni_cur.execute(self.student_update_sql)
                self.conn.commit()

            except:
                QMessageBox.information(self, "삽입 오류", "올바른 형식으로 입력하세요.",
                                        QMessageBox.Yes, QMessageBox.Yes)
                self.student_init()
                return
        else:
            QMessageBox.information(self, "입력 오류", "빈칸 없이 입력하세요.",
                                    QMessageBox.Yes, QMessageBox.Yes)
            self.student_init()
            return

        QMessageBox.information(self, "수정 성공", "수정되었습니다.",
                                QMessageBox.Yes, QMessageBox.Yes)
        self.student_init()
        self.studentList(self)

    #학생 정보 삭제
    def student_delete(self):
        if (self.edit_sd_no.text() != ""):
            try:
                agree = QMessageBox.question(self, "삭제 확인", "정말로 삭제 하시겠습니까?",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if agree == QMessageBox.Yes:
                    self.student_delete_sql = "delete from student where sd_no = '{}'" \
                        .format(self.edit_sd_no.text())
                    print(self.student_delete_sql)

                    self.uni_cur.execute(self.student_delete_sql)
                    self.conn.commit()

                    self.student_init()
                    self.studentList(self)

            except:
                QMessageBox.information(self, "삭제 오류!", "잘못 선택된 회원입니다.",
                                        QMessageBox.Yes, QMessageBox.Yes)
                return
        else:
            QMessageBox.information(self, "삭제 오류!", "회원 번호가 없습니다.",
                                    QMessageBox.Yes, QMessageBox.Yes)
            return

        QMessageBox.information(self, "삭제 성공!", "삭제되었습니다.",
                                QMessageBox.Yes, QMessageBox.Yes)

    #학생 목록 테이블 클릭 이벤트
    def item_select(self):
        self.edit_sd_no.setText(str(self.student_item_list.index(self.studentlist.currentIndex().row(), 0).data()))
        self.edit_sd_num.setText(str(self.student_item_list.index(self.studentlist.currentIndex().row(), 1).data()))
        self.edit_sd_name.setText(str(self.student_item_list.index(self.studentlist.currentIndex().row(), 2).data()))
        self.edit_sd_id.setText(str(self.student_item_list.index(self.studentlist.currentIndex().row(), 3).data()))
        self.edit_sd_id.setDisabled(True)
        self.edit_sd_passwd.setText(str(self.student_item_list.index(self.studentlist.currentIndex().row(), 4).data()))
        self.date_sd_birthday.setDate(QDate.currentDate())
        self.edit_sd_phone.setText(str(self.student_item_list.index(self.studentlist.currentIndex().row(), 7).data()))
        self.edit_sd_address.setText(str(self.student_item_list.index(self.studentlist.currentIndex().row(), 8).data()))
        self.edit_sd_email.setText(str(self.student_item_list.index(self.studentlist.currentIndex().row(), 9).data()))

        self.edit_sd_name.setDisabled(True)
        self.btn_id_check.setDisabled(True)
        self.btn_studentName_load.setDisabled(True)
        self.btn_student_update.setDisabled(False)
        self.btn_student_delete.setDisabled(False)
        self.btn_student_insert.setDisabled(True)

    #학생 목록 등록 후 전체 목록 보여주기
    def studentList(self, QShowEvent):
        self.student_totallist = "select * from student"
        self.uni_cur.execute(self.student_totallist)
        self.conn.commit()

        rs = self.uni_cur.fetchall()

        self.student_item_list.removeRow(len(rs))

        for i in range(len(rs)):
            self.student_item_list.removeRow(i)
            self.student_item_list.insertRow(i)
            self.student_item_list.setData(self.student_item_list.index(i, 0), rs[i][0])
            self.student_item_list.setData(self.student_item_list.index(i, 1), rs[i][1])
            self.student_item_list.setData(self.student_item_list.index(i, 2), rs[i][2])
            self.student_item_list.setData(self.student_item_list.index(i, 3), rs[i][3])
            self.student_item_list.setData(self.student_item_list.index(i, 4), rs[i][4])
            self.student_item_list.setData(self.student_item_list.index(i, 5), rs[i][5])
            self.student_item_list.setData(self.student_item_list.index(i, 6), rs[i][6])
            self.student_item_list.setData(self.student_item_list.index(i, 7), rs[i][7])
            self.student_item_list.setData(self.student_item_list.index(i, 8), rs[i][8])
            self.student_item_list.setData(self.student_item_list.index(i, 9), rs[i][9])
            self.student_item_list.setData(self.student_item_list.index(i, 10), rs[i][10])

    #초기화 버튼 이벤트 핸들러
    def student_init(self):
        self.edit_sd_no.clear()
        self.subjectName.setText("학과명을 선택하세요.")
        self.edit_sd_num.clear()
        self.edit_sd_name.clear()
        self.edit_sd_name.setDisabled(False)
        self.edit_sd_id.clear()
        self.edit_sd_id.setDisabled(False)
        self.edit_sd_passwd.clear()
        self.date_sd_birthday.setDate(QDate.currentDate())
        self.edit_sd_phone.clear()
        self.edit_sd_address.clear()
        self.edit_sd_email.clear()

        self.btn_id_check.setDisabled(False)
        self.btn_studentName_load.setDisabled(False)
        self.btn_student_update.setDisabled(True)
        self.btn_student_delete.setDisabled(True)

    #아이디 체크 메소드
    def id_check(self):
        if (self.edit_sd_id.text() != ""):
            try:
                self.id_check_sql = "select sd_id from student where sd_id = '{}'".format(self.edit_sd_id.text())
                print(self.id_check_sql)
                self.uni_cur.execute(self.id_check_sql)

                rs = self.uni_cur.fetchall()

                if (rs != None):
                    self.edit_sd_id.setDisabled(True)
                    QMessageBox.information(self, "아이디 체크 성공", "사용할 수 있는 아이디 입니다.",
                                            QMessageBox.Yes, QMessageBox.Yes)
                else:
                    self.edit_sd_id.clear()
                    QMessageBox.information(self, "아이디 체크 성공", "사용할 수 없는 아이디 입니다.",
                                            QMessageBox.Yes, QMessageBox.Yes)

            except:
                QMessageBox.information(self, "아이디 체크 오류", "아이디를 잘못 입력하였습니다.",
                                        QMessageBox.Yes, QMessageBox.Yes)
                return
        else:
            QMessageBox.information(self, "아이디 체크 오류", "아이디를 입력하세요.",
                                        QMessageBox.Yes, QMessageBox.Yes)
            return

    #학과명 선택 핸들러
    def onActivated(self, text):
        self.subjectName.setText(text)
        self.sd_num_create(self.subjectName.text())

    #학번 생성
    def sd_num_create(self, s_name):
        # 학번 생성(연도 2자리 + 학과 2자리 + 일련번호 - 예로 06 01 0001)
        self.subject_num = "select s_num from subject where s_name = '{}'".format(self.subjectName.text())
        self.uni_cur.execute(self.subject_num)
        self.conn.commit()

        s_num = self.uni_cur.fetchone()

        self.student_sd_no = "select max(sd_no) from student"
        self.uni_cur.execute(self.student_sd_no)
        self.conn.commit()

        sd_no = self.uni_cur.fetchone()
        sd_no = list(sd_no)

        now = QDate.currentDate()
        year = now.toString('yy')


        print(sd_no)


        if sd_no[0] == None:
            sd_no[0] = 1

            sd_num = str(year) + str(s_num[0]) + str(sd_no[0]).zfill(4)  # 학번 일련번호 4자리 중 빈공간을 0으로 채움
            self.edit_sd_num.setText(sd_num)

        else:
            sd_num = str(year) + str(s_num[0]) + str(sd_no[0]+1).zfill(4)  # 학번 일련번호 4자리 중 빈공간을 0으로 채움
            self.edit_sd_num.setText(sd_num)




        sd_num = str(year) + str(s_num[0]) + str(sd_no[0]).zfill(4) #학번 일련번호 4자리 중 빈공간을 0으로 채움

        self.edit_sd_num.setText(sd_num)

    #학과명 불러오는 이벤트 핸들러
    def subject_nameList(self):
        self.subject_name_sql = "select s_name from subject order by s_no"
        self.uni_cur.execute(self.subject_name_sql)
        self.conn.commit()

        rs = self.uni_cur.fetchall()

        subject_name = []
        subject_name = rs

        return  subject_name


class LessonTab(QWidget):
    def __init__(self):
        super().__init__()
        self.dbConnect()
        self.initUI()
        self.lessonList(self)

    #DB 연동
    def dbConnect(self):
        #DB 연동 pymysql.connect() 메소드 사용 // 예외처리
        try:
            self.conn = pymysql.connect(
                host = "127.0.0.1",
                user = "manager",
                password = "manager",
                db = "universitydb",
                port = 3306,
                charset = "utf8"
            )
        except:
            print("접속 실패!")
            exit(1)
        print("접속 성공!")

        self.uni_cur = self.conn.cursor() #연결된 DB에 커서 두기

    #UI
    def initUI(self):
        self.lbl_lesson_register = QLabel("과목 등록", self)
        self.lbl_lesson_register.move(30, 25)

        self.lbl_frist_lesson = QLabel("전공 과목 :", self)
        self.lbl_frist_lesson.move(35, 55)
        self.lbl_frist_lesson_ex = QLabel('과목 번호 끝자리가 1', self)
        self.lbl_frist_lesson_ex.move(100, 55)

        self.lbl_second_lesson = QLabel("부전공 과목 :", self)
        self.lbl_second_lesson.move(35, 75)
        self.lbl_second_lesson_ex = QLabel('과목 번호 끝자리가 3', self)
        self.lbl_second_lesson_ex.move(110, 75)

        self.lbl_Third_lesson = QLabel("교양 과목 :", self)
        self.lbl_Third_lesson.move(35, 95)
        self.lbl_Third_lesson_ex = QLabel('과목 번호 끝자리가 3', self)
        self.lbl_Third_lesson_ex.move(100, 95)


        self.lbl_lesson_no = QLabel("일련 번호 :", self)
        self.lbl_lesson_no.move(55, 130)
        self.edit_lesson_no = QLineEdit(self)
        self.edit_lesson_no.move(125, 125)
        self.edit_lesson_no.setReadOnly(True)

        self.lbl_lesson_num = QLabel("과목 번호 :", self)
        self.lbl_lesson_num.move(55, 160)
        self.edit_lesson_num = QLineEdit(self)
        self.edit_lesson_num.move(125, 155)

        self.lbl_lesson_name = QLabel("과  목  명 :", self)
        self.lbl_lesson_name.move(55, 190)
        self.edit_lesson_name = QLineEdit(self)
        self.edit_lesson_name.move(125, 185)


        self.btn_lesson_insert = QPushButton("등 록", self)
        self.btn_lesson_insert.move(55, 230)
        self.btn_lesson_insert.clicked.connect(self.lesson_insert)

        self.btn_lesson_update = QPushButton("수 정", self)
        self.btn_lesson_update.move(135, 230)
        self.btn_lesson_update.clicked.connect(self.lesson_edit)

        self.btn_lesson_delete = QPushButton("삭 제", self)
        self.btn_lesson_delete.move(215, 230)
        self.btn_lesson_delete.clicked.connect(self.lesson_delete)

        self.btn_lesson_init = QPushButton("초 기 화", self)
        self.btn_lesson_init.move(135, 260)
        self.btn_lesson_init.clicked.connect(self.lesson_init)

        self.lbl_lesson = QLabel("과목 목록", self)
        self.lbl_lesson.move(350, 25)

        self.btn_lesson_update.setDisabled(True)
        self.btn_lesson_delete.setDisabled(True)

        # 트리뷰
        self.lessonlist = QTreeView(self)
        self.lessonlist.setRootIsDecorated(False)
        self.lessonlist.setAlternatingRowColors(True)
        self.lessonlist.resize(400, 450)
        self.lessonlist.move(350, 50)

        # 과목 목록 트리뷰 into 헤더
        self.lesson_item_list = QStandardItemModel(0, 3, self)
        self.lesson_item_list.setHeaderData(0, Qt.Horizontal, "일련 번호")
        self.lesson_item_list.setHeaderData(1, Qt.Horizontal, "과목 번호")
        self.lesson_item_list.setHeaderData(2, Qt.Horizontal, "과 목 명")

        # 과목 목록 테이블 클릭 이벤트 연결
        self.lessonlist.clicked.connect(self.lesson_item_select)

        # 과목 목록 리스트를 트리뷰 리스트에 추가
        self.lessonlist.setModel(self.lesson_item_list)

    #과목 등록
    def lesson_insert(self):
        if ((self.edit_lesson_num.text() != "") and (self.edit_lesson_name.text() != "")):
            try:
                self.lesson_insert_sql = "insert into lesson(l_num, l_name) values('{}','{}')"\
                .format(self.edit_lesson_num.text(), self.edit_lesson_name.text())
                print(self.lesson_insert_sql)

                # sql에서 insert 실행
                self.uni_cur.execute(self.lesson_insert_sql)
                self.conn.commit()

            except:
                QMessageBox.information(self, "삽입 실행 오류!", "올바른 형식으로 입력하세요.",
                                        QMessageBox.Yes, QMessageBox.Yes)
                return
        else:
            QMessageBox.information(self, "입력 오류!", "빈칸 없이 입력하세요.",
                                    QMessageBox.Yes, QMessageBox.Yes)
            return

        self.lesson_init()
        self.lessonList(self)

    #과목 수정
    def lesson_edit(self):
        if ((self.edit_lesson_num.text() != "") and (self.edit_lesson_name.text() != "")):
            try:
                self.lesson_update_sql = "update lesson set l_num = '{}', l_name = '{}' where l_no = '{}'"\
                .format(self.edit_lesson_num.text(), self.edit_lesson_name.text(), self.edit_lesson_no.text())

                self.uni_cur.execute(self.lesson_update_sql)
                self.conn.commit()

            except:
                QMessageBox.information(self, "삽입 오류", "올바른 형식으로 입력하세요.",
                                        QMessageBox.Yes, QMessageBox.Yes)
                self.lesson_init()
                return
        else:
            QMessageBox.information(self, "입력 오류", "빈칸 없이 입력하세요.",
                                    QMessageBox.Yes, QMessageBox.Yes)
            self.lesson_init()
            return

        QMessageBox.information(self, "수정 성공", "수정되었습니다.",
                                QMessageBox.Yes, QMessageBox.Yes)
        self.lesson_init()
        self.lessonList(self)

    #과목 삭제
    def lesson_delete(self):
        if (self.edit_lesson_no.text() != ""):
            try:
                agree = QMessageBox.question(self, "삭제 확인", "정말로 삭제 하시겠습니까?",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if agree == QMessageBox.Yes:
                    self.delete_sql = "delete from lesson where l_no = '{}'"\
                    .format(self.edit_lesson_no.text())
                    print(self.delete_sql)

                    self.uni_cur.execute(self.delete_sql)
                    self.conn.commit()

                    self.lesson_init()
                    self.lessonList(self)

            except:
                QMessageBox.information(self, "삭제 오류", "잘못 선택된 회원입니다.",
                                        QMessageBox.Yes,QMessageBox.Yes)
                return
        else:
            QMessageBox.information(self, "삭제 오류", "회원 번호가 없습니다.",
                                    QMessageBox.Yes, QMessageBox.Yes)
            return

        QMessageBox.information(self, "삭제 성공", "삭제되었습니다.",
                                 QMessageBox.Yes, QMessageBox.Yes)

    #line edit 클리어
    def lesson_init(self):
        self.edit_lesson_no.clear()
        self.edit_lesson_num.clear()
        self.edit_lesson_name.clear()

        # 버튼 비활성화 기본 값 False
        self.btn_lesson_insert.setDisabled(False)  # 등록 버튼 활성화
        self.btn_lesson_update.setDisabled(True)  # 수정 버튼 비활성화
        self.btn_lesson_delete.setDisabled(True)  # 삭제 버튼 비활성화

    #트리뷰 과목 보여주기
    def lessonList(self, QShowEvent):
        self.lesson_total_list = "select * from lesson"  # select 질의문 등록
        self.uni_cur.execute(self.lesson_total_list)  # selcet 질의문 실행 // uni_cur는 데이터 창에 커서를 옮기기 위함
        self.conn.commit()

        rs = self.uni_cur.fetchall()  # 데이터 자료를 한번에 모든 로우 데이터 읽기

        self.lesson_item_list.removeRow(len(rs))

        for i in range(len(rs)):
            self.lesson_item_list.removeRow(i)
            self.lesson_item_list.insertRow(i)

            self.lesson_item_list.setData(self.lesson_item_list.index(i, 0), rs[i][0])
            self.lesson_item_list.setData(self.lesson_item_list.index(i, 1), rs[i][1])
            self.lesson_item_list.setData(self.lesson_item_list.index(i, 2), rs[i][2])

        self.edit_lesson_no.clear()
        self.edit_lesson_num.clear()
        self.edit_lesson_name.clear()

    #트리뷰에 클릭 하는 이벤트
    def lesson_item_select(self):
        self.edit_lesson_no.setText(str(str(self.lesson_item_list.index(self.lessonlist.currentIndex().row(), 0).data())))
        self.edit_lesson_num.setText(self.lesson_item_list.index(self.lessonlist.currentIndex().row(), 1).data())
        self.edit_lesson_name.setText(str(self.lesson_item_list.index(self.lessonlist.currentIndex().row(), 2).data()))

        self.btn_lesson_update.setDisabled(False)
        self.btn_lesson_delete.setDisabled(False)
        self.btn_lesson_insert.setDisabled(True)






class TraineeTab(QWidget):
    def __init__(self):
        super().__init__()
        self.dbConnect()
        self.initUI()
        self.traineeList(self)

    # DB 연동
    def dbConnect(self):
        # DB 연동 pymysql.connect() 메소드 사용 // 예외처리
        try:
            self.conn = pymysql.connect(
                host="127.0.0.1",
                user="manager",
                password="manager",
                db="universitydb",
                port=3306,
                charset="utf8"
            )
        except:
            print("접속 실패!")
            exit(1)
        print("접속 성공!")

        self.uni_cur = self.conn.cursor()  # 연결된 DB에 커서 두기

    #UI
    def initUI(self):
        self.lbl_trainee_register = QLabel("수강 신청", self)
        self.lbl_trainee_register.move(30, 25)

        self.lbl_t_no = QLabel("일련 번호 :", self)
        self.lbl_t_no.move(30, 60)
        self.edit_t_no = QLineEdit(self)
        self.edit_t_no.move(95, 55)
        self.edit_t_no.setDisabled(True)

        self.lbl_sd_num = QLabel('학   번 :', self)
        self.lbl_sd_num.move(30, 90)
        self.edit_sd_num = QLineEdit(self)
        self.edit_sd_num.move(95, 85)


        self.btn_sd_num = QPushButton('학번 확인', self)
        self.btn_sd_num.move(250, 85)
        self.btn_sd_num.clicked.connect(self.check_sd_num)

        self.lbl_t_section = QLabel("학 과 명 :", self)
        self.lbl_t_section.move(30, 120)
        self.edit_t_section = QLineEdit(self)
        self.edit_t_section.move(95, 115)
        self.edit_t_section.setReadOnly(True)

        self.lbl_l_num = QLabel("과목 번호 :", self)
        self.lbl_l_num.move(30, 150)
        self.edit_l_num = QLineEdit(self)
        self.edit_l_num.move(95, 145)
        self.edit_l_num.setReadOnly(True)

        self.lbl_l_division = QLabel("과목 구분 :", self)
        self.lbl_l_division.move(30, 180)
        self.edit_l_division = QLineEdit(self)
        self.edit_l_division.move(95, 175)
        self.edit_l_division.setReadOnly(True)

        self.lbl_t_select = QLabel("수강 과목 선택", self)
        self.lbl_t_select.move(30, 250)

        self.traineeNamecombo = QComboBox(self)
        self.traineeNamecombo.move(100, 275)
        self.traineeNamecombo.activated[str].connect(self.onActivated)

        self.cb1 = QRadioButton('전공', self)
        self.cb1.move(30, 280)
        self.cb1.clicked.connect(self.r_checking)
        self.cb1.setChecked(False)

        self.cb2 = QRadioButton('교양', self)
        self.cb2.move(30, 300)
        self.cb2.clicked.connect(self.r_checking)
        self.cb2.setChecked(False)

        self.lbl_t_list = QLabel("수강 신청 목록", self)
        self.lbl_t_list.move(350, 25)

        self.btn_trainee_insert = QPushButton("등 록", self)
        self.btn_trainee_insert.move(55, 330)
        self.btn_trainee_insert.clicked.connect(self.trainee_insert)

        self.btn_trainee_update = QPushButton("수 정", self)
        self.btn_trainee_update.move(135, 330)
        # self.btn_trainee_update.clicked.connect(self.trainee_edit)

        self.btn_trainee_delete = QPushButton("삭 제", self)
        self.btn_trainee_delete.move(215, 330)
        # self.btn_trainee_delete.clicked.connect(self.lesson_delete)

        self.btn_trainee_init = QPushButton("초 기 화", self)
        self.btn_trainee_init.move(135, 360)
        self.btn_trainee_init.clicked.connect(self.trainee_init)

        #트리뷰
        self.traineelist = QTreeView(self)
        self.traineelist.setRootIsDecorated(False)
        self.traineelist.setAlternatingRowColors(True)
        self.traineelist.resize(800, 450)
        self.traineelist.move(350, 50)

        #해더
        self.trainee_item_list = QStandardItemModel(0, 6, self)
        self.trainee_item_list.setHeaderData(0, Qt.Horizontal, "No")
        self.trainee_item_list.setHeaderData(1, Qt.Horizontal, "학번")
        self.trainee_item_list.setHeaderData(2, Qt.Horizontal, "과목번호")
        self.trainee_item_list.setHeaderData(3, Qt.Horizontal, "과목명")
        self.trainee_item_list.setHeaderData(4, Qt.Horizontal, "과목 구분")
        self.trainee_item_list.setHeaderData(5, Qt.Horizontal, "등록 날짜")

        #트리뷰-수강목록 연결
        self.traineelist.setModel(self.trainee_item_list)

        #트리뷰 클릭 이벤트
        self.traineelist.clicked.connect(self.trainee_item_select)

        self.btn_trainee_delete.setDisabled(True)
        self.btn_trainee_update.setDisabled(True)


    #학번 확인
    def check_sd_num(self):
        if (self.edit_sd_num.text() != ""):
            try:
                self.check_sd_num_sql = "select sd_num from student where sd_num = '{}'"\
                .format(self.edit_sd_num.text())
                print(self.check_sd_num_sql)
                self.uni_cur.execute(self.check_sd_num_sql)

                rs = self.uni_cur.fetchall()

                if (rs != None):
                    QMessageBox.information(self, "학번 체크 성공", "확인되었습니다.",
                                            QMessageBox.Yes, QMessageBox.Yes)

                    s_num = self.edit_sd_num.text()
                    s_num = s_num[2:4]
                    self.subject_sql = "select s_name from subject where s_num = '{}'".format(s_num)
                    self.uni_cur.execute(self.subject_sql)
                    self.conn.commit()
                    r = self.uni_cur.fetchone()[0]
                    self.edit_t_section.setText(r)


                else:
                    self.edit_sd_num.clear()
                    QMessageBox.information(self, "학번 체크 오류", "확인 할수 없는 학번입니다.",
                                            QMessageBox.Yes, QMessageBox.Yes)
                    return
            except:
                QMessageBox.information(self, "학번 체크 오류", "학번을 잘못 입력하셨습니다.",
                                        QMessageBox.Yes, QMessageBox.Yes)
                return
        else:
            QMessageBox.information(self, "학번 체크 오류", "빈칸없이 입력하세요.",
                                    QMessageBox.Yes, QMessageBox.Yes)
            return

    #전공/교양 체크 일때  edit_l_division 말 넣기//콤보박스 바꾸기
    def r_checking(self):
        if self.cb1.isChecked():
            self.edit_l_division.setText("전공")
            self.traineeNamecombo.clear()

            self.trainee_name_sql = "select l_name from lesson where l_num like '%1' order by l_no"
            self.uni_cur.execute(self.trainee_name_sql)
            self.conn.commit()

            rs = self.uni_cur.fetchall()

            trainee_name = rs

            for i in range(len(trainee_name)):
                self.traineeNamecombo.addItem(trainee_name[i][0])

            return trainee_name

        elif self.cb2.isChecked():
            self.edit_l_division.setText("교양")
            self.traineeNamecombo.clear()

            self.trainee_name_sql = "select l_name from lesson where l_num like '%2' order by l_no"
            self.uni_cur.execute(self.trainee_name_sql)
            self.conn.commit()

            rs = self.uni_cur.fetchall()

            trainee_name = rs

            for i in range(len(trainee_name)):
                self.traineeNamecombo.addItem(trainee_name[i][0])

            return trainee_name

    #과목번호 콤보박스 연결된 로드 데이터
    def onActivated(self, text):
        self.sql = "select l_num, l_name from lesson where l_name = '{}'".format(text)
        self.uni_cur.execute(self.sql)
        self.conn.commit()
        s_num = self.uni_cur.fetchall()


        for i in range(len(s_num)):
            r = s_num[i][0]
            self.edit_l_num.setText(r)
            s = s_num[i][1]


    #트리뷰 클릭 이벤트
    def trainee_item_select(self):
        l_division = ''
        print(self.edit_l_num.text())
        # if self.edit_l_num[-1] == 1:
        #     l_division = "전공"
        # elif self.edit_l_num[:-1] == 2:
        #     l_division = "교양"
        self.edit_t_no.setText(str(self.trainee_item_list.index(self.traineelist.currentIndex().row(), 0).data()))
        self.edit_sd_num.setText(str(self.trainee_item_list.index(self.traineelist.currentIndex().row(), 1).data()))
        self.edit_l_num.setText(str(self.trainee_item_list.index(self.traineelist.currentIndex().row(), 2).data()))
        self.edit_t_section.setText(str(self.trainee_item_list.index(self.traineelist.currentIndex().row(), 3).data()))
        self.edit_l_division.setText(l_division)

        self.btn_trainee_delete.setDisabled(False)
        self.btn_trainee_update.setDisabled(False)
        self.btn_trainee_insert.setDisabled(True)

        s_num = self.edit_sd_num.text()
        s_num = s_num[2:4]
        self.subject_sql = "select s_name from subject where s_num = '{}'".format(s_num)
        self.uni_cur.execute(self.subject_sql)
        self.conn.commit()
        r = self.uni_cur.fetchone()[0]
        self.edit_t_section.setText(r)
        print(r)





        # self.edit_l_division.setText(str(self.trainee_item_list.index(self.traineelist.currentIndex().row(), 4).data()))
    #edit 클리어
    def trainee_init(self):
        self.edit_t_no.clear()
        self.edit_sd_num.clear()
        self.edit_t_section.clear()
        self.edit_l_num.clear()
        self.edit_l_division.clear()

        self.btn_trainee_delete.setDisabled(True)
        self.btn_trainee_update.setDisabled(True)
        self.btn_trainee_insert.setDisabled(False)

    #수강 등록
    def trainee_insert(self):
        if (self.edit_sd_num.text() != "") and (self.edit_t_section.text() != "") and (self.edit_l_num.text() != "") and (self.edit_l_division.text() != ""):
            try:
                self.student_list = "select sd_num from student where sd_num = '{}'" \
                .format(self.edit_sd_num.text())
                self.uni_cur.execute(self.student_list)
                self.conn.commit()
                sd_num = self.uni_cur.fetchall()

                self.lesson_list = "select l_num from lesson where l_num = '{}'" \
                .format(self.edit_l_num.text())
                self.uni_cur.execute(self.lesson_list)
                self.conn.commit()
                l_num = self.uni_cur.fetchall()

                self.trainee_insert_sql = "insert into trainee(sd_num, l_num, t_section) values('{}','{}','{}')"\
                .format(sd_num[0][0], l_num[0][0], self.edit_l_division.text())
                print(self.trainee_insert_sql)
                self.uni_cur.execute(self.trainee_insert_sql)
                self.conn.commit()

            except:
                QMessageBox.information(self, "삽입 오류", "올바른 형식으로 입력하세요.",
                                        QMessageBox.Yes, QMessageBox.Yes)
                return
        else:
            QMessageBox.information(self, "입력 오류", "빈칸 없이 입력하세요.",
                                    QMessageBox.Yes, QMessageBox.Yes)
            return
        self.trainee_init()
        self.traineeList(self)

    # def trainee_edit(self):
    #     if (self.edit_l_num.text() != "") and (self.edit_l_division.text() != ""):
    #         try:
    #             self.trainee_update_sql = "update trainee set sd_num, l_num, t_section"

    #트리뷰 수강신청목록 보여주기
    def traineeList(self, QShowEvent):
        self.trainee_sql = "select * from trainee"
        self.uni_cur.execute(self.trainee_sql)
        self.conn.commit()
        rs = self.uni_cur.fetchall()

        for i in range(len(rs)):
            self.trainee_item_list.removeRow(i)
            self.trainee_item_list.insertRow(i)

            self.trainee_item_list.setData(self.trainee_item_list.index(i, 0), rs[i][0])
            self.trainee_item_list.setData(self.trainee_item_list.index(i, 1), rs[i][1])
            self.trainee_item_list.setData(self.trainee_item_list.index(i, 2), rs[i][2])
            self.trainee_item_list.setData(self.trainee_item_list.index(i, 3), rs[i][3])
            self.trainee_item_list.setData(self.trainee_item_list.index(i, 4), rs[i][4])

        self.trainee_item_list.setData(self.trainee_item_list.index(5, 4), rs[5][4])
        self.edit_t_no.clear()
        self.edit_sd_num.clear()
        self.edit_t_section.clear()
        self.edit_l_num.clear()
        self.edit_l_division.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())