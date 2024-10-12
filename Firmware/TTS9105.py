ADC_REPORT_TIME = 0.300
ADC_SAMPLE_TIME = 0.001
ADC_SAMPLE_COUNT = 8
ADC_RANGE_CHECK_COUNT = 4
FILA_THRESHOLD = 1.16


import logging
import math

class AlphaBetaFilter:
    def __init__(self, alpha, beta, initial_position, initial_velocity):
        self.alpha = alpha                # Control position estimation
        self.beta = beta                  # Control velocity estimation
        self.position = initial_position  # Initial position estimation
        self.velocity = initial_velocity  # Initial velocity estimation
    def update(self, measurement, delta_time):
        self.position += self.velocity * delta_time
        residual = measurement - self.position
        self.position += self.alpha * residual
        self.velocity += self.beta * (residual / delta_time)
        return self.position, self.velocity

class TTS9105SENSOR:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.reactor = self.printer.get_reactor()
        self.name = config.get_name().split(' ')[-1]
        self.pin = config.get('sensor_pin')
        # Data init
        self.offset = self.fila = self.timestamp = self.lasetime = self.last_value  = 0.
        self.filament_present = self.last_status = False
        self.sensor_enabled = True
        self.enable_gcode = self.disable_gcode =  self.toolhead = self.query_adc = self.ppins = self.mcu_adc = None
        self.fila_minmax_threshold = self.threshold = self.Filter = self.alpha_beta = self.conversion_code = None
        # Get config
        if config.get('sensor_threshold', None) is not None:
            self.threshold = config.getlists('sensor_threshold', seps=(','),parser=float, count=2)
        if self.threshold is None or self.threshold == []: 
            self.threshold = [0.4,0.6] 
        self.sensortype = config.getint('sensor_type', 0, minval = 0, maxval = 2)
        self.sensorupdate = config.getfloat('sensor_update', 1., minval = 0., maxval = 10.)
        # Adc init
        self.ppins = self.printer.lookup_object('pins')
        self.mcu_adc = self.ppins.setup_pin('adc', self.pin)
        self.mcu_adc.setup_minmax(ADC_SAMPLE_TIME, ADC_SAMPLE_COUNT)
        self.mcu_adc.setup_adc_callback(ADC_REPORT_TIME, self.adc_callback)
        # extrude factor updating
        self.printer.register_event_handler("klippy:ready", self.handle_ready)
        self.extrude_update_timer = self.reactor.register_timer(self.extruder_update_event)
        self.query_adc = config.printer.load_object(config, 'query_adc')
        self.query_adc.register_adc(self.name, self.mcu_adc)
        gcode_macro = self.printer.load_object(config, 'gcode_macro')
        self.min_event_systime = self.reactor.NEVER
        self.gcode = self.printer.lookup_object('gcode')
      
        # Get width config
        if self.sensortype == 2:
            self.is_active = True
            self.printer.load_object(config, 'pause_resume')
            self.offset = config.getfloat('width_offset', 0.)
            if config.get('conversion_code', None) is not None:
                self.conversion_code = config.get('conversion_code', None)
            if config.get('alpha_beta', None) is not None:
                self.alpha_beta = config.getlists('alpha_beta', seps=(','),parser=float, count=2)
            self.compensate = config.getboolean('compensate', True)
            if config.get('fila_minmax_threshold', None) is not None:
                self.fila_minmax_threshold = config.getlists('fila_minmax_threshold', seps=(','),parser=float, count=2)
            if self.fila_minmax_threshold is None or self.fila_minmax_threshold == []: 
                self.fila_minmax_threshold = [1.5,2.0]             
            if self.alpha_beta is None or self.alpha_beta == []: 
                self.alpha_beta = [0.85,0.01]                                               
            self.Filter = AlphaBetaFilter(alpha=self.alpha_beta[0], beta=self.alpha_beta[1], initial_position=1.75, initial_velocity=0) 
            self.gcode.register_mux_command('DISABLE_FILA_TTS9105',"NAME",self.name,self.cmd_M406, desc="DISABLE_FILA_TTS9105")
            self.gcode.register_mux_command('ENABLE_FILA_TTS9105',"NAME",self.name,self.cmd_M405, desc="ENABLE_FILA_TTS9105")
      # Register G-code command      
        eventtime = self.reactor.monotonic()
        if eventtime < self.min_event_systime or not self.sensor_enabled:
            return
        idle_timeout = self.printer.lookup_object("idle_timeout")
        is_printing = idle_timeout.get_status(eventtime)["state"] == "Printing"
        if self.filament_present:
            if not is_printing and self.enable_gcode is not None:
                self.min_event_systime = self.reactor.NEVER
                logging.info('TTS9105 object "%s": Enable'  % (self.name) )
                logging.info('value %.6f (timestamp %.3f)' % (self.last_value, self.timestamp) )
                logging.info('enabled: %s sensor_type: %d' % (bool(self.sensor_enabled),self.sensortype))
                self.reactor.register_callback(self.enable_event_handler)
        elif is_printing and self.disable_gcode is not None:
            self.min_event_systime = self.reactor.NEVER
            logging.info('TTS9105 object "%s": Disable'  % (self.name) )
            logging.info('value %.6f (timestamp %.3f)' % (self.last_value, self.timestamp) )
            logging.info('enabled: %s sensor_type: %d' % (bool(self.sensor_enabled),self.sensortype))
            self.reactor.register_callback(self.disable_event_handler)
    # Cut off detection execution code
    def enable_event_handler(self, eventtime):
        self.exec_gcode("", self.disable_gcode)
        logging.info('TTS9105 object "%s": Enable ;enable_event_handler'  % (self.name) )
    def disable_event_handler(self, eventtime):
        pause_prefix = ""
        if self.sensortype == 2:
            pause_resume = self.printer.lookup_object('pause_resume')
            pause_resume.send_pause_command()
            logging.exception("Stop(timestamp %.3f)" % (self.timestamp))
            pause_prefix = "PAUSE\n"
            logging.info('TTS9105 object "%s": Disable ;disable_event_handler'  % (self.name) )
            self.printer.get_reactor().pause(eventtime + self.pause_delay)
        self.exec_gcode(pause_prefix, self.enable_gcode)
    def exec_gcode(self, prefix, template):
        try:
            self.gcode.run_script(prefix + template.render() + "\nM400")
        except Exception:   
            logging.exception("Script running error(timestamp %.3f)" % (self.timestamp))
        self.min_event_systime = self.reactor.monotonic() + self.event_delay
    # Command debugging macro instruction
    def cmd_CUT_TTS9105(self, gcmd):
        if self.sensortype == 0:
            gcmd.respond_info("sensor_type: 0.None;Can not cut material")
        elif self.sensortype == 2:
            gcmd.respond_info("sensor_type: 2.Fila;Can not cut material")
        else:
            curtime = self.printer.get_reactor().monotonic()
            kin_status = self.toolhead.get_kinematics().get_status(curtime)
            if ('x' not in kin_status['homed_axes']):
                self.gcode.run_script_from_command("G28 X")
            #gcmd.respond_info("Homed Axes: %s" % (kin_status)['homed_axes'])
            for i in range(0,10):
                self.gcode.run_script_from_command("G1 x236 F36000")
                self.gcode.run_script_from_command("G1 x256 F7800")
                gcmd.respond_info('Count :%d' % (i+1))                
                if self.force_update_sensor(timeout=self.sensorupdate):
                    #gcmd.respond_info('Cutting stopped due to sensor status')
                    break
    # adc acquisition
    def force_update_sensor(self, timeout):
        end_time = self.reactor.monotonic() + timeout
        while self.reactor.monotonic() < end_time:
            self.reactor.pause(0.1) 
            value, timestamp = self.mcu_adc.get_last_value()
            self.adc_callback(timestamp, value)     
            if self.last_status and self.sensor_enabled:
                return True
        return False
    def cmd_QUERY_TTS9105(self, gcmd):
        value, timestamp = self.mcu_adc.get_last_value()
        self.adc_callback(timestamp, value)     
        if self.last_status :gcmd.respond_info('TTS9105 object "%s": Enable'  % (self.name) )
        else:gcmd.respond_info('TTS9105 object "%s": Disable'  % (self.name) )
        gcmd.respond_info('value: %.6f (timestamp: %.3f)' % (self.last_value, self.timestamp) )
        gcmd.respond_info('enabled: %s sensor_type: %d' % (bool(self.sensor_enabled),self.sensortype))
    def cmd_QUERY_WIDTH(self, gcmd):
        if self.sensortype == 0:
            gcmd.respond_info("sensor_type: 0.None;Can not query width")
        elif self.sensortype == 1:
            gcmd.respond_info("sensor_type: 1.Cut;Can not query width")
        else:
            value, timestamp = self.mcu_adc.get_last_value()
            self.adc_callback(timestamp, value)    
            velocity,filawidth = self.update_filament_width(value,timestamp)
            #gcmd.respond_info('position: %.6f ; velocity: %.6f ' % (self.fila, velocity ) )
            gcmd.respond_info('TTS9105 object "%s": %.6f'  % (self.name, self.fila) )
            gcmd.respond_info('value: %.6f ; filawidth:%s '  % (self.last_value, filawidth ) )
    def cmd_SET_WIDTH_OFFSET(self, gcmd):
        if self.sensortype == 0:
            gcmd.respond_info("sensor_type: 0.None;Can not query width")
        elif self.sensortype == 1:
            gcmd.respond_info("sensor_type: 1.Cut;Can not query width")
        else:
            self.offset = gcmd.get_float('OFFSET', 0.)
            gcmd.respond_info('TTS9105 object "%s": %.6f'  % (self.name, self.offset) )
    def cmd_SET_TTS9105(self, gcmd):
        if not self.sensor_enabled:
            self.sensor_enabled = gcmd.get_int("ENABLE",1)
            self.reactor.update_timer(self.extrude_update_timer, self.reactor.NOW)
        gcmd.respond_info('TTS9105 object "%s"(enabled: %s)' % (self.name,self.sensor_enabled))
    def cmd_CLEAR_TTS9105(self, gcmd):
        if self.sensor_enabled:
            self.sensor_enabled = gcmd.get_int("DISABLE",0)
            self.reactor.update_timer(self.extrude_update_timer, self.reactor.NEVER)
        gcmd.respond_info('TTS9105 object "%s"(enabled: %s)' % (self.name,self.sensor_enabled))
    def cmd_INVERT_TTS9105(self, gcmd):
        if self.sensor_enabled:
            self.sensor_enabled = gcmd.get_int("DISABLE",0)
            self.reactor.update_timer(self.extrude_update_timer, self.reactor.NEVER)
        else:
            self.sensor_enabled = gcmd.get_int("ENABLE", 1)
            self.reactor.update_timer(self.extrude_update_timer, self.reactor.NOW)
        gcmd.respond_info('TTS9105 object "%s"(enabled: %s)' % (self.name,self.sensor_enabled))
    def cmd_M405(self, gcmd):
        if self.sensortype == 0:
            gcmd.respond_info("sensor_type: 0.None;Can not cut material")
        elif self.sensortype == 1:
            gcmd.respond_info("sensor_type: 1.CUT;Can not cut material")
        else:
            response = "Filament width sensor Turned On"
            if self.is_active:
                response = "Filament width sensor is already On"
            else:
                self.is_active = True
                self.compensate = True
            gcmd.respond_info(response)
    def cmd_M406(self, gcmd):
        if self.sensortype == 0:
            gcmd.respond_info("sensor_type: 0.None;Can not cut material")
        elif self.sensortype == 1:
            gcmd.respond_info("sensor_type: 1.CUT;Can not cut material")
        else:
            response = "Filament width sensor Turned Off"
            if not self.is_active:
                response = "Filament width sensor is already Off"
            else:
                self.is_active = False
                self.compensate = False
                self.gcode.run_script_from_command("M221 S100")
                gcmd.respond_info(response)
    def get_status(self, eventtime):
        return {
            'value': self.last_value,
            'status': "Enable" if self.last_status else "Disable",
            'enabled': bool(self.sensor_enabled)
        }   

def load_config_prefix(config):
    return TTS9105SENSOR(config)