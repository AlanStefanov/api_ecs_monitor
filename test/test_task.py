import unittest
from ecs_app.utils import get_task_info
from ecs_app.views import list_tasks
from ecs_app.views import list_tasks_for_service

class TestECSFunctions(unittest.TestCase):

    def test_get_task_info(self):
        # Simula un ARN de tarea válido
        cluster_name = "farmu-platform-dev"
        task_arn = "arn:aws:ecs:us-east-1:363019666687:cluster/farmu-platform-dev"

        # Llama a la función y verifica si no devuelve un error
        task_info = get_task_info(cluster_name, task_arn)
        self.assertNotIn('error', task_info)

        # Agrega más aserciones según sea necesario para verificar la salida esperada
        self.assertEqual(task_info['last_status'], 'RUNNING')

if __name__ == '__main__':
    unittest.main()

import unittest
from ecs_app.utils import get_task_info_using_describe_tasks

class TestECSFunctions(unittest.TestCase):
    def test_get_task_info(self):
        cluster_name = 'farmu-platform-dev'
        task_id = '05234ac59d4844029691c89aaba4def8'

        # Obtener información de la tarea utilizando describe-tasks
        task_info = get_task_info_using_describe_tasks(cluster_name, task_id)

        print(task_info)  # Agrega esta línea para imprimir la información obtenida

        # Verificar que no haya errores en la información de la tarea
        self.assertNotIn('error', task_info)

if __name__ == '__main__':
    unittest.main()