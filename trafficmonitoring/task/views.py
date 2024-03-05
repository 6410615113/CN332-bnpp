from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from .models import Task, Input, Result, Loop, Car, TotalCar
from django.contrib.auth.models import User
from user.models import Account
from .task import detect_track
from opt import OptJson
import cv2
import os
import matplotlib.pyplot as plt
import math
from .loop import Loops as set_loop

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:signin'))
    
    task = Task.objects.all().order_by('-date_time')

    list_detail_task = {}
    for t in task:
        total = 0
        if t.status != "SUCCESS":
            continue
        try:
            input = Input.objects.get(task=t)
            result = Result.objects.get(input=input)
            totalCar = TotalCar.objects.filter(result=result)
            for car in totalCar:
                total += car.total
        except:
            pass
        list_detail_task[t] = {'input':input, 'total': total}

    return render(request, 'task/index.html', {
        # 'task': task,
        'list_detail_task': list_detail_task
    })

def counting_result(request, task_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:signin'))
    
    task = Task.objects.get(id=task_id)
    input = Input.objects.get(task=task)
    result = Result.objects.get(input=input)
    loop = Loop.objects.filter(input=input)
    totalcar = TotalCar.objects.filter(result=result)
    list_totalcar = {}
    list_index = {}
    index = 1
    for t in totalcar:
        list_totalcar[t.type] = t.total

    for l in loop:
        list_index[l.id] = index
        index +=1 

    if request.method == 'POST':
        loop_id = request.POST['loop_id']
        loop_detail = Loop.objects.get(id=int(loop_id))
        car = Car.objects.filter(loop=loop_detail)

        list_left = {}
        list_right = {}
        list_straight = {}
        for c in car:
            if(c.direction == 'LEFT'):
                list_left[c.car_type] = c.car_total
            elif(c.direction == 'RIGHT'):
                list_right[c.car_type] = c.car_total
            elif(c.direction == 'STRAIGHT'):
                list_straight[c.car_type] = c.car_total
        return render(request, 'task/result.html', {
            'task': task,
            'result': result,
            'loop': loop,
            'totalcar': totalcar,
            'list_totalcar': list_totalcar,
            'loop_detail': loop_detail,
            'list_left': list_left,
            'list_right': list_right,
            'list_straight': list_straight,
            'list_index': list_index
        })
    return render(request, 'task/result.html', {
        'task': task,
        'result': result,
        'loop': loop,
        'totalcar': totalcar,
        'list_totalcar': list_totalcar,
        'list_index': list_index
    })
    
def create_task(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:signin'))
    
    if request.method == 'POST':
        user = User.objects.get(username=request.user.username)
        account = Account.objects.get(user=user)
        name = request.POST['name']
        location = request.POST['location']
        description = request.POST['description']  
        weather = request.POST['weather']  

        task = Task.objects.create(account=account, name=name, location=location, weather=weather,
                                    description=description, status=Task.STATUS_PENDING )
        
        video = request.FILES['video']
        input = Input.objects.create(task=task, video=video)
        cam = cv2.VideoCapture(input.video.path)
        ret, frame = cam.read()
        if ret:
            name = str(input.video.name.split('.')[0]) + ".png"
            cv2.imwrite("./media/frame/" + name, frame)
            input.sample_img = "./frame/" + name
            pic = plt.imread("./media/frame/" + name)
            fig = plt.figure()
            ax = fig.subplots()
            ax.imshow(pic)
            plt.savefig("./media/fig/" + name)
            input.fig_img = "./fig/" + name
            input.save()

        return HttpResponseRedirect(reverse('task:edit_loop', args=(task.id,)))
    
    return render(request, 'task/create_task.html')

def edit_loop(request, task_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:signin'))
    
    task = Task.objects.get(id=task_id)
    input = Input.objects.get(task=task)
    if request.method == "POST":
        loop_name = request.POST["loop_name"]
        x = int(request.POST["x"])
        y = int(request.POST["y"])
        width = int(request.POST["width"])
        height = int(request.POST["height"])
        angle = int(request.POST["angle"])
        direction = int(request.POST["direction"])

        loop = Loop.objects.create(input=input, loop_name=loop_name, x=x, y=y,
                                   width=width, height=height, angle=angle, direction=direction)
        set_loop(input).draw_loop()
    all_loop = Loop.objects.filter(input=input)
    return render(request, 'task/edit_loop.html', {
        "task": task,
        "input": input,
        "all_loop": all_loop,
    })

def delete_loop(request, loop_id):
    try:
        loop = Loop.objects.get(id=loop_id)
    except:
        return HttpResponseRedirect(reverse('task:index'))
    
    input = loop.input

    loop.delete()
    set_loop(input).draw_loop()
    return HttpResponseRedirect(reverse('task:edit_loop', args=(input.task.id,)))

def run_task(request, task_id):
    task = Task.objects.get(id=task_id)
    input = Input.objects.get(task=task)
    opt = OptJson
    opt['source'] = input.video.path
    opt['project'] = './media/uploads/' + str(request.user.username) + '/' + str(task.id)
    opt['loop'] = set_loop(input).create_loop(Loop.objects.filter(input=input))

    task.status=Task.STATUS_PENDING
    task.save()

    detect_track.delay(opt, task.id)
    return HttpResponseRedirect(reverse('task:mytask'))


def my_task(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:signin'))
    
    user = User.objects.get(username=request.user.username)
    account = Account.objects.get(user=user)
    task = Task.objects.filter(account=account).order_by('-date_time')

    return render(request, 'task/mytask.html', {
        'task': task,
    })

def modify_loop(request, task_id, loop_id):
    task = Task.objects.get(id=task_id)
    input = Input.objects.get(task=task)
    loop = Loop.objects.get(id=loop_id)
    if request.method == "POST":
        loop.loop_name = request.POST["loop_name"]
        loop.x = int(request.POST["x"])
        loop.y = int(request.POST["y"])
        loop.width = int(request.POST["width"])
        loop.height = int(request.POST["height"])
        loop.angle = int(request.POST["angle"])
        loop.direction = int(request.POST["direction"])
        loop.save()
        set_loop(input).draw_loop()
        return HttpResponseRedirect(reverse('task:edit_loop', args=(task.id,)))

    return render(request, 'task/modify_loop.html',{
        'task': task,
        'input': input,
        "loop":loop
    })