#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   lmdb_to_image.py
@Time    :   2023/09/28 11:07:29
@Author  :   moyan 
@Contact :   ice_moyan@163.com
'''
import os
import cv2
import lmdb
import moyan
import numpy as np
from tqdm import tqdm

def get_img_data(value):
    """get_img_data"""
    if not value:
        return None
    imgdata = np.frombuffer(value, dtype='uint8')
    if imgdata is None:
        return None
    imgori = cv2.imdecode(imgdata, 1)
    if imgori is None:
        return None
    return imgori

def load_hierarchical_lmdb_dataset(data_dir):
    lmdb_sets = {}
    dataset_idx = 0
    for dirpath, dirnames, filenames in os.walk(data_dir + '/'):
        if not dirnames:
            env = lmdb.open(
                dirpath,
                max_readers=32,
                readonly=True,
                lock=False,
                readahead=False,
                meminit=False)
            txn = env.begin(write=False)
            num_samples = int(txn.get('num-samples'.encode()))
            lmdb_sets[dataset_idx] = {"dirpath":dirpath, "env":env, \
                "txn":txn, "num_samples":num_samples}
            dataset_idx += 1
    return lmdb_sets

def get_lmdb_sample_info(txn, index):
    label_key = 'label-%09d'.encode() % index
    label = txn.get(label_key)
    if label is None:
        return None
    label = label.decode('utf-8')
    img_key = 'image-%09d'.encode() % index
    imgbuf = txn.get(img_key)
    return imgbuf, label


def main():

    save_tag = 'test'
    data_dir = r"E:\DataSet\OCR\gen_idcard_dict3k_200w_moyan_230823\gen_idcard_dict3k_200w_moyan_230823_test"
    save_dir = r"E:\DataSet\OCR\gen_idcard_dict3k_200w_moyan_230823\gen_idcard_dict3k_200w_moyan_230823_test_img"
    moyan.pathExit(save_dir)
    
    lmdb_sets = load_hierarchical_lmdb_dataset(data_dir)
    lmdb_num = len(lmdb_sets)
    total_sample_num = 0
    for lno in range(lmdb_num):
        total_sample_num += lmdb_sets[lno]['num_samples']
    data_idx_order_list = np.zeros((total_sample_num, 2))
    beg_idx = 0
    for lno in range(lmdb_num):
        tmp_sample_num = lmdb_sets[lno]['num_samples']
        end_idx = beg_idx + tmp_sample_num
        data_idx_order_list[beg_idx:end_idx, 0] = lno
        data_idx_order_list[beg_idx:end_idx, 1] \
            = list(range(tmp_sample_num))
        data_idx_order_list[beg_idx:end_idx, 1] += 1
        beg_idx = beg_idx + tmp_sample_num

    gt = []
    # total_sample_num = 100 # for test
    for idx in tqdm(range(total_sample_num-1)):
        name = f'{save_tag}_%09d' % idx
        save_name = name + ".jpg"
        lmdb_idx, file_idx = data_idx_order_list[idx]
        lmdb_idx = int(lmdb_idx)
        file_idx = int(file_idx)
        sample_info = get_lmdb_sample_info(lmdb_sets[lmdb_idx]['txn'], file_idx)
        img, label = sample_info
        im = get_img_data(img)
        gt.append(f"{save_name}\t{label}")
        save_path = os.path.join(save_dir, save_name)
        cv2.imwrite(save_path, im)
    
    save_gt_path = os.path.join(save_dir, 'gt.txt')
    moyan.write_txt_to_lines(gt, save_gt_path)


if __name__=='__main__':
    main()
