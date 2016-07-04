from PyQt5 import QtCore
from time import sleep


class QueueLoop(QtCore.QThread):
    def __init__(self, queue_controller):
        QtCore.QThread.__init__(self)

        self.queue_controller = queue_controller

    trigger = QtCore.pyqtSignal()

    def run(self):
        while self.queue_controller.should_run:
            # do all the trial stuff
            print(self.queue_controller.current_trial, self.queue_controller.trial_list[self.queue_controller.current_trial])
            sleep(1)

            # signal end of trial and break to the next thread
            self.trigger.emit()
            break

    def run_selected(self, trial):
        if self.queue_controller.should_run:
            # do all the trial stuff

            self.trigger.emit()


class QueueController:
    def __init__(self, trial_list):
        self.trial_list = trial_list
        self.current_trial = 0
        self.should_run = False
        self.thread = QueueLoop(self)
        self.thread.trigger.connect(self.finish_trial)

    def start_queue(self):
        if not self.should_run:
            self.should_run = True
            self.thread.start()

    def pause_queue(self):
        if self.should_run:
            self.should_run = False
            self.current_trial += 1

    def stop_queue(self):
        if self.should_run:
            self.should_run = False
            self.current_trial = 0

    def run_selected(self, trial):
        if not self.should_run:
            self.should_run = True
            self.thread.run_selected(trial)
            self.should_run = False

    def finish_trial(self):
        # stuff that happens when a trial finished
        if self.should_run:
            self.current_trial += 1

            if self.current_trial < len(self.trial_list):
                self.thread.start()
            else:
                self.stop_queue()


