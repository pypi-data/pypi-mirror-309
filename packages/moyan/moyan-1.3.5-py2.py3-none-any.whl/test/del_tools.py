#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   del_tools.py
@Time    :   2023/08/07 09:15:54
@Author  :   Moyan 
'''
import os
import moyan
import shutil
import random

def ocr_dict():
    txt_path = "ocr_dict_label.txt"
    txt_list = moyan.read_txt_to_lines(txt_path)
    label = [int(x) for x in txt_list]
    label = list(set(label))
    label.sort()
    label = [str(x) for x in label]
    moyan.write_txt_to_lines(label, "ocr_dict_label_v2.txt")


def ocr_label_to_str():
    ocr_dict_path = "ocr_dict_label_v3.txt"
    ocr_dict_list = moyan.read_txt_to_lines(ocr_dict_path)
    label = [int(x) for x in ocr_dict_list]
    
    new_list = []
    for  x in label:
        new_list.append(chr(x))
    moyan.write_txt_to_lines(new_list, "ocr_dict_label_v3_str.txt")


def check2diff():
    ocr_dict_path = r"C:\Users\ice_m\Desktop\ppocr_keys_9309_v2.txt"
    ocr_dict_list = moyan.read_txt_to_lines(ocr_dict_path)
    print(len(ocr_dict_list))

    new_list = []
    for ind, x in enumerate(ocr_dict_list):
        print(ind, x)
        print(x, ord(x))
        new_list.append(ord(x))
    print(len(new_list)) 

    print(len(set(new_list))) 
  
    # label = [int(x) for x in ocr_dict_list]
    
    # new_list = []
    # for  x in label:
    #     new_list.append(chr(x))
    # moyan.write_txt_to_lines(new_list, "ocr_dict_label_v3_str.txt")


def cal_unique_dict():
    txt_path = r"C:\Users\ice_m\Desktop\ocr_dict\省市区县镇.txt"
    org_dict_path_3k = r"C:\Users\ice_m\Desktop\ocr_dict\cn_char_3753.txt"
    org_dict_path_2k = r"C:\Users\ice_m\Desktop\ocr_dict\cn_char_2000.txt"

    dict3k_list = moyan.read_txt_to_lines(org_dict_path_3k)
    dict2k_list = moyan.read_txt_to_lines(org_dict_path_2k)

    txt_list = moyan.read_txt_to_lines(txt_path)
    txt_dict = set()
    for line in txt_list:
        line = line.strip()
        for chr in line:
            txt_dict.add(chr)  
    # print(txt_dict)
    # print(len(txt_dict))
    diff_2k = txt_dict - set(dict2k_list)
    diff_3k = txt_dict - set(dict3k_list)
    print(diff_2k)
    print(len(diff_2k))
    print(diff_3k)
    print(len(diff_3k))

    new_set = list(dict2k_list) + list(diff_2k)
    print(len(new_set))
    
    family_list = moyan.read_txt_to_lines(r"C:\Users\ice_m\Desktop\ocr_dict\family_name_100.txt")
    print(set(family_list)-set(new_set))

    # moyan.write_txt_to_lines(new_set, "cn_char_3565.txt")
    
    # print(txt_dict-set(dict3k_list))


def sp_trainval_rewrite_txt():
    img_dir = "/mnt/f/data/OCR_DataSet_All/dataset"
    txt_list = ["Art_recognition_train.txt",
                "LSVT_recognition_train.txt",
                "MTWI2018_recognition_train.txt",
                "ReCTS_recognition_train.txt",
                "SROIE2019_recognition_train.txt",
                "baidu_chinese_train.txt",
                "icdar2017rctw_recognition_train.txt",
                "mlt2019_recognition_train.txt"]
    train_list = []
    test_list = []
    sp_ind = 0.1

    for txt_name in txt_list:
        file_list = moyan.read_txt_to_lines(os.path.join(img_dir, txt_name))
        new_list = []
        for t_line in file_list:
            f_name, f_gt, f_laug = t_line.split("\t")
            if f_laug not in ["Latin", "Chinese"]:
                continue
            # print(f_name, f_gt, f_laug)    
            new_list.append(f"{f_name}\t{f_gt}")
        random.shuffle(new_list)
        sp_test = int(len(new_list) * sp_ind)
        test_list += new_list[:sp_test]
        train_list += new_list[sp_test:]
    
    save_test_path = os.path.join(img_dir, "test.txt")
    save_trainval_path = os.path.join(img_dir, "trainval.txt")
    moyan.write_txt_to_lines(test_list, save_test_path)
    moyan.write_txt_to_lines(train_list, save_trainval_path)

def reload_txt():
    
    # org_dict_list = moyan.read_txt_to_lines(r"D:\Code\OCR\PaddleOCR\ppocr\utils\ppocr_moyan_keys_9175_with_aug.txt")
    # SimilarCharacter_file = r"C:\Users\ice_m\Desktop\SimilarCharacter.txt"
    # sim_list = moyan.read_txt_to_lines(SimilarCharacter_file)
    # new_file = r"C:\Users\ice_m\Desktop\SimilarCharacter_dick9175.txt"
    # with open(new_file, "w", encoding='utf-8') as f:
    #     for ind, lines in enumerate(sim_list):
    #         new = ""
    #         for chr in lines:
    #             if chr in org_dict_list:
    #                 new+=chr
    #         # print(chr)
    #         f.write(new+"\n")

    #         # new_lines = []
    #         # for chr in lines:
    #         #     if chr in org_dict_list:
    #         #         new_lines.append(chr)
    #         # tmpd = 5
    #         # split_a = [new_lines[i:i+tmpd] for i in range(0, len(new_lines), tmpd)] 
    #         # for x in split_a:
    #         #     print(x)
    #         # for i in range(len(new_lines), 5):
    #         #     print(i)
    #         #     print(new_lines[:i])
    #         # if len(new_lines) > 1:
    #         #     print(ind, lines)
    #         #     f.write(new_lines+"\n")

    label_file = r"E:\DataSet\corpus\SimilarCharacter_dick9175.txt"
    txt_list = moyan.read_txt_to_lines(label_file)
    new_file = r"C:\Users\ice_m\Desktop\similar_character_household_name.txt"
    with open(new_file, "w", encoding='utf-8') as f:
        tmp = ""
        for ind, lines in enumerate(txt_list):
            # print(ind, lines, len(lines))
            for chr in lines:
                tmp += chr
                if len(tmp) == 3:
                    # print(tmp)
                    f.write(tmp+"\n")
                    tmp=""


def split_ocr_txt():
    txt_path = r"D:\Code\sunc\synthtiger-1.2.1\results\gt.txt"
    txt_list = moyan.read_txt_to_lines(txt_path)
    for ind, line in enumerate(txt_list):
        print(ind, line)
        abs_path, gt_char = line.split("\t")
        img_path = os.path.join(os.path.dirname(txt_path), abs_path)
        assert os.path.exists(img_path)
        save_path = img_path.replace(".jpg", ".txt")
        with open(save_path, "w", encoding='utf-8') as f:
            f.write(gt_char)
        # exit()

def main():
    # ocr_dict()
    # ocr_label_to_str()
    # check2diff()
    # cal_unique_dict()
    # sp_trainval_rewrite_txt()
    # reload_txt()
    split_ocr_txt()
    
if __name__ == '__main__':
    main()