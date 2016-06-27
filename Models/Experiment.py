from PyQt5 import QtCore, QtGui
import pickle as pickle


class ExperimentModel(QtCore.QAbstractTableModel):
    def __init__(self, parent=None, *args):
        QtCore.QAbstractTableModel.__init__(self, parent, *args)
        self.headerdata = ['Active Valves', 'Parameters']
        self.arraydata = [[0, []]]

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
        if self.arraydata[0] == [0, []]:
            self.arraydata[0] = row
        else:
            self.arraydata.append(row)
        self.layoutChanged.emit()

    def update_row(self, idx, row):
        self.arraydata[idx] = row
        self.layoutChanged.emit()

    def remove_row(self, row_i):
        if len(self.arraydata) < 2:
            self.arraydata = [[0, []]]
        else:
            self.arraydata.pop(row_i)
        self.layoutChanged.emit()

    def insert_row(self, row_i, row):
        self.arraydata.insert(row_i, row)
        self.layoutChanged.emit()

    def append_valve(self, row, valve_params):
        self.arraydata[row][0] += 1
        self.arraydata[row][1].append(valve_params)
        self.layoutChanged.emit()

    def load_arraydata(self, file_conf):
        with open(file_conf, 'rb') as fn:
            arraydata = pickle.load(fn)

        self.arraydata = arraydata
        self.layoutChanged.emit()

    def save_arraydata(self, file_conf):
        with open(file_conf[0] + file_conf[1], 'wb') as fn:
            pickle.dump(self.arraydata, fn)



