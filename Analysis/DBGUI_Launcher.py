from PyQt4 import QtCore, QtGui
from DBGUI_Launcher_UI import Ui_MainWindow
from DBGUI import DBGUI_main, DBGUI_init
import pandas as pd
from datetime import datetime
import time
import sys

try:
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s

try:
	_encoding = QtGui.QApplication.UnicodeUTF8
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig)

class ChangedHandler:
	def __init__(self, ui, sessions):
		# # # Register event listeners # # #

		self.ui = ui
		self.currentTab = 0

		# Tab Date Range
		self.ui.calendarWidget_from.clicked.connect(self.setDateFrom)
		self.ui.calendarWidget_to.clicked.connect(self.setDateTo)
		self.ui.timeEdit_from.timeChanged.connect(self.setTimeFrom)
		self.ui.timeEdit_to.timeChanged.connect(self.setTimeTo)
		self.ui.button_ViewPlayback.clicked.connect(self.buttonPlayback)

		# Tab Sessions
		self.ui.tableWidget_sessions.clicked.connect(self.sessionHandler)
		self.ui.tabWidget.currentChanged.connect(self.tabSwitch)
		print("Number of rows of Sessions is ",len(sessions))
		self.ui.tableWidget_sessions.setRowCount(len(sessions))
		self.ui.tableWidget_sessions.setColumnCount(3)

		self.ui.tableWidget_sessions.setHorizontalHeaderLabels("Start Time;End Time;Distance (Inches)".split(";"))
		# self.ui.tableWidget_sessions.setVerticalHeaderLabels("1;2;3;4".split(";"))

		self.sessions = sessions
		self.selectedRowEvent = 0
		self.fillRows(self.sessions)

		# # # Constants # # #

		# Minimum time difference allowed for an analysis
		self.minDiffSeconds = 30
		# Date format when requesting data from server
		self.dateTimeFormatServer = "yyyy-MM-dd hh:mm:ss.zzz"
		# Date format when displaying dates in output message
		# self.dateTimeFormat = "yyyy-MM-dd h:mm AP"
		self.dateTimeFormat = "yyyy MM dd, hh:mm:ss"

		# # # Set default dates # # #

		self.dateTimeTo = QtCore.QDateTime.currentDateTime()
		# set interval to the minimum length in past from current time
		self.dateTimeFrom = self.dateTimeTo.addSecs(-self.minDiffSeconds)

		self.loadDefaultTimes()

		# # # Sync GUI # # #

		self.ui.calendarWidget_from.setSelectedDate(self.dateTimeFrom.date())
		self.ui.timeEdit_from.setTime(self.dateTimeFrom.time())

		self.ui.calendarWidget_to.setSelectedDate(self.dateTimeTo.date())
		self.ui.timeEdit_to.setTime(self.dateTimeTo.time())

		self.updateMessageDate()

	def fillRows(self, arr):
		print("Array: ",arr)

		index = 0
		while(index < len(arr)):
			self.addRow(index, arr[index][0], arr[index][1], arr[index][2])
			index = index + 1

	def addRow(self, index, col1, col2, col3):
		self.ui.tableWidget_sessions.setItem(index,0, QtGui.QTableWidgetItem(col1))
		self.ui.tableWidget_sessions.setItem(index,1, QtGui.QTableWidgetItem(col2))
		self.ui.tableWidget_sessions.setItem(index,2, QtGui.QTableWidgetItem(col3))

	def setDateFrom(self,dateChosen):
		self.dateTimeFrom.setDate(dateChosen)
		self.updateMessageDate()

	def setTimeFrom(self, timeChosen):
		self.dateTimeFrom.setTime(timeChosen)
		self.updateMessageDate()

	def setDateTo(self, dateChosen):
		self.dateTimeTo.setDate(dateChosen)
		self.updateMessageDate()

	def setTimeTo(self, timeChosen):
		self.dateTimeTo.setTime(timeChosen)
		self.updateMessageDate()

	# Listens for switching of tabs
	def tabSwitch(self, val):
		print("Tab was changed to: ", val)
		self.currentTab = val

	def sessionHandler(self, val):
		# QtCore.QModelIndex.column()
		print("Table row: ",val.row())
		self.selectedRowEvent = val

	def buttonPlayback(self):
		start = self.dateTimeFrom.toString(self.dateTimeFormatServer)
		end = self.dateTimeTo.toString(self.dateTimeFormatServer)
		if(self.currentTab == 0):
			# Check for valid date range
			if(self.dateTimeFrom.addSecs(self.minDiffSeconds) > self.dateTimeTo):
				self.setMessage("Date range invalid.")
				return
		elif(self.currentTab == 1):
			# self.ui.tableWidget_sessions.emit()
			temp = self.sessions[self.selectedRowEvent.row()]

			print(temp[0]," to ", temp[1])
			start = temp[0]
			end = temp[1]
			# self.setDateFrom(tempSt)
			# self.setTimeFrom()
			#
			# self.setDateTo()
			# self.setTimeTo()

		# print("Sent datetimes: ",self.dateTimeFrom.toString(self.dateTimeFormatServer), self.dateTimeTo.toString(self.dateTimeFormatServer))
		T = DBGUI_init(start, end)

		# Launch the DBGUI playback analyzer
		if(DBGUI_main(T)):
			# Date selection is bad, update GUI to reflect
			self.setMessage("Date range has no data.")

	def setMessage(self, text):
		self.ui.label_output.setText(text)

	# Updates the messages shown to user after date is chosen
	def updateMessageDate(self):
		self.setMessage("From <b>{}</b> to <b>{}</b>".format(self.dateTimeFrom.toString(self.dateTimeFormat), self.dateTimeTo.toString(self.dateTimeFormat)))

	def saveDefaultTimes(self):
		# if(self.savedStartDate is None or self.savedEndDate is None):
		# 	self.savedStartDate
		# 	pass
		try:
			file = open('Times.txt', 'w')
			file.writelines(str(self.dateTimeFrom.toString(self.dateTimeFormatServer)))
			file.writelines("\n")
			file.writelines(str(self.dateTimeTo.toString(self.dateTimeFormatServer)))
			file.close()
		except:
			print("INFO [ChangedHandler:saveDefaultTimes]: Could not save default times file")

	def loadDefaultTimes(self):
		try:
			file = open('Times.txt', 'r')
			temp1 = file.readline().strip()
			temp2 = file.readline().strip()
			# print("from",temp1)
			# print("to",temp2)
			self.dateTimeFrom = QtCore.QDateTime.fromString(temp1, self.dateTimeFormatServer)
			self.dateTimeTo = QtCore.QDateTime.fromString(temp2, self.dateTimeFormatServer)
			# print("from {} to {}".format(self.dateTimeFrom, self.dateTimeTo))
			file.close()
		except:
			print("INFO [ChangedHandler:loadDefaultTimes]: Could not open default times file")

if __name__ == "__main__":

	### Qt ###

	# initialize
	app = QtGui.QApplication(sys.argv)
	MainWindow = QtGui.QMainWindow()

	# add method to insert display into generated UI class
	# Ui_MainWindow.insertContent = insertContent

	# create GUI object
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)

	# Make temporary object to get all sessions from database so GUI can have list in sessions tab (second tab)
	T = DBGUI_init(pd.to_datetime(0), datetime.now())
	sessions = T.getSessions(sessionGapMinutes=2)

	# Handler setup
	handler = ChangedHandler(ui, sessions)
	app.aboutToQuit.connect(handler.saveDefaultTimes)

	try:
		MainWindow.show()
		sys.exit(app.exec_())
		print("Application window closed", flush=True)
	except Exception as e:
		print(e)
