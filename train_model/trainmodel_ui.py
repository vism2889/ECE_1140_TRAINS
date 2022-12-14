##############################################################################
# AUTHOR(S):    Sushmit Acharya
# DATE:         11/14/2022
# FILENAME:     trainmodel_ui.py
# DESCRIPTION:
#  Primary Train Model UI that runs the Train Model UI
##############################################################################


# from train import Train
import sys

from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
# from DispatchPopUp import DispatchPopUp
# from MiniOffice import Ui_MainWindow
# from LayoutParser import LayoutParser
import sys
import os
import time
from train import Train



class TrainModel(QtWidgets.QMainWindow):
    '''Primary Train Model UI Window that contains all childs/widgets'''
    trainDict = {}
    blockList = None

    def __init__(self, ui, hw, signals):
        super().__init__()
        # path = os.getcwd()+'\\train_model\\train.ui'
        uic.loadUi(ui, self)
        self.t = Train()
        self.hw = hw

        if self.hw:
            from Server_Comm import MyPub, MySub
            self.mp = MyPub(self.t)
            self.ms = MySub(self.t)

        self.signals = signals
        self.last_update = 0
        self.UI()
        #self.show()
        self.signals.trackBlocksToTrainModelSignal.connect(self.set_blocks)
        self.brake_update = time.time()

    def beaconSignal(self,msg):
        if len(msg) > 1:
            self.t.stationSide = msg[0]
            self.t.stationName = msg[1]
            self.t.underground = msg[2]

    def set_blocks(self,msg):
        #red is msg[0] and green is msg[1]
        self.blockList = msg
        # self.t.pm.BlockModels = msg[1]

    def dispatch(self, msg):

        self.t.id = msg[0]
        if msg[1] == 'Green Line':
            self.t.pm.BlockModels = self.blockList[1]
            self.t.line = 1
            self.t.pm.prev_block = 0
            self.t.pm.curr_block = 63
        else:
            self.t.pm.BlockModels = self.blockList[0]
            self.t.pm.prev_block = 0
            self.t.pm.curr_block = 9
            self.t.line = 0
           
        
        self.t.pm.suggSpeed = float(msg[2])
        self.trainDict.update({msg[0]: self.t})
        

        # print(f'------------DISPATCHED!!!!!!!!!!!------------------')
        self.t.dispatched = True

    def setTrainPower(self, msg):
        # print(f'Message is:{msg}')
        # print(f'Message type is: {type(msg)}')
        # print(f'---------RECEIVED POWER IS: {p}------------------')
        self.t.pm.power = msg['power']
    
    def setBrake(self, msg):
        self.t.service_brake = msg['serviceBrake'] 
        self.t.e_brake = msg['emergencyBrake'] 

        if self.t.service_brake:
            self.t.pm.brake(0)
        elif self.t.e_brake:
            self.t.pm.brake(1)


    def nonVitals(self,msg):
        for key in msg:
            setattr(self.t, key, msg[key])
    
    def ctc_authority(self, msg):
        for i,m in enumerate(msg):
            msg[i] = int(m)
        self.t.pm.ctc_authority.extend(msg)

    
    def wayside_authority(self,msg):
        self.t.pm.waysideAuthority = msg[2]
    
    def speedup(self, msg):
        self.t.pm.speedUp = int(msg)
    def UI(self):
        
        self.signals.dispatchTrainSignal.connect(self.dispatch)
        self.signals.powerSignal.connect(self.setTrainPower)
        self.signals.brakeDictSignal.connect(self.setBrake)
        self.signals.nonVitalDictSignal.connect(self.nonVitals)
        self.signals.ctcAuthoritySignal.connect(self.ctc_authority)
        self.signals.clockSpeedSignal.connect(self.speedup)
        self.signals.waysideAuthority.connect(self.wayside_authority)
        self.signals.beaconFromTrackModelSignal.connect(self.beaconSignal)
        # if sys.argv[1] == 'user':
        #     self.test_win.setVisible(False)
        # else:
        #     self.test_win.setVisible(True)

       
        self.test_win.clicked.connect(self.test_window)
        #connecting failure buttons to respective slots
        self.sig_fail.clicked.connect(self.sig_failure)
        self.train_eng_fail.clicked.connect(self.train_eng_failure)
        self.brake_fail.clicked.connect(self.brake_failure)
        #setting failure button colors
        self.train_eng_fail.setStyleSheet("background-color: gray")
        self.sig_fail.setStyleSheet("background-color: gray")
        self.brake_fail.setStyleSheet("background-color: gray")

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_display)
        self.timer.start(100)

        #Setting up Thread and worker to continuously update labels
        # self.disp_thread = QThread()
        # self.disp_worker = DisplayWorker(self)
        # self.disp_worker.moveToThread(self.disp_thread)
        #connecting signals and slots
        # self.disp_thread.started.connect(self.disp_worker.run)
        # self.disp_worker.finished.connect(self.disp_thread.quit)
        
        # self.disp_thread.start()
    
    def train_eng_failure(self):
        if self.t.train_engine_failure:
            # print('Train Engine Failure Pressed Again! removing failure')
            self.t.train_engine_failure = False
            self.train_eng_fail.setStyleSheet("background-color: gray")
        else:
            # print('Train Engine Failure Triggered')
            self.t.train_engine_failure = True
            self.train_eng_fail.setStyleSheet("background-color: red")

    def sig_failure(self):
        if self.t.signal_pickup_failure:
            # print('Signal Failure Pressed Again! removing failure')
            self.t.signal_pickup_failure = False
            self.sig_fail.setStyleSheet("background-color: gray")
        else:
            # print('Signal Failure Triggered')
            self.t.signal_pickup_failure = True
            self.sig_fail.setStyleSheet("background-color: red")
    
    def brake_failure(self):
        if self.t.brake_failure:
            # print('Brake Failure Pressed Again! removing failure')
            self.t.brake_failure = False
            self.brake_fail.setStyleSheet("background-color: gray")
        else:
            # print("Brake Failure Triggered")
            self.t.brake_failure = True
            self.brake_fail.setStyleSheet("background-color: red")
    
    def update_display(self):
        if self.hw:
            self.ms.spinOnce()

        #lights
        if self.t.int_lights:
            self.int_lights_disp.setText('On')
        else:
            self.int_lights_disp.setText('Off')
        
        if self.t.ext_lights:
            self.ext_lights_disp.setText('On')
        else:
            self.ext_lights_disp.setText('Off')
        
        #power
        self.cmd_pwr_disp.setText(f'{round(float(self.t.pm.power)/1000)} kW')
        # self.qt.t.set_power(round(float(self.qt.t.curr_power)/1000))

        self.cmd_speed_disp.setText('%.1f mph' %(float(self.t.pm.cmdSpeed)*2.23694))
        
        self.curr_speed_disp.setText(f'{self.t.pm.curr_speed} mph')

        #temperature
        self.temp_disp.setText(f'{self.t.temperature} F')

        #doors
        #lights
        if self.t.left_doors:
            self.left_doors_disp.setText('Open')
        else:
            self.left_doors_disp.setText('Closed')
        
        if self.t.right_doors:
            self.right_doors_disp.setText('Open')
        else:
            self.right_doors_disp.setText('Closed')

        
        
        
        self.pass_disp.setText(f'{self.t.passenger_count}')
        self.crew_disp.setText(f'{self.t.crew_count}')

        #critical info
        self.serv_brake_disp.setText(f'{self.t.service_brake}')
        self.ebrake_disp.setText(f'{self.t.e_brake}')
        self.auth_disp.setText(f'{self.t.pm.train_authority}')
        self.grade_disp.setText(f'{self.t.pm.grade * 100} %')
        self.switch_disp.setText(f'{self.t.switch} miles')

        #stations
        self.last_st_disp.setText(f'{self.t.last_station}')
        self.next_st_disp.setText(f'{self.t.next_station}')
        
        if time.time()-self.last_update > 0.1:
            if self.t.line != None and self.t.pm.prev_block != None and self.t.pm.curr_block != 0:
                # print(f'values are, line: {self.t.line}, previous block: {self.t.pm.prev_block}, curr block: {self.t.pm.curr_block}')
                self.signals.trainLocation.emit([int(self.t.line), self.t.id, int(self.t.pm.prev_block), int(self.t.pm.curr_block)])
            # print("inside if statement")
            if self.t.e_brake == False and self.t.service_brake == False and self.t.dispatched:
                self.t.set_power(self.t.pm.power)
                self.signals.currentSpeedOfTrainModel.emit([self.t.id, self.t.pm.curr_vel])
                # print(f'Occ_list is: {self.t.pm.occ_list}')
                # print(f'Curr Pos in block {self.qt.t.pm.curr_block} is: {self.qt.t.pm.curr_pos}')
                self.signals.occupancyFromTrainSignal.emit(self.t.pm.occ_list)
                self.signals.commandedSpeedSignal.emit([self.t.id,self.t.pm.cmdSpeed])
                self.signals.speedLimitSignal.emit([self.t.id,self.t.pm.speedLimit])
                self.signals.authoritySignal.emit([self.t.id,self.t.pm.train_authority])
                self.last_update = time.time()
                # print('PUBLISHING!!!')
                
                if self.hw:
                    self.mp.publish()
            if self.t.pm.stationStop:
                self.signals.stationStop.emit(self.t.pm.stationStop)
            
            # elif type(self.t.line) != int:
            #     print("LINE not int")
            # elif type(self.t.pm.prev_block ) != int:
            #     print("LINE not int")
            # elif type(self.t.pm.curr_block ) != int:
            #     print("LINE not int")


        if time.time()-self.brake_update > 0.5:
            if self.t.service_brake == True:
                self.t.pm.brake(0)

                if self.hw:
                    self.mp.publish()

                self.signals.currentSpeedOfTrainModel.emit(self.t.pm.curr_vel)
                self.signals.occupancyFromTrainSignal.emit(self.t.pm.occ_list)
                self.signals.commandedSpeedSignal.emit(self.t.pm.speedLimit)
                self.brake_update = time.time()
            elif self.t.e_brake == True:
                self.t.pm.brake(1)

                if self.hw:
                    self.mp.publish()

                self.signals.currentSpeedOfTrainModel.emit(self.t.pm.curr_vel)
                self.signals.occupancyFromTrainSignal.emit(self.t.pm.occ_list)
                self.signals.commandedSpeedSignal.emit(self.t.pm.speedLimit)
                self.brake_update = time.time()


    def update_model(self, dict):
        for key in dict:
            if key == 'signal_pickup_failure':
                self.sig_failure()
            elif key == 'curr_power':
                self.t.set_power(float(dict[key]))
            elif key == 'train_engine_failure':
                self.train_eng_failure()
            elif key == 'brake_failure':
                self.brake_failure()
            elif key == 'curr_speed':
                self.t.curr_speed = dict[key]
            elif key == 'e_brake':
                if self.t.e_brake == 'On':
                    self.t.e_brake = 'Off'
                else:
                    self.t.e_brake = 'On'
                    self.t.curr_power = 0
                    self.ebrake_thread = QThread()
                    self.ebrake_worker = Ebrake(self)
                    self.ebrake_worker.moveToThread(self.ebrake_thread)

                    #connecting signals and slots
                    self.ebrake_thread.started.connect(self.ebrake_worker.run)
                    self.ebrake_worker.stopped.connect(self.ebrake_thread.quit)
                    self.ebrake_worker.stopped.connect(self.ebrake_worker.deleteLater)
                    self.ebrake_thread.finished.connect(self.ebrake_thread.deleteLater)

                    self.ebrake_thread.start()
            elif key == 'service_brake':
                if self.t.service_brake == 'On':
                    self.t.service_brake = 'Off'
                else:
                    self.t.service_brake = 'On'
                    self.t.curr_power = 0
                    self.servbrake_thread = QThread()
                    self.servbrake_worker = ServBrake(self)
                    self.servbrake_worker.moveToThread(self.servbrake_thread)

                    self.servbrake_thread.started.connect(self.servbrake_worker.run)
                    self.servbrake_worker.stopped.connect(self.servbrake_thread.quit)
                    self.servbrake_worker.stopped.connect(self.servbrake_worker.deleteLater)
                    self.servbrake_thread.finished.connect(self.servbrake_thread.deleteLater)

                    self.servbrake_thread.start()
            else:
                if key == 'curr_power' and self.t.e_brake == 'On':
                    self.t.curr_power = 0
                else:
                    setattr(self.t, key, dict[key])          
    
    def test_window(self):
        self.w = TestWindow()
        self.w.test_clicked.connect(self.update_model)
        # self.w.show()



