from django.urls import path
from .views import list_clusters, list_services, list_tasks, register, user_logout

urlpatterns = [
    path('list_clusters/', list_clusters, name='list_clusters'),
    path('list_services/<str:cluster_name>/', list_services, name='list_services'),
    path('list_tasks/<str:cluster_name>/<str:task_arn>/', list_tasks, name='list_tasks'),
    path('register/', register, name='register'),
    path('logout/', user_logout, name='logout'),
    # Otras rutas aquí si las tienes
]
