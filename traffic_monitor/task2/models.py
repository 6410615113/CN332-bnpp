from django.db import models
from django import forms
from django.utils import timezone

# Create your models here.
class Task(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date_time = models.DateTimeField('date time', default=timezone.now)
    location = models.CharField(max_length=100)
    description = models.TextField()
    migration = None       
    
    def __str__(self):
        return self.name
    
class FormTask(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'location', 'description']
        labels = {
            'name': 'Task Name',
            'location': 'Location',
            'description': 'Description',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }
        
class TaskStatus(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    status = models.BooleanField()
    
    def __str__(self):
        return self.task.name + ' - ' + self.user.username
    
class Video(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    video = models.FileField(upload_to='videos/')
    date_time = models.DateTimeField('date time', default=timezone.now)
    
    def __str__(self):
        return self.task.name + ' - ' + self.user.username
    
class FormVideo(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['video']
        labels = {
            'video': 'Video',
        }
        
class Loop(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    start_x = models.IntegerField(blank=True)
    start_y = models.IntegerField(blank=True)
    end_x = models.IntegerField(blank=True)
    end_y = models.IntegerField(blank=True)
    
    def __str__(self):
        return self.task.name + ' - ' + self.user.username + ' (' + str(self.x) + ', ' + str(self.y) + ')'
    
class FormLoop(forms.ModelForm):
    class Meta:
        model = Loop
        fields = ['start_x', 'start_y', 'end_x', 'end_y']
        labels = {
            'start_x': 'Start X',
            'start_y': 'Start Y',
            'end_x': 'End X',
            'end_y': 'End Y',
        }
        
class Vehicle(models.Model):
    loop = models.ForeignKey(Loop, on_delete=models.CASCADE)
    car_type = models.CharField(max_length=100)
    car_total = models.IntegerField()
    
    def __str__(self):
        return self.car_type + ' - ' + str(self.car_total)