class ServBrake(QObject):
    stopped = pyqtSignal()

    def __init__(self,qt):
        super(ServBrake, self).__init__()
        self.qt = qt
    
    def run(self):
        if self.qt.t.service_brake == True and self.qt.t.pm.curr_vel > 0:
            self.qt.t.pm.serv_brake()
        
        # print('train stopped')
        self.stopped.emit()

class Ebrake(QObject):
    stopped = pyqtSignal()

    def __init__(self,qt):
        super(Ebrake, self).__init__()
        self.qt = qt
    
    def run(self):
        # print('EBrake initiated')
        if self.qt.t.e_brake == True and self.qt.t.pm.curr_vel > 0:
            self.qt.t.e_brake_func()

        # print('train stopped')
        self.stopped.emit()

# class DisplayWorker(QObject):
#     progress = pyqtSignal(QObject)
    
#     def __init__(self, qt):
#         super(DisplayWorker, self).__init__()
#         self.qt = qt

#     def run(self):
#         last_update = time.time()
#         while True:
#             #lights
#             self.qt.int_lights_disp.setText(self.qt.t.int_lights)
#             self.qt.ext_lights_disp.setText(self.qt.t.ext_lights)
           
#             #power
#             self.qt.cmd_pwr_disp.setText(f'{round(float(self.qt.t.pm.power)/1000)} kW')
#             # self.qt.t.set_power(round(float(self.qt.t.curr_power)/1000))
#             self.qt.cmd_speed_disp.setText(f'{self.qt.t.cmd_speed} mph')
            
