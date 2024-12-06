#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   from_file_move_file.py
@Time    :   2023/09/21 16:02:34
@Author  :   moyan 
@Contact :   ice_moyan@163.com
'''
import os
import moyan
import shutil

def main():
    img_dir = "/mnt/e/DataSet/GenerateIMG_Xinjiang_IDCard_220708/images/"
    
    source_dir = '/mnt/e/DataSet/GenerateIMG_Xinjiang_IDCard_220708/yolo/labels/train'
    target_dir = '/mnt/e/DataSet/GenerateIMG_Xinjiang_IDCard_220708/yolo/images/train'

    names_list = moyan.walkDir2List(source_dir)
    for names in names_list:
        name = os.path.splitext(names)[0]
        source_path = os.path.join(img_dir, name+'.jpg')
        assert os.path.exists(source_path), f"{source_path} not exist!"
        target_path = os.path.join(target_dir, name+'.jpg')
        shutil.copyfile(source_path, target_path)

if __name__=='__main__':
    main()
