from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'task'

urlpatterns = [
    path('', views.index, name='index'),
    path('result/<int:task_id>', views.counting_result, name='result'),
    path('create_task', views.create_task, name='create_task'),
    path('mytask/', views.my_task, name='mytask'),
    path('edit_loop/<int:task_id>', views.edit_loop, name='edit_loop'),
    path('delete_loop/<int:loop_id>', views.delete_loop, name='delete_loop'),
    path('run_task/<int:task_id>', views.run_task, name='run_task'),
    path('modify_loop/<int:task_id>/<int:loop_id>', views.modify_loop, name='modify_loop'),

] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