#             self.qt.curr_speed_disp.setText(f'{self.qt.t.pm.curr_speed} mph')

#             #temperature
#             self.qt.temp_disp.setText(f'{self.qt.t.temperature} F')

#             #doors
            
#             self.qt.left_doors_disp.setText(self.qt.t.left_doors)
#             self.qt.right_doors_disp.setText(self.qt.t.right_doors)
            
            
#             self.qt.pass_disp.setText(f'{self.qt.t.passenger_count}')
#             self.qt.crew_disp.setText(f'{self.qt.t.crew_count}')

#             #critical info
#             self.qt.serv_brake_disp.setText(f'{self.qt.t.service_brake}')
#             self.qt.ebrake_disp.setText(f'{self.qt.t.e_brake}')
#             self.qt.auth_disp.setText(f'{self.qt.t.authority}')
#             self.qt.grade_disp.setText(f'{self.qt.t.grade} %')
#             self.qt.switch_disp.setText(f'{self.qt.t.switch} miles')

#             #stations
#             self.qt.last_st_disp.setText(f'{self.qt.t.last_station}')
#             self.qt.next_st_disp.setText(f'{self.qt.t.next_station}')
            
#             if time.time()-last_update > 1:
#                 if self.qt.t.e_brake == 'Off' and self.qt.t.service_brake == 'Off' and self.qt.t.dispatched:
#                     # print('Setting Train Power')
#                     self.qt.t.set_power(self.qt.t.pm.power)
#                     self.qt.signals.currentSpeedOfTrainModel.emit(self.qt.t.pm.curr_vel)
#                     print(f'Occ_list is: {self.qt.t.pm.occ_list}')
#                     # print(f'Curr Pos in block {self.qt.t.pm.curr_block} is: {self.qt.t.pm.curr_pos}')
#                     self.qt.signals.occupancyFromTrainSignal.emit(self.qt.t.pm.occ_list)
#                     last_update = time.time()





