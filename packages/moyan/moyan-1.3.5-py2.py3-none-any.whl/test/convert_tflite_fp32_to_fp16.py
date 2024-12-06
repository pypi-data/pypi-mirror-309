#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   convert_tflite_fp32_to_fp16.py
@Time    :   2023/08/17 15:33:28
@Author  :   Moyan 
'''
import os
import cv2
import argparse
import numpy as np
import tensorflow as tf

# 您可以通过将权重量化为 float16（16 位浮点数的 IEEE 标准）来缩减浮点模型的大小。要启用权重的 float16 量化，请使用以下步骤：
# float16 量化的优点如下：
# 将模型的大小缩减一半（因为所有权重都变成其原始大小的一半）。
# 实现最小的准确率损失。
# 支持可直接对 float16 数据进行运算的部分委托（例如 GPU 委托），从而使执行速度比 float32 计算更快。
# float16 量化的缺点如下：
# 它不像对定点数学进行量化那样减少那么多延迟。
# 默认情况下，float16 量化模型在 CPU 上运行时会将权重值“反量化”为 float32。（请注意，GPU 委托不会执行此反量化，因为它可以对 float16 数据进行运算。）
def convert_fp16_quantize(pb_file, output_file):
    input_array = ["inputs"]
    output_array = ["Identity"]
    converter = tf.compat.v1.lite.TFLiteConverter.from_frozen_graph(pb_file, input_array, output_array)

    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    converter.target_spec.supported_types = [tf.float16]

    tflite_model = converter.convert()

    with open(output_file, 'wb') as f:
        f.write(tflite_model)

# 动态范围量化, 训练后量化最简单的形式是仅将权重从浮点静态量化为整数（具有 8 位精度）：
# 推断时，权重从 8 位精度转换为浮点，并使用浮点内核进行计算。此转换会完成一次并缓存，以减少延迟。
# 为了进一步改善延迟，“动态范围”算子会根据激活的范围将其动态量化为 8 位，并使用 8 位权重和激活执行计算。
# 此优化提供的延迟接近全定点推断。但是，输出仍使用浮点进行存储，因此使用动态范围算子的加速小于全定点计算。
def convert_dynamic_quantize(pb_file, output_file):
    input_array = ["inputs"]
    output_array = ["Identity"]
    converter = tf.compat.v1.lite.TFLiteConverter.from_frozen_graph(pb_file, input_array, output_array)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    tflite_model = converter.convert()

    with open(output_file, 'wb') as f:
        f.write(tflite_model)

def main():
    model_dir = r"D:\Code\OCR\PaddleOCR\proj_moyan\rec\idcardlite_dict3k_mbv3-largex0.35_none_none_230919\output\infer_best_it28\tflite"
    # model_dir = r'D:\Code\AI-in-air\yolov5-7.0\runs\train-seg\exp\weights'
    pb_file = os.path.join(model_dir, "model_float32.pb")
    # tflite_fp16_path = os.path.join(model_dir, "model_fp16.tflite") 
    # convert_fp16_quantize(pb_file, tflite_fp16_path)
    tflite_dynimic_path = os.path.join(model_dir, "model_dynimic.tflite")
    convert_dynamic_quantize(pb_file, tflite_dynimic_path)

if __name__ == '__main__':
    main()