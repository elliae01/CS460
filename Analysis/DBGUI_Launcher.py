from PyQt4 import QtCore, QtGui
from DBGUI_Launcher_UI import Ui_MainWindow
from DBGUI import DBGUI_main
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
	def __init__(self, ui):
		# # # Register event listeners # # #

		self.ui = ui
		self.ui.calendarWidget_from.clicked.connect(self.setDateFrom)
		self.ui.calendarWidget_to.clicked.connect(self.setDateTo)
		self.ui.timeEdit_from.timeChanged.connect(self.setTimeFrom)
		self.ui.timeEdit_to.timeChanged.connect(self.setTimeTo)
		self.ui.button_ViewPlayback.clicked.connect(self.buttonPlayback)

		# # # Constants # # #

		# Minimum time difference allowed for an analysis
		self.minDiffMinutes = 2
		# Date format when displaying dates in output message
		self.dateTimeFormat = "yyyy-MM-dd h:mm AP"
		# Date format when requesting data from server
		self.dateTimeFormatServer = "yyyy-MM-dd hh:mm:ss.zzz"

		# # # Set default dates # # #

		self.dateTimeTo = QtCore.QDateTime.currentDateTime()
		# set interval to the minimum length in past from current time
		self.dateTimeFrom = self.dateTimeTo.addSecs(-self.minDiffMinutes*60)

		# # # Sync GUI # # #

		self.ui.calendarWidget_from.setSelectedDate(self.dateTimeFrom.date())
		self.ui.timeEdit_from.setTime(self.dateTimeFrom.time())

		self.ui.calendarWidget_to.setSelectedDate(self.dateTimeTo.date())
		self.ui.timeEdit_to.setTime(self.dateTimeTo.time())

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

	def buttonPlayback(self):
		# Check for valid date range
		if(self.dateTimeFrom.addSecs(self.minDiffMinutes*60) > self.dateTimeTo):
			self.setMessage("Date range invalid.")
			return

		# Launch the DBGUI playback analyzer
		if(DBGUI_main(self.dateTimeFrom.toString(self.dateTimeFormatServer), self.dateTimeTo.toString(self.dateTimeFormatServer))):
			# Date selection is bad, update GUI to reflect
			self.setMessage("Date range has no data.")

	def setMessage(self, text):
		self.ui.label_output.setText(text)

	def updateMessageDate(self):
		self.setMessage("From <b>{}</b> to <b>{}</b>".format(self.dateTimeFrom.toString(self.dateTimeFormat), self.dateTimeTo.toString(self.dateTimeFormat)))

	def checkDates(self):
		pass

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

	# Handler setup
	handler = ChangedHandler(ui)


	try:
		MainWindow.show()
		sys.exit(app.exec_())
		print("Application window closed", flush=True)
	except Exception as e:
		print(e)
