# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DBGUI_Launcher_UI.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(590, 380)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(590, 380))
        MainWindow.setMaximumSize(QtCore.QSize(590, 380))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.gridLayout.setContentsMargins(-1, -1, -1, 0)
        self.gridLayout.setVerticalSpacing(6)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.calendarWidget_to = QtGui.QCalendarWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.calendarWidget_to.sizePolicy().hasHeightForWidth())
        self.calendarWidget_to.setSizePolicy(sizePolicy)
        self.calendarWidget_to.setGridVisible(True)
        self.calendarWidget_to.setObjectName(_fromUtf8("calendarWidget_to"))
        self.gridLayout.addWidget(self.calendarWidget_to, 2, 1, 1, 1)
        self.label_from = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_from.setFont(font)
        self.label_from.setObjectName(_fromUtf8("label_from"))
        self.gridLayout.addWidget(self.label_from, 0, 0, 1, 1)
        self.label_to = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_to.setFont(font)
        self.label_to.setObjectName(_fromUtf8("label_to"))
        self.gridLayout.addWidget(self.label_to, 0, 1, 1, 1)
        self.calendarWidget_from = QtGui.QCalendarWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.calendarWidget_from.sizePolicy().hasHeightForWidth())
        self.calendarWidget_from.setSizePolicy(sizePolicy)
        self.calendarWidget_from.setGridVisible(True)
        self.calendarWidget_from.setObjectName(_fromUtf8("calendarWidget_from"))
        self.gridLayout.addWidget(self.calendarWidget_from, 2, 0, 1, 1)
        self.timeEdit_from = QtGui.QTimeEdit(self.centralwidget)
        self.timeEdit_from.setObjectName(_fromUtf8("timeEdit_from"))
        self.gridLayout.addWidget(self.timeEdit_from, 3, 0, 1, 1)
        self.timeEdit_to = QtGui.QTimeEdit(self.centralwidget)
        self.timeEdit_to.setObjectName(_fromUtf8("timeEdit_to"))
        self.gridLayout.addWidget(self.timeEdit_to, 3, 1, 1, 1)
        self.line_2 = QtGui.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout.addWidget(self.line_2, 1, 0, 1, 2)
        self.horizontalLayout.addLayout(self.gridLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        spacerItem = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_output = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_output.setFont(font)
        self.label_output.setObjectName(_fromUtf8("label_output"))
        self.verticalLayout.addWidget(self.label_output)
        self.line = QtGui.QFrame(self.centralwidget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.button_ViewPlayback = QtGui.QCommandLinkButton(self.centralwidget)
        self.button_ViewPlayback.setObjectName(_fromUtf8("button_ViewPlayback"))
        self.verticalLayout.addWidget(self.button_ViewPlayback)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 590, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Launcher", None))
        self.label_from.setText(_translate("MainWindow", "From", None))
        self.label_to.setText(_translate("MainWindow", "To", None))
        self.timeEdit_from.setDisplayFormat(_translate("MainWindow", "h:mm AP", None))
        self.timeEdit_to.setDisplayFormat(_translate("MainWindow", "h:mm AP", None))
        self.label_output.setText(_translate("MainWindow", "UI not initialized", None))
        self.button_ViewPlayback.setText(_translate("MainWindow", "View Playback", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

