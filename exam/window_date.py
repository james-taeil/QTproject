from datetime import time

from PyQt5.QtCore import QDate, Qt, QTime

# now = QDate.currentDate()
# print(now.toString('d.M.yy'))
# print(now.toString('dd.MM.yyyy'))
# print(now.toString('ddd.MMMM.yyyy'))
# print(now.toString(Qt.ISODate))
# print(now.toString(Qt.DefaultLocaleLongDate))

time = QTime.currentTime()
print(time.toString())

time = QTime.currentTime()
print(time.toString('h.m.s'))
print(time.toString('hh.mm.ss'))
print(time.toString('hh.mm.ss.zzz'))
print(time.toString(Qt.DefaultLocaleLongDate))
print(time.toString(Qt.DefaultLocaleShortDate))