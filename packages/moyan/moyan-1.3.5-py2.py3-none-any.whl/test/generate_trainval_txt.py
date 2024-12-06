#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   generate_trainval_txt.py
@Time    :   2023/08/21 17:16:59
@Author  :   Moyan 
'''
import os
import moyan
import random

def main():
    img_dir = r"E:\DataSet\GenerateIMG_Xinjiang_IDCard_220708\images"
    img_list = moyan.walkDir2List(img_dir, filter_postfix=[".jpg"])
    
    img_list = [names.replace(".jpg", "") for names in img_list]
    random.shuffle(img_list)

    all = len(img_list)
    test_num = int(all*0.2)
    train_list = img_list[test_num:all]
    test_list = img_list[:test_num]
    moyan.writeLines2Txt(train_list, "train.txt")
    moyan.writeLines2Txt(test_list, "test.txt")


if __name__ == '__main__':
    main()