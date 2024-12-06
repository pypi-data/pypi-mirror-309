#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   lableme_and_paddleocr.py
@Time    :   2023/11/01 15:27:20
@Author  :   moyan 
@Contact :   ice_moyan@163.com
'''
import os
from tqdm import tqdm
import numpy as np
import json


def dump_paddleocr():

    img_list = ['01.jpg', '02.jpg', '03.jpg', '04.jpg', ] 
    new_doc = ""
    for names in tqdm(img_list):
        names = "xx.jpg"
        label_list = [{'text': "xx", 'bbox': [0,0,0,0]}, {'text': "xx", 'bbox': [0,0,0,0]}]
        new_gt_info = []
        for label in label_list:
            res = {}
            res['transcription'] = label['text']
            res['points'] = np.array(label['bbox'], dtype=np.int64)
            res['key_cls'] = "None"
            res['difficult'] = "false"
            new_gt_info.append(res)
        new_doc += "images/" + f"{names}" + "\t" +json.dumps(new_gt_info, ensure_ascii=False) + "\n"
    
    save_path = "Label.txt"
    with open(save_path, "w", encoding="utf-8") as f:
        f.writelines(new_doc)


def main():
    pass


if __name__=='__main__':
    main()
