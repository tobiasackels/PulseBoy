from PyQt5 import QtCore
from time import sleep
import daqface.DAQ as daq
import PulseInterface
import matplotlib.pyplot as plt
import scipy.io as sio
import numpy as np


class QueueLoop(QtCore.QThread):
    def __init__(self, queue_controller):
        QtCore.QThread.__init__(self)

        self.queue_controller = queue_controller
        self.analog_data = []

    finish_trigger = QtCore.pyqtSignal()
    start_trigger = QtCore.pyqtSignal()

    def run(self):
        while self.queue_controller.should_run:
            self.start_trigger.emit()

            # do all the trial stuff
            self.do_trial(self.queue_controller.current_trial)

            # signal end of trial and break to the next thread
            self.finish_trigger.emit()
            break

    def run_selected(self, trial):
        if self.queue_controller.should_run:
            self.start_trigger.emit()

            # do all the trial stuff
            self.do_trial(trial)

            self.finish_trigger.emit()

    def do_trial(self, trial):
        trial_params = self.queue_controller.trial_list[self.queue_controller.current_trial][1]
        hardware_params = self.queue_controller.get_hardware_params()
        global_params = self.queue_controller.get_global_params()
        export_params = self.queue_controller.get_export_params()

        pulses, t = PulseInterface.make_pulse(hardware_params['samp_rate'],
                                              global_params['global_onset'],
                                              global_params['global_offset'],
                                              trial_params)

        trial_daq = daq.DoAiMultiTask(hardware_params['analog_dev'], hardware_params['analog_channels'],
                                      hardware_params['digital_dev'], hardware_params['samp_rate'],
                                      len(t) / hardware_params['samp_rate'], pulses, hardware_params['sync_clock'])

        self.analog_data = trial_daq.DoTask()

#       Save data
        save_string = export_params['export_path'] + str(trial) + export_params['export_suffix'] + '.mat'
        sio.savemat(save_string, {'analog_data': self.analog_data, 'pulses': pulses, 't': t})


class QueueController:
    def __init__(self, trial_list, get_global_params, get_hardware_params, get_export_params):
        self.trial_list = trial_list
        self.current_trial = 0
        self.should_run = False
        self.thread = QueueLoop(self)
        self.thread.finish_trigger.connect(self.finish_trial)

        # getter functions for global parameters
        self.get_global_params = get_global_params
        self.get_hardware_params = get_hardware_params
        self.get_export_params = get_export_params

    def start_queue(self):
        if not self.should_run:
            self.should_run = True
            self.thread.start()

    def pause_queue(self):
        if self.should_run:
            self.should_run = False
            self.current_trial += 1

    def stop_queue(self):
        self.thread.exit() # not sure if needed
        if self.should_run:
            self.should_run = False
            self.current_trial = 0

    def run_selected(self, trial):
        if not self.should_run:
            self.current_trial = trial
            self.should_run = True
            self.thread.run_selected(trial)
            self.should_run = False

    def finish_trial(self):
        # stuff that happens when a trial finished
        self.thread.exit() # not sure if needed
        if self.should_run:
            self.current_trial += 1

            if self.current_trial < len(self.trial_list):
                self.thread.start()
            else:
                self.stop_queue()


