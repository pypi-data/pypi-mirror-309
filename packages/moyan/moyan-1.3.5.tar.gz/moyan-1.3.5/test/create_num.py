#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   create_num.py
@Time    :   2023/03/29 09:29:18
@Author  :   Moyan 
'''
import os
import moyan
import random
from tqdm import tqdm
        
sp = ["-", ".", ":"]

def get_random_num():

    A1 = str(random.randint(1, 9))
    A10 = str(random.randint(0, 9))

    A2 = str(random.randint(0, 9)) if random.random()>0.2 else sp[random.randint(0, 2)]
    if A2 in sp:
        A3 = str(random.randint(0, 9))
        if random.random()>0.1: 
            # print(A1+A2+A3+A10)
            return A1+A2+A3+A10
    else:
        A3 = str(random.randint(0, 9)) if random.random()>0.2 else sp[random.randint(0, 2)]
    if A3 in sp:
        A4 = str(random.randint(0, 9))
        if random.random()>0.1: return A1+A2+A3+A4+A10
    else:
        A4 = str(random.randint(0, 9)) if random.random()>0.2 else sp[random.randint(0, 2)]
    if A4 in sp:
        A5 = str(random.randint(0, 9))
        if random.random()>0.2: 
            # print(A1+A2+A3+A4+A5+A10)
            return A1+A2+A3+A4+A5+A10
    else:
        A5 = str(random.randint(0, 9)) if random.random()>0.2 else sp[random.randint(0, 2)]
    if A5 in sp:
        A6 = str(random.randint(0, 9))
    else:
        A6 = str(random.randint(0, 9)) if random.random()>0.2 else sp[random.randint(0, 2)]
    if A6 in sp:
        A7 = str(random.randint(0, 9))
    else:
        A7 = str(random.randint(0, 9)) if random.random()>0.2 else sp[random.randint(0, 2)]
    if A7 in sp:
        A8 = str(random.randint(0, 9))
    else:
        A8 = str(random.randint(0, 9)) if random.random()>0.2 else sp[random.randint(0, 2)]                                    
    if A8 in sp:
        A9 = str(random.randint(0, 9))
    else:
        A9 = str(random.randint(0, 9)) if random.random()>0.2 else sp[random.randint(0, 2)]
    anum = A1+A2+A3+A4+A5+A6+A7+A8+A9+A10    
    return anum

def main():
    
    num=100000
    new_num = []
    for i in tqdm(range(num)):
        n_num = get_random_num()
        new_num.append(n_num)
    moyan.write_txt_to_lines(new_num, "random_10w_num.txt")

if __name__ == '__main__':
    # main()

    txt = r"G:\data\AVADataPath\csv\trainval_file_list.txt"
    txt_list = moyan.read_txt_to_lines(txt)
    img_dir = r"G:\data\AVADataPath\orig_videos\trainval"
    img_list = os.listdir(img_dir)

    for name in txt_list:
        if name not in img_list:
            print(name)