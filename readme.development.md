You can run the project by doing the following:

    docker-compose build  # download and build all the docker dependencies
    docker-compose up  # start the docker based on the configuration

If you want to log into the machine you can:

    docker exec -it transmitata_web_1 bash

The project should be under the /transmitata/ directory

The following commands will help you accomplish certain tasks

    python manage.py shell_plus  # an overpower shell! xD
    python manage.py runserver 0.0.0.0:8000  # run the server

# Troubleshooting

1. Check for logs: `docker logs transmitata_web_1 --tail 1000`
2. Enter into the instance: `docker exec -it transmitata_web_1 bash`

# Service on RPi

Taken from https://stackoverflow.com/questions/43671482/how-to-run-docker-compose-up-d-at-system-start-up

## Transmitata
0. Create `transmitata.service` on `/etc/systemd/system/` with
```bash
[Unit]
Description=Docker Compose Application Service
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/pi/Documents/code/transmitata
ExecStart=/usr/local/bin/docker-compose up -d
ExecStop=/usr/local/bin/docker-compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```
0. Enable the service with `systemctl enable transmitata`. Now you will only need to restart the RPi to test it.
0. Check for the status `systemctl status transmitata`.

## Transmitata Status Checker
0. Create `transmitata_status_checker.service` on `/etc/systemd/system/` with
```bash
[Unit]
Description=Service to check Transmitata disponibility

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/pi/Documents/code/transmitata
ExecStart=python internet_checker.py
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```
0. Enable the service with `systemctl enable transmitata_status_checker`. Now you will only need to restart the RPi to test it.
0. Check for the status `systemctl status transmitata_status_checker`.
