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
from torchvision import transforms
from transformers import AutoTokenizer
from onnxruntime import InferenceSession

class HouseHoldLayoutLMv3NER:
    def __init__(self, onnx_model_dir, max_length=512) -> None:
        self.tokenizer = AutoTokenizer.from_pretrained(
            "xlm-roberta-base", use_fast=True, add_prefix_space=True)
        self.patch_transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(
                mean=torch.tensor((0.5, 0.5, 0.5)),
                std=torch.tensor((0.5, 0.5, 0.5)))
            ])
        # need add special tokens
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
    
    def normalize_image(self, img):
        assert isinstance(img, Image.Image)
        w, h = img.size
        img_resize = img.resize((224, 224))
        img_tensor = self.patch_transform(img_resize)
        return img_tensor.numpy(), (w, h)

    def normalize_bbox(self, bbox, width, height, SCALED_SIZE=1000):
        normal_bbox = []
        for box in bbox:
            x0, y0, x1, y1 = box   
            x0 = min(max(x0 / width * SCALED_SIZE , 0), SCALED_SIZE)
            y0 = min(max(y0 / height * SCALED_SIZE, 0), SCALED_SIZE)
            x1 = min(max(x1 / width * SCALED_SIZE , 0), SCALED_SIZE)
            y1 = min(max(y1 / height * SCALED_SIZE, 0), SCALED_SIZE)        
            assert x1 >= x0  
            assert y1 >= y0
            normal_bbox.append([x0, y0, x1, y1])
        return normal_bbox
    
    def unnormalize_box(self, bbox, width, height):
        return [
            width * (bbox[0] / 1000),
            height * (bbox[1] / 1000),
            width * (bbox[2] / 1000),
            height * (bbox[3] / 1000),
        ]

    def convert_rect_bbox(self, bbox):
        converted_bbox = []
        for box in bbox:
            xmin = min(box[0], box[2], box[4], box[6])
            ymin = min(box[1], box[3], box[5], box[7])
            xmax = max(box[0], box[2], box[4], box[6])
            ymax = max(box[1], box[3], box[5], box[7])
            converted_bbox.append([xmin, ymin, xmax, ymax])
        return converted_bbox

    def generate_chunks(self, p_text, p_rect_boxes, points_indexs):
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
        image_features = features.pop("pixel_values")
        batch = self.tokenizer.pad(
            features,
            padding='max_length',
            max_length=self.max_length,
            pad_to_multiple_of=None,
            return_tensors=None
        )
        if batch['bbox'].shape[1] < self.max_length:
            add_num = self.max_length - batch['bbox'].shape[1]
            add_bbox = np.array([[[0,0,0,0]] * add_num])
            batch['bbox'] = np.concatenate((batch['bbox'], add_bbox), axis=1)
        batch['pixel_values'] = image_features
        for key in ['input_ids', 'bbox', 'attention_mask']:
            batch[key] = batch[key].astype(np.int64)
        return batch

    def add_special_tokens(self, input_ids, bboxs, image_feature):
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

    def pre_process(self, image, text_list, point_list):
        inputs, point_index = [], []
        assert len(text_list)==len(point_list)
        points_index = list(range(len(point_list)))
        image_feature, (w, h) = self.normalize_image(image)
        bbox_list = self.normalize_bbox(self.convert_rect_bbox(point_list), w, h)
        for chunk_input_ids, chunk_bboxs, chunk_points_indexs in self.generate_chunks(text_list, bbox_list, points_index):
            print(len(chunk_input_ids))
            chunk_points_indexs.insert(0, -1)
            point_index.append(chunk_points_indexs)
            features = self.add_special_tokens(chunk_input_ids, chunk_bboxs, image_feature)
            input_features = self.collate_batch(features)
            inputs.append(input_features)
        return inputs, point_index,  (w, h)
    
    def do_inference(self, inputs):
        return self.session.run(output_names=['logits'], input_feed=dict(inputs))

    def post_process(self, inputs:dict, points_ind:list, predict_labels:np.ndarray, predict_scores:np.ndarray, width:int, height:int):
        final_predict_texts, final_predict_bboxs, final_points_ind, final_predict_labels, final_predict_scores = [], [], [], [], []
        input_ids = inputs['input_ids'].squeeze()
        bbox = inputs['bbox'].squeeze()
        attention_mask = inputs['attention_mask'].squeeze()
        predict_labels = predict_labels.squeeze()
        predict_scores = predict_scores.squeeze()

        input_ids = input_ids[attention_mask>0]
        bbox = bbox[attention_mask>0]
        predict_scores = predict_scores[attention_mask>0]
        predict_labels = predict_labels[attention_mask>0]

        predict_labels = [self.id2label[pred] for pred in predict_labels]
        end = -1
        for ind, pred in enumerate(predict_labels):
            if ind < end:
                continue
            if pred == "O":
                continue
            s0, tag = pred.split("-")
            if s0 == "I":
                continue
            else:
                end = ind+1
                while end < len(predict_labels) and predict_labels[end] == 'I-' + tag:
                    end +=1
                
                e_text = self.tokenizer.decode(input_ids[ind:end])
                e_score = predict_scores[ind:end].mean()
                e_bbox = np.unique(bbox[ind:end], axis=0).tolist()
                e_point_ind = np.unique(points_ind[ind:end]).tolist()
                
                if e_text:
                    final_predict_texts.append(e_text)
                    final_predict_labels.append(tag)
                    # TODO return multi bbox 
                    final_predict_bboxs.append(self.unnormalize_box(e_bbox[0], width, height))
                    final_points_ind.append(e_point_ind[0])
                    final_predict_scores.append(e_score)
        return final_predict_texts, final_predict_bboxs, final_points_ind, final_predict_labels, final_predict_scores

    # def post_process(self, input_ids, points_org, predict_labels, predict_scores, width, height):
    #     results = []
    #     input_ids = input_ids['input_ids'].squeeze()
    #     bbox = input_ids['bbox'].squeeze()
    #     attention_mask = input_ids['attention_mask'].squeeze()
    #     predict_labels = predict_labels.squeeze()
    #     predict_scores = predict_scores.squeeze()

    #     for start_idx in range(len(input_ids)):
    #         if attention_mask[start_idx] == 0:
    #             continue
    #         end_idx = start_idx + 1
    #         # 找到一个完整的实体
    #         while end_idx < len(input_ids) and attention_mask[end_idx] == 1 and predict_labels[end_idx].startswith('I-'):
    #             end_idx += 1

    #         entity_text = self.tokenizer.decode(input_ids[start_idx:end_idx])
    #         entity_label = predict_labels[start_idx].split('-')[1]
    #         entity_score = predict_scores[start_idx:end_idx].mean()
    #         entity_bbox = self.unnormalize_box(bbox[start_idx], width, height)
    #         entity_points = points_org[start_idx]
            
    #         results.append({
    #             'text': entity_text,
    #             'label': entity_label,
    #             'score': entity_score,
    #             'bbox': entity_bbox,
    #             'points': entity_points
    #         })
    #     return results

    def run(self, image, text_list, point_list):
        final_predict_texts, final_predict_bboxs, final_points, final_predict_labels, final_predict_scores = [], [], [], [], []
        inputs, point_index, (w, h) = self.pre_process(image, text_list, point_list)
        for i in range(len(inputs)):
            pred_tensor_logist = self.do_inference(inputs=inputs[i])[0]
            pred_tensor_softmax = torch.softmax(torch.tensor(pred_tensor_logist), dim=-1).numpy()
            pred = pred_tensor_logist.argmax(-1)
            prob = pred_tensor_softmax.max(-1)
            final_predict_text, final_predict_bbox, final_points_ind, final_predict_label, final_predict_score = self.post_process(inputs[i], point_index[i], pred, prob, w, h)
            print(len(final_points_ind), final_points_ind)
            # 14 [0, 17, 17, 17, 19, 22, 24, 39, 43, 43, 45, 46, 48, 51]
            # 14 [55, 56, 57, 58, 60, 69, 80, 81, 86, 110, 112, 118, 126, 127]

            final_predict_texts += final_predict_text
            final_point = [point_list[p_ind] for p_ind in final_points_ind]
            final_points += final_point            
            final_predict_bboxs += final_predict_bbox
            final_predict_labels += final_predict_label
            final_predict_scores += final_predict_score
        return final_predict_texts, final_predict_bboxs, final_points, final_predict_labels, final_predict_scores



