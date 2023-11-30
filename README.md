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

Migraciones de la Base de Datos

Realiza las migraciones de la base de datos con los siguientes comandos:



python manage.py makemigrations
python manage.py migrate

Iniciar el Servidor

Inicia el servidor con el siguiente comando:



python manage.py runserver

El servidor estará disponible en http://localhost:8000/.
Endpoints
Listar Clusters

    URL: /list_clusters/
    Método: GET
    Descripción: [Lista todos los clusters en la zona indicada en el archivo de variables de entorno]

Listar Servicios

    URL: /list_services/<str:cluster_name>/
    Método: GET
    Descripción: [Muestra todos los servicios de un determinado cluster en AWS ECS]

Listar Tareas

    URL: /list_tasks/<str:cluster_name>/<str:task_arn>/
    Método: GET
    Descripción: [Devuelve toda la información de la tarea seleccion de determinado servicio]