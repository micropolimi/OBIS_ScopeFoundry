from __future__ import division, print_function
import serial
import time

class LaserDevice(object):

    def __init__(self, port, debug=False, dummy=False): #change port according to device listing in windows.
        
        self.debug = debug
        self.dummy = dummy
        self.port = port
        
        if not self.dummy:
            self.ser = ser = serial.Serial(port=self.port, baudrate=921600, 
                                           bytesize=8, parity='N', 
                                           stopbits=1, xonxoff=False, timeout=3.0)
            ser.flush()
            
    def close(self):
        if not self.dummy:
            self.ser.close()

    def write_cmd(self, cmd):
        serialcmd = cmd+'\r\n'
        self.ser.write(serialcmd.encode())
        echo = self.ser.readline()
        response = self.ser.readline()
        
        if self.debug:
            print ('write:', repr(serialcmd))
            print ('echo:', echo)
            print ('response:', response)
        if 'Error'.encode() in response:
            raise IOError('laser command error:' + repr(response))
        echo = echo.decode('utf-8')
        echo=echo.splitlines()[0]
        return echo
        
    def get_identification(self):
        """ Gets the laser's identification string """
        fullresp = self.write_cmd('*IDN?')
        # The SCPI protocol provides a method to communicate with multiple
        # virtual devices within an instrument.
        # SCPI channel selection is performed by appending a numeric suffix to the
        # base word in any command string. When the numeric suffix is left off or
        # has a value of zero, the command refers to the first connected device.
        # For example, *idn?* and *idn0? query strings both refer to the first
        # connected device. 
        resp=fullresp    
        return resp
    
    def reset(self):
        """ Causes a device to warm boot if implemented """
        fullresp = self.write_cmd('*RST')
        resp=fullresp    
        return resp
    
    def get_model(self):
        """ Retrieves the model name of the laser """
        fullresp = self.write_cmd('SYSTem1:INFormation:MODel?')
        resp=fullresp    
        return resp
    
    def get_wavelength(self):
        """ Retrieves the wavelength of the laser """
        fullresp = self.write_cmd('SYSTem:INFormation:WAVelength?')
        resp=fullresp    
        return resp
    
    def get_power_rating(self):
        """ Retrieves the power (mW) rating of the laser """
        fullresp = self.write_cmd('SYSTem:INFormation:POWer?')
        resp=fullresp    
        return float(resp)*1000
    
    def get_minimum_power(self):
        """Returns the minimum CW laser output power in (mW)"""
        fullresp = self.write_cmd('SOURce:POWer:LIMit:LOW?')
        resp=fullresp    
        return float(resp)*1000
    
    def get_maximum_power(self):
        """Returns the maximum CW laser output power in (mW)"""
        fullresp = self.write_cmd('SOURce:POWer:LIMit:HIGH?')
        resp=fullresp    
        return float(resp)*1000
        
    def set_laser_auto_start(self, cmd):
        ''' Enables or disables the laser Auto Start feature. Setting is saved in persistent memory.
        The factory default is OFF. If the laser is connected to a OBIS Remote, this setting is overriden by the
        hardware switch of the min-controller '''
        
        fullresp = self.write_cmd('SYSTem1:AUTostart '+cmd) # cmd = ON|OFF
        resp=fullresp    
        return resp
    
    def get_status(self):
        """ Queries the system status """
        fullresp = self.write_cmd('SYSTem:STATus?')
        resp=fullresp    
        return resp
    
    def get_faults(self):
        """ Queries current system faults """
        fullresp = self.write_cmd('SYSTem:FAULt?')
        resp=fullresp    
        return resp
    
    def get_temperature(self):
        """ Returns the present laser base plate temperature """
        fullresp = self.write_cmd('SOURce:TEMPerature:BASeplate?')
        resp=fullresp    
        return resp
    
    def get_interlock_status(self):
        """ Returns the status of the system interlock """
        fullresp = self.write_cmd('SYSTem:LOCK?')
        resp=fullresp    
        return resp
    
    # ===== Laser Operating Mode Selection =====
    # Seven mutually exclusive operating modes are available:
    # - CWP (continuous wave, constant power)
    # - CWC (continuous wave, constant current)
    # - DIGITAL (CW with external digital modulation)
    # - ANALOG (CW with external analog modulation)
    # - MIXED (CW with external digital + analog modulation)
    # - DIGSO (External digital modulation with power feedback) Note: This
    # operating mode is not supported in some device models.
    # - MIXSO (External mixed modulation with power feedback) Note: This
    # operating mode is not supported in some device models.
    # The exact meaning of the selected mode is device-dependent.
    
    def select_operating_mode(self, cmd):
        '''cmd = CWP|CWC :                         Sets the laser operating mode to internal CW and deselects external modulation. The default setting is CW with constant power or CWP.
           cmd = DIGital|ANALog|MIXed|DIGSO|MIXSO: Sets the laser operating mode to CW constant current modulated by one or more external sources. MIXED source combines both external digital and external analog modulation. 
        The setting is saved in non-volatile memory '''
        if cmd=='CWP' or cmd=='CWC':
            fullresp = self.write_cmd('SOURce:AM:INTernal '+cmd) 
        else:
            fullresp = self.write_cmd('SOURce:AM:EXTernal '+cmd)
        resp=fullresp    
        return resp
    
    def get_operating_mode(self):
        ''' Queries the current operating mode of the laser.  '''
        fullresp = self.write_cmd('SOURce:AM:SOURce?') 
        resp=fullresp    
        return resp
    
    def set_laser_status(self, cmd):
        ''' Turns the laser ON or OFF. When turning the laser ON, actual laser
        emission may be delayed due to internal circuit stabilization logic and/or
        CDRH delays.   '''
        fullresp = self.write_cmd('SOURce:AM:STATe '+cmd) # cmd = ON|OFF
        resp=fullresp    
        return resp
    
    def get_laser_status(self):
        ''' Queries the current laser emission status.  '''
        fullresp = self.write_cmd('SOURce:AM:STATe?') 
        resp=fullresp    
        return resp
    
    def set_laser_power(self, value):
        ''' Sets present laser power level (mW). Setting power level does not turn
        the laser on.    '''
        fullresp = self.write_cmd('SOURce:POWer:LEVel:IMMediate:AMPLitude '+str(value/1000)) 
        resp=fullresp    
        return resp 
    
    def get_laser_power(self):
        ''' Gets laser power setting level (mW)'''
        fullresp = self.write_cmd('SOURce:POWer:LEVel:IMMediate:AMPLitude?') 
        resp=fullresp    
        return float(resp )*1000
    
    def present_output_power(self):
        """ Returns the present output power of the laser (mW)"""
        fullresp = self.write_cmd('SOURce:POWer:LEVel?')
        resp=fullresp    
        return float(resp)*1000
    
    
if __name__ == '__main__':

    try:    
        laser = LaserDevice(port='COM7', debug=False)
        
        print(laser.get_identification())
        print(laser.get_wavelength())
        print(laser.set_laser_auto_start('OFF'))
        print(laser.get_model())
        print(laser.get_status())
        print(laser.get_faults()) 
        print(laser.get_temperature())       
        print(laser.get_power_rating())
        print(laser.get_laser_power())
        #print(laser.set_laser_power(0.002))
        #print(laser.set_laser_status('OFF'))
        #print(laser.set_laser_status('ON'))
        #time.sleep(10)
        #print(laser.set_laser_status('OFF'))
        #print(laser.select_operating_mode('CWP'))
        #print(laser.reset())
    except Exception as err:
        print(err)
    finally:
        laser.close()
    
