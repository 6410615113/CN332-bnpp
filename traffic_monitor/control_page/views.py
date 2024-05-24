from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage

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

from task2.models import Task, FormTask, Video, FormVideo, Loop, FormLoop
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

from moviepy.editor import VideoFileClip
def task(request, id):
    task = Task.objects.get(id=id)
    video = Video.objects.get(task=task)
    loop = Loop.objects.filter(task=task, user=request.user)
    formLoop = FormLoop()
    if request.method == 'POST':
        sx = int(request.POST.get('start_x'))
        sy = int(request.POST.get('start_y'))
        ex = int(request.POST.get('end_x'))
        ey = int(request.POST.get('end_y'))
        videoSize = VideoFileClip('./media/'+str(video.video)).size
        r = int(videoSize[0] / videoSize[1] * 360)
        sx = int((sx / r) * videoSize[0])
        sy = int((sy / 360) * videoSize[1])
        ex = int((ex / r) * videoSize[0])
        ey = int((ey / 360) * videoSize[1])
        inLoop = {
            'task': task.id,
            'user': request.user.id,
            'start_x': sx,
            'start_y': sy,
            'end_x': ex,
            'end_y': ey,
        }
        formLoop = FormLoop(inLoop)
        if formLoop.is_valid():
            loop = formLoop.save(commit=False)
            loop.save()
            return redirect('view_task', id=id)

    data = {
        'task': task,
        'video': video.video,
        'loops': loop,
        'formLoop': formLoop,
    }
    return taskRender(request, data)

def taskRender(request, context):
    return render(request, 'dashboard/task.html', context)