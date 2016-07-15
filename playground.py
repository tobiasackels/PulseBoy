from PyQt5 import QtGui, QtCore, QtWidgets
import sys

my_array = [['00','01','02'],
            ['10','11','12'],
            ['20','21','22']]


def main():
    app = QtWidgets.QApplication(sys.argv)
    w = MyWindow()
    w.show()
    sys.exit(app.exec_())


class MyWindow(QtWidgets.QWidget):
    def __init__(self, *args):
        QtWidgets.QWidget.__init__(self, *args)

        tablemodel = MyTableModel(my_array, self)
        tableview = QtWidgets.QTableView()
        tableview.setModel(tablemodel)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(tableview)
        self.setLayout(layout)


class MyTableModel(QtCore.QAbstractTableModel):
    def __init__(self, datain, parent=None, *args):
        QtCore.QAbstractTableModel.__init__(self, parent, *args)
        self.arraydata = datain

    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        return len(self.arraydata[0])

    def data(self, index, role):
        if not index.isValid():
            return QtCore.QVariant()
        elif role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()
        return QtCore.QVariant(self.arraydata[index.row()][index.column()])

if __name__ == "__main__":
    main()