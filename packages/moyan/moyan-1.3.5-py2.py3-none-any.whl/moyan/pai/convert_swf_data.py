#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   convert_swf_data.py
@Time    :   2024/07/24 11:26:59
@Author  :   moyan 
@Contact :   ice_moyan@163.com
'''
import os
import json
from copy import deepcopy


class SwfOneTurnData:
    def __init__(self) -> None:
        self.data = []

    def get_template(self):
        tmp = {
            "query": "",
            "response": "",
            "images": []
        }
        return deepcopy(tmp)

    def validate_data(self, query, response, image_path):
        if not query or not response:
            raise ValueError("Query and response cannot be empty")
        if not image_path:
            raise ValueError("Image path cannot be empty")
        if not os.path.exists(image_path):
            raise FileNotFoundError("Image path does not exist")


    def add_data(self, query, response, image_path):
        self.validate_data(query, response, image_path)
        tmp = self.get_template()
        tmp["query"] = query
        tmp["response"] = response
        tmp["images"].append(image_path)
        return self.data.append(tmp)

    def save(self, save_path):
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)


def test_SwfOneTurnData():
    
    # 测试用例1：添加一条数据并保存
    swf_data1 = SwfOneTurnData()
    query1 = '描述下这张图片'
    response1 = "一张图片"
    image_path1 = r"D:\Code\AI-in-air\moyan\test\household.jpg"
    image_path1 = os.path.abspath(image_path1)

    swf_data1.add_data(query1, response1, image_path1)
    swf_data1.save("test1.json")
    assert os.path.exists("test1.json")
    with open("test1.json", "r", encoding="utf-8") as f:
        data1 = json.load(f)
    assert data1 == [{"query": query1, "response": response1, "images": [image_path1]}]
    print("All test cases pass")



def main():
    
    test_SwfOneTurnData()

    

if __name__=='__main__':
    main()
