API Monitor ECS

Requerimientos

    Python 3.11.6
    venv (se recomienda, pero opcional)
    pip (se instala con Python)

Instalación

    Clona el repositorio  y luego acceder al repositorio


Crea un entorno virtual dentro del proyecto: 


python -m venv venv

Activa el entorno virtual:

    En Windows:

    

venv\Scripts\activate

En Linux/macOS:



    source venv/bin/activate

Instala las dependencias:



    pip install -r requirements.txt


------------------------------

Migraciones de la Base de Datos

Realiza las migraciones de la base de datos con los siguientes comandos:



python manage.py makemigrations
python manage.py migrate

------------------------------

Inicia el servidor con el siguiente comando:


python manage.py runserver

El servidor estará disponible en http://localhost:8000/.

*Endpoints*

Listar Clusters

    URL: ecs_app/list_clusters/
    Método: GET
    Descripción: [Lista todos los clusters en la zona indicada en el archivo de variables de entorno]

Listar Servicios por Cluster

    URL: ecs_app/list_services/<str:cluster_name>/
    Método: GET
    Descripción: [Muestra todos los servicios de un determinado cluster en AWS ECS]
    Ejemplo: http://127.0.0.1:8000/ecs_app/list_services/farmu-platform-dev

Listar Tareas

    URL: ecs_app/list_tasks/<str:cluster_name>/<str:task_id>/
    Método: GET
    Descripción: [Devuelve toda la información de la tarea seleccion de determinado servicio por su id]
    Ejemplo: http://127.0.0.1:8000/ecs_app/list_task/farmu-platform-dev/<id>


Listar Tarea especifica por nombre

    URL: ecs_app/list_tasks_for_service/<str:cluster_name>/<str:service_namen>/
    Método: GET
    Descripción: [Devuelve toda la información de la tarea seleccion de determinado servicio]
    Ejemplo: http://127.0.0.1:8000/ecs_app/list_tasks_for_service/farmu-platform-dev/co-front-account-dev0/


    ----

Gestion de usuarios::

Login:
    URL: ecs_app/login
    Método: POST
    Descripción: [Se ingresa "user" y "password"]


    URL: ecs_app/logout
    Método: GET
    Descripción: [Cierrra sesion y redirecciona al login]
