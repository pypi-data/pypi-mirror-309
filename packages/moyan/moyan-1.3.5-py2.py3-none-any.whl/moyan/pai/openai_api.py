#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   openai_api.py
@Time    :   2024/07/24 11:14:37
@Author  :   moyan 
@Contact :   ice_moyan@163.com
'''
import os
import base64
from openai import OpenAI


class VLMModelAPI:
    def __init__(self, url) -> None:
        self.client = OpenAI(api_key='none', base_url=url)
        self.model_name = self.client.models.list().data[0].id
        print(f"find model: {self.model_name}")


    def encode_image(self, img_path):
        with open(img_path, "rb") as img_file:
            base64_data = base64.b64encode(img_file.read()).decode('utf-8')
        return f'data:image/jpeg;base64,{base64_data}'


    def run(self, img_path, query='describe the image please', temperature=0.8, top_p=0.8):
        assert os.path.exists(img_path), f"{img_path} not exist!"
        img_data = self.encode_image(img_path)

        response = self.client.chat.completions.create(
            model=self.model_name, 
            messages=[
                {
                    "role": "user", 
                    "content": [
                        {
                            'type': 'text',
                            'text': query
                        },
                        {
                            'type': 'image_url',
                            'image_url': {
                                'url': img_data
                            }
                        }
                    ]
                }
            ], 
            temperature=temperature, 
            top_p=top_p
        )
        return response