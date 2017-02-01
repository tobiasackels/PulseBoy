from PyQt5 import QtCore
from time import sleep
import daqface.DAQ as daq
from PyPulse import PulseInterface
import matplotlib.pyplot as plt
import scipy.io as sio
import numpy as np


class QueueWorker(QtCore.QObject):
    finished = QtCore.pyqtSignal()

    def __init__(self, experiment, get_hardware_params, get_global_params):
        super(self.__class__, self).__init__(None)
        self.experiment = experiment
        self.get_hardware_params = get_hardware_params
        self.get_global_params = get_global_params

    @QtCore.pyqtSlot()
    def trial(self):
        print(self.experiment.current_trial)
        trial_params = self.experiment.arraydata[self.experiment.current_trial][1]
        hardware_params = self.get_hardware_params()
        global_params = self.get_global_params()

        pulses, t = PulseInterface.make_pulse(hardware_params['samp_rate'],
                                              global_params['global_onset'],
                                              global_params['global_offset'],
                                              trial_params)

        trial_daq = daq.DoAiMultiTask(hardware_params['analog_dev'], hardware_params['analog_channels'],
                                      hardware_params['digital_dev'], hardware_params['samp_rate'],
                                      len(t) / hardware_params['samp_rate'], pulses,
                                      hardware_params['sync_clock'])

        analog_data = trial_daq.DoTask()
        print(analog_data)

        self.experiment.advance_trial()

        self.finished.emit()


class QueueController(QtCore.QObject):
    trial_start = QtCore.pyqtSignal()

    def __init__(self, parent, experiment, get_global_params, get_hardware_params, get_export_params):
        super(self.__class__, self).__init__(None)
        self.parent = parent

        self.get_global_params = get_global_params
        self.get_hardware_params = get_hardware_params
        self.get_export_params = get_export_params
        self.experiment = experiment

        self.safe_to_run = True
        self.to_stop = False
        self.prepare_thread()

    def prepare_thread(self):
        self.obj = QueueWorker(self.experiment, self.get_hardware_params, self.get_global_params)
        self.thread = QtCore.QThread()

        self.obj.moveToThread(self.thread)
        self.obj.finished.connect(self.finished)
        self.thread.started.connect(self.obj.trial)

    def start(self):
        if self.safe_to_run:
            self.safe_to_run = False
            self.to_stop = False
            self.thread.start()

    def stop(self):
        self.to_stop = True
        self.experiment.current_trial = 0

    def finished(self):
        self.thread.quit()
        self.thread.wait()
        self.safe_to_run = True

        if self.to_stop:
           pass
        else:
            self.prepare_thread()
            self.start()
