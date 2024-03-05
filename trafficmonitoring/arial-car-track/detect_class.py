import os
import cv2
import time
import torch
import argparse
from pathlib import Path
from numpy import random
from random import randint
import torch.backends.cudnn as cudnn

from models.experimental import attempt_load
from utils.datasets import LoadStreams, LoadImages
from utils.general import check_img_size, check_requirements, \
                check_imshow, non_max_suppression, apply_classifier, \
                scale_coords, xyxy2xywh, strip_optimizer, set_logging, \
                increment_path
from utils.plots import plot_one_box
from utils.torch_utils import select_device, load_classifier, \
                time_synchronized, TracedModel
from utils.download_weights import download

#For SORT tracking
import skimage
from sort import *
from line_intersect import isIntersect
import json
import count_table
from opt import Opt

def check_clock_wise(p1,p2,p3):
    vec1  = (p2[0]-p1[0],p2[1]-p1[1])
    vec2 = (p3[0]-p2[0],p3[1]-p2[1])
    cross = vec2[0] * vec1[1] - vec2[1] * vec1[0];
    if cross>=0:
        return True
    else:
        return False
    
count_boxes = []
loop_boxes = [] #loop statistics
time_stamp = 0 # time in second
save_dir = ""
names = ""

#............................... Tracker Functions ............................
""" Random created palette"""
palette = (2 ** 11 - 1, 2 ** 15 - 1, 2 ** 20 - 1)

"""" Calculates the relative bounding box from absolute pixel values. """
class Box():
    def bbox_rel(*xyxy):
        bbox_left = min([xyxy[0].item(), xyxy[2].item()])
        bbox_top = min([xyxy[1].item(), xyxy[3].item()])
        bbox_w = abs(xyxy[0].item() - xyxy[2].item())
        bbox_h = abs(xyxy[1].item() - xyxy[3].item())
        x_c = (bbox_left + bbox_w / 2)
        y_c = (bbox_top + bbox_h / 2)
        w = bbox_w
        h = bbox_h
        return x_c, y_c, w, h


    """Function to Draw Bounding boxes"""
    def draw_boxes(img, bbox, identities=None, categories=None, names=None,offset=(0, 0)):
        for i, box in enumerate(bbox):
            x1, y1, x2, y2 = [int(i) for i in box]
            x1 += offset[0]
            x2 += offset[0]
            y1 += offset[1]
            y2 += offset[1]
            cat = int(categories[i]) if categories is not None else 0
            id = int(identities[i]) if identities is not None else 0
            data = (int((box[0]+box[2])/2),(int((box[1]+box[3])/2)))
            label = str(id) + ":"+ str(cat) + ":"+ names[cat]
            (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.4, 1)
            cv2.rectangle(img, (x1, y1), (x2, y2), (255,0,20), 1)
            cv2.rectangle(img, (x1, y1 - 20), (x1 + w, y1), (255,144,30), -1)
            cv2.putText(img, label, (x1, y1 - 5),cv2.FONT_HERSHEY_SIMPLEX, 
                        0.4, [255, 255, 255], 1)
            # cv2.circle(img, data, 6, color,-1)
        return img
#..............................................................................
def append_to_file(filename, text):
    with open(filename, "a") as file:
        file.write(text + "\n")

class Line():
    def __init__(self, time_stamp, loop_boxes, loop_id):
        self.time_stamp = time_stamp
        self.loop_boxes = loop_boxes
        self.loop_id = loop_id

    def line_enter_check_and_set(self, loop,track,tp1,tp2,line_start,line_end):
        if isIntersect(tp1,tp2,line_start,line_end):
            if loop["id"] not in track.aoi_entered :
                track.aoi_entered.append(loop["id"])
                msg = f'{loop["id"]},{track.id},{names[int(track.detclass)]},{self.time_stamp},ENTERED'
                append_to_file(str(save_dir)+"\\loop.txt",msg)
                print(f'track {track.id} of type {track.detclass} entered loop {loop["id"]} at time ...{self.time_stamp}')
    
    #check if the object exit the line, if the first time mark it and prevent the re entry by setting the flag 
    def line_exit_check_and_set(self, loop,track,tp1,tp2,line_start,line_end,line_side): #line_side is the left or right border
        if isIntersect(tp1,tp2,line_start,line_end):
            if loop["id"] in track.aoi_entered and loop["id"] not in track.aoi_exited:
                track.aoi_exited.append(loop["id"])  # means already exit
                print(f'track {track.id} of type {track.detclass} exit loop {loop["id"]} at time ...{self.time_stamp}')
                if (loop["orientation"] == "clockwise" and line_side=="left" or 
                    loop["orientation"] == "counterclockwise" and line_side=="right"): #turn left
                    print("1111------------")
                    self.loop_boxes[self.loop_id.index(int(loop["id"]))].add_left(int(track.detclass))
                    print("1111111111111111")
                    msg = f'{loop["id"]},{track.id},{names[int(track.detclass)]},{self.time_stamp},LEFT'
                    append_to_file(str(save_dir)+"\\loop.txt",msg)
                    
                if(loop["orientation"] == "clockwise" and line_side=="right" or 
                    loop["orientation"] == "counterclockwise" and line_side=="left"): #turn right
                    print("2222------------")
                    self.loop_boxes[self.loop_id.index(int(loop["id"]))].add_right(int(track.detclass)) # turn right
                    print("2222222222222222")
                    msg = f'{loop["id"]},{track.id},{names[int(track.detclass)]},{self.time_stamp},RIGHT'
                    append_to_file(str(save_dir)+"\\loop.txt",msg)

                if line_side == "straight":
                    print("3333------------")
                    print(self.loop_boxes)
                    self.loop_boxes[self.loop_id.index(int(loop["id"]))].add_straight(int(track.detclass))
                    print("3333333333333333")
                    msg = f'{loop["id"]},{track.id},{names[int(track.detclass)]},{self.time_stamp},STRAIGHT'
                    append_to_file(str(save_dir)+"\\loop.txt",msg)