# cls_dlpack_tensor = cls_pre_tensors[0].to_dlpack()
# cls_input_tensor = pb_utils.Tensor.from_dlpack("x", cls_dlpack_tensor)
# inference_request = pb_utils.InferenceRequest(
#     model_name='cls_pp',
#     requested_output_names=['cls_labels', 'cls_scores'],
#     inputs=[cls_input_tensor])
# inference_response = inference_request.exec()

# if inference_response.has_error():
#     raise pb_utils.TritonModelException(
#         inference_response.error().message())
# else:
#     # Extract the output tensors from the inference response.
#     cls_labels = pb_utils.get_output_tensor_by_name(
#         inference_response, 'cls_labels')
#     cls_labels = cls_labels.as_numpy()

#     cls_scores = pb_utils.get_output_tensor_by_name(
#         inference_response, 'cls_scores')
#     cls_scores = cls_scores.as_numpy()





# rec_dlpack_tensor = rec_pre_tensors[0].to_dlpack()
# rec_input_tensor = pb_utils.Tensor.from_dlpack("x", rec_dlpack_tensor)
# inference_request = pb_utils.InferenceRequest(
#     model_name='rec_pp',
#     requested_output_names=['rec_texts', 'rec_scores'],
#     inputs=[rec_input_tensor])
# inference_response = inference_request.exec()
# if inference_response.has_error():
#     raise pb_utils.TritonModelException(
#         inference_response.error().message())
# else:
#     # Extract the output tensors from the inference response.
#     rec_texts = pb_utils.get_output_tensor_by_name(
#         inference_response, 'rec_texts')
#     rec_texts = rec_texts.as_numpy()

