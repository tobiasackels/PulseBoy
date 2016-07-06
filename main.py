from PyQt5 import QtWidgets
import sys
import mainDesign
import PBWidgets
import Models.Experiment as Experiment
import numpy as np
import PulseInterface
import QueueControl


# noinspection PyBroadException
class MainApp(QtWidgets.QMainWindow, mainDesign.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        # Setup Experiment Data
        self.trialBankModel = Experiment.ExperimentModel(self)
        self.trialBankTable.setModel(self.trialBankModel)
        self.queue_controller = QueueControl.QueueController(self.trialBankModel.arraydata, self.get_global_params, self.get_hardware_params)

        # Setup Button Bindings
        self.addValveButton.clicked.connect(lambda f: self.add_valve(v_type=self.valveTypeCombo.currentText()))

        self.addTrialButton.clicked.connect(self.add_trial)
        self.updateTrialButton.clicked.connect(self.update_trial)
        self.removeTrialButton.clicked.connect(self.remove_trial)

        self.actionSave.triggered.connect(self.save)
        self.actionLoad.triggered.connect(self.load)

        # self.trialBankTable.clicked.connect(self.trial_selected)
        self.trialBankTable.selectionModel().selectionChanged.connect(self.trial_selected)
        self.queue_controller.thread.start_trigger.connect(self.select_current_trial)

        self.startQueueButton.clicked.connect(self.queue_controller.start_queue)
        self.stopQueueButton.clicked.connect(self.queue_controller.stop_queue)
        self.pauseQueueButton.clicked.connect(self.queue_controller.pause_queue)
        # self.runSelectedButton.clicked.connect(self.queue_controller.run_selected)

    def add_valve(self, v_type='Simple', params=None):
        if v_type == 'Simple':
            new_valve = PBWidgets.SimpleValveWidget(self.valveBankContents)
        elif v_type == 'Noise':
            new_valve = PBWidgets.NoiseValveWidget(self.valveBankContents)
        else:
            new_valve = PBWidgets.SimpleValveWidget(self.valveBankContents)

        if params is not None:
            new_valve.set_parameters(params)
        self.valveBankContents.layout().addWidget(new_valve)

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

    def update_trial(self):
        selected_trial = self.trialBankTable.selectionModel().selectedRows()[0].row()
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
            self.trialBankModel.update_row(selected_trial, [n_valves, all_params])

    def remove_trial(self):
        selected_trial = self.trialBankTable.selectionModel().selectedRows()[0].row()
        self.trialBankModel.remove_row(selected_trial)

    def trial_selected(self):
        try:
            selected_trial = self.trialBankTable.selectionModel().selectedRows()[0].row()
            trial_params = self.trialBankModel.arraydata[selected_trial][1]

            pulses, t = PulseInterface.make_pulse(float(self.sampRateEdit.text()),
                                                  float(self.globalOnsetEdit.text()),
                                                  float(self.globalOffsetEdit.text()), trial_params)

            self.graphicsView.plotItem.clear()
            for p, pulse in enumerate(pulses):
                self.graphicsView.plotItem.plot(t, np.array(pulse) - (p * 1.1))

            self.update_valve_bank(selected_trial)
        except:
            pass

    def select_current_trial(self):
        self.trialBankTable.selectRow(self.queue_controller.current_trial)

    def update_valve_bank(self, trial_idx):
        for widget in self.valveBankContents.children():
            try:
                widget.remove_from_parent()
            except:
                pass

        for valve in self.trialBankModel.arraydata[trial_idx][1]:
            self.add_valve(v_type=valve['type'], params=valve)

    def save(self):
        fname = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", "", ".trialbank")
        self.trialBankModel.save_arraydata(fname)

    def load(self):
        fname, suff = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", '', '*.trialbank')
        print(fname)
        self.trialBankModel.load_arraydata(fname)

    def get_hardware_params(self):
        params = dict()
        params['analog_dev'] = self.analogInDevEdit.text()
        params['analog_channels'] = int(self.analogChannelsEdit.text())
        params['digital_dev'] = self.digitalOutDevEdit.text()
        params['digital_channels'] = int(self.digitalChannelsEdit.text())
        params['sync_clock'] = self.syncClockEdit.text()
        params['samp_rate'] = float(self.sampRateEdit.text())

        return params

    def get_global_params(self):
        params = dict()
        params['global_onset'] = float(self.globalOnsetEdit.text())
        params['global_offset'] = float(self.globalOffsetEdit.text())

        return params

# Back up the reference to the exceptionhook
sys._excepthook = sys.excepthook


def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)

# Set the exception hook to our wrapping function
sys.excepthook = my_exception_hook


def main():
    app = QtWidgets.QApplication(sys.argv)
    form = MainApp()
    form.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
