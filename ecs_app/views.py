from django.shortcuts import render
from botocore.exceptions import ClientError

import boto3
from django.http import JsonResponse


def list_clusters(request):
    ecs_client = boto3.client('ecs')
    clusters = ecs_client.list_clusters()['clusterArns']
    return JsonResponse({'clusters': clusters})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')  # Redirige a la página principal después del registro
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')  # Redirige a la página de inicio de sesión después del cierre de sesión

from django.shortcuts import render
from botocore.exceptions import ClientError
import boto3


def list_services(request, cluster_name):
    # Configura el cliente de ECS
    ecs_client = boto3.client('ecs')

    # Obtiene la lista de servicios para el cluster especificado
    response = ecs_client.list_services(cluster=cluster_name)

    # Extrae información relevante de la respuesta
    service_arns = response.get('serviceArns', [])

    # Información sobre servicios y tareas
    service_info = []

    for service_arn in service_arns:
        # Obtiene información detallada sobre el servicio
        service_response = ecs_client.describe_services(cluster=cluster_name, services=[service_arn])

        # Obtiene la lista de tareas del servicio
        tasks_info = []

        try:
            # Obtiene información sobre las tareas
            tasks_response = ecs_client.list_tasks(cluster=cluster_name, serviceName=service_response['services'][0]['serviceName'])
            task_arns = tasks_response.get('taskArns', [])

            for task_arn in task_arns:
                # Obtiene información detallada sobre la tarea
                task_response = ecs_client.describe_tasks(cluster=cluster_name, tasks=[task_arn])

                # Extrae información relevante de la tarea
                task_info = {
                    'task_id': task_arn.split('/')[-1],  # Usa el ID de la tarea desde la ARN
                    'last_status': task_response['tasks'][0]['lastStatus'],
                    'started_at': task_response['tasks'][0]['createdAt'],
                    # Agrega más información según sea necesario
                }

                # Agrega información de la tarea al resultado
                tasks_info.append(task_info)

        except Exception as e:
            tasks_info.append({'error': str(e)})

        # Agrega información del servicio y las tareas al resultado
        service_info.append({
            'service_arn': service_arn,
            'service_name': service_response['services'][0]['serviceName'],
            'tasks': tasks_info,
            # Agrega más información del servicio según sea necesario
        })

    # Pasa la información a la plantilla para su representación
    return render(request, 'ecs_app/services_list.html', {'services': service_info})


from django.shortcuts import render
import boto3

def list_tasks(request, cluster_name, task_arn):
    # Configura el cliente de ECS
    ecs_client = boto3.client('ecs')

    try:
        # Obtiene información detallada sobre la tarea
        task_response = ecs_client.describe_tasks(cluster=cluster_name, tasks=[task_arn])

        # Extrae información relevante de la tarea
        task_info = {
            'task_arn': task_response['tasks'][0]['taskArn'],
            'last_status': task_response['tasks'][0]['lastStatus'],
            'started_at': task_response['tasks'][0]['createdAt'],
            # Agrega más información según sea necesario
        }

        # Pasa la información a la plantilla para su representación
        return render(request, 'ecs_app/task_details.html', {'task': task_info})

    except Exception as e:
        # Si ocurre un error, muestra un mensaje de error
        return render(request, 'ecs_app/task_details.html', {'error': str(e)})
    
import subprocess
import json
from django.http import JsonResponse
from .utils import extract_last_hash

def list_tasks_for_service(request, cluster_name, service_name):
    try:
        # Obtener la lista de tareas del servicio
        task_arns = subprocess.check_output(
            ['aws', 'ecs', 'list-tasks', '--cluster', cluster_name, '--service', service_name]
        )
        task_arns = json.loads(task_arns)['taskArns']

        # Información sobre tareas
        tasks_info = []

        for task_arn in task_arns:
            # Extraer el último hash después del último '/'
            task_hash = extract_last_hash(task_arn)

            # Obtener información específica de la tarea utilizando describe-tasks
            task_info = get_task_info_using_describe_tasks(cluster_name, task_hash)

            tasks_info.append(task_info)

        # Pasa la información a la plantilla para su representación
        return JsonResponse({'tasks': tasks_info})

    except Exception as e:
        # Si ocurre un error, muestra un mensaje de error
        return JsonResponse({'error': str(e)})


def get_task_info_using_describe_tasks(cluster_name, task_id):
    try:
        # Obtener información detallada sobre la tarea utilizando describe-tasks
        task_info_json = subprocess.check_output(
            ['aws', 'ecs', 'describe-tasks', '--cluster', cluster_name, '--tasks', task_id]
        )
        task_info = json.loads(task_info_json)['tasks'][0]

        # Formatear la información según sea necesario
        formatted_info = {
            'last_status': task_info['lastStatus'],
            'started_at': task_info['createdAt'],
            'task_id': task_id,
            # Agregar más información según sea necesario
        }

        return formatted_info

    except Exception as e:
        return {'error': str(e)}
