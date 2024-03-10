from celery import shared_task
import sys
sys.path.append('./arial-car-track')
from detect_class import Detect
from opt import Opt
from .models import Task, Input, Result, Loop, Car, TotalCar
from django.contrib.auth.models import User


@shared_task()
def detect_track(opt_json, task_id):
    task = Task.objects.get(id=task_id)
    try:
        task.status = Task.STATUS_START
        task.save()
        opt = Opt()
        opt.set_opt(opt_json)
        detect = Detect(opt)
        detect.run()

        input = Input.objects.get(task=task)
        user = User.objects.get(username=task.account.user.username) 
        file_name = str(input.video).split('/')[1]

        video = './uploads/' + str(user.username) + '/' + str(task.id) + '/object_tracking/' + file_name

        result = Result.objects.create(input=input, video=video)

        report_result = './media/uploads/' + str(user.username) + '/' + str(task.id) + '/object_tracking/loop.txt'
        report_car = []
        try:
            f = open(report_result, "r")
            for x in f:
                report_car.append(x.split(','))
            print(report_car)
        except:
            pass
        loop = Loop.objects.filter(input=input)
        list_type_car = ['car', 'motorcycle', 'truck']
        list_direction = ['LEFT', 'RIGHT', 'STRAIGHT']
        for t in list_type_car:
            TotalCar.objects.create(result=result, type=t, total=0)

        for l in loop:
            for t in list_type_car:
                for d in list_direction:
                    Car.objects.create(loop=l, car_total=0, car_type=t, direction=d)

        
        all_car_id = {}
        for i in range(len(report_car)):
            direction = report_car[i][-1][:-1]
            loop_id = report_car[i][0]
            car_id = report_car[i][1]
            car_type = report_car[i][2]
            if " " in direction: direction = direction[1:]

            if(direction == 'ENTERED'):
                all_car_id[car_id] = car_type
            else:
                if (car_id in all_car_id):
                    t = ''
                    if(all_car_id[car_id] == 'Car'):
                        t = 'car'
                    elif(all_car_id[car_id] == 'Motorcycle sidecar'):
                        t = 'motorcycle'
                    elif(all_car_id[car_id] == 'Pickup truck'):
                        t = 'truck'
                    else:
                        pass
                    totalcar = TotalCar.objects.get(result=result, type=t)
                    loop = Loop.objects.get(id=int(loop_id))

                    car = Car.objects.get(loop=loop, car_type=t, direction=direction)
                    totalcar.total += 1
                    car.car_total += 1
                    totalcar.save()
                    car.save()
                    del all_car_id[car_id]
            
        task.status = Task.STATUS_SUCCESS
    except Exception as e:
        print(e)
        task.status = Task.STATUS_ERROR
    task.save()
    return "finish!"