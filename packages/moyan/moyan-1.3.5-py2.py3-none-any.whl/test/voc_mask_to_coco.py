import os
import json
import cv2
import sys
from tqdm import tqdm
import numpy as np
import random
from PIL import Image
from skimage import measure
from pycocotools import mask as mask_utils

def pascal_voc_to_coco(voc_dir, save_path):
    # 创建COCO数据集的基本结构
    coco_dataset = {
        "info": {},
        "images": [],
        "annotations": [],
        "categories": []
    }

    # 添加COCO数据集的信息
    coco_dataset["info"] = {
        "description": "Pascal VOC to COCO conversion",
        "version": "1.0",
        "year": 2023,
        "contributor": "moyan"
    }

    # 添加COCO数据集的类别
    coco_dataset["categories"] = [
        {"id": 1, "name": "front_name"},  
        {"id": 2, "name": "front_gender"},  
        {"id": 3, "name": "front_nation"},  
        {"id": 4, "name": "front_addr"},  
        {"id": 5, "name": "front_idnum"},  
        {"id": 6, "name": "back_effetive_data"},  
        {"id": 7, "name": "back_organize"},       
    ]

    class_id = [x['id'] for x in coco_dataset["categories"]]

    # 读取Pascal VOC数据集的标注文件
    if sys.platform=='win32':
        annotation_file = os.path.join(voc_dir, 'train.txt')
    else:
        annotation_file = os.path.join(voc_dir, 'ImageSets', 'Segmentation', 'train.txt')
    with open(annotation_file, 'r') as f:
        annotations = f.read().splitlines()

    # random.seed(100)
    # random.shuffle(annotations)
    # annotations = annotations[:10]

    # 记录所有标注的id
    num_anno_id = 0

    # 遍历每个标注
    for ind, ann in tqdm(enumerate(annotations)):
        image_name = ann.strip()

        # 读取图像
        if sys.platform=='win32':
            image_path = os.path.join(voc_dir, "images", image_name + ".jpg")
        else:
            image_path = os.path.join(voc_dir, "JPEGImages", image_name + ".jpg")
        image = cv2.imread(image_path)
        height, width, _ = image.shape

        # 添加图像信息到COCO数据集
        image_info = {
            "id": int(ind),
            "file_name": image_name + ".jpg",
            "width": width,
            "height": height
        }
        coco_dataset["images"].append(image_info)

        # 读取8位掩码图像
        mask_path = os.path.join(voc_dir, "mask8bit", image_name + ".png")
        # mask_image = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
        mask_image = np.array(Image.open(mask_path))
        # cv2.imwrite("a.png", mask_image*50)
        mask_image_label = list(np.unique(mask_image))
        # print(mask_image.shape)

        # 将8位掩码转换为二值掩码
        for tid in class_id:
            if tid not in mask_image_label: continue

            binary_mask = np.zeros_like(mask_image, dtype=np.uint8)    
            binary_mask[mask_image == tid] = 1
            # cv2.imwrite("a1.png", binary_mask*255)

            contours = measure.find_contours(binary_mask, 0.5)

            # 遍历轮廓
            for contour in contours:
                # 创建一个空白图像，用于绘制当前轮廓
                contour_mask = np.zeros_like(mask_image, dtype=np.uint8)
                contour_pts = np.round(contour).astype(int)
                contour_pts = np.flip(contour_pts, axis=1)  # 交换坐标的顺序
                cv2.fillPoly(contour_mask, [contour_pts], 1)
                # cv2.imwrite("a2.png", contour_mask*255)

                # 将二值掩码转换为RLE编码
                rle_mask = mask_utils.encode(np.asfortranarray(contour_mask))

                num_anno_id+=1

                # 创建COCO数据集的标注信息
                annotation = {
                    "id": int(num_anno_id),  # 每个分割的id
                    "image_id": int(ind), # 对应图片的id
                    "category_id": tid,  # 分割对应类别的id
                    "segmentation": [],
                    "area": int(np.sum(binary_mask)),
                    "bbox": mask_utils.toBbox(rle_mask).tolist(),
                    "iscrowd": 0
                }
                contour = np.flip(contour, axis=1)
                segmentation = contour.ravel().tolist()
                annotation["segmentation"].append(segmentation)
                coco_dataset["annotations"].append(annotation)

    # 保存COCO数据集的JSON文件
    with open(save_path, 'w', encoding='utf-8') as f: 
        json.dump(coco_dataset, f)

    print("Conversion completed successfully.")


# print(sys.platform)
if sys.platform=='linux':
    pascal_voc_dir = '/mnt/e/DataSet/GenerateIMG_Xinjiang_IDCard_220708/pascal_voc/'
    img_dir = os.path.join(pascal_voc_dir, 'JPEGImages')
    mask_dir = os.path.join(pascal_voc_dir, 'SegmentationClass')
    file_list = os.path.join(pascal_voc_dir, 'ImageSets', 'Segmentation', 'test.txt')
elif sys.platform=='win32':
    pascal_voc_dir = r'E:\DataSet\GenerateIMG_Xinjiang_IDCard_220708/'
    img_dir = os.path.join(pascal_voc_dir, 'images')
    mask_dir = os.path.join(pascal_voc_dir, 'mask8bit')
    file_list = os.path.join(pascal_voc_dir, 'train_mini.txt')

# 示例用法
save_path = r'E:\DataSet\GenerateIMG_Xinjiang_IDCard_220708\train.json'
pascal_voc_to_coco(pascal_voc_dir, save_path)