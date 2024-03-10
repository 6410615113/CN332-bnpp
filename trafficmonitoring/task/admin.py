from django.contrib import admin
from task.models import Task, Result, Input, Loop, Car, TotalCar
# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    list_display = ("account", "name", "date_time", "date_time_modify", "date_time_upload", "location", "description", "weather", "status")

class InputAdmin(admin.ModelAdmin):
    list_display = ("task", "video", "sample_img", "fig_img")

class ResultAdmin(admin.ModelAdmin):
    list_display = ("input", "video")
class LoopAdmin(admin.ModelAdmin):
    list_display = ("input", "loop_name", "x", "y", "width", "height", "angle", "direction")

class CarAdmin(admin.ModelAdmin):
    list_display = ("loop", "car_total", "car_type", "direction")

class TotalCarAdmin(admin.ModelAdmin):
    list_display = ("result", "type", "total")

admin.site.register(Task, TaskAdmin)
admin.site.register(Input, InputAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(Loop, LoopAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(TotalCar, TotalCarAdmin)
