from PyQt5 import QtCore
from time import sleep
import daqface.DAQ as daq
from PyPulse import PulseInterface
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

            self.queue_controller.should_run = False
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
            self.current_trial = 0
            self.thread.start()

    def pause_queue(self):
        if self.should_run:
            self.should_run = False
            self.current_trial += 1

    def stop_queue(self):
        self.thread.exit()
        if self.should_run:
            self.should_run = False
            self.current_trial = 0

    def run_selected(self, trial):
        if not self.should_run:
            self.current_trial = trial
            self.should_run = True
            self.thread.run_selected(trial)

    def finish_trial(self):
        # stuff that happens when a trial finished
        self.thread.exit()
        if self.should_run:
            self.current_trial += 1

            if self.current_trial < len(self.trial_list):
                self.thread.start()
            else:
                self.stop_queue()


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

                # trial_daq = daq.DoAiMultiTask(hardware_params['analog_dev'], hardware_params['analog_channels'],
                #                               hardware_params['digital_dev'], hardware_params['samp_rate'],
                #                               len(t) / hardware_params['samp_rate'], pulses, hardware_params['sync_clock'])
                #
                # analog_data = trial_daq.DoTask()

                self.trial_end.emit()
                sleep(1)

        self.finished.emit()
        print("donzo")


class QueueControllerExperimental:
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
            self.start()
        else:
            self.stop()

