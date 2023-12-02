import boto3
import subprocess
import json


def extract_last_hash(arn):
    # Split the ARN by '/'
    parts = arn.split('/')
    
    # Take the last element of the list
    last_part = parts[-1]
    
    return last_part


def get_task_info(cluster_name, task_arn):
    # Configurar el cliente de ECS
    ecs_client = boto3.client('ecs')

    try:
        # Obtener información detallada sobre la tarea
        task_response = ecs_client.describe_tasks(cluster=cluster_name, tasks=[task_arn])

        # Extraer información relevante de la tarea
        task_info = {
            'last_status': task_response['tasks'][0]['lastStatus'],
            'started_at': task_response['tasks'][0]['createdAt'],
            'task_id': task_response['tasks'][0]['taskArn'].split('/')[-1],  # Utilizar el ID de la tarea desde la ARN
            # Agregar más información según sea necesario
        }

        return task_info

    except Exception as e:
        return {'error': f'An error occurred: {str(e)}'}
    

    import subprocess
import json

def get_task_info_using_describe_tasks(cluster_name, task_id):
    try:
        # Ejecutar el comando describe-tasks y capturar la salida
        describe_tasks_command = [
            'aws', 'ecs', 'describe-tasks', '--cluster', cluster_name, '--tasks', task_id
        ]
        task_info_json = subprocess.check_output(describe_tasks_command)

        # Cargar la salida JSON
        task_info = json.loads(task_info_json)['tasks'][0]

        # Formatear la información según sea necesario
        formatted_info = {
            'last_status': task_info['lastStatus'],
            'started_at': task_info['createdAt'],
            'task_id': task_id,
            # Agregar más información según sea necesario
        }

        return formatted_info

    except subprocess.CalledProcessError as e:
        # Si el comando devuelve un código de error, capturar la salida de error
        return {'error': f'An error occurred: {e.output.decode("utf-8").strip()}'}

    except Exception as e:
        return {'error': str(e)}
