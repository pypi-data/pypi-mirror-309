#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   run_paddleocr_tflite.py
@Time    :   2023/09/20 10:10:48
@Author  :   moyan 
@Contact :   ice_moyan@163.com
'''
import os
import cv2
import math
import moyan
import numpy as np
from moyan.template.TFLite import TFLiteModel

class PaddleOCRLite(TFLiteModel):
    def __init__(self, 
                 model_path: str, 
                 character_dict_path:str,
                 use_space_char=False
            ) -> None:
        super().__init__(model_path)
        self.use_space_char = use_space_char
        self.rec_image_shape = [32, 320, 3]
        self.character_str = []
        self.reverse = False
        self.init_char_dict(character_dict_path)

    def init_char_dict(self, character_dict_path, is_ctct=True):
        with open(character_dict_path, "rb") as fin:
            lines = fin.readlines()
            for line in lines:
                line = line.decode('utf-8').strip("\n").strip("\r\n")
                self.character_str.append(line)
        if self.use_space_char:
                self.character_str.append(" ")
        dict_character = list(self.character_str)
        dict_character = self.add_special_char(dict_character)
        self.dict = {}
        for i, char in enumerate(dict_character):
            self.dict[char] = i
        self.character = dict_character

    def preprocess(self, img):
        imgH, imgW, imgC = self.rec_image_shape
        assert imgC == img.shape[2]
        h, w = img.shape[:2]
        ratio = w / float(h)
        if math.ceil(imgH * ratio) > imgW:
            resized_w = imgW
        else:
            resized_w = int(math.ceil(imgH * ratio))
        resized_image = cv2.resize(img, (resized_w, imgH))
        resized_image = resized_image.astype('float32')
        resized_image = resized_image / 255
        resized_image -= 0.5
        resized_image /= 0.5
        padding_im = np.zeros((imgH, imgW, imgC), dtype=np.float32)
        padding_im[:, 0:resized_w, :] = resized_image
        input_tensor = np.expand_dims(padding_im, axis=0)
        return input_tensor

    def postprocess(self, output_tensor):
        preds = output_tensor[0]
        preds_idx = preds.argmax(axis=2)
        preds_prob = preds.max(axis=2)
        text = self.decode(preds_idx, preds_prob, is_remove_duplicate=True)
        return text

    def decode(self, text_index, text_prob=None, is_remove_duplicate=False):
        """ convert text-index into text-label. """
        result_list = []
        ignored_tokens = self.get_ignored_tokens()
        batch_size = len(text_index)
        for batch_idx in range(batch_size):
            selection = np.ones(len(text_index[batch_idx]), dtype=bool)
            if is_remove_duplicate:
                selection[1:] = text_index[batch_idx][1:] != text_index[
                    batch_idx][:-1]
            for ignored_token in ignored_tokens:
                selection &= text_index[batch_idx] != ignored_token

            char_list = [
                self.character[text_id]
                for text_id in text_index[batch_idx][selection]
            ]
            if text_prob is not None:
                conf_list = text_prob[batch_idx][selection]
            else:
                conf_list = [1] * len(selection)
            if len(conf_list) == 0:
                conf_list = [0]

            text = ''.join(char_list)

            if self.reverse:  # for arabic rec
                text = self.pred_reverse(text)

            result_list.append((text, np.mean(conf_list).tolist()))
        return result_list

    def get_ignored_tokens(self):
        return [0]  # for ctc blank
    
    def add_special_char(self, dict_character):
        dict_character = ['blank'] + dict_character
        return dict_character


def main():
    model_path = r"D:\Code\OCR\PaddleOCR\proj_moyan\rec\idcardlite_dict3k_mbv3-largex0.35_none_none_230919\output\infer_best_it28\tflite\model_dynimic.tflite"
    character_dict_path = r"D:\Code\OCR\PaddleOCR\ppocr\utils\cn_char_idcard_3579.txt"
    model = PaddleOCRLite(model_path, character_dict_path)
    # img_path = "./crop_name.jpg" 
    # img_path = "./crop_addre.jpg" 
    img_path = "./crop_idnum.jpg" 
    im = cv2.imread(img_path)
    pred_text = model.run(im)
    print(pred_text)

if __name__=='__main__':
    main()
