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
        self.offsetEdit = QtWidgets.QLineEdit(Form)
        self.offsetEdit.setObjectName("offsetEdit")
        self.gridLayout.addWidget(self.offsetEdit, 1, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)
        self.valuetobinariseEdit = QtWidgets.QLineEdit(Form)
        self.valuetobinariseEdit.setObjectName("valuetobinariseEdit")
        self.gridLayout.addWidget(self.valuetobinariseEdit, 1, 5, 1, 1)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 5, 1, 1)
        self.shatterEdit = QtWidgets.QLineEdit(Form)
        self.shatterEdit.setObjectName("shatterEdit")
        self.gridLayout.addWidget(self.shatterEdit, 1, 6, 1, 1)
        self.onsetEdit = QtWidgets.QLineEdit(Form)
        self.onsetEdit.setObjectName("onsetEdit")
        self.gridLayout.addWidget(self.onsetEdit, 1, 1, 1, 1)
        self.removeButton = QtWidgets.QToolButton(Form)
        self.removeButton.setObjectName("removeButton")
        self.gridLayout.addWidget(self.removeButton, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        self.line_2 = QtWidgets.QFrame(Form)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 2, 1, 1, 6)
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 0, 6, 1, 1)
        self.binsizeEdit = QtWidgets.QLineEdit(Form)
        self.binsizeEdit.setObjectName("binsizeEdit")
        self.gridLayout.addWidget(self.binsizeEdit, 1, 4, 1, 1)
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 3, 1, 1)
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 4, 1, 1)
        self.numofbinsEdit = QtWidgets.QLineEdit(Form)
        self.numofbinsEdit.setObjectName("numofbinsEdit")
        self.gridLayout.addWidget(self.numofbinsEdit, 1, 3, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.offsetEdit.setText(_translate("Form", "0.1"))
        self.label_2.setText(_translate("Form", "Offset"))
        self.valuetobinariseEdit.setText(_translate("Form", "2"))
        self.label_3.setText(_translate("Form", "Value to binarise"))
        self.shatterEdit.setText(_translate("Form", "500"))
        self.onsetEdit.setText(_translate("Form", "0.1"))
        self.removeButton.setText(_translate("Form", "-"))
        self.label.setText(_translate("Form", "Onset"))
        self.label_6.setText(_translate("Form", "Shatter (Hz)"))
        self.binsizeEdit.setText(_translate("Form", "0.05"))
        self.label_4.setText(_translate("Form", "Number of bins"))
        self.label_5.setText(_translate("Form", "Bin size"))
        self.numofbinsEdit.setText(_translate("Form", "8"))

