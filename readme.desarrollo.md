# Guia

Esta es la guia para ejecutar el proyecto local.

## Paso 1: Entrar a la carpeta

Debes navegar a la carpeta usando `cd`. Ejemplo:

```
cd Documentos
cd github/transmitata
``` 

## Paso 2: Subir docker 

En la terminal ejecutamos el siguiente comando  `docker compose up` 

Sabremos si lo hemos hecho demanera correcta cuando en la terminal nos aparece fecha y hora actualizandoce cada 3 segundos

## Paso 3: Entrar al contenedor de docker

Para esto debemos abrir una nueva terminal en el signo +.

Una vez que tengamos la nueva ventana de terminal le damos el siguiente comando `docker exec -ti transmitata-web-1 bash`

Sabremos que hemos ingresado al contenedor por que apareceremos en la terminal de la maaquina virtual Ejemplo: 

``` root@673d66b621a1 ```

## Paso 4: Ejecutar Servidor de Python

En la terminal del contenedor colocamos el siguiente comando `python manage.py runserver 0.0.0.0:8000`

sabremos que se ha realizado de manera exitosa cuando nos arroja el siguiente mensaje en la terminal.

```
Django version 4.1.2, using settings 'transmitata.settings'
Starting development server at http://0.0.0.0:8000/
Quit the server with CONTROL-C.
```

para Comprobar que se han realizado bien los pasos debemos pasar al ultimo paso y debe cargar nuestra aplicacion.

## Paso 5: Ingresa a la url

Cuando ingresas a la URL http://localhost:8218/ te debe abrir la pagina del proyecto.

...

