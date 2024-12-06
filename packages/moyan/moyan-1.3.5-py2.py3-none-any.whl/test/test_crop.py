
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_crop.py
@Time    :   2023/07/07 10:26:51
@Author  :   Moyan 
'''
import os
import cv2
import numpy as np

def get_rotate_crop_image(img, points):
    # Use Green's theory to judge clockwise or counterclockwise
    # author: biyanhua
    d = 0.0
    for index in range(-1, 3):
        d += -0.5 * (points[index + 1][1] + points[index][1]) * (
                points[index + 1][0] - points[index][0])
    if d < 0:  # counterclockwise
        tmp = np.array(points)
        points[1], points[3] = tmp[3], tmp[1]

    try:
        img_crop_width = int(
            max(
                np.linalg.norm(points[0] - points[1]),
                np.linalg.norm(points[2] - points[3])))
        img_crop_height = int(
            max(
                np.linalg.norm(points[0] - points[3]),
                np.linalg.norm(points[1] - points[2])))
        pts_std = np.float32([[0, 0], [img_crop_width, 0],
                              [img_crop_width, img_crop_height],
                              [0, img_crop_height]])
        M = cv2.getPerspectiveTransform(points, pts_std)
        dst_img = cv2.warpPerspective(
            img,
            M, (img_crop_width, img_crop_height),
            borderMode=cv2.BORDER_REPLICATE,
            flags=cv2.INTER_CUBIC)
        dst_img_height, dst_img_width = dst_img.shape[0:2]
        if dst_img_height * 1.0 / dst_img_width >= 1.5:
            dst_img = np.rot90(dst_img)
        return dst_img
    except Exception as e:
        print(e)

def main():
    im = cv2.imread("mask.png")
    bbox = [687, 100, 849, 100, 849, 150, 687, 150]
    bbox = np.array(bbox).reshape(4,2)
    crop_im = get_rotate_crop_image(im, bbox)
    cv2.imwrite("mask_crop.png", crop_im)

if __name__ == '__main__':
    main()