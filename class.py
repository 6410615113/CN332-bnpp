class User:
    def init(self, user_id, user_name, user_email):
        self.user_id = user_id
        self.user_name = user_name
        self.user_email = user_email

    def getUser_id(self):
        return self.user_id

    def getUser_name(self):
        return self.user_name

    def getUser_email(self):
        return self.user_email

    def setUser_id(self, user_id):
        self.user_id = user_id

    def setUser_name(self, user_name):
        self.user_name = user_name

    def setUser_email(self, user_email):
        self.user_email = user_email

class Accout(User):
    def init(seft, account_id, img_profile, role):
        seft.account_id = account_id
        seft.img_profile = img_profile
        seft.role = role

    def get_account_id(seft):
        return seft.accout_id

    def get_img_profile(seft):
        return seft.img_profile

    def get_role(seft):
        return seft.role

    def set_account_id(seft, account_id):
        seft.account_id = account_id

    def set_img_profile(seft, img_profile):
        seft.img_profile = img_profile

    def set_role(seft, role):
        seft.role = role

class Result:
    def __init__(self, result_id, video, weather, loop):
        self.result_id = result_id
        self.video = video
        self.weather = weather
        self.loop = loop

    def get_result_id(self):
        return self.result_id

    def get_video(self):
        return self.video

    def get_weather(self):
        return self.weather

    def set_video(self, video):
        self.video = video

    def set_weather(self, weather):
        self.weather = weather

class Car:
    def __init__(self, car_id, car_type, direct, car_total):
        self.car_id = car_id
        self.car_type = car_type
        self.direct = direct
        self.car_total = car_total

    def get_car_id(self):
        return self.car_id

    def get_car_type(self):
        return self.car_type

    def get_direct(self):
        return self.direct

    def get_car_total(self):
        self.car_total += 1

    def set_car_id(self, car_id):
        self.car_id = car_id

    def set_car_type(self, car_type):
        self.car_type = car_type

    def set_direct(self, direct):
        self.direct = direct

    def set_car_total(self, car_total):
        self.car_total = car_total

class Task:
    def __init__(self, task_id, date_time, date_time_modify, date_time_upload, location, description, status):
        self.task_id = task_id
        self.date_time = date_time
        self.date_time_modify = date_time_modify
        self.date_time_upload = date_time_upload
        self.location = location
        self.description = description
        self.status = status

    def setTaskId(self, task_id):
        self.task_id = task_id
    
    def getTaskId(self):
        return self.task_id

    def setDateTime(self, date_time):
        self.date_time = date_time

    def getDateTime(self):
        return self.date_time

    def setDateTimeModify(self, date_time_modify):
        self.date_time_modify = date_time_modify

    def getDateTimeModify(self):
        return self.date_time_modify

    def setDateTimeUpload(self, date_time_upload):
        self.date_time_upload = date_time_upload

    def getDateTimeUpload(self):
        return self.date_time_upload

    def setLocation(self, location):
        self.location = location

    def getLocation(self):
        return self.location

    def setDescription(self, description):
        self.description = description

    def getDescription(self):
        return self.description

    def setStatus(self, status):
        self.status = status

    def getStatus(self):
        return self.status

    def editTasK(task_id):
        pass

    def deleteTask(task_id):
        pass

class Loop:
    def __init__(self, loop_id, loop_name, side_x, side_y, width, height, angle):
        self.loop_id  = loop_id
        self.loop_name = loop_name
        self.side_x = side_x
        self.side_y = side_y
        self.width = width
        self.height = height
        self.angle = angle

    def get_loop_id(self):
        return self.loop_id
    def get_loop_name(self):
        return self.loop_name
    def get_side_x(self):
        return self.side_x
    def get_side_y(self):
        return self.side_y
    def get_width(self):
        return self.width
    def get_height(self):
        return self.height
    def get_angle(self):
        return self.angle

    def set_loop_id(self, loop_id):
        self.loop_id = loop_id
    def set_loop_name(self, loop_name):
        self.loop_name = loop_name
    def set_side_x(self, side_x):
        self.side_x = side_x
    def set_side_y(self, side_y):
        self.side_y = side_y
    def set_width(self, width):
        self.width = width
    def set_height(self, height):
        self.height = height
    def set_angle(self, angle):
        self.angle = angle

class Input:
    def __init__(self, input_id, video):
        self.input_id  = input_id
        self.video = video

    def set_input_id(self, input_id):
        self.input_id = input_id
    
    def get_input_id(self):
        return self.input_id

    def set_video(self, video):
        self.video = video

    def get_video(self):
        return self.video