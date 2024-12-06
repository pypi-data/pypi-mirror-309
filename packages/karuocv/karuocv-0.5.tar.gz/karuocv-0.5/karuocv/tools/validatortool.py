# -*- encoding: utf-8 -*-
'''
@文件    :validatortool.py
@说明    :
@时间    :2024/10/25 16:18:36
@作者    :caimiao@kingsoft.com
@版本    :0.1
'''

import os
import tqdm
from ultralytics import YOLO
import cv2
import supervision as sv
import numpy as np
import matplotlib.pyplot as plt
from karuocv.hub.datautils import yolo_annotation_to_bbox
from karuocv.hub.inference import ImageAnnotator
import logging

logger = logging.getLogger(__file__)


class RegressionAnnotationTool:
    """
    把所有的标注样本信息都显示出来，分别显示标注信息和推理信息
    """
    def __init__(self, base_model: str, dataset: str, dest: str = None) -> None:
        self.base_model = base_model
        self.dataset = dataset
        self.dest = dest if dest else os.path.join(dataset, "checks")
        self.annotator = None

    def _annotation(self, image_file: str, label_file: str, mixer_file: str):
        cv_img = cv2.imread(f"{image_file}")
        inference_img = cv_img.copy()
        _label_boxes = np.loadtxt(f"{label_file}") 
        _h, _w, _dtp = cv_img.shape
        _label_boxes = _label_boxes.reshape(-1, 5)
        _label_list = _label_boxes[:, 0]
        boxes_list = yolo_annotation_to_bbox(_label_boxes, _h, _w)
        for _label, _box in zip(_label_list, boxes_list):
            _x1, _y1, _x2, _y2 = _box
            cv2.rectangle(cv_img, (_x1, _y1), (_x2, _y2), (0, 255, 0), 2)
            cv2.putText(cv_img, self.annotator._model.names[int(_label)], (_x1, _y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(cv_img, f"ori: {image_file.split('/')[-1]}", (15, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        dest_img = np.ones((_h, _w * 2, _dtp), dtype=np.uint8) * 255
        _annotated_image = self.annotator.fullAnnotateImage(inference_img)
        cv2.putText(_annotated_image, f"inference: {image_file.split('/')[-1]}", (15, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        sv.draw_image(dest_img, cv_img, 1, sv.Rect(0, 0, _w, _h))
        sv.draw_image(dest_img, _annotated_image, 1, sv.Rect(_w, 0, _w, _h))
        cv2.imwrite(mixer_file, dest_img)

    def walkCheckDataset(self):
        self.annotator = ImageAnnotator(self.base_model)
        if os.path.exists(self.dataset):
            os.makedirs(self.dest, exist_ok=True)
            subdirs = ["train", "test", "valid"]
            for _sub in subdirs:
                _image_path = os.path.join(self.dataset, _sub, "images")
                _label_path = os.path.join(self.dataset, _sub, "labels")
                if os.path.exists(_image_path) and os.path.exists(_label_path):
                    logger.info(f"check image path {_sub}")
                    for _root, _, _files in os.walk(_image_path):
                        for _f in tqdm.tqdm(_files):
                            _fname = _f.split(".")[0]
                            _image_file = os.path.join(_root, _f)
                            _label_file = os.path.join(_label_path, f"{_fname}.txt")
                            if os.path.exists(_image_file) and os.path.exists(_label_file):
                                self._annotation(_image_file, _label_file, os.path.join(self.dest, f"{_fname}.jpg"))
        else:
            logger.info(f"please checkout path valid {self.dataset}")