class TestWindow(QtWidgets.QMainWindow):
    
    test_clicked = pyqtSignal(dict)
    def __init__(self):
        super(TestWindow, self).__init__()
        path = os.getcwd()+'\\train_model\\test.ui'
        uic.loadUi(path, self)
        self.UI()

    def UI(self):
        self.train_eng_fail.clicked.connect(self.train_eng_failure)
        self.sig_fail.clicked.connect(self.sig_failure)
        self.brake_fail.clicked.connect(self.brake_failure)
        self.ebrake.clicked.connect(self.e_brake_trigger)
        self.test_inputs.clicked.connect(self.send_msg)
        self.serv_brake.clicked.connect(self.serv_brake_trigger)
    
    def send_msg(self):
        self.dict = {'int_lights': self.int_lights_box.currentText(),
                'ext_lights': self.ext_lights_box.currentText(),
                'temperature': self.temp_edit.toPlainText(),
                'left_doors': self.left_doors_edit.toPlainText(),
                'right_doors': self.right_doors_edit.toPlainText(),
                'passenger_count':self.pass_edit.toPlainText(),
                'crew_count': self.crew_edit.toPlainText(),
                'authority': self.auth_edit.toPlainText(),
                'grade': self.grade_edit.toPlainText(),
                'switch': self.switch_edit.toPlainText(),
                'curr_power':self.cmd_pwr_edit.toPlainText(),
                'cmd_speed':self.cmd_speed_edit.toPlainText(),
                'curr_speed':self.curr_speed_edit.toPlainText(),
                'last_station':self.last_station_edit.toPlainText(),
                'next_station':self.nxt_station_edit.toPlainText()}
        
        empty_vals = []
        for key in self.dict:
            if len(self.dict[key]) == 0:
                if key == 'curr_speed':
                    self.dict[key] = None
                else:
                    empty_vals.append(key)

        [self.dict.pop(key) for key in empty_vals]

        if 'curr_power' in self.dict:
            curr_pwr = float(self.cmd_pwr_edit.toPlainText()) * 1000
            self.dict['curr_power'] = curr_pwr

        # print(self.temp_edit.toPlainText())
        self.test_clicked.emit(self.dict)
    
    def sig_failure(self):
        self.dict = {'signal_pickup_failure': True}
        self.test_clicked.emit(self.dict)
    def train_eng_failure(self):
        self.dict = {'train_engine_failure': True}
        self.test_clicked.emit(self.dict)
    def brake_failure(self):
        self.dict = {'brake_failure': True}
        self.test_clicked.emit(self.dict)
    def e_brake_trigger(self):
        self.dict = {'e_brake': 'On'}
        self.test_clicked.emit(self.dict)
    def serv_brake_trigger(self):
        self.dict = {'service_brake': 'On'}
        self.test_clicked.emit(self.dict)
     


# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     signals = Signals()
#     file = r"C:\Users\achar\OneDrive\Desktop\fall_2022\trains\ECE_1140_TRAINS\train_model\train.ui"
#     window = TrainModel(file, signals)
#     app.exec_()