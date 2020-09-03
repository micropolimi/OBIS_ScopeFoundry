#import serial.tools.list_ports

from PyQt5.QtCore import QTimer
from ScopeFoundry import HardwareComponent

from OBIS_ScopeFoundry.laser_device import LaserDevice

 
class LaserHW(HardwareComponent):
    
    name = 'LaserHW'
    
    def setup(self):
        #self.timer = QTimer()
        #self.timer.timeout.connect(self.update_ports)
        #self.timer.start(1000)
        self.port = self.add_logged_quantity('port', dtype=str, initial = 'COM1', choices=['COM1','COM2','COM3','COM4','COM5','COM6','COM7','COM8','COM9','COM10']) 
        self.model = self.add_logged_quantity('name', dtype=str, initial='', ro=1)
        self.wavelength = self.add_logged_quantity('wavelength', dtype=str, initial='', ro=1)
        self.power_rating = self.add_logged_quantity('power_rating', dtype=float, ro=1, unit = 'mW')
        self.temperature = self.add_logged_quantity('temperature', dtype=str, initial='', ro=1)
        #self.interlock = self.add_logged_quantity('interlock', dtype=str, initial='', ro=1)
        self.operating_mode = self.add_logged_quantity('operating_mode', dtype=str, si=False, ro=0, choices=['CWP', 'DIGITAL', 'ANALOG', 'MIXED']) # reread_from_hardware_after_write = True )
        self.laser_status = self.add_logged_quantity('laser_status', dtype=str, si=False, ro=0, choices=['OFF', 'ON']) # reread_from_hardware_after_write = True)
        self.laser_power = self.add_logged_quantity('laser_power', dtype=float, si=False, ro=0, spinbox_decimals = 1, unit = 'mW') # reread_from_hardware_after_write = True)
        self.present_output_power = self.add_logged_quantity('present_output_power', dtype=float, spinbox_decimals = 1, unit = 'mW', ro=1)
        
        
    def connect(self):
        if hasattr(self, 'timer'):
            del self.timer
        self.port.change_readonly(True)
        
        # open connection to hardware
        self.laser = LaserDevice(port=self.port.val, debug=self.debug_mode.val)
        
        # connect logged quantities   
        self.model.hardware_read_func = self.laser.get_model 
        self.wavelength.hardware_read_func = self.laser.get_wavelength
        self.power_rating.hardware_read_func = self.laser.get_power_rating
        self.temperature.hardware_read_func = self.laser.get_temperature
        #self.interlock.hardware_read_func = self.laser.get_interlock_status
        self.operating_mode.hardware_set_func = self.laser.select_operating_mode
        self.operating_mode.hardware_read_func = self.laser.get_operating_mode
        self.laser_status.hardware_set_func = self.laser.set_laser_status
        self.laser_status.hardware_read_func = self.laser.get_laser_status
        self.laser_power.change_min_max(vmin=self.laser.get_minimum_power(), vmax=self.laser.get_maximum_power())
        self.laser_power.hardware_set_func = self.laser.set_laser_power
        self.laser_power.hardware_read_func = self.laser.get_laser_power
        self.present_output_power.hardware_read_func = self.laser.present_output_power
        
        #print(self.laser_status.val)
        self.read_from_hardware() #read from hardware at connection
        self.laser_status.add_listener(self.present_output_power.read_from_hardware)
        self.laser_power.add_listener(self.present_output_power.read_from_hardware)
        

    def disconnect(self):
        self.port.change_readonly(False)
        
        # disconnect hardware
        if hasattr(self, 'laser'):
            self.laser.close()   
            # clean up hardware object      
            del self.laser
        
        # disconnect logged quantities from hardware
        for lq in self.settings.as_list():
            lq.hardware_read_func = None
            lq.hardware_set_func = None
            
#     def update_ports(self):
#         ''' Check for new serial COM ports available and update self.port choice list'''
#         comlist = serial.tools.list_ports.comports()
#         connected = []
#         for element in comlist:
#             connected.append(element.device) 
#         if self.port.choices != connected:
#             self.port.change_choice_list(connected)
#             if connected == []:
#                 self.port.val=0
#             else:
#                 self.port.val=connected[0]

        

        