class Loop(Line):
    #check if item entering or exit loop
    def check_enter_exit_loop(track, count_boxes, time_stamp, loop_boxes, loop_id):
        loops = count_boxes["loops"]
        for loop in loops:
            #print(loop)
            pt0,pt1,pt2,pt3 = loop["points"]
            #check entering line
            if len(track.centroidarr)>20:
                tp2,tp1 = track.centroidarr[-1], track.centroidarr[-20]            
                #check entering line
                Line(time_stamp, loop_boxes, loop_id).line_enter_check_and_set(loop,track,tp1,tp2,pt0,pt1)
                
                #check exit line left straight and right
                Line(time_stamp, loop_boxes, loop_id).line_exit_check_and_set(loop,track,tp1,tp2,pt1,pt2,"left")
                Line(time_stamp, loop_boxes, loop_id).line_exit_check_and_set(loop,track,tp1,tp2,pt2,pt3,"straight")
                Line(time_stamp, loop_boxes, loop_id).line_exit_check_and_set(loop,track,tp1,tp2,pt3,pt0,"right")

    #draw bouncing box to loop
    def draw_loops(img, count_boxes):
        loops = count_boxes["loops"]
        for loop in loops:
            pt0,pt1,pt2,pt3 = loop["points"]
            
            cv2.line(img, (pt0["x"],pt0["y"]),(pt1["x"],pt1["y"]),(255,0,0),2) #entering line
            cv2.line(img, (pt1["x"],pt1["y"]),(pt2["x"],pt2["y"]),(255,255,0),2) #left line
            cv2.line(img, (pt2["x"],pt2["y"]),(pt3["x"],pt3["y"]),(255,255,0),2) #straight
            cv2.line(img, (pt3["x"],pt3["y"]),(pt0["x"],pt0["y"]),(255,255,0),2) #right
            cv2.putText(img,loop["name"],(pt0["x"],pt0["y"]),cv2.FONT_HERSHEY_SIMPLEX, 0.6, [0, 255, 0], 2)


