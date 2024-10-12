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
