#  SK1 Extruder kit: New design with cutter function and consumable detection

>The SK1 Extrusion Head Kit is a high-performance extrusion system designed for 3D printers. It integrates the latest hardware and intelligent features to provide higher printing accuracy, ease of use and a flexible modular design. The kit is suitable for a variety of 3D printer users, especially those who need efficient, accurate and stable printing.

## Introduction

<img src="Image/preview.png" width="900"/>

The SK1 extruder kit was inspired by the user's urgent need to improve printing efficiency and reduce clog. Most printer users will experience the problem of blocked extrusion heads, resulting in print interruptions and difficult maintenance, especially when replacing consumables, requiring manual handling of residual material filaments.To address these challenges SK1 By adopting a newly designed control scheme, SK1 can not only increase the extrusion flow rate and increase the extrusion speed, but also significantly improve the overall stability and accuracy of the printing. Most importantly, the new cutter function greatly simplifies the material return operation, effectively avoiding material residue in the printer and eliminating the problem of extrusion head clogging. A smarter and more reliable extrusion system for high-end users and those who need fast print speeds.

## Usage scenario

- **High-speed printing users:**  The SK1 extruder head significantly increases the extrusion flow rate, and with the enhanced heating block, users can still maintain stable print quality at high-speed printing.
- **Users of flexible materials such as TPU:**  SK1's cutter function and flow compensation technology ensure that materials can be easily returned when handling flexible materials, ensuring smooth printing.
- **Multi-material switching needs users:**  The modular design of the quick disassembly function, so that users can easily maintain the extrusion head, especially when the need to frequently change different types of materials, greatly improving the efficiency of operation.

## Key Features

<img src="Image/cutter.png" width="300"/>
![SK1 Extruder kit: New design with cutter function and consumable detection](./Image/structure.png)

- **Increased extrusion flow and speed:**  The upgraded extrusion head allows users to print at higher flow rates, accepting up to 37.68mm3/s, while maintaining a stable material flow through a more efficient heating block design and intelligent control.
- **Cutter function:**  The cutter greatly simplifies the material return operation and reduces the blockage problem caused by the material staying in the heating block after tearing. This not only improves the life of the extruder head, but also speeds up the speed of material replacement.
- **Intelligent flow compensation:**  The built-in consumable detector can monitor the use of consumables in real time, and automatically compensate the extrusion flow to ensure that the extrusion is consistent during the printing process, even when the material width error will not affect the printing effect.
- **New PCB control scheme:**  GD32F303 controller: integrated lis2dw gyroscope, improved overall control accuracy, stability and extruder response speed.
- **Modular quick-remove design:**  The simple quick-remove feature allows users to quickly perform routine maintenance or replace modular parts, reducing downtime and significantly improving the user experience.

## Hardware Detailsi
<img src="https://github.com/TWOTREES-TTS/SK1-Extruder-kit-New-design-with-cutter-function-and-consumable-detection/blob/f2b71958c4ee512bc262cedc83f4881f1c707725/Image/STL.png" width="600"/><img src="https://github.com/TWOTREES-TTS/SK1-Extruder-kit-New-design-with-cutter-function-and-consumable-detection/blob/f2b71958c4ee512bc262cedc83f4881f1c707725/Image/STL.png" width="600"/>

 
The STL is a model of the sk1 extruder kit, you can download slices from the Hardware/STL path to print them.
 ![SK1 Extruder kit: New design with cutter function and consumable detection](/Image/STL.png)
 

 
## Compatibility

>The SK1 Extruder Kit is compatible with most 3D printers, particularly those using the CoreXY system. For non-CoreXY machines, some additional configurations may be necessary to optimize performance. The cutter and detection function can be adapted to older klipper versions and sk1's existing screen firmware

## How to Use

- **Filament Loading and Unloading:**  The SK1 system includes the filament cutter for quick and easy filament switching. Simply engage the cutter after the print job to cleanly cut the filament.
- **Flow Compensation Calibration:**  Ensure the filament detector is calibrated by running a few test prints. The system will automatically adjust the extrusion based on real-time filament data.
- **Maintenance:**  Use the quick-release feature to remove the extruder for cleaning or replacement of parts. This reduces downtime and allows for faster printer maintenance.