class Detect(Loop, Box):
    def __init__(self, opt):
        global save_dir
        global names

        self.loop_boxes = []
        
        self.opt = opt
        self.source, self.weights, self.view_img, self.save_txt, self.imgsz, self.trace, self.colored_trk= opt.source, \
        opt.weights, opt.view_img, opt.save_txt, opt.img_size, not opt.no_trace, opt.colored_trk
        self.save_img = not opt.nosave and not self.source.endswith('.txt')  # save inference images
        self.webcam = self.source.isnumeric() or self.source.endswith('.txt') or self.source.lower().startswith(
            ('rtsp://', 'rtmp://', 'http://', 'https://'))
        # f = open(opt.loop)
        # self.count_boxes = json.load(f)
        # f.close()

        self.count_boxes = self.opt.loop
        self.loop_id = self.opt.loop["loop_id"]
        #.... Initialize SORT .... 
        #......................... 
        self.sort_max_age = 25 #5 
        self.sort_min_hits = 5 #2
        self.sort_iou_thresh = 0.5 #0.2
        self.sort_tracker = Sort(max_age=self.sort_max_age,
                        min_hits=self.sort_min_hits,
                        iou_threshold=self.sort_iou_thresh) 
        #......................... 
        # Directories
        save_dir = Path(increment_path(Path(opt.project) / opt.name, exist_ok=opt.exist_ok))  # increment run
        (save_dir / 'labels' if self.save_txt else save_dir).mkdir(parents=True, exist_ok=True)  # make dir

        # Initialize
        set_logging()
        self.device = select_device(opt.device)
        self.half = self.device.type != 'cpu'  # half precision only supported on CUDA

        # Load model
        self.model = attempt_load(self.weights, map_location=self.device)  # load FP32 model
        self.stride = int(self.model.stride.max())  # model stride
        self.imgsz = check_img_size(self.imgsz, s=self.stride)  # check img_size

        if self.trace:
            self.model = TracedModel(self.model, self.device, opt.img_size)

        if self.half:
            self.model.half()  # to FP16
        
        # Second-stage classifier
        self.classify = False
        if self.classify:
            self.modelc = load_classifier(name='resnet101', n=2)  # initialize
            self.modelc.load_state_dict(torch.load('weights/resnet101.pt', map_location=self.device)['model']).to(self.device).eval()

        # Set Dataloader
        self.vid_path, self.vid_writer = None, None
        if self.webcam:
            self.view_img = check_imshow()
            cudnn.benchmark = True  # set True to speed up constant image size inference
            self.dataset = LoadStreams(self.source, img_size=self.imgsz, stride=self.stride)
        else:
            self.dataset = LoadImages(self.source, img_size=self.imgsz, stride=self.stride)

        # Get names and colors
        names = self.model.module.names if hasattr(self.model, 'module') else self.model.names
        self.colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]
        for loop in self.count_boxes["loops"]:
            self.loop_boxes.append(count_table.LoopCount(len(names),loop["summary_location"],loop))

    def run(self):
        if self.device.type != 'cpu':
            self.model(torch.zeros(1, 3, self.imgsz, self.imgsz).to(self.device).type_as(next(self.model.parameters())))  # run once
        old_img_w = old_img_h = self.imgsz
        old_img_b = 1

        t0 = time.time()

        #........Rand Color for every trk.......
        rand_color_list = []
        for i in range(0,5005):
            r = randint(0, 255)
            g = randint(0, 255)
            b = randint(0, 255)
            rand_color = (r, g, b)
            rand_color_list.append(rand_color)
        #.........................
        img = None
        counttable = count_table.CountTable(img,None,
                    list(names),["Straight","Left","Right"],border_color=(0,255,0),text_color=(0,0,255))
        frame_count = 0
        for path, img, im0s, vid_cap in self.dataset:
            fps = vid_cap.get(cv2.CAP_PROP_FPS)
            self.time_stamp = frame_count/fps #calculate time stamp
            frame_count+=1
            img = torch.from_numpy(img).to(self.device)
            img = img.half() if self.half else img.float()  # uint8 to fp16/32
            img /= 255.0  # 0 - 255 to 0.0 - 1.0
            if img.ndimension() == 3:
                img = img.unsqueeze(0)

            # Warmup
            if self.device.type != 'cpu' and (old_img_b != img.shape[0] or old_img_h != img.shape[2] or old_img_w != img.shape[3]):
                old_img_b = img.shape[0]
                old_img_h = img.shape[2]
                old_img_w = img.shape[3]
                for i in range(3):
                    self.model(img, augment=self.opt.augment)[0]

            # Inference
            t1 = time_synchronized()
            pred = self.model(img, augment=self.opt.augment)[0]
            t2 = time_synchronized()

            # Apply NMS
            pred = non_max_suppression(pred, self.opt.conf_thres, self.opt.iou_thres, classes=self.opt.classes, agnostic=self.opt.agnostic_nms)
            t3 = time_synchronized()

            # Apply Classifier
            if self.classify:
                pred = apply_classifier(pred, self.modelc, img, im0s)
        
            # Process detections
            for i, det in enumerate(pred):  # detections per image
                if self.webcam:  # batch_size >= 1
                    p, s, im0, frame = path[i], '%g: ' % i, im0s[i].copy(), self.dataset.count
                else:
                    p, s, im0, frame = path, '', im0s, getattr(self.dataset, 'frame', 0)

                p = Path(p)  # to Path
                save_path = str(save_dir / p.name)  # img.jpg
                txt_path = str(save_dir / 'labels' / p.stem) + ('' if self.dataset.mode == 'image' else f'_{frame}')  # img.txt
                gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
                if len(det):
                    # Rescale boxes from img_size to im0 size
                    det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                    # Print results
                    for c in det[:, -1].unique():
                        n = (det[:, -1] == c).sum()  # detections per class
                        #s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

                    #..................USE TRACK FUNCTION....................
                    #pass an empty array to sort
                    dets_to_sort = np.empty((0,6))
                    
                    # NOTE: We send in detected object class too
                    for x1,y1,x2,y2,conf,detclass in det.cpu().detach().numpy():
                        dets_to_sort = np.vstack((dets_to_sort, 
                                    np.array([x1, y1, x2, y2, conf, detclass])))
                    
                    # Run SORT
                    tracked_dets = self.sort_tracker.update(dets_to_sort)
                    tracks = self.sort_tracker.getTrackers()
                    
                    #loop over tracks
                    for track in tracks:

                        #tracking object passing line check and update
                        Loop.check_enter_exit_loop(track, self.count_boxes, self.time_stamp, self.loop_boxes, self.loop_id)

                        # color = compute_color_for_labels(id)
                        #draw colored tracks
                        if self.colored_trk:
                            [cv2.line(im0, (int(track.centroidarr[i][0]),
                                        int(track.centroidarr[i][1])), 
                                        (int(track.centroidarr[i+1][0]),
                                        int(track.centroidarr[i+1][1])),
                                        rand_color_list[track.id], thickness=1) 
                                        for i,_ in  enumerate(track.centroidarr) 
                                        if i < len(track.centroidarr)-1 ] 
                        #draw same color tracks
                        else:
                            [cv2.line(im0, (int(track.centroidarr[i][0]),
                                        int(track.centroidarr[i][1])), 
                                        (int(track.centroidarr[i+1][0]),
                                        int(track.centroidarr[i+1][1])),
                                        (255,0,0), thickness=1) 
                                        for i,_ in  enumerate(track.centroidarr) 
                                        if i < len(track.centroidarr)-1 ] 
                    
                    # draw boxes for visualization
                    if len(tracked_dets)>0:
                        bbox_xyxy = tracked_dets[:,:4]
                        identities = tracked_dets[:, 8]
                        categories = tracked_dets[:, 4]
                        Box.draw_boxes(im0, bbox_xyxy, identities, categories, names)

                    #........................................................
                    
            # Print time (inference + NMS)
            #print(f'{s}Done. ({(1E3 * (t2 - t1)):.1f}ms) Inference, ({(1E3 * (t3 - t2)):.1f}ms) NMS')


            #add bounding box to the main image
            #line 1 entering line
            #cv2.line(im0s, (200,200),(400,20),(255,0,0),5)
            #line2 left turn line
            #cv2.line(im0s, (400,20),(600,200),(0,255,0),5)
            #line3  straigh line
            #cv2.line(im0s, (600,200),(400,400),(0,255,0),5)
            #line4 right turn line
            #cv2.line(im0s, (400,400),(200,200),(0,255,0),5)


            #add counting table
            counttable.img = im0s
            
            # for lb in loop_boxes:
            #     lb.draw(counttable)

            # cv2.rectangle(im0s,(500,400),(900,550),(0,0,0),cv2.FILLED)
            # cv2.putText(im0s,"        Straight    Left        Right", (500, 420),cv2.FONT_HERSHEY_SIMPLEX, 
            #             0.6, [0, 255, 0], 2)
            # cv2.putText(im0s,f"Car      {cnts[0][0]}           {cnts[0][1]}           {cnts[0][2]} ", (500, 450),cv2.FONT_HERSHEY_SIMPLEX, 
            #             0.6, [0, 255, 0], 2)
            # cv2.putText(im0s,f"Bike      {cnts[1][0]}           {cnts[1][1]}           {cnts[1][2]} ", (500, 480),cv2.FONT_HERSHEY_SIMPLEX, 
            #             0.6, [0, 255, 0], 2)
            # cv2.putText(im0s,f"Pickup   {cnts[2][0]}           {cnts[2][1]}           {cnts[2][2]} ", (500, 510),cv2.FONT_HERSHEY_SIMPLEX, 
            #             0.6, [0, 255, 0], 2)

            Loop.draw_loops(im0s, self.count_boxes)
                # Stream results
            if self.view_img:
                cv2.imshow(str(p), im0)
                if cv2.waitKey(1) == ord('q'):  # q to quit
                    cv2.destroyAllWindows()
                    raise StopIteration

                # Save results (image with detections)
            if self.save_img:
                if self.dataset.mode == 'image':
                    cv2.imwrite(save_dir, im0)
                    print(f" The image with the result is saved in: {save_path}")
                else:  # 'video' or 'stream'
                    if self.vid_path != save_path:  # new video
                        self.vid_path = save_path
                        if isinstance(self.vid_writer, cv2.VideoWriter):
                            self.vid_writer.release()  # release previous video writer
                        if vid_cap:  # video
                            fps = vid_cap.get(cv2.CAP_PROP_FPS)
                            w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                            h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                        else:  # stream
                            fps, w, h = 30, im0.shape[1], im0.shape[0]
                            save_path += '.mp4'
                        self.vid_writer = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'vp09'), fps, (w, h))
                    self.vid_writer.write(im0)

        #if save_txt or save_img:
            #s = f"\n{len(list(save_dir.glob('labels/*.txt')))} labels saved to {save_dir / 'labels'}" if save_txt else ''
            #print(f"Results saved to {save_dir}{s}")

        print(f'Done. ({time.time() - t0:.3f}s)')

