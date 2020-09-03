from ScopeFoundry import BaseMicroscopeApp

class Laser_App(BaseMicroscopeApp):

    # this is the name of the microscope that ScopeFoundry uses 
    # when storing data
    name = 'laser_app'
    
    # You must define a setup function that adds all the 
    #capablities of the microscope and sets default settings
    def setup(self):
        
        #Add App wide settings
        
        #Add hardware components
        print("Adding Hardware Components")
        from laser_hardware import LaserHW
        self.add_hardware(LaserHW(self))
        
        #Add measurement components
        print("Create Measurement objects")
        # Connect to custom gui
        
        # load side panel UI
        
        # show ui
        self.ui.show()
        self.ui.activateWindow()


if __name__ == '__main__':
    import sys
    
    app = Laser_App(sys.argv)
    sys.exit(app.exec_())