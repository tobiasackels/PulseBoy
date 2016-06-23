from PyQt5 import QtWidgets
import simpleValveDesign
import noiseValveDesign
import trialDesign


# TODO - These widgets could inherit from a common PBWidget parent that implements remove_from_parent etc.
class SimpleValveWidget(QtWidgets.QWidget, simpleValveDesign.Ui_Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        self.parent = parent

        self.removeButton.clicked.connect(self.remove_from_parent)

    def remove_from_parent(self):
        self.parent.layout().removeWidget(self)
        self.deleteLater()

    def get_parameters(self):
        params = dict()

        params['type'] = 'simple'

        params['fromValues'] = bool(self.fromValuesRadio.isChecked())
        params['fromDuty'] = bool(self.fromDutyRadio.isChecked())
        params['isClean'] = bool(self.cleanRadio.isChecked())
        params['isShatter'] = bool(self.shatterRadio.isChecked())
        params['fromRepeats'] = bool(self.repeatsRadio.isChecked())
        params['fromLength'] = bool(self.lengthRadio.isChecked())

        params['onset'] = float(self.onsetEdit.text())
        params['offset'] = float(self.offsetEdit.text())
        params['pulse_width'] = float(self.pulseWidthEdit.text())
        params['pulse_delay'] = float(self.pulseDelayEdit.text())
        params['frequency'] = float(self.frequencyEdit.text())
        params['duty'] = float(self.pulseDutyEdit.text()) * 0.01
        params['shatter_frequency'] = float(self.shatterHzEdit.text())
        params['shatter_duty'] = float(self.shatterDutyEdit.text()) * 0.01
        params['repeats'] = int(self.repeatsEdit.text())
        params['length'] = float(self.lengthEdit.text())

        return params


class NoiseValveWidget(QtWidgets.QWidget, noiseValveDesign.Ui_Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        self.parent = parent

        self.removeButton.clicked.connect(self.remove_from_parent)

    def remove_from_parent(self):
        self.parent.layout().removeWidget(self)
        self.deleteLater()

    def get_parameters(self):
        params = dict()

        params['type'] = 'simple'

        params['fromRepeats'] = bool(self.repeatsRadio.isChecked())
        params['fromLength'] = bool(self.lengthRadio.isChecked())

        params['onset'] = float(self.onsetEdit.text())
        params['offset'] = float(self.offsetEdit.text())
        params['frequency'] = float(self.frequencyEdit.text())
        params['seed'] = float(self.seedEdit.text())
        params['amp_min'] = float(self.ampMinEdit.text()) * 0.01
        params['amp_max'] = float(self.ampMaxEdit.text()) * 0.01
        params['repeats'] = int(self.repeatsEdit.text())
        params['length'] = float(self.lengthEdit.text())

        return params


class TrialWidget(QtWidgets.QWidget, trialDesign.Ui_Form):
    def __init__(self, n_valves, parent=None):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        self.parent = parent

        self.removeButton.clicked.connect(self.remove_from_parent)

        self.activeValvesEdit.setText(str(n_valves))

    def remove_from_parent(self):
        self.parent.layout().removeWidget(self)
        self.close()
