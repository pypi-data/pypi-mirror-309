#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   remove_chinese_mark.py
@Time    :   2023/05/01 16:27:27
@Author  :   Moyan 
'''
import os
import re
import moyan
from tqdm import tqdm

def fillter_chinese_mark(text):
    pattern = "[\uFF01-\uFF5E]"  # 匹配全角字符
    result = re.sub(pattern, lambda x: chr(ord(x.group(0)) - 65248), text)  # 将全角字符转换为半角字符
    result = result.replace('，', ',').replace('。', '.')  # 将中文标点符号替换为英文标点符号
    return result


def demo_one():
    text = "这是一个测试，１２３４５。"
    print(fillter_chinese_mark(text))



def main():
    
    # demo_one()

    txt_file = r"E:\DataSet\OCR\GenTextMoyan\GenBasebkqa2019_300w_moyan\gt.txt"
    txt_line = moyan.readTxt2Lines(txt_file)
    # txt_line = txt_line[:100]

    gt_remove_chinese_mark_relative_path = []
    gt_remove_chinese_mark = []

    for tline in tqdm(txt_line):
        # print(tline)
        t_path, t_gt = tline.strip().split("\t")
        re_gt = fillter_chinese_mark(t_gt)

        new_line = tline
        if t_gt != re_gt:
            new_line = f"{t_path}	{re_gt}"
        new_line_relative = f"../../GenBasebkqa2019_300w_moyan/{new_line}"

        gt_remove_chinese_mark.append(new_line)
        gt_remove_chinese_mark_relative_path.append(new_line_relative)
    
    moyan.writeLines2Txt(gt_remove_chinese_mark, "gt_remove_chinese_mark.txt")
    moyan.writeLines2Txt(gt_remove_chinese_mark_relative_path, "gt_remove_chinese_mark_relative_path.txt")



if __name__ == '__main__':
    main()