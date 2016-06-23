from PyQt5 import QtCore, QtGui


class ExperimentModel(QtCore.QAbstractTableModel):
    def __init__(self, parent=None, *args):
        QtCore.QAbstractTableModel.__init__(self, parent, *args)
        self.headerdata = ['Active Valves', 'Parameters']
        self.arraydata = [['', '']]

    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        return len(self.arraydata[0])

    def data(self, index, role):
        if not index.isValid():
            return QtCore.QVariant()
        elif role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()
        return QtCore.QVariant(str(self.arraydata[index.row()][index.column()]))

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(self.headerdata[col])
        return QtCore.QVariant()

    def append_row(self, row):
        if self.arraydata[0] == ['', '']:
            self.arraydata[0] = row
        else:
            self.arraydata.append(row)
        self.layoutChanged.emit()

    def remove_row(self, row_i):
        self.arraydata.pop(row_i)
        self.layoutChanged.emit()

    def insert_row(self, row_i, row):
        self.arraydata.insert(row_i, row)
        self.layoutChanged.emit()
