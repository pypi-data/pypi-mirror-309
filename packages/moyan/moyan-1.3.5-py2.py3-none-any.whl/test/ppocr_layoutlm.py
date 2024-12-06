#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   ppocr_layoutlm.py
@Time    :   2023/06/14 17:22:03
@Author  :   Moyan 
'''
import os
from ppocr import PPOCRv3

import cv2
import torch
import numpy as np
from PIL import Image
from typing import List, Tuple, Dict
from torchvision import transforms
from transformers import AutoTokenizer
from onnxruntime import InferenceSession

#add householdlayoutlmv3ner class test

def get_ppocr_dict():
    character_str = []
    use_space_char = True
    character_dict_path = "E:/models/PaddleOCR/ch_PP-OCRv3_xx_16.2M/ppocr_keys_v1.txt"
    with open(character_dict_path, "rb") as fin:
        lines = fin.readlines()
        for line in lines:
            line = line.decode('utf-8').strip("\n").strip("\r\n")
            character_str.append(line)
    if use_space_char:
        character_str.append(" ")
    dict_character = list(character_str)
    character_reverse = {}
    for i, char in enumerate(dict_character):
        character_reverse[char] = i
    character = dict_character
    return character, character_reverse

Character, Character_reverse = get_ppocr_dict()


class HouseHoldLayoutLMv3NER:
    def __init__(self, onnx_model_dir, max_length=512) -> None:
        self.tokenizer = AutoTokenizer.from_pretrained(
            # "xlm-roberta-base", 
            "E:/models/huggingface/xlm-roberta-base-tokenizer/",
            use_fast=True, add_prefix_space=True)
        self.patch_transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(
                mean=torch.tensor((0.5, 0.5, 0.5)),
                std=torch.tensor((0.5, 0.5, 0.5)))
            ])
        # add special tokens
        self.max_len = max_length-2
        self.max_length = max_length
        self.id2label = {
            0: "O",
            1: "B-HEADER",
            2: "I-HEADER",
            3: "B-QUESTION",
            4: "I-QUESTION",
            5: "B-ANSWER",
            6: "I-ANSWER",
        }
        self.session = InferenceSession(onnx_model_dir)    
    
    def normalize_image(self, img: Image.Image) -> Tuple:
        """
        将图像进行标准化处理，并返回标准化后的图像和原始图像的尺寸

        Args:
        - img: PIL.Image.Image 类型的图像对象

        Returns:
        - img_tensor: 标准化后的图像，类型为 numpy.ndarray
        - original_size: 原始图像的尺寸，类型为 Tuple[int, int]
        """        
        assert isinstance(img, Image.Image)
        w, h = img.size
        img_resize = img.resize((224, 224))
        img_tensor = self.patch_transform(img_resize)
        return img_tensor.numpy(), (w, h)

    def normalize_bbox(self, bbox: List[List[float]], width: int, height: int, SCALED_SIZE: int = 1000) -> List[List[float]]:
        """
        将边界框进行标准化处理，并返回标准化后的边界框

        Args:
        - bbox: 边界框列表，每个边界框为一个元素，包含四个浮点型数值，依次表示左上角的 x、y 坐标和右下角的 x、y 坐标
        - width: 原始图像宽度
        - height: 原始图像高度
        - SCALED_SIZE: 缩放后的图像大小，默认为 1000

        Returns:
        - normal_bbox: 标准化后的边界框列表，每个边界框为一个元素，包含四个浮点型数值，依次表示左上角的 x、y 坐标和右下角的 x、y 坐标
        """
        normal_bbox = []
        for box in bbox:
            x0, y0, x1, y1 = box   
            x0 = min(max(x0 / width * SCALED_SIZE , 0), SCALED_SIZE)
            y0 = min(max(y0 / height * SCALED_SIZE, 0), SCALED_SIZE)
            x1 = min(max(x1 / width * SCALED_SIZE , 0), SCALED_SIZE)
            y1 = min(max(y1 / height * SCALED_SIZE, 0), SCALED_SIZE)        
            # 检查边界框坐标是否合法
            assert x1 >= x0, "边界框坐标不合法"
            assert y1 >= y0, "边界框坐标不合法"
            normal_bbox.append([x0, y0, x1, y1])
        return normal_bbox
    
    def unnormalize_box(self, bbox: List[float], width: int, height: int) -> List[float]:
        """
        将标准化后的边界框坐标进行反标准化处理，并返回反标准化后的边界框坐标

        Args:
        - bbox: 标准化后的边界框坐标，包含四个浮点型数值，依次表示左上角的 x、y 坐标和右下角的 x、y 坐标
        - width: 原始图像宽度
        - height: 原始图像高度

        Returns:
        - unnormal_bbox: 反标准化后的边界框坐标，包含四个浮点型数值，依次表示左上角的 x、y 坐标和右下角的 x、y 坐标
        """        
        return [
            width * (bbox[0] / 1000),
            height * (bbox[1] / 1000),
            width * (bbox[2] / 1000),
            height * (bbox[3] / 1000),
        ]

    def convert_rect_bbox(self, bbox):
        """
        将四边形边界框转换为矩形边界框，并返回转换后的边界框

        Args:
        - bbox: 四边形边界框列表，每个边界框为一个元素，包含八个浮点型数值，依次表示四个顶点的 x、y 坐标

        Returns:
        - converted_bbox: 矩形边界框列表，每个边界框为一个元素，包含四个浮点型数值，依次表示左上角的 x、y 坐标和右下角的 x、y 坐标
        """        
        converted_bbox = []
        for box in bbox:
            xmin = min(box[0], box[2], box[4], box[6])
            ymin = min(box[1], box[3], box[5], box[7])
            xmax = max(box[0], box[2], box[4], box[6])
            ymax = max(box[1], box[3], box[5], box[7])
            converted_bbox.append([xmin, ymin, xmax, ymax])
        return converted_bbox

    def generate_chunks(self, p_text, p_rect_boxes, points_indexs):
        """
        将文本和边界框拆分成多个块，每个块的最大长度为 max_len，返回拆分后的块列表

        Args:
        - p_text: 文本列表，每个元素为一个字符串，表示一行文本
        - p_rect_boxes: 边界框列表，每个元素为一个列表，其中每个元素为一个浮点型数值，依次表示四个顶点的 x、y 坐标
        - points_indexs: 边界框对应的文本中的起始字符位置

        Returns:
        - chunk_input_ids: 拆分后的文本块列表，每个元素为一个列表，其中包含多个整型数值，表示每个词汇的 ID
        - chunk_bboxs: 拆分后的边界框块列表，每个元素为一个列表，其中每个元素为一个浮点型数值，依次表示左上角的 x、y 坐标和右下角的 x、y 坐标
        - chunk_points_indexs: 拆分后的边界框块对应的文本中的起始字符位置列表，每个元素为一个整型数值
        """        
        chunk_input_ids, chunk_bboxs, chunk_points_indexs = [], [], []
        for line, bbox, point_ind in zip(p_text, p_rect_boxes, points_indexs):
            input_ids = self.tokenizer(
                line.strip(), truncation=False, add_special_tokens=False,
                return_attention_mask=False)["input_ids"]
            if not input_ids:
                continue
            if len(input_ids) + len(chunk_input_ids) > self.max_len:
                yield chunk_input_ids, chunk_bboxs, chunk_points_indexs
                chunk_input_ids, chunk_bboxs, chunk_points_indexs = [], [], []
            chunk_input_ids += input_ids
            chunk_bboxs += [bbox] * len(input_ids)
            chunk_points_indexs += [point_ind] * len(input_ids)

        if chunk_input_ids:
            yield chunk_input_ids, chunk_bboxs, chunk_points_indexs

    def collate_batch(self, features):
        """
        对数据集中的多个样本进行批量处理，返回处理后的批量数据

        Args:
        - features: 样本列表，每个样本为一个字典，包含图像像素值、文本词汇 ID、边界框坐标和注意力掩码

        Returns:
        - batch: 批量数据，包含图像像素值、文本词汇 ID、边界框坐标和注意力掩码
        """        
        image_features = features.pop("pixel_values")
        batch = self.tokenizer.pad(
            features,
            padding='max_length',
            max_length=self.max_length,
            pad_to_multiple_of=None,
            return_tensors='np'
        )
        if batch['bbox'].shape[1] < self.max_length:
            add_num = self.max_length - batch['bbox'].shape[1]
            add_bbox = np.array([[[0,0,0,0]] * add_num])
            batch['bbox'] = np.concatenate((batch['bbox'], add_bbox), axis=1)
        
        batch['pixel_values'] = image_features
        for key in ['input_ids', 'bbox', 'attention_mask']:
            batch[key] = batch[key].astype(np.int64)
        return batch

    def add_special_tokens(self, input_ids: List[int], bboxs: List[List[float]], image_feature: np.ndarray) -> Dict[str, np.ndarray]:
        """
        给输入文本添加特殊标记，包括 CLS 和 SEP 标记，并在边界框列表的开头和结尾添加全零和全千的边界框

        Args:
        - input_ids: 输入文本的词汇 ID 列表
        - bboxs: 边界框坐标的列表
        - image_feature: 图像特征的 numpy 数组

        Returns:
        - feature: 包含特殊标记和填充的文本词汇 ID、边界框坐标、注意力掩码和图像特征的字典
        """
        end = min(len(input_ids), 510)
        input_ids_add = [self.tokenizer.cls_token_id] + input_ids[:end] + [self.tokenizer.sep_token_id]
        bboxs_add = [[0,0,0,0]] + bboxs[:end] + [[1000,1000,1000,1000]]
        attention_mask_add = [1] * (end+2)
        feature = {
            'bbox': np.expand_dims(bboxs_add, axis=0),
            'input_ids': np.expand_dims(input_ids_add, axis=0),
            'attention_mask': np.expand_dims(attention_mask_add, axis=0),
            'pixel_values': np.expand_dims(image_feature, axis=0),
        }
        return feature


    def filter_text_with_bbox_width(self, text_list, points_index, bbox_list, w_threshold=100):
        """
        根据边界框宽度阈值过滤文本。

        参数：
        text_list: list，待过滤的文本列表。
        points_index: list，文本对应的点的索引列表。
        bbox_list: list，文本对应的边界框列表。
        w_threshold: int，边界框宽度阈值。

        返回值：
        tuple，包含过滤后的文本列表、点的索引列表和边界框列表。
        """
        bbox_array = np.array(bbox_list)
        bbox_w_array = bbox_array[:, 2] - bbox_array[:, 0]  # 计算边界框的宽度
        mask = bbox_w_array > w_threshold  # 构建布尔掩码
        text_list_filtered = np.array(text_list)[mask]
        points_index_filtered = np.array(points_index)[mask]
        bbox_list_filtered = bbox_array[mask].tolist()
        return text_list_filtered.tolist(), points_index_filtered.tolist(), bbox_list_filtered


    def pre_process(self, image: Image, text_list: List[str], point_list: List[Tuple[float, float, float, float]]) -> Tuple[List[Dict[str, np.ndarray]], List[List[int]], Tuple[int, int]]:
        """
        对输入图像和文本进行预处理，包括图像归一化、边界框坐标归一化、生成特殊标记、批量处理等步骤

        Args:
        - image: 输入图像的 PIL.Image 对象
        - text_list: 输入文本的列表
        - point_list: 输入文本所在的边界框坐标的列表，每个坐标为一个四元组，分别表示左上角和右下角的坐标

        Returns:
        - inputs: 包含特殊标记和填充的文本词汇 ID、边界框坐标、注意力掩码和图像特征的字典的列表
        - point_index: 文本列表中每个元素所在的 chunk 的索引列表
        - (w, h): 图像的宽度和高度
        """
        inputs, point_index = [], []
        assert len(text_list)==len(point_list)
        points_index = list(range(len(point_list)))
        image_feature, (w, h) = self.normalize_image(image)
        bbox_list_convert = self.convert_rect_bbox(point_list)
        # Filter text_lines that are too long
        text_list, points_index, bbox_list_convert = self.filter_text_with_bbox_width(text_list, points_index, bbox_list_convert, w_threshold=100)

        bbox_list = self.normalize_bbox(bbox_list_convert, w, h)
        for chunk_input_ids, chunk_bboxs, chunk_points_indexs in self.generate_chunks(text_list, bbox_list, points_index):
            chunk_points_indexs.insert(0, -1)
            point_index.append(chunk_points_indexs)
            features = self.add_special_tokens(chunk_input_ids, chunk_bboxs, image_feature)
            input_features = self.collate_batch(features)
            inputs.append(input_features)
        return inputs, point_index,  (w, h)
    
    def do_inference(self, inputs):
        return self.session.run(output_names=['logits'], input_feed=dict(inputs))

    def filter_by_attention_mask(self, mask: np.ndarray, *arrays: np.ndarray) -> Tuple[np.ndarray, ...]:
        """
        根据注意力掩码过滤出有效部分的数据

        Args:
        - mask: 注意力掩码的 numpy 数组，用于指示哪些数据是有效的
        - *arrays: 任意数量的 numpy 数组，需要和 mask 的维度相同

        Returns:
        - 一个元组，其中包含了在 mask 中为真的位置上，所有输入的 numpy 数组相应位置上的元素
        """
        return tuple(array[mask > 0] for array in arrays)

    def extract_entities(self, labels: List[str], *arrays: List) -> Tuple[List, ...]:
        """
        从标签列表中提取实体，并返回实体的列表和标签的列表

        Args:
        - labels: 标签列表，需要和 arrays 的维度相同
        - *arrays: 任意数量的列表，需要和 labels 的维度相同

        Returns:
        - 一个元组，其中包含了所有实体的列表和标签的列表
        """        
        final_results = [list() for _ in range(len(arrays) + 1)]
        end = -1
        
        for ind, label in enumerate(labels):
            if ind < end:
                continue
            if label == "O":
                continue
                
            s0, tag = label.split("-")
            if s0 == "I":
                continue
            
            end = ind + 1
            while end < len(labels) and labels[end] == 'I-' + tag:
                end += 1

            for i, array in enumerate(arrays):
                final_results[i].append(array[ind:end])
            final_results[-1].append(tag)
        
        return tuple(final_results)

    def post_process(
                    self,
                    inputs: dict, 
                    points_ind: List[int], 
                    predict_labels: np.ndarray, 
                    predict_scores: np.ndarray, 
                    width: int, 
                    height: int) -> Tuple[List[str], List[List[float]], List[int], List[str], List[float]]:
        """
        对模型的输出进行后处理，返回预测的文本、边界框、点索引、标签和得分

        Args:
        - inputs: 输入数据的字典，包含 input_ids、bbox 和 attention_mask 字段
        - points_ind: ppocr输出4个点bbox坐标的索引列表
        - predict_labels: 模型预测的标签数组
        - predict_scores: 模型预测的得分数组
        - width: 图像的宽度
        - height: 图像的高度

        Returns:
        - 一个元组，其中包含了预测的文本、边界框、点索引、标签和得分
        """        
        final_predict_texts, final_predict_bboxs, final_points_ind = [], [], []
        final_predict_scores, final_predict_labels = [], []

        input_ids, bbox, attention_mask, predict_labels, predict_scores = (
            inputs['input_ids'].squeeze(),
            inputs['bbox'].squeeze(),
            inputs['attention_mask'].squeeze(),
            predict_labels.squeeze(),
            predict_scores.squeeze()
        )
        input_ids, bbox, predict_scores, predict_labels = self.filter_by_attention_mask(
            attention_mask, input_ids, bbox, predict_scores, predict_labels
        )
        predict_labels = [self.id2label[pred] for pred in predict_labels]

        text_chunks, bbox_chunks, point_ind_chunks, score_chunks, label_tags = self.extract_entities(
            predict_labels, input_ids, bbox, points_ind, predict_scores
        )
        for text_chunk, bbox_chunk, point_ind_chunk, score_chunk, label_tag in zip(
            text_chunks, bbox_chunks, point_ind_chunks, score_chunks, label_tags
        ):
            decode_text = self.tokenizer.decode(text_chunk)
            if decode_text:
                final_predict_texts.append([Character_reverse[x] for x in decode_text])
                final_predict_texts.append(decode_text)
                final_predict_bboxs.append(self.unnormalize_box(bbox_chunk[0], width, height))
                final_points_ind.append(point_ind_chunk[0])
                final_predict_scores.append(score_chunk.mean())
                final_predict_labels.append(label_tag)
        return final_predict_texts, final_predict_bboxs, final_points_ind, final_predict_labels, final_predict_scores

    def run(self, image, text_list, point_list):
        """
        运行模型，返回预测的文本、边界框、坐标、标签和得分

        Args:
        - image: 输入的图像
        - text_list: 包含文本的列表
        - point_list: 包含点坐标的列表

        Returns:
        - 一个元组，其中包含了预测的文本、边界框、点坐标、标签和得分
        """
        final_predict_texts, final_predict_bboxs, final_points, final_predict_labels, final_predict_scores = [], [], [], [], []
        inputs, point_index, (w, h) = self.pre_process(image, text_list, point_list)
        for i in range(len(inputs)):
            pred_tensor_logist = self.do_inference(inputs=inputs[i])[0]
            pred_tensor_softmax = torch.softmax(torch.tensor(pred_tensor_logist), dim=-1).numpy()
            pred = pred_tensor_logist.argmax(-1)
            prob = pred_tensor_softmax.max(-1)
            final_predict_text, final_predict_bbox, final_points_ind, final_predict_label, final_predict_score = self.post_process(inputs[i], point_index[i], pred, prob, w, h)
            final_predict_texts += final_predict_text
            final_point = [point_list[p_ind] for p_ind in final_points_ind]
            final_points += final_point            
            final_predict_bboxs += final_predict_bbox
            final_predict_labels += final_predict_label
            final_predict_scores += final_predict_score
        return final_predict_texts, final_predict_bboxs, final_points, final_predict_labels, final_predict_scores


def demo_for_layout():


    from PIL import Image, ImageDraw, ImageFont
    import moyan

    det_model_dir = r"E:\models\PaddleOCR\ch_PP-OCRv3_xx_16.2M\inference_model\ch_PP-OCRv3_det_infer"
    cls_model_dir = r"E:\models\PaddleOCR\ch_PP-OCRv3_xx_16.2M\inference_model\ch_ppocr_mobile_v2.0_cls_infer"
    rec_model_dir = r"E:\models\PaddleOCR\ch_PP-OCRv3_xx_16.2M\inference_model\ch_PP-OCRv3_rec_infer"
    rec_label_file = r"E:\models\PaddleOCR\ch_PP-OCRv3_xx_16.2M\ppocr_keys_v1.txt"
    # det_model_dir = "/mnt/e/models/PaddleOCR/ch_PP-OCRv3_xx_16.2M/inference_model/ch_PP-OCRv3_det_infer"
    # cls_model_dir = "/mnt/e/models/PaddleOCR/ch_PP-OCRv3_xx_16.2M/inference_model/ch_ppocr_mobile_v2.0_cls_infer"
    # rec_model_dir = "/mnt/e/models/PaddleOCR/ch_PP-OCRv3_xx_16.2M/inference_model/ch_PP-OCRv3_rec_infer"
    # rec_label_file = "/mnt/e/models/PaddleOCR/ch_PP-OCRv3_xx_16.2M/ppocr_keys_v1.txt"

    model = PPOCRv3(det_model_dir, cls_model_dir, rec_model_dir, rec_label_file)


    img_path = "doc.jpg"  # zh_val_1  household doc
    im = cv2.imread(img_path)
    results = model.run(im)
    p_point_boxes, p_text, p_rec_scores = results["boxes"], results["text"], results["rec_scores"] 
    
    
    image = Image.open(img_path)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("./simsun.ttc", 20, encoding="utf-8")
    label2color = {'question':'blue', 'answer':'green', 'header':'orange', 'other':'violet'}

    # onnx_model_dir = r"D:\Code\sunc\ner_pytorch_moyan\onnx\model.onnx"
    onnx_model_dir = "../../PaddleOCR_TRT_SERVER/server/model_repository/layoutlmv3_2_inference/1/model_fp16.onnx"
    model = HouseHoldLayoutLMv3NER(onnx_model_dir=onnx_model_dir)

    # predict_txts, predict_bboxs, predict_labels = model.run(image, p_text, p_point_boxes)
    predict_txts, predict_bboxs, p_points,  predict_labels, p_rec_scores = model.run(image, p_text, p_point_boxes)

    for text, bbox, label, p_point in zip(predict_txts, predict_bboxs, predict_labels, p_points):
        print(text, bbox, label)
        # draw.rectangle(list(bbox), outline=label2color[label.lower()])
        draw.polygon(p_point, outline=label2color[label.lower()])
        draw.text((bbox[0] + 10, bbox[1] - 10), text=label.lower()+"    "+text, fill=label2color[label.lower()], font=font)
    image.save("drawv1.png")





def main():
    demo_for_layout()
    
if __name__ == '__main__':
    main()