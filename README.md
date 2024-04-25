# TMI-PlacesForU
## La aplicación "PlacesForU" es desarrollada por un equipo de estudiantes de la asignatura de Tecnologías Multimedia e Interacción.

## Instalación de dependencias  

 Para instalar todas las dependencias del proyecto, ejecuta el siguiente comando en tu terminal dentro del directorio project:

    pip install -r requirements.txt

Es recomendable usar un Entorno Virtual de Python para evitar colisiones con las dependencias de otros proyectos de python, si los hubiera.

## Comandos de utilidad:

Dentro de project: 

Para arrancar el servidor de desarrollo local

    python manage.py runserver [port]

Para generar migraciones (archivos que describen los cambios en la base de datos):

    python manage.py makemigrations

Para aplicar migraciones:

    python manage.py migrate

## Plantilla de Configuración

Dentro del directorio `config`, encontrarás un archivo de plantilla de configuración llamado `config_template.json`. Esta plantilla sirve como guía para configurar los ajustes del proyecto. 

Es importante tener en cuenta que a partir de esta plantilla deberás crear un archivo `config.json` con tus configuraciones específicas en directorio `config`.


