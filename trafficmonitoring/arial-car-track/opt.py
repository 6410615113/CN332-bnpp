class Opt:
    def __init__(self):
        self.weights = './arial-car-track/yolov7.pt'
        self.download = False
        self.no_download = True
        self.source = './arial-car-track/vt.mp4'
        self.img_size = 900
        self.conf_thres = 0.6
        self.iou_thres = 0.5
        self.device = ''
        self.view_img = False
        self.save_txt = True
        self.save_conf = True
        self.nosave = False
        self.classes = [1, 2, 3, 5, 7]
        self.agnostic_nms = True
        self.augment = True
        self.update = True
        self.project = './arial-car-track/runs/detect'
        self.exist_ok = True
        self.no_trace = True
        self.name = 'object_tracking'
        self.colored_trk = True
        self.loop = './arial-car-track/loop.json'

    def set_opt(self, opt_json):
        self.weights = opt_json['weights']
        self.download = opt_json['download']
        self.no_download = opt_json['no_download']
        self.source = opt_json['source']
        self.img_size = opt_json['img_size']
        self.conf_thres = opt_json['conf_thres']
        self.iou_thres = opt_json['iou_thres']
        self.device = opt_json['device']
        self.view_img = opt_json['view_img']
        self.save_txt = opt_json['save_txt']
        self.save_conf = opt_json['save_conf']
        self.nosave = opt_json['nosave']
        self.classes = opt_json['classes']
        self.agnostic_nms = opt_json['agnostic_nms']
        self.augment = opt_json['augment']
        self.update = opt_json['update']
        self.project = opt_json['project']
        self.exist_ok = opt_json['exist_ok']
        self.no_trace = opt_json['no_trace']
        self.name = opt_json['name']
        self.colored_trk = opt_json['colored_trk']
        self.loop = opt_json['loop']
    
OptJson = {
    'weights' : './arial-car-track/yolov7.pt',
    'download' : True,
    'no_download' : False,
    'source' : 'inference/images',
    'img_size' : 640,
    'conf_thres' : 0.6,
    'iou_thres' : 0.5,
    'device' : '',
    'view_img' : False,
    'save_txt' : True,
    'save_conf' : True,
    'nosave' : False,
    'classes' : [1, 2, 3, 5, 7],
    'agnostic_nms' : True,
    'augment' : True,
    'update' : True,
    'project' : './arial-car-track/runs/detect',
    'exist_ok' : True,
    'no_trace' : True,
    'name' : 'object_tracking',
    'loop' : './arial-car-track/loop.json',
    'colored_trk': True,
    'loop_txt': True,
    'summary-txt': True
}
    
        
