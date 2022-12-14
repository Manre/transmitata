You can run the project by doing the following:

    docker-compose build  # download and build all the docker dependencies
    docker-compose up  # start the docker based on the configuration

If you want to log into the machine you can:

    docker exec -it transmitata_web_1 bash

The project should be under the /transmitata/ directory

The following commands will help you accomplish certain tasks

    python manage.py shell_plus  # an overpower shell! xD
    python manage.py runserver 0.0.0.0:8000  # run the server

# Service on RPi

Taken from https://stackoverflow.com/questions/43671482/how-to-run-docker-compose-up-d-at-system-start-up

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