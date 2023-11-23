'''
Copyright © 2023 Clément Foucher

Distributed under the GNU GPL v2. For full terms see the file LICENSE.txt.

This script is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 2 of the License.

This script is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this file. If not, see <http://www.gnu.org/licenses/>.

==================== What is this file? ====================

This script can be used to upload a custom firmware binary
to a STM32 board using PlatformIO in Visual Studio Code.

Suported protocols:
- ST Link
- Mbed

======================== How to use ========================

1) Place this script and your firmware binary at the root of you PlatformIO project
2) Add the following two lines in the [env] section of your platformio.ini file:
        custom_firmware = <firmware file name>
        extra_scripts = pre:upload_firmware.py
3) Save the file
4) Access the PlatformIO tab on the left of Visual Studio Code
5) Select <Your environment name> => Platform => Upload custom firmware
'''

import os
import subprocess

Import("env")


def uploadWithStlink(firmware_path):
	# Build uploader command line
	platform = env.PioPlatform()
	uploader_path = [platform.get_package_dir("tool-openocd") + "/bin/openocd"]

	debug_level = ["-d1"]

	board = env.BoardConfig()
	debug_tools = board.get("debug.tools", {})
	upload_protocol = env.subst("$UPLOAD_PROTOCOL")
	server_arguments = debug_tools.get(upload_protocol).get("server").get("arguments", [])

	firmware_address = board.get("upload.offset_address", "0x08000000")
	program_arguments = ["-c", f"program {firmware_path} {firmware_address} verify reset; shutdown;"]

	command_line = uploader_path + debug_level + server_arguments + program_arguments

	# Replace $PACKAGE_DIR by its path
	command_line = [
		f.replace("$PACKAGE_DIR",
			platform.get_package_dir("tool-openocd") or "")
		for f in command_line
	]

	# Display command and run it
	print(command_line)
	subprocess.run(command_line)

def uploadWithMbed(firmware_path):
	env.AutodetectUploadPort(env)

	assert "UPLOAD_PORT" in env

	from shutil import copyfile
	copyfile(firmware_path, os.path.join(env.subst("$UPLOAD_PORT"), firmware_path))
	print(
		"Firmware has been successfully uploaded.\n"
		"(Some boards may require manual hard reset)"
	)

def uploadCustomFirmware(target, source, env):
	firmware_file = env.GetProjectOption("custom_firmware")
	firmware_path = os.path.join(".", firmware_file)
	if not os.path.isfile(firmware_path):
		print(f"ERROR: unable to find firmware file '{firmware_file}'")
		print("Please make sure file exists and parameter 'custom_firmware' is correctly set in the platformio.ini file")
		exit(-1)

	try:
		protocol = env.GetProjectOption("upload_protocol")
	except NoOptionError:
		print("'upload_protocol' is not defined in 'platformio.ini'.")
		print("Defaulting to ST Link for upload")
		protocol = "stlink"

	if protocol == "stlink":
		print("ST Link will be used for upload")
		uploadWithStlink(firmware_path)
	elif protocol == "mbed":
		print("Mbed will be used for upload")
		uploadWithMbed(firmware_path)
	else:
		print("Unkown or unsuppored protocol.")
		print("Defaulting to ST Link for upload")
		uploadWithStlink(firmware_path)


env.AddPlatformTarget(
    name="upload-custom-firmware",
    dependencies=None,
    actions=[env.VerboseAction(uploadCustomFirmware, "Uploading firmware...")],
    title="Upload custom firmware",
    description="Upload a custom firmware"
)
