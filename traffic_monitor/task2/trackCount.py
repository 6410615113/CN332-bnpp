import cv2
import numpy as np

import supervision as sv
from supervision.geometry.core import Vector
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO("yolov8x.pt")

def lineCounter(sx, sy, ex, ey, path):
    tracker = sv.ByteTrack()
    frames_generator = sv.get_video_frames_generator(path)
    start, end = sv.Point(x=sx, y=sy), sv.Point(x=ex, y=ey)
    # line_zone = sv.LineZone(start=start, end=end)
    line = Vector(start=start, end=end)

    # Define class IDs for vehicles
    CAR_CLASS_ID = 2      # Example class ID for car, adjust based on YOLOv8 class mapping
    TRUCK_CLASS_ID = 7    # Example class ID for truck
    BIKE_CLASS_ID = 3     # Example class ID for motorcycle

    count_car = 0
    count_truck = 0
    count_bike = 0
    tracker_id = {
        'id': [],
        'class': [],
        'start': [],
        'end': [],
        'crossed': []
    }
    for frame in frames_generator:
        result = model(frame)[0]
        detections = sv.Detections.from_ultralytics(result)

        # Filter detections by class IDs
        vehicle_detections = sv.Detections(
            xyxy=detections.xyxy,
            confidence=detections.confidence,
            class_id=detections.class_id
        )
        
        # Keep only the vehicles of interest
        indices = [i for i, class_id in enumerate(vehicle_detections.class_id) if class_id in {CAR_CLASS_ID, TRUCK_CLASS_ID, BIKE_CLASS_ID}]
        vehicle_detections.xyxy = vehicle_detections.xyxy[indices]
        vehicle_detections.confidence = vehicle_detections.confidence[indices]
        vehicle_detections.class_id = vehicle_detections.class_id[indices]

        # Update tracker with filtered detections
        tracked_detections = tracker.update_with_detections(vehicle_detections)
        for d in tracked_detections.tracker_id:
            i = tracked_detections.tracker_id.tolist().index(d)
            if d not in tracker_id['id']:
                tracker_id['id'].append(d)
                tracker_id['class'].append(tracked_detections.class_id[i])
                tracker_id['start'].append(tracked_detections.xyxy[i])
                tracker_id['end'].append(tracked_detections.xyxy[i]) 
                tracker_id['crossed'].append(False)
            else:
                tracker_id['end'][tracker_id['id'].index(d)] = tracked_detections.xyxy[i]
                if (not tracker_id['crossed'][tracker_id['id'].index(d)] and 
                    line.cross_product(sv.Point(*tracker_id['start'][tracker_id['id'].index(d)][0:2])) * 
                    line.cross_product(sv.Point(*tracker_id['end'][tracker_id['id'].index(d)][2:4])) < 0):
                    tracker_id['crossed'][tracker_id['id'].index(d)] = True
                    
    for i in range(len(tracker_id['id'])):
        if tracker_id['crossed'][i]:
            if tracker_id['class'][i] == CAR_CLASS_ID:
                count_car += 1
            elif tracker_id['class'][i] == TRUCK_CLASS_ID:
                count_truck += 1
            elif tracker_id['class'][i] == BIKE_CLASS_ID:
                count_bike += 1            

    return count_car, count_truck, count_bike
