##############################################################################
# AUTHOR(S):    Sushmit Acharya
# DATE:         12/15/2022
# FILENAME:     trainmodel_ui.py
# DESCRIPTION:
#  Primary UI for the Train Model that runs the Train Model UI
##############################################################################


# from train import Train
import sys

from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
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
        uic.loadUi(ui, self)
        self.t = Train()
        self.hw = hw
        

        if self.hw:
            from Server_Comm import MyPub, MySub
            self.mp = MyPub(self.t)
            self.ms = MySub(self.t)

        self.signals = signals
        self.UI()
        self.last_update = 0
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
        

        self.t.dispatched = True
        self.comboTrain.addItem(msg[0])
        self.comboTrain.show()

    def setTrainPower(self, msg):
        self.t = self.trainDict[msg['trainID']]
        self.t.pm.power = msg['power']
    
    def setBrake(self, msg):
        self.t = self.trainDict[msg['trainID']]
        self.t.service_brake = msg['serviceBrake'] 
        if msg['emergencyBrake']:
            self.t.e_brake = msg['emergencyBrake'] 


    def nonVitals(self,msg):
        self.t = self.trainDict[msg['trainID']]
        for key in msg:
            if key != 'trainID':
                setattr(self.t, key, msg[key])
            
            if key == 'advertisementState':
                if msg[key]:
                    self.advertisement.show()
                else:
                    self.advertisement.hide()
    
    def ctc_authority(self, msg):
        for i,m in enumerate(msg[1]):
            msg[1][i] = int(m)
        self.t = self.trainDict[msg[0]]
        self.t.pm.ctc_authority.extend(msg[1])

    
    def wayside_authority(self,msg):
        self.t = self.trainDict[msg[1]]
        self.t.pm.waysideAuthority = msg[2]
    
    def speedup(self, msg):
        for train in self.trainDict.values():
            self.t = train
            self.t.pm.speedUp = int(msg)
    
    def trainStopped (self, msg):
        self.t = self.trainDict[msg['trainID']]
        self.t.pm.stopAtStation = msg['stoppedAtStation']
    
    def passEbrake(self,msg):
        if self.t.e_brake:
            self.t.e_brake = False
        else:
            self.t.e_brake = True

    def addPassengers(self,msg):
        self.t = self.trainDict[msg[0]]
        self.t.passenger_count = msg[1]
    def UI(self):
        
        self.signals.dispatchTrainSignal.connect(self.dispatch)
        self.signals.powerSignal.connect(self.setTrainPower)
        self.signals.brakeDictSignal.connect(self.setBrake)
        self.signals.nonVitalDictSignal.connect(self.nonVitals)
        self.signals.ctcAuthoritySignal.connect(self.ctc_authority)
        self.signals.clockSpeedSignal.connect(self.speedup)
        self.signals.waysideAuthority.connect(self.wayside_authority)
        self.signals.beaconFromTrackModelSignal.connect(self.beaconSignal)
        self.signals.stoppedAtStationSignal.connect(self.trainStopped)
        
        #connecting failure buttons to respective slots
        self.sig_fail.clicked.connect(self.sig_failure)
        self.train_eng_fail.clicked.connect(self.train_eng_failure)
        self.brake_fail.clicked.connect(self.brake_failure)
        #setting failure button colors
        self.train_eng_fail.setStyleSheet("background-color: gray")
        self.sig_fail.setStyleSheet("background-color: gray")
        self.brake_fail.setStyleSheet("background-color: gray")

        #passenger emergency brake button red color
        self.comboTrain.hide()
        self.ebrake_button.clicked.connect(self.passEbrake)
        self.ebrake_button.setStyleSheet("background-color: red")

        #advertisements
        self.advertisement         = QLabel(self)
        self.pixmap                = QPixmap('advert.png')
        self.pixmap.scaled(10000,10000)
        self.advertisement.setPixmap(self.pixmap)
        self.advertisement.setGeometry(550,750,30,30)
        self.advertisement.resize(self.pixmap.width(),
                          self.pixmap.height())
        self.advertisement.hide()
        self.advertisement.show()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_display)
        self.timer.start(100)
    
    def train_eng_failure(self):
        if self.t.train_engine_failure:
            self.t.train_engine_failure = False
            self.train_eng_fail.setStyleSheet("background-color: gray")
        else:
            self.t.train_engine_failure = True
            self.train_eng_fail.setStyleSheet("background-color: red")

    def sig_failure(self):
        if self.t.signal_pickup_failure:
            self.t.signal_pickup_failure = False
            self.sig_fail.setStyleSheet("background-color: gray")
        else:
            self.t.signal_pickup_failure = True
            self.sig_fail.setStyleSheet("background-color: red")
    
    def brake_failure(self):
        if self.t.brake_failure:
            self.t.brake_failure = False
            self.brake_fail.setStyleSheet("background-color: gray")
        else:
            self.t.brake_failure = True
            self.brake_fail.setStyleSheet("background-color: red")
    
    def update_display(self):
        if self.hw:
            self.ms.spinOnce()

        if len(self.trainDict) > 0:
            if self.comboTrain.currentText() != 'Choose Train':
                self.t = self.trainDict[self.comboTrain.currentText()]

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
        self.accel_disp.setText('%.1f ft/s^2' % float((self.t.pm.curr_accel)*3.28084) )        
        self.curr_speed_disp.setText(f'{self.t.pm.curr_speed} mph')

        #temperature
        self.temp_disp.setText(f'{self.t.temperature} F')

        #doors
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
        if self.t.service_brake == 1:
            self.serv_brake_disp.setText('On')
        elif self.t.service_brake == 0:
            self.serv_brake_disp.setText('Off')
        if self.t.e_brake:
            self.ebrake_disp.setText('On')
        if self.t.e_brake:
            self.ebrake_disp.setText('Off')
        self.auth_disp.setText('%d'%int(self.t.pm.train_authority))
        self.grade_disp.setText(f'{self.t.pm.grade * 100} %')

        #stations
        self.last_st_disp.setText(f'{self.t.last_station}')
        self.next_st_disp.setText(f'{self.t.next_station}')
        
        for train in self.trainDict.values():
            self.t = train
            if time.time()-self.last_update > 0.1/self.t.pm.speedUp:
                if self.t.line != None and self.t.pm.prev_block != None and self.t.pm.curr_block != 0:
                    self.signals.trainLocation.emit([int(self.t.line), self.t.id, int(self.t.pm.prev_block), int(self.t.pm.curr_block)])
                if self.t.e_brake == False and self.t.service_brake == False and self.t.dispatched:
                    self.t.pm.setPower(self.t.pm.power, time.time())
                    if self.hw:
                        self.mp.publish()
                elif self.t.pm.stationStop and not self.t.pm.stopAtStation:
                    self.signals.stationStop.emit([self.t.id, self.t.pm.stationStop, self.t.line, self.t.pm.curr_block])
                    self.t.passenger_count = 0
                elif self.t.service_brake == True:
                    self.t.pm.brake(0)
                    if self.hw:
                        self.mp.publish()  
                elif self.t.e_brake == True:
                    self.t.pm.brake(1)
                    if self.hw:
                        self.mp.publish()
                
                self.signals.currentSpeedOfTrainModel.emit([self.t.id, self.t.pm.curr_vel])
                self.signals.commandedSpeedSignal.emit([self.t.id,self.t.pm.cmdSpeed])
                self.signals.speedLimitSignal.emit([self.t.id,self.t.pm.speedLimit])
                self.signals.authoritySignal.emit([self.t.id,self.t.pm.train_authority])
                self.signals.ctcStopBlock.emit([self.t.line, self.t.pm.ctcStationStop])
                self.signals.trainFailuresSignal.emit([self.t.id, 
                                                        [self.t.train_engine_failure,
                                                        self.t.signal_pickup_failure,
                                                        self.t.brake_failure]])
                self.last_update = time.time()


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



class ServBrake(QObject):
    stopped = pyqtSignal()

    def __init__(self,qt):
        super(ServBrake, self).__init__()
        self.qt = qt
    
    def run(self):
        if self.qt.t.service_brake == True and self.qt.t.pm.curr_vel > 0:
            self.qt.t.pm.serv_brake()
        
        self.stopped.emit()

class Ebrake(QObject):
    stopped = pyqtSignal()

    def __init__(self,qt):
        super(Ebrake, self).__init__()
        self.qt = qt
    
    def run(self):
        if self.qt.t.e_brake == True and self.qt.t.pm.curr_vel > 0:
            self.qt.t.e_brake_func()

        self.stopped.emit()



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
     