## Calibration
1.	 The offset value is mainly used to calibrate the error between the measured value and the actual value, and the user only needs to modify its configuration file
2.	 Formula converter, mainly used for users who have strong hands-on ability and are not satisfied with the existing calculation algorithm,(not recommended to modify) can use matlab online function to import measurement data into Firmware/Matlab_simulation/Fourier. M refit the function and convert the formula into python language to write the configuration file (can be compatible with math module)
 ![filter](https://github.com/user-attachments/assets/4b90a529-a230-4081-a3e8-6332506ff2df)

[ ![SK1 Extruder kit: New design with cutter function and consumable detection](/Images/fourier.jpg)](https://github.com/TWOTREES-TTS/SK1-Extruder-kit-New-design-with-cutter-function-and-consumable-detection/blob/18d19fde80f542f92330e23c25ab3c6808a5bc6d/Image/filter.png)
3.	  Alpha-Beta filter is mainly used to suppress the mechanical error generated by the acquisition of consumable sensors, and it is a simplified version of a small computational load similar to Kalman filter. We built a pseudo-model that generates random data so that users can debug the appropriate Alpha and Beta values to adjust the sensitivity and noise resistance of the data
  ![SK1 Extruder kit: New design with cutter function and consumable detection](/Images/filter.jpg)

## Frequently Asked Questions (FAQ)

**Q:  Does SK1 support mmu/ams multi-color printing?**
> A:  Yes, but ams and mmu are our current concept products, and we do not have a released multi-color printing system at the moment.However, the current new extrusion head can be adapted to install open source multi-color printing projects, such as the[EnragedRabbitProject](https://github.com/EtteGit/EnragedRabbitProject)

**Q:  How do SK1 extruders prevent material clog?**
> A:  The SK1 features a new heating block design and integrated cutter function, which automatically cuts off consumables each time the material is changed, avoiding material clogging remaining in the heating block. At the same time, the modular quick-disassembly design is also convenient for users to clean and maintain, greatly reducing the occurrence of clogging.

**Q:  How does the cutter function work?**
> A:  The cutter function automatically cuts off the material after each change of consumables or printing, preventing the material from becoming brittle and blocking the extrusion channel due to prolonged heating. This function not only improves the speed of material switching, but also extends the service life of the extrusion head.

**Q:  Does SK1 support printing of flexible materials such as TPU?**
> A:  Yes, SK1 supports printing of flexible materials such as TPU. Its flow compensation function adjusts the extrusion flow rate in real time to ensure uniform material output during printing. At the same time, the cutting tool function makes the process of returning materials smoother, avoiding the problem of winding or breaking of flexible materials during the return of materials.

**Q:  How do I use the flow compensation function?**
> A:  The flow compensation function relies on SK1's built-in consumable detector, which monitors the consumption of consumables in real time and automatically adjusts the output flow of the extruder. Users do not need to make additional Settings, just ensure that the consumables detector is installed correctly.

**Q:  What are the advantages of SK1's modular quick-disassembly design?**
> A:  The modular quick-release design allows users to quickly remove the extruder head for cleaning, maintenance or replacement parts, reducing downtime. Compared to conventional extruder heads, SK1 is significantly more efficient in maintenance, making it easier for users to change materials or troubleshoot.

**Q:  Can SK1 extruder improve printing speed?**
> A:  Yes. Most machines are limited by the extrusion flow rate rather than the machine's maximum motor motion speed, and SK1 effectively improves the overall print speed by increasing the extrusion flow rate. At the same time, intelligent flow compensation technology ensures that material output remains stable at high speed printing, avoiding quality degradation.

**Q:  How to maintain SK1 extruder?**
> A:  The SK1's modular quick-release design makes maintenance very easy. Users can quickly remove the extruder head and clean the heating block, cutter and consumable transfer channels. It is recommended to periodically clean the consumable detector to ensure its normal operation.Contributing & Feedback

We welcome community contributions to improve and expand the SK1 Extruder Kit. If you have suggestions or encounter any issues, please submit them via the Issues tab. Pull requests are also encouraged for bug fixes, feature enhancements, or documentation improvements.

# Look forward to your feedback

- **The design and development of the SK1 extruder kit has been supported by a lot of user feedback, and we are always committed to continuously improving the product according to the actual needs of users. While the current version still uses some 3D printed parts, we are actively developing an upgraded version that is more durable and has higher performance. User feedback is what drives us forward, and every suggestion will help us optimize the product to ensure that the SK1 extruder can better address pain points in future official launches and provide a first-class user experience.**

- **In this process, we will first publish the design concept, related code, and print model to the GitHub page of the project. We hope to share these ideas with you and encourage you to come up with better ideas and ways to improve. If you have any suggestions or ideas, welcome to contribute your wisdom through the Pull Request, we look forward to working with you to improve this product!**

- **We sincerely invite you to participate in the development and testing of SK1 extruder, whether it is functional suggestions, or experience feedback during use, your opinion is very important to us. Let's promote the development of 3D printing technology!**

- **Stay tuned for our next updates, your support and feedback will help us make SK1 the most competitive extrusion system on the market. You are welcome to leave your valuable comments and suggestions, we look forward to witnessing the growth and progress of SK1 with you!**

## Note

Thank you for using SK1 Extruder Kit! If you have any questions or suggestions during use, please feel free to contact us, we will be happy to work with you to solve. For more product updates and tutorial materials, you can always follow our GitHub page for the latest updates and support.

**Thank you! We are twotrees, looking forward to growing and progressing together with you.**

- **Offical:**  [https://twotrees3d.com](https://twotrees3d.com)
- **Wiki:**     [https://wiki.twotrees3d.com](https://wiki.twotrees3d.com)

