#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   rewrite_ocr_datat_gt_label.py
@Time    :   2023/10/05 15:27:03
@Author  :   moyan 
@Contact :   ice_moyan@163.com
'''
import os
import cv2
import moyan
import numpy as np
from tqdm import tqdm


class relod_ocr_gt:
    def __init__(self, character_dict_path, use_space_char=False) -> None:
        self.character_str = []
        with open(character_dict_path, "rb") as fin:
            lines = fin.readlines()
            for line in lines:
                line = line.decode('utf-8').strip("\n").strip("\r\n")
                self.character_str.append(line)
        if use_space_char:
            self.character_str.append(" ")
        dict_character = list(self.character_str)
        self.dict = {}
        for i, char in enumerate(dict_character):
            self.dict[char] = i
        self.character = dict_character
        self.dict_character_ord = [ord(x) for x in dict_character]
        self.special_char = "####@####"

    def fullwidth_to_halfwidth(self, s, remove_span=True):
        """
        将文本中的全角字符转换为半角字符
        """
        halfwidth_str = ""
        for char in s:
            code = ord(char)
            if code == 12288:  # 全角空格直接转换
                if remove_span:
                    continue
                else:
                    code = 32
            elif code == 65509: # ￥ ¥
                code = 165
            elif code == 65111: # ﹗ !
                code = 33
            elif code == 65105: # ﹑、
                code = 12289
            elif code == 65117: # ﹝ 〔
                code = 12308
            elif code == 65118:
                code = 12309  # ﹞ 〕
            elif 65281 <= code <= 65374:  # 全角字符（除空格）根据关系转化
                code -= 65248

            if code not in self.dict_character_ord:
                print(f"code not in dict_character_ord, code: {code}, dict: {chr(code)}")
                return self.special_char
            halfwidth_str += chr(code)
        return halfwidth_str


def main():

    char_file_path = r"D:\Code\OCR\PaddleOCR\ppocr\utils\ppocr_moyan_keys_9175.txt"
    reog = relod_ocr_gt(char_file_path)

    # f_type =  
    img_dir = r"E:\DataSet\OCR\benchmark\benchmark_dataset\images"
    gt_file = r"E:\DataSet\OCR\benchmark\benchmark_dataset\test.txt"
    save_file = r"E:\DataSet\OCR\benchmark\benchmark_dataset\test_m1.txt"

    data_lines = moyan.read_txt_to_lines(gt_file)
    # data_lines = data_lines[:100]
    
    with open(save_file, "w", encoding='utf-8') as f:
        for ind, line in tqdm(enumerate(data_lines)):
            # print(f"{ind}, {line}")
            f_names, f_gt = line.strip().split("\t")
            img_path = os.path.join(img_dir, f_names)
            assert os.path.exists(img_path), f"{img_path} not exist!"
            
            im = cv2.imread(img_path)
            h, w = im.shape[:2]
            area = h*w
            ratio = h*1./w
            # print(h, w, area)

            # 过滤质量差的图片
            if area < (64*32):
                continue
            
            # 过滤竖直排列的图片
            if ratio > 2:
                continue
                
            new_f_gt = reog.fullwidth_to_halfwidth(f_gt)

            # 过滤gt不在字典内的图片
            if new_f_gt == reog.special_char:
                continue
            
            new_line = f"{f_names}\t{new_f_gt}\n"
            # print(new_line)
            # new_gt.append(new_f_gt)
            f.write(new_line)
    

if __name__=='__main__':
    main()
