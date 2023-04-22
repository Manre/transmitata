import subprocess
import time

cmd_str = "/transmitata/bin/loophole1.0.0-beta.15.armv7 http --hostname transmitata 8000"
# cmd_str = "./loophole http --hostname transmitata 8000"

while True:
    try:
        subprocess.run(cmd_str, shell=True)
    except Exception as error:
        print(f"An exception has occurred {str(error)}")
        time.sleep(25)
        pass
