from PyQt5 import QtCore
from time import sleep
import daqface.DAQ as daq
from PyPulse import PulseInterface
import matplotlib.pyplot as plt
import scipy.io as sio
import numpy as np


class QueueWorker(QtCore.QObject):
    finished = QtCore.pyqtSignal()
    trial_end = QtCore.pyqtSignal()
    trial_start = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(None)
        self.parent = parent

    def trial(self):
        while self.parent.current_trial < len(self.parent.trial_list) and self.parent.should_run:
            if self.parent.should_run:

                self.trial_start.emit()
                print("doing trial " + str(self.parent.current_trial))

                trial_params = self.parent.trial_list[self.parent.current_trial][1]
                hardware_params = self.parent.get_hardware_params()
                global_params = self.parent.get_global_params()
                export_params = self.parent.get_export_params()

                pulses, t = PulseInterface.make_pulse(hardware_params['samp_rate'],
                                                      global_params['global_onset'],
                                                      global_params['global_offset'],
                                                      trial_params)

                trial_daq = daq.DoAiMultiTask(hardware_params['analog_dev'], hardware_params['analog_channels'],
                                              hardware_params['digital_dev'], hardware_params['samp_rate'],
                                              len(t) / hardware_params['samp_rate'], pulses, hardware_params['sync_clock'])

                analog_data = trial_daq.DoTask()

                sleep(1)

                self.trial_end.emit()

            sleep(1)

        self.finished.emit()
        print("donzo")


class QueueController:
    def __init__(self, parent, trial_list, get_global_params, get_hardware_params, get_export_params):
        self.parent = parent
        self.trial_list = trial_list
        self.current_trial = 0

        self.get_global_params = get_global_params
        self.get_hardware_params = get_hardware_params
        self.get_export_params = get_export_params

        self.thread = QtCore.QThread()
        self.trial_job = QueueWorker(self)
        self.trial_job.moveToThread(self.thread)

        self.thread.finished.connect(self.thread.quit)
        self.thread.started.connect(self.trial_job.trial)
        self.trial_job.trial_end.connect(self.trial_end)

        self.should_run = False

    def start(self):
        if not self.should_run:
            self.should_run = True
            self.thread.start()

    def stop(self):
        self.should_run = False
        self.thread.terminate()
        self.thread.wait()
        self.current_trial = 0

    def pause(self):
        if self.should_run:
            self.should_run = False
            self.thread.terminate()
            self.thread.wait()

    def trial_end(self):
        self.should_run = False
        if (self.current_trial+1) < len(self.trial_list):
            self.current_trial += 1
            # self.start()
            self.should_run = True
        else:
            self.stop()

