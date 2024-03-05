from django.db import models
from user.models import Account
# Create your models here.
    
class Task(models.Model):
    STATUS_PENDING = 'PENDING'
    STATUS_START = 'START'
    STATUS_ERROR = 'ERROR'
    STATUS_SUCCESS = 'SUCCESS'

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default="")
    date_time = models.DateTimeField('date_time', auto_now_add=True)
    date_time_modify = models.CharField(max_length=100, default="")
    date_time_upload = models.CharField(max_length=100, default="")
    location = models.CharField(max_length=100, default="")
    description = models.CharField(max_length=256, default="")
    weather = models.CharField(max_length=20, default="", blank=True)
    status = models.CharField(max_length=15, default="")

    def __str__(self):
        return f"{self.name}"
    
class Input(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    video = models.FileField(upload_to = 'uploads/', blank=True)
    sample_img = models.FileField(upload_to = 'uploads/', blank=True)
    fig_img = models.FileField(upload_to = 'uploads/', blank=True)

    def __str__(self):
        return f"{self.video}"
    
class Result(models.Model):
    input = models.ForeignKey(Input, on_delete=models.CASCADE)
    video = models.FileField(upload_to = 'uploads/', blank=True)

    def __str__(self):
        return f"{self.video}"

class Loop(models.Model):
    input = models.ForeignKey(Input, on_delete=models.CASCADE)
    loop_name = models.CharField(max_length=100, blank=True)
    x = models.IntegerField(blank=True)
    y = models.IntegerField(blank=True)
    width = models.IntegerField(blank=True)
    height = models.IntegerField(blank=True)
    angle = models.IntegerField(blank=True)
    direction = models.IntegerField(blank=True)

    def __str__(self):
        return f"{self.loop_name}"
class Car(models.Model):
    loop = models.ForeignKey(Loop, on_delete=models.CASCADE)
    car_total = models.IntegerField(default=0)
    car_type = models.CharField(max_length=20)
    direction = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.car_total}"

class TotalCar(models.Model):
    result = models.ForeignKey(Result, on_delete=models.CASCADE)
    type = models.CharField(max_length=20)
    total = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.type}"
