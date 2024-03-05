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

class Loops:
    def __init__(self, input):
        self.input = input

    def draw_loop(self):
        self.draw_all_loop(self.input)

    def add_point(self, ptx, begin):
        point = []
        for i in range(len(ptx)):
            point.append({"x": ptx[(begin+i)%len(ptx)][0], "y": ptx[(begin+i)%len(ptx)][1]})
        return point

    def draw_all_loop(self, input):
        image = cv2.imread(input.sample_img.path)
        name = str(input.video.name.split('.')[0]) + ".png"
        color = (0, 255, 0)
        thickness = 2
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 1
        for loop in Loop.objects.filter(input=input):
            image = self.draw_angled_rec(image, loop.x, loop.y, loop.width,
                                    loop.height, loop.angle, thickness,
                                    loop.direction)
            org = (loop.y, loop.x)
            image = cv2.putText(image, loop.loop_name, org, font, 
                    fontScale, color, thickness, cv2.LINE_AA)
        fig = plt.figure()
        ax = fig.subplots()
        ax.imshow(image)
        plt.savefig("./media/fig/" + name)
        input.fig_img = "./fig/" + name
        input.save()

    def draw_angled_rec(self, img, x, y, width, height, angle, thickness, direction):
        pt, pt0, pt1, pt2, pt3 = self.find_rec(x, y, width, height, angle)
        cv2.line(img, pt0, pt1, self.color_line(pt, pt0, pt1, direction), thickness)
        cv2.line(img, pt1, pt2, self.color_line(pt, pt1, pt2, direction), thickness)
        cv2.line(img, pt2, pt3, self.color_line(pt, pt2, pt3, direction), thickness)
        cv2.line(img, pt3, pt0, self.color_line(pt, pt3, pt0, direction), thickness)
        return img
    
    def find_rec(self, x, y, width, height, angle):
        _angle = -angle * math.pi / 180.0
        b = math.cos(_angle) * 0.5
        a = math.sin(_angle) * 0.5
        pt0 = (int(y - a * height - b * width),
            int(x + b * height - a * width))
        pt1 = (int(y + a * height - b * width),
            int(x - b * height - a * width))
        pt2 = (int(2 * y - pt0[0]), int(2 * x - pt0[1]))
        pt3 = (int(2 * y - pt1[0]), int(2 * x - pt1[1]))

        pt = [pt0, pt1, pt2, pt3]
        for i in range(len(pt)):
            pt[i] = (pt[i][1], pt[i][0])
        
        return pt, pt0, pt1, pt2, pt3
    
    def color_line(self, pt, pt0, pt1, direction):
        if self.find_line_entry(pt, pt0, pt1, direction):
            color = (255, 0, 30)
        else:
            color = (0, 255, 0)
        return color
    
    def find_line_entry(self, pt, p0, p1, direction):
        p0 = p0[1], p0[0]
        p1 = p1[1], p1[0]

        max_x, min_x = max([x[0] for x in pt]), min([x[0] for x in pt])
        max_y, min_y = max([x[1] for x in pt]), min([x[1] for x in pt])
            
        if direction == 1:
            return ((max_x == p0[0]) or (max_x == p1[0])) and ((max_y == p0[1]) or (max_y == p1[1]))
        elif direction == 2:
            return ((max_x == p0[0]) and (max_x == p1[0]))
        elif direction == 3:
            return ((max_x == p0[0]) or (max_x == p1[0])) and ((min_y == p0[1]) or (min_y == p1[1]))
        elif direction == 4:
            return ((min_y == p0[1]) and (min_y == p1[1]))
        elif direction == 5:
            return ((min_x == p0[0]) or (min_x == p1[0])) and ((min_y == p0[1]) or (min_y == p1[1]))
        elif direction == 6:
            return ((min_x == p0[0]) and (min_x == p1[0]))
        elif direction == 7:
            return ((min_x == p0[0]) or (min_x == p1[0])) and ((max_y == p0[1]) or (max_y == p1[1]))
        elif direction == 8:
            return ((max_y == p0[1]) and (max_y == p1[1]))
        
    def create_loop(self, all_loop):
        loops = []
        loops_id = []
        for loop in all_loop:
            points = []
            pt, pt0, pt1, pt2, pt3 = self.find_rec(loop.x, loop.y, loop.width, loop.height, loop.angle)
            ptx = [pt0, pt1, pt2, pt3]
            if self.find_line_entry(pt, pt0, pt1, loop.direction):
                points = self.add_point(ptx, 0)
            elif self.find_line_entry(pt, pt1, pt2, loop.direction):
                points = self.add_point(ptx, 1)
            elif self.find_line_entry(pt, pt2, pt3, loop.direction):
                points = self.add_point(ptx, 2)
            elif self.find_line_entry(pt, pt3, pt0, loop.direction):
                points = self.add_point(ptx, 3)

            loops.append({
                "name": loop.loop_name,
                "id": loop.id,
                "points": points,
                "orientation":"clockwise",
                "summary_location":{"x":0,"y":"0"}
            })
            loops_id.append(loop.id)
        loop_json = {"loops": loops, "loop_id":loops_id}
        return loop_json