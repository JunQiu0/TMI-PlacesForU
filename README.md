# TMI-PlacesForU
## La aplicación "PlacesForU" es desarrollado por un equipo de estudiantes de la asignatura de Tecnología Multimedia e Interacción.

## Instalación de dependencias  

 Para instalar todas las dependencias del proyecto, ejecuta el siguiente comando en tu terminal dentro del directorio proejct:

    pip install -r requirements.txt

Es recomentable usar Entorno Virtual de Python para evitar colisiones con las dependencias de otros proyectos de python, si los hubiera.

## Comandos de utilidad:

Dentro de project: 

Para arrancar servidor de desarrollo local

    python manage.py runserver [port]

Para generar migraciones (archivos que describen los cambios en la base de datos):

    python manage.py makemigrations,

Comando para aplicar migraciones:

    python manage.py migrate



