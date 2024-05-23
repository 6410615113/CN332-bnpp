from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
def login(request):
    return redirect('account_login')

@login_required
def profile(request):
    if (request.user.is_superuser):
        return redirect('admin:index')
    return profileRender(request, {})

def profileRender(request, context):
    return render(request, 'account/profile.html', context)

from task2.models import Task, FormTask, TaskStatus, Video, FormVideo, Loop
@login_required
def dashboard(request):
    formTask = FormTask()
    formVideo = FormVideo()
    if request.method == 'POST':
        formTask = FormTask(request.POST)
        if formTask.is_valid():
            task = formTask.save(commit=False)
            task.user = request.user
            task.save()
            Video.objects.create(task=task, user=request.user, video=None)
            return redirect('dashboard')
                
    task = Task.objects.filter(user=request.user)
    print(task)
    data = {
        'formTask': formTask,
        'formVideo': formVideo,
        'tasks': task,
    }
    return dashboardRender(request, data)

def dashboardRender(request, context):
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def edit(request, id):
    task = Task.objects.get(id=id)
    video = Video.objects.get(task=task)
    formTask = FormTask(instance=task)
    formVideo = FormVideo(instance=task.video_set.first())
    if request.method == 'POST' and not int(request.POST.get('upload')):
        inTask = {
            'task': task.id,
            'name': request.POST.get('name'),
            'location': request.POST.get('location'),
            'description': request.POST.get('description'),
        }
        formTask = FormTask(inTask, instance=task)
        if formTask.is_valid():
            task = formTask.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('edit_task', id=id)
    elif request.method == 'POST' and int(request.POST.get('upload')):
        inVideo = {
            'task': task.id,
            'user': request.user.id,
        }
        formVideo = FormVideo(inVideo, request.FILES, instance=video)
        print(formVideo)
        if formVideo.is_valid():
            video = formVideo.save(commit=False)
            video.save()
            return redirect('edit_task', id=id)
        
    data = {
        'task': task,
        'formTask': formTask,
        'formVideo': formVideo,
        'video': video.video,
    }
    return editRender(request, data)

def editRender(request, context):
    return render(request, 'dashboard/edit.html', context)

def delete(request, id):
    task = Task.objects.get(id=id)
    task.delete()
    return redirect('dashboard')

def task(request, id):
    task = Task.objects.get(id=id)
    video = Video.objects.get(task=task)
    loop = Loop.objects.filter(task=task, user=request.user)
    data = {
        'task': task,
        'video': video,
        'loops': loop,
    }
    return taskRender(request, data)

def taskRender(request, context):
    return render(request, 'dashboard/task.html', context)