#     rec_scores = pb_utils.get_output_tensor_by_name(
#         inference_response, 'rec_scores')
#     rec_scores = rec_scores.as_numpy()

#     # batch_rec_texts.append(rec_texts)
#     # batch_rec_scores.append(rec_scores)

#     b_batch_rec_texts = np.append(b_batch_rec_texts, rec_texts)
#     b_batch_rec_scores = np.append(b_batch_rec_scores, rec_scores)








def demo_for_layout():


    from PIL import Image, ImageDraw, ImageFont
    import moyan


    det_model_dir = r"E:\models\PaddleOCR\ch_PP-OCRv3_xx_16.2M\inference_model\ch_PP-OCRv3_det_infer"
    cls_model_dir = r"E:\models\PaddleOCR\ch_PP-OCRv3_xx_16.2M\inference_model\ch_ppocr_mobile_v2.0_cls_infer"
    rec_model_dir = r"E:\models\PaddleOCR\ch_PP-OCRv3_xx_16.2M\inference_model\ch_PP-OCRv3_rec_infer"
    rec_label_file = r"E:\models\PaddleOCR\ch_PP-OCRv3_xx_16.2M\ppocr_keys_v1.txt"
    model = PPOCRv3(det_model_dir, cls_model_dir, rec_model_dir, rec_label_file)


    img_path = "zh_val_1.jpg"
    # img_path = "household.jpg"
    im = cv2.imread(img_path)
    results = model.run(im)
    p_point_boxes, p_text, p_rec_scores = results["boxes"], results["text"], results["rec_scores"] 
    
    
    image = Image.open(img_path)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(r"C:\Users\ice_m\simsun.ttc", 20, encoding="utf-8")
    label2color = {'question':'blue', 'answer':'green', 'header':'orange', 'other':'violet'}

    onnx_model_dir = r"D:\Code\sunc\ner_pytorch_moyan\onnx\model.onnx"
    model = HouseHoldLayoutLMv3NER(onnx_model_dir=onnx_model_dir)

    # predict_txts, predict_bboxs, predict_labels = model.run(image, p_text, p_point_boxes)
    predict_txts, predict_bboxs, p_points,  predict_labels, p_rec_scores = model.run(image, p_text, p_point_boxes)

    for text, bbox, label, p_point in zip(predict_txts, predict_bboxs, predict_labels, p_points):
        print(text, bbox, label)
        # draw.rectangle(list(bbox), outline=label2color[label.lower()])
        draw.polygon(p_point, outline=label2color[label.lower()])
        draw.text((bbox[0] + 10, bbox[1] - 10), text=label.lower()+"    "+text, fill=label2color[label.lower()], font=font)
    image.save("drawv2.png")


def main():
    demo_for_layout()
    
if __name__ == '__main__':
    main()