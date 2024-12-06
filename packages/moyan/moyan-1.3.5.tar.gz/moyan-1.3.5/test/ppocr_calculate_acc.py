#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   ppocr_calculate_acc.py
@Time    :   2024/05/11 11:12:47
@Author  :   moyan 
@Contact :   ice_moyan@163.com
'''
import os
import cv2
import moyan
import numpy as np
from  paddleocr import PaddleOCR
from rapidfuzz.distance import Levenshtein


def full_to_half(str):
    half_str = ""
    for char in str:
        code = ord(char)
        if code == 12288:
            code = 32
        if 65281 <= code <= 65374:
            code -= 65248
        half_str += chr(code)
    return half_str

def remove_punctuation(str):
    return str.replace("。","")


class PPOCRv4:
    def __init__(self, det_model_dir, cls_model_dir, rec_model_dir, rec_char_dict_path, ocr_version="PP-OCRv4", use_gpu=False) -> None:
        self.model = PaddleOCR(
            det_model_dir=det_model_dir,
            cls_model_dir=cls_model_dir,
            rec_model_dir=rec_model_dir,
            rec_char_dict_path=rec_char_dict_path,
            ocr_version=ocr_version,
            use_gpu=use_gpu 
        )
    
    def run_rec(self, img_path):
        return self.model.ocr(img_path, det=False, cls=False)
    
    def run_det_rec(self, img_path):
        return self.model.ocr(img_path, det=True, cls=False)



def main():
    
    RemovePunctuation = False
    cls_model_dir = ""
    det_model_dir = ""
    rec_model_dir = ""
    rec_char_dict_path = ""

    model = PPOCRv4(
        det_model_dir,
        cls_model_dir,
        rec_model_dir,
        rec_char_dict_path
    )


    img_dir = ""
    gt_path = ""
    txt_list = moyan.read_txt_to_lines(gt_path)
    all_nums = len(txt_list)

    eps = 1e-5
    all_num, correct_num, norm_edit_dis = 0, 0, 0.0
    pred_parse_half, gt_parse_half = "", ""

    for ind, pline in enumerate(txt_list):
        names, target = pline.split("\t")
        img_path  = os.path.join(img_dir, names)

        pred, score = model.run_rec(img_path)[0][0]

        pred = full_to_half(pred)
        target = full_to_half(target)

        if RemovePunctuation:
            pred = remove_punctuation(pred)
            target = remove_punctuation(target)

        pred = pred.replace(" ", "")

        pred_parse_half += pred
        gt_parse_half += target

        ned = Levenshtein.normalized_distance(pred, target)
        norm_edit_dis += ned

        if pred == target:
            correct_num += 1

        all_num +=1

    acc = correct_num / (all_num+eps)
    norm_edit_dis = 1-norm_edit_dis/(all_num+eps)
    print(f"acc: {acc}, ned: {norm_edit_dis}")

    norm_edit_dis2 = Levenshtein.normalized_distance(pred_parse_half, gt_parse_half)
    print(f"ned2: {norm_edit_dis2}")

if __name__=='__main__':
    main()
