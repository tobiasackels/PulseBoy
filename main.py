from PyQt5 import QtWidgets
import sys
import mainDesign
import PBWidgets
import Models.Experiment as Experiment
import numpy as np
import PulseGeneration


# noinspection PyBroadException
class MainApp(QtWidgets.QMainWindow, mainDesign.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        # Setup Experiment Data
        self.trialBankModel = Experiment.ExperimentModel(self)
        self.trialBankTable.setModel(self.trialBankModel)

        # Setup Button Bindings
        self.addValveButton.clicked.connect(lambda f: self.add_valve(v_type=self.valveTypeCombo.currentText()))
        self.addTrialButton.clicked.connect(self.add_trial)
        self.trialBankTable.clicked.connect(self.trial_selected)

    def add_valve(self, v_type='Simple'):
        if v_type == 'Simple':
            self.valveBankContents.layout().addWidget(PBWidgets.SimpleValveWidget(self.valveBankContents))
        elif v_type == 'Noise':
            self.valveBankContents.layout().addWidget(PBWidgets.NoiseValveWidget(self.valveBankContents))

    def add_trial(self):
        n_valves = 0
        all_params = list()
        for valve in self.valveBankContents.children():
            try:
                params = valve.get_parameters()
                all_params.append(params)
                n_valves += 1
            except:
                pass

        if n_valves > 0:
            self.trialBankModel.append_row([n_valves, all_params])

    def trial_selected(self):
        selected_trial = self.trialBankTable.selectionModel().selectedRows()[0].row()
        trial_params = self.trialBankModel.arraydata[selected_trial][1]

        pulses, t = PulseGeneration.multi_simple_pulse(float(self.sampRateEdit.text()),
                                                       float(self.globalOnsetEdit.text()),
                                                       float(self.globalOffsetEdit.text()), trial_params)

        self.graphicsView.plotItem.clear()
        for p, pulse in enumerate(pulses):
            self.graphicsView.plotItem.plot(t, np.array(pulse) - (p * 1.1))


def main():
    app = QtWidgets.QApplication(sys.argv)
    form = MainApp()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
