# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 10:21:35 2021

@author: webst
"""

from PyQt5.QtWidgets import QFileDialog
import NuDAS



class Ui_MainWindow(object):
    # gui+
    def __init__(self):
        self.nudas = NuDAS()
        self.stimulus_file_path = ""
        self.spike_times_file_path = ""

    def setupUi(self, MainWindow):
        # gui+
        # File connections
        self.actionOpenStimulus.triggered. \
            connect(lambda: self.open_file_dialog("Open Stimulus File", "Image Files (*.mat)", 0))
        self.actionOpenActionPotentials.triggered. \
            connect(lambda: self.open_file_dialog("Open Action Potential File", "Image Files (*.mat)", 1))

        # Tools connections
        self.actionBinning.triggered. \
            connect(lambda: self.bin_data())

    # gui+
    def open_file_dialog(self, c, f, dialog_type):
        if dialog_type == 0:
            self.stimulus_file_path, x = QFileDialog.getOpenFileName(self.centralwidget,
                                                                     c,
                                                                     "/home",
                                                                     f)
            print(self.stimulus_file_path)
            self.nudas.load_stimulus(self.stimulus_file_path)
        elif dialog_type == 1:
            self.spike_times_file_path, x = QFileDialog.getOpenFileName(self.centralwidget,
                                                                        c,
                                                                        "/home",
                                                                        f)
            print(self.spike_times_file_path)
            self.nudas.load_spike_times(self.spike_times_file_path)

    # gui+
    # c is for comb. it's like some kind of matplotlib backend for embedding graphs
    def bin_data(self, c=0):
        if self.stimulus_file_path == "" or self.spike_times_file_path == "":
            msg = "First, you must load the stimulus and action potential data (which can be accessed under the " + \
                  "File menu) to bin any data"
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setText(msg)
            msg_box.exec_()
        else:
            # TODO tw or time_window will have to be a user specified value from the GUI
            # we also likely require input for which neuron you would like to do binning on and which stimulus
            # trial we are currently using
            stimulus_trial_idx = 0
            neuron_idx = 0
            tw = 1
            dmr = 1
            bin_window = tw * 0.001
            # neural_data_path = np.load('./neural_data_path.npy', allow_pickle=True)
            # neural_data_path = str(neural_data_path)
            # print('path:::' + neural_data_path)

            self.nudas.bin_spike_matrix(neuron_idx, 1000, False)
            # ALL OF THIS BELOW HERE IS PLOTTING THE RESULT FROM spike_matrix
            # # fig = Figure(figsize = (5, 5),dpi = 100)
            # c = comb[1]
            # fig = comb[0]
            # plot1 = fig.add_subplot(111)
            # plt.title('Density plot (time window=' + str(tw) + ' ms')
            # plot1.clear()
            # plot1.imshow(spt_mat, origin='lower left', aspect='auto', interpolation=None, cmap='cividis')
            # # canvas = FigureCanvasTkAgg(fig,master = root,tag={'cvs'})
            # c.draw()
            # # placing the canvas on the Tkinter window
            # c.get_tk_widget().pack()
            # # canvas.delete('all')
            # np.save('spike_matrix.npy', spt_mat)