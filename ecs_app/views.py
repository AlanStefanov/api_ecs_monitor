from django.shortcuts import render
from botocore.exceptions import ClientError
import boto3
from django.http import JsonResponse
from .utils import extract_last_hash
import subprocess

import json
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

# Gestion de usuarios

@csrf_exempt  
@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        username = data.get('username')
        password = data.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True, 'message': 'Login exitoso'})
        else:
            return JsonResponse({'success': False, 'message': 'Credenciales inválidas'})
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'success': True, 'message': 'Logout exitoso'})
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})



#----------------------------
#Vistas de la aplicacion ECS
#Lista de cluster

def list_clusters(request):
    ecs_client = boto3.client('ecs')
    
    try:
        # Obtener la lista de clusters
        response = ecs_client.list_clusters()
        cluster_arns = response.get('clusterArns', [])

        # Extraer solo los nombres de los clusters
        cluster_names = [arn.split('/')[1] for arn in cluster_arns]

        return JsonResponse({'clusters': cluster_names})

    except Exception as e:
        return JsonResponse({'error': str(e)})

#Lista de servicios

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

    return JsonResponse({'services': service_info})
    

#Lista de tareas

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

        return JsonResponse({'task': task_info})

    except Exception as e:
                return JsonResponse({'error': str(e)})
    

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

        return JsonResponse({'tasks': tasks_info})

    except Exception as e:
        return JsonResponse({'error': str(e)})

#Describir tareas utilizando su id con mayor precision.
def get_task_info_using_describe_tasks(cluster_name, task_id):
    try:
        # Obtener información detallada sobre la tarea utilizando describe-tasks
        task_info_json = subprocess.check_output(
            ['aws', 'ecs', 'describe-tasks', '--cluster', cluster_name, '--tasks', task_id]
        )
        task_info = json.loads(task_info_json)['tasks'][0]

        formatted_info = {
            'last_status': task_info['lastStatus'],
            'started_at': task_info['createdAt'],
            'task_id': task_id,
        }

        return formatted_info

    except Exception as e:
        return {'error': str(e)}
