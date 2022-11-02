You can run the project by doing the following:

    docker-compose build  # download and build all the docker dependencies
    docker-compose up  # start the docker based on the configuration

If you want to log into the machine you can:

    docker exec -it transmitata_web_1 bash

The project should be under the /transmitata/ directory

The following commands will help you accomplish certain tasks

    python manage.py shell_plus  # an overpower shell! xD
    python manage.py runserver 0.0.0.0:8000  # run the server
