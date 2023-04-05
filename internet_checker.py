import subprocess
import time

# cmd_str = "curl -Is transmitata.loophole.site | head -n 1"
# cmd_str = "curl transmitata.loophole.site -s -o /dev/null -w '%{http_code}\n'"
# cmd_str = "curl -IsL --insecure  https://transmitata.loophole.site"
status_check_command = "curl -IsL --insecure  https://transmitata.loophole.site -o /dev/null -w '%{http_code}\n'"
reboot_command = "sudo reboot"

UNRESPONSIVE_MINUTES = 10
TIMEOUT_IN_SECONDS = 8

unresponsive_server = 0
while True:
    exception_occurred = False
    error = None

    try:
        response = subprocess.run(status_check_command, shell=True, capture_output=True, timeout=TIMEOUT_IN_SECONDS)
    except Exception as error:
        exception_occurred = True
        status_code = "None"
    else:
        status_code = response.stdout.decode()  # "200\n"

    if exception_occurred is True or ("200" not in status_code):
        unresponsive_server = unresponsive_server + 1
        print(
            f"An exception has occurred {str(error)} - status_code: {status_code} "
            f"Unresponsive server count {unresponsive_server}, "
            f"{unresponsive_server * UNRESPONSIVE_MINUTES} seconds, "
            f"{unresponsive_server * UNRESPONSIVE_MINUTES / 60} minutes."
        )
    else:
        print("Server is responding...")
        unresponsive_server = 0

    time.sleep(10)

    if unresponsive_server >= 6 * UNRESPONSIVE_MINUTES:
        print(f"Rebooting server... Unresponsive server count {unresponsive_server}")
        subprocess.run(reboot_command, shell=True)