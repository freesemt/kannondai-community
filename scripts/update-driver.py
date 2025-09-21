import os
import sys
from subprocess import run
from molass_legacy import get_version
from molass_legacy.Build.Chrome import get_installed_chrome_version, get_available_driver_version

assert get_version() >= "0.2.6", "molass_legacy>=0.2.6 is required."

chrome_version = get_installed_chrome_version()
print(chrome_version)

driver_version = get_available_driver_version(chrome_version)
print(driver_version)

command = [sys.executable, "-m", "pip", "install", "chromedriver-binary==%s" % driver_version]
print(command)
run(command)
