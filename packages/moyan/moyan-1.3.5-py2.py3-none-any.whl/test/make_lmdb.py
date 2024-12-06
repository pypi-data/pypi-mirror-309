
# -*- coding: utf-8 -*-
import os
import lmdb
import argparse
import shutil
import json

import numpy as np
import cv2


def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_root_dir', type=str)
    parser.add_argument('--label_file_paths', nargs='+')
    parser.add_argument('--delimiter', type=str, default='tab')
    parser.add_argument('--lmdb_out_dir', type=str)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    return args


def convert2lmdb(
    data_root_dir, label_file_paths, delimiter, lmdb_out_dir, is_check):
    """
    Convert `SimpleDataset`(Icdar2015) format data to LmdbDataset format.
    Params usage description can be found in README.md
    """
    def checkImageIsValid(image_bin):
        if image_bin is None:
            return False
        image_buf = np.frombuffer(image_bin, dtype=np.uint8)
        img = cv2.imdecode(image_buf, cv2.IMREAD_GRAYSCALE)
        img_h, img_w = img.shape[0], img.shape[1]
        if img is None or img_h * img_w == 0:
            return False
        
        # 过滤小图片
        if (img_h*img_w) < (12*12):
            return False

        return True

    def fullwidth_to_halfwidth(s):
        """
        将文本中的全角字符转换为半角字符
        """
        halfwidth_str = ""
        for char in s:
            code = ord(char)
            if code == 12288:  # 全角空格直接转换
                code = 32
            elif code == 65509: # ￥ ¥
                code = 165
            elif code == 65111: # ﹗ !
                code = 33
            elif code == 65105: # ﹑、
                code = 12289
            elif code == 65117: # ﹝ 〔
                code = 12308
            elif code == 65118:
                code = 12309  # ﹞ 〕
            elif 65281 <= code <= 65374:  # 全角字符（除空格）根据关系转化
                code -= 65248
            halfwidth_str += chr(code)
        return halfwidth_str

    def writeCache(env, cache):
        with env.begin(write=True) as txn:
            for k, v in cache.items():
                txn.put(k.encode('utf-8'), v)

    if os.path.exists(lmdb_out_dir) and os.path.isdir(lmdb_out_dir):
        while True:
            print(f'{lmdb_out_dir} already exists, delete or not? [y/n]')
            Yn = input().strip()
            if Yn in ['Y', 'y']:
                shutil.rmtree(lmdb_out_dir)
                break
            if Yn in ['N', 'n']:
                return
    os.makedirs(lmdb_out_dir)

    delimiter_dict = {
        'blank': ' ',
        'tab': '\t'
    }
    assert delimiter in delimiter_dict, \
        f'unsupported delimiter: \'{delimiter}\', you can update the '\
        f'"delimiter_dict" to fit for your task.'
    
    # 此处跟着自己电脑的内存来调整map_size  1024*1024*1024*10 = 10G
    env = lmdb.open(lmdb_out_dir, map_size=1024*1024*1024*30) 
    cache = {}
    cnt = 1  # in ppocr's lmdb_dataset.py, idx start from 1
    total_nums = 0

    for label_file_path in label_file_paths:
        with open(label_file_path, 'r', encoding='utf-8') as fp1:
            lines = fp1.read().strip().split('\n')
            nums = len(lines)
            total_nums += nums
            for i in range(nums):
                relative_img_path, label = lines[i].split(delimiter_dict[delimiter], 1)
                img_path = os.path.join(data_root_dir, relative_img_path)
                if not os.path.exists(img_path):
                    print(f'Img path: {img_path} isn\'t exist, continue.')
                    continue
                with open(img_path, 'rb') as fp2:
                    image_bin = fp2.read()
                    if is_check and not checkImageIsValid(image_bin):
                        print(
                            f'Img path: {img_path} is an invalid image, continue.')
                        continue
                    
                    # 矫正圆角半角
                    label = fullwidth_to_halfwidth(label)

                    image_key = 'image-%09d' % cnt
                    label_key = 'label-%09d' % cnt
                    cache[image_key] = image_bin
                    cache[label_key] = label.encode('utf-8')
                    if cnt % 1000 == 0:
                        writeCache(env, cache)
                        print(
                            f'{label_file_path} : {i + 1}/{nums} completed.',
                            end='\r',
                            flush=True)
                        cache = {}
                    cnt += 1
            print()

    cache['num-samples'] = str(cnt - 1).encode('utf-8')
    writeCache(env, cache)
    print(f'Total : {cnt - 1}/{total_nums} completed.')
    print(f'Created "{lmdb_out_dir}" lmdb dataset with {total_nums} samples successfully')


if __name__ == "__main__":
    args = getArgs()
    convert2lmdb(
        args.data_root_dir, args.label_file_paths, args.delimiter,
        args.lmdb_out_dir, args.check)


# python make_lmdb.py --data_root_dir rec_data \
#   					--label_file_paths .\rec_data\rec_gt_test.txt \
#    					--delimiter tab --lmdb_out_dir ./lmdb/train


# python .\make_lmdb.py --data_root_dir E:\DataSet\text\Synthetic_Chinese_String_Dataset\images\ --label_file_path E:\DataSet\text\Synthetic_Chinese_String_Dataset\data_test_text.txt --delimiter tab --lmdb_out_dir Synthetic_Chinese_String_Dataset_Test
