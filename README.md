### What is this project? ###

This project contains a script (upload_firmware.py) that can be used to upload
a custom firmware binary to a STM32 board using PlatformIO in Visual Studio Code.

### How to use ###

1. Place the script and your firmware binary at the root of you PlatformIO project
2. Add the following two lines in the [env] section of your platformio.ini file:
~~~~
custom_firmware = <firmware file name>
extra_scripts = pre:upload_firmware.py
~~~~
3. Save the file
4. Access the PlatformIO tab on the left of Visual Studio Code
5. Select `<Your environment name>` => Platform => Upload custom firmware

### Using from a subfolder

You can also place the script and the firmware in a project subfolder.
To do so, you have to adapt the syntax in the platformio.ini as follows:
~~~~
custom_firmware = path/to/your/firmware.bin
extra_scripts = pre:path/to/this/script.py
~~~~
Notes:
- both files must be in the project
- do not add a leading "/" to the path.
