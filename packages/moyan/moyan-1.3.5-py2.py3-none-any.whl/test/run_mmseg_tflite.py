#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   run_mmseg_tflite.py
@Time    :   2023/08/17 15:21:24
@Author  :   Moyan 
'''
import os
import cv2
import moyan
import numpy as np
from moyan.template.TFLite import TFLiteModel

class MMSegDeepLabPlus(TFLiteModel):
    def __init__(self, 
                 model_path: str, 
                 input_size=512, 
                 mean=[123.675, 116.28, 103.53],
                 std=[58.395, 57.12, 57.375]
            ) -> None:
        super().__init__(model_path)
        self.input_size = input_size
        self.org_w, self.org_h = 0, 0
        self.mean = np.float64(np.array(mean).reshape(1,-1))
        self.std = 1 / np.float64(np.array(std).reshape(1,-1))
    
    def preprocess(self, img_src: np.ndarray):
        self.org_h, self.org_w = img_src.shape[:2]
        img = cv2.resize(img_src, (self.input_size, self.input_size), interpolation=cv2.INTER_LINEAR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img.astype(np.float32)
        cv2.subtract(img, self.mean, img)
        cv2.multiply(img, self.std, img)    
        input_tensor = np.expand_dims(img, axis=0)
        return input_tensor

    def postprocess(self, output_tensor):
        print(output_tensor[0].shape)
        x = output_tensor[0][0]
        print(np.unique(x))
        output_im = cv2.resize(x.astype('uint8'), (self.org_w, self.org_h), interpolation=cv2.INTER_LINEAR)
        return output_im
        

def main():
    model_path = r"D:\Code\AI-in-air\mmsegmentation\work_dirs\idcardseg_deeplabv3plus_mbv2x0.25-d8_4xb4-40k_voc12-512x512\convert_onnx2\tflite\model_dynimic.tflite"
    model = MMSegDeepLabPlus(model_path=model_path, input_size=512)
    img_path = r"D:\Code\AI-in-air\mmsegmentation\demo\idcard_fake.jpg" # idcard_fake  idcard
    im = cv2.imread(img_path)
    mask = model.run(im)
    class_id = np.unique(mask)
    for i in class_id:
        mask[np.where(mask==i)] = (i*20)
    cv2.imwrite("a_fp16.png", mask)
    
if __name__ == '__main__':
    main()