#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   coco_json_vis.py
@Time    :   2023/09/19 09:57:45
@Author  :   moyan 
@Contact :   ice_moyan@163.com
'''
import os
import sys
import cv2
import moyan
import getopt
from PIL import Image, ImageDraw
from pycocotools.coco import COCO
import matplotlib.pyplot as plt


def main():

    inputfile = r'E:\DataSet\GenerateIMG_Xinjiang_IDCard_220708\images'   # './data/coco/val2017/'
    jsonfile = r'E:\DataSet\GenerateIMG_Xinjiang_IDCard_220708/train.json'    # './data/coco/annotations/instances_val2017.json'
    outputfile = './vis'  # './data/coco/vis/'

    print('\n输入的文件为：', inputfile)
    print('\n输入的json为：', jsonfile)
    print('\n输出的文件为：', outputfile)

    moyan.pathExit(outputfile)

    coco = COCO(jsonfile)
    print(coco.getCatIds()  )
    
        # {"id": 1, "name": "front_name"},  
        # {"id": 2, "name": "front_gender"},  
        # {"id": 3, "name": "front_nation"},  
        # {"id": 4, "name": "front_addr"},  
        # {"id": 5, "name": "front_idnum"},  
        # {"id": 6, "name": "back_effetive_data"},  
        # {"id": 7, "name": "back_organize"}, 

    catIds = coco.getCatIds(catNms=['front_name'])  # front_name=1 表示姓名这一类
    # catIds = coco.getCatIds()  
    # catIds = [0,2,5,7]
    imgIds = coco.getImgIds(catIds=catIds)  # 图片id，许多值
    print(f'id: {catIds}, have images: {imgIds}')

    for i, imgId in enumerate(imgIds):
        print(i, "/", len(imgIds))
        img = coco.loadImgs(imgId)[0]

        cvImage = cv2.imread(os.path.join(inputfile, img['file_name']), -1)
        cvImage = cv2.cvtColor(cvImage, cv2.COLOR_BGR2GRAY)
        cvImage = cv2.cvtColor(cvImage, cv2.COLOR_GRAY2BGR)

        plt.cla()
        plt.axis('off')
        plt.imshow(cvImage) 

        annIds = coco.getAnnIds(imgIds=img['id'], catIds=catIds, iscrowd=None)
        anns = coco.loadAnns(annIds)
        coco.showAnns(anns)
        plt.savefig(os.path.join(outputfile, img['file_name']))  

    # for i, imgId in enumerate(imgIds):
    #     image = coco.loadImgs(imgId)[0] 
    #     anns_ids = coco.getAnnIds(imgIds=[imgId]) # 当前图片的所有标注的id
    #     target = coco.loadAnns(anns_ids) # 根据所有id获取所有标注信息

    #     img_path = os.path.join(inputfile, image['file_name'])
    #     img = Image.open(img_path)

    #     draw = ImageDraw.Draw(img)
    #     annIds = coco.getAnnIds(imgIds=img['id'], catIds=catIds, iscrowd=None)

if __name__=='__main__':
    main()
