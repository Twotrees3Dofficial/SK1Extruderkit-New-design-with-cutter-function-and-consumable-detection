# Firmware function description

<img src="https://github.com/Twotrees3Dofficial/SK1Extruderkit-New-design-with-cutter-function-and-consumable-detection/blob/main/Image/preview.png" width="1000"/>

## Renewal folder

Mainly store the updated firmware, you need to copy the files in the folder to the USB flash drive, and update it in the Settings page on the screen firmware,
>please ensure that the firmware version is greater than V2.0.2.34
>[If not, please click on the update firmware](https://wiki.twotrees3d.com/en/3DPrinterSeries/SK1)

## M file

M file is matlab language, you can enter the matlab official website online with online mode debugging it;
We mainly use the quadratic Fourier transform to convert the Hall acquisition data and the consumable width
>The AlphaBetafilter is a simplified version of Kalman that is less computant than Kalman and avoids the need for too much computing in the printing process

## PY file

The py file can be placed in the directory klippy/extra

- LIS2DW ports the gyroscope sensor that came with the newer klipper version
>Services Older versions of klipper lack a change module, if your klipper is newer you can choose to ignore it
- TTS9105 is the py file we wrote for the 9105 linear ic Hall sensor, if you are using other sensors can also refer to our function modeling method to create it

# Configuration file modification.

We keep the configuration of the machine in printer.cfg 
Put custom code in the fliudd.cdf 
If you want to use our solution, 
please modify the following key configurations

Change the gyro configuration 
```
[lis2dw]
cs_pin: MKS_THR:PA4#gpio13
spi_software_sclk_pin: MKS_THR:PA5#gpio14
spi_software_mosi_pin: MKS_THR:PA7#gpio15
spi_software_miso_pin: MKS_THR:PA6#gpio12
axes_map:x,-z,-y

[resonance_tester]
accel_chip: lis2dw
probe_points:
    128, 128, 20  # an example
```

Advance and retreat code we modify
```
[gcode_macro INVERT]
gcode:
    {% if printer["output_pin caselight"].value == 0 %}
        SET_PIN PIN=caselight VALUE=1
    {% else %}
        SET_PIN PIN=caselight VALUE=0
    {% endif %}

[gcode_macro A_LOAD_MATERIAL]
variable_saved_extmp: 240
gcode:
    RESPOND PREFIX=LOAD: MSG={"LOAD-MATERIAL"}
    SAVE_GCODE_STATE NAME=recovery_state
    {% set current_temp = printer.extruder.temperature %}
    SET_HEATER_TEMPERATURE HEATER=extruder TARGET={current_temp}
    {% if printer.extruder.temperature < 180 %}
        RESPOND PREFIX=LOAD: MSG={"Heating"}
        M109 S240
    {% endif %}
    RESPOND PREFIX=LOAD: MSG={"Loading"}
    M400
    M83
    G1 E120 F1200 
    M400
    RESTORE_GCODE_STATE NAME=recovery_state
    {% if printer["print_stats"].state == "paused" %}
        M104 S{saved_extmp}
    {% else %}
        {% if current_temp < 180 %}
            M109 S0
        {% else %}
            M109 S{current_temp}
        {% endif %}
    {% endif %}
    RESPOND PREFIX=LOAD: MSG={"END"}
[gcode_macro A_CUT_MATERIAL]
gcode:
    RESPOND PREFIX=CUT: MSG={"CUT-MATERIAL"}
    SAVE_GCODE_STATE NAME=recovery_state
    INVERT
    {% if 'x' not in printer["toolhead"].homed_axes %}
        RESPOND PREFIX=CUT: MSG={"Home"}
        G28 X
        {% set current_x = 128  %}
    {% else %}
        G1 x200 F36000
        {% set current_x = printer.gcode_move.position.x %}
    {% endif %}
    RESPOND PREFIX=CUT: MSG={"Cutting"}
    G90
    G1 x236 F36000
    G1 x256 F7800
    CUT_TTS9105 Name=FILA
    G1 x{current_x} F36000
    INVERT
    RESTORE_GCODE_STATE NAME=recovery_state
    RESPOND PREFIX=CUT: MSG={"END"}
[gcode_macro A_UNLOAD_MATERIAL]
gcode:
    RESPOND PREFIX=UNLOAD: MSG={"UNLOAD-MATERIAL"}
    SAVE_GCODE_STATE NAME=recovery_state

    A_CUT_MATERIAL
    RESPOND PREFIX=UNLOAD: MSG={"Unloading"}
    
    M400
    M83
    G1 E-50 F1200 
    M400
  
    RESTORE_GCODE_STATE NAME=recovery_state
    RESPOND PREFIX=UNLOAD: MSG={"END"}
```

9105Sensor code
```
[TTS9105 CUT]
sensor_pin: MKS_THR:PA3
sensor_type: 1
sensor_threshold:0.3,0.7
sensor_update:1.0

[TTS9105 FILA]
sensor_pin: MKS_THR:PA2
sensor_type: 2                         # Type :1 is cut material 2 cut material detection
sensor_threshold:0.4,0.6               # The detection is for a range without consumables
sensor_update:1.0                      # Update time
conversion_code:None                   # Whether to customize the conversion function
#1.301+0.9384*math.cos(x*7.406)+0.4135*math.sin(x*7.406)-0.4723*math.cos(14.812*x)-0.07153*math.sin(14.812*x)
alpha_beta: 0.85,0.01                  # Filter parameter
fila_minmax_threshold:1.5,2.0          # Consumable width output result range
compensate:True                        # Open compensation

event_delay:3
pause_delay:0.5 
width_offset:0.0                       # For example, 
    # if the output result is 1.76 but the actual result is not 1.75, you can input -0.01
    # if the output result is 1.74 but the actual result is not 1.75, you can input 0.01
For example, if the output result is 1.74 but the actual result is not 1.75, you can input 0.01
enable_gcode:   # If trigger is enabled, please customize macro instruction; You can use the original
disable_gcode:  # If trigger is disabled, please customize macro instruction; You can use the original

```

# Use command

Related code
```
    self.gcode.register_mux_command("CUT_TTS9105","NAME", self.name,self.cmd_CUT_TTS9105, desc="CUT FILAMENT") 
    self.gcode.register_mux_command("QUERY_TTS9105","NAME", self.name,self.cmd_QUERY_TTS9105, desc="Query TTS9105 sensor value") 
    self.gcode.register_mux_command("SET_TTS9105","NAME",self.name,self.cmd_SET_TTS9105,desc="SET TTS9105")
    self.gcode.register_mux_command("CLEAR_TTS9105","NAME",self.name,self.cmd_CLEAR_TTS9105,desc="CLEAR TTS9105")
    self.gcode.register_mux_command("INVERT_TTS9105","NAME",self.name,self.cmd_INVERT_TTS9105,desc="INVERt TTS9105")
    self.gcode.register_mux_command('DISABLE_FILA_TTS9105',"NAME",self.name,self.cmd_M406, desc="DISABLE_FILA_TTS9105")
    self.gcode.register_mux_command('ENABLE_FILA_TTS9105',"NAME",self.name,self.cmd_M405, desc="ENABLE_FILA_TTS9105")
    self.gcode.register_mux_command("QUERY_WIDTH","NAME", self.name,self.cmd_QUERY_WIDTH, desc="QUERY WIDTH") 
    self.gcode.register_mux_command("SET_WIDTH_OFFSET","NAME",self.name, self.cmd_SET_WIDTH_OFFSET, desc="SET WIDTH OFFSET")
```
Format "Command + name + Requirement"
For example
   
    QUERY_WIDTH  NAME=FILA
    SET_WIDTH_OFFSET  NAME=FILA OFFSET = 0.01