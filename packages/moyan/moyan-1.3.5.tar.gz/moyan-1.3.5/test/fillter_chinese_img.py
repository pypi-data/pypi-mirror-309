#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   fillter_chinese_img.py
@Time    :   2023/03/07 14:48:56
@Author  :   Moyan 
'''
import os
import re
import cv2
import moyan

import shutil
from tqdm import tqdm


import regex

def is_only_chinese_or_arabic(string):
    # 如果字符串为空，返回False
    if not string:
        return False
    # 如果字符串只包含中文字符或阿拉伯数字，返回True
    if regex.search(r'[\p{Han}0-9]+', string) and regex.fullmatch(r'[\p{Han}0-9]+', string):
        return True
    # 否则，返回False
    return False

# 检验是否全是中文字符
def is_all_chinese(strs):
    for _char in strs:
        if not '\u4e00' <= _char <= '\u9fa5':
            return False
    return True


def main():

    label_file_path = r"F:\data\OCR_DataSet_All\dataset\百度中文场景文字识别\train.txt"
    img_dir = r"F:\data\OCR_DataSet_All\dataset\百度中文场景文字识别\train_images"
    label_list = moyan.read_txt_to_lines(label_file_path)

    save_dir = r"F:\data\OCR_DataSet_All\data_chinese_moyan\BaiduChineseSceneText\crop_image"
    moyan.pathExit(save_dir)
    save_gt_path = r"F:\data\OCR_DataSet_All\data_chinese_moyan\BaiduChineseSceneText_label.txt"

    gt_list = []
    for tmp_line in tqdm(label_list):
        tmp_path, gt, luag = tmp_line.strip().split("\t")
        names = os.path.basename(tmp_path)
        if is_only_chinese_or_arabic(gt) and gt != "":
            # print(tmp_line)
            img_path = os.path.join(img_dir, names)
            assert os.path.exists(img_path)
            # print(img_path)
            # im = cv2.imread(img_path)
            im = moyan.cv_read(img_path)
            h, w = im.shape[:2]

            # 过滤小图
            if (h*w) < 625:
                continue

            # 过滤竖直排列图
            if ((h*1.)/w) > 1.5:
                continue

            save_path = os.path.join(save_dir, names)
            shutil.copyfile(img_path, save_path)
            tmp_t = f"Art/crop_image/{names}	{gt}"
            gt_list.append(tmp_t)

    moyan.write_txt_to_lines(gt_list, save_gt_path)

        # if gt == "":
        #     print(tmp_line)
    
if __name__ == '__main__':
    # main()

    # import random
    # dir_path = r"F:\data\OCR_DataSet_All\data_chinese_moyan"
    # list_txt_path = moyan.walkDir2List(dir_path, filter_postfix=[".txt"])

    # txt_gt_list = []
    # for txt_name in list_txt_path:
    #     txt_path = os.path.join(dir_path, txt_name)
    #     assert os.path.exists(txt_path), f"txt path exist, {txt_path}"

    #     tmp_list = moyan.read_txt_to_lines(txt_path)
    #     txt_gt_list += tmp_list
    
    # print(f"len txt: {len(txt_gt_list)}")
    # random.shuffle(txt_gt_list)
    # moyan.writeLines2Txt(txt_gt_list, "gt_all.txt")
    


    dir_path = r"E:\DataSet\OCR\data_chinese_moyan"
    txt_file = r"E:\DataSet\OCR\data_chinese_moyan\gt_all.txt"
    txt_list = moyan.read_txt_to_lines(txt_file)

    for tmp_line in txt_list:
        txt_name, gt = tmp_line.strip().split("\t")
        txt_path = os.path.join(dir_path, txt_name)
        assert os.path.exists(txt_path), f"txt path exist, {txt_path}"

        im = cv2.imread(txt_path)
        print(im.shape)