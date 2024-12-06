#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   ocr_dict.py
@Time    :   2023/09/28 10:50:11
@Author  :   moyan 
@Contact :   ice_moyan@163.com
'''
import os
import moyan




def reload_dict(file_path):
    txt_list = moyan.read_txt_to_lines(file_path)
    labels_num = []
    for char in txt_list:
        # print(char, ord(char))
        labels_num.append(ord(char))
    labels_num.sort()
    # print(labels_num[-20])
    labels_str = []
    for num in labels_num:
        labels_str.append(chr(num))
    return labels_str

    

def main():

    dict_9k_path = r"D:\Code\OCR\PaddleOCR\ppocr\utils\ppocr_keys_9309_v2.txt"
    labels_str = reload_dict(dict_9k_path)
    print(len(labels_str))
    save_path = r"D:\Code\OCR\PaddleOCR\ppocr\utils\ppocr_moyan_keys_9309.txt"
    moyan.write_txt_to_lines(labels_str, save_path)


if __name__=='__main__':
    main()
