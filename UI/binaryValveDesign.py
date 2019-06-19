# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'BinaryValveWidget.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(848, 76)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        Form.setFont(font)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.removeButton = QtWidgets.QToolButton(Form)
        self.removeButton.setObjectName("removeButton")
        self.gridLayout.addWidget(self.removeButton, 1, 0, 1, 1)
        self.openBinaryDataButton = QtWidgets.QPushButton(Form)
        self.openBinaryDataButton.setObjectName("openBinaryDataButton")
        self.gridLayout.addWidget(self.openBinaryDataButton, 0, 3, 1, 1)
        self.binaryDataLabel = QtWidgets.QLabel(Form)
        self.binaryDataLabel.setObjectName("binaryDataLabel")
        self.gridLayout.addWidget(self.binaryDataLabel, 1, 3, 1, 1)
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 4, 1, 1)
        self.line_2 = QtWidgets.QFrame(Form)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 2, 1, 1, 5)
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        self.onsetEdit = QtWidgets.QLineEdit(Form)
        self.onsetEdit.setObjectName("onsetEdit")
        self.gridLayout.addWidget(self.onsetEdit, 1, 1, 1, 1)
        self.dataSamplingRateEdit = QtWidgets.QLineEdit(Form)
        self.dataSamplingRateEdit.setObjectName("dataSamplingRateEdit")
        self.gridLayout.addWidget(self.dataSamplingRateEdit, 1, 4, 1, 1)
        self.offsetEdit = QtWidgets.QLineEdit(Form)
        self.offsetEdit.setObjectName("offsetEdit")
        self.gridLayout.addWidget(self.offsetEdit, 1, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.removeButton.setText(_translate("Form", "-"))
        self.openBinaryDataButton.setText(_translate("Form", "Open Binary Data"))
        self.binaryDataLabel.setText(_translate("Form", "-"))
        self.label_5.setText(_translate("Form", "Data Sampling Rate"))
        self.label.setText(_translate("Form", "Onset"))
        self.onsetEdit.setText(_translate("Form", "0.1"))
        self.dataSamplingRateEdit.setText(_translate("Form", "10000"))
        self.offsetEdit.setText(_translate("Form", "0.1"))
        self.label_2.setText(_translate("Form", "Offset"))

