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


def uploadCustomFirmware(target, source, env):
	# Build uploader command line
	platform = env.PioPlatform()
	uploader_path = [platform.get_package_dir("tool-openocd") + "/bin/openocd"]

	debug_level = ["-d1"]

	board = env.BoardConfig()
	debug_tools = board.get("debug.tools", {})
	upload_protocol = env.subst("$UPLOAD_PROTOCOL")
	server_arguments = debug_tools.get(upload_protocol).get("server").get("arguments", [])

	firmware_path = os.path.join(".", env.GetProjectOption("custom_firmware"))
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

env.AddPlatformTarget(
    name="upload-custom-firmware",
    dependencies=None,
    actions=[env.VerboseAction(uploadCustomFirmware, "Uploading firmware...")],
    title="Upload custom firmware",
    description="Upload a custom firmware"
)
