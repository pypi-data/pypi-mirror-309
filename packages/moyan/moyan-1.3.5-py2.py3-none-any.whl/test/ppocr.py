#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   ppocr.py
@Time    :   2023/06/13 18:24:24
@Author  :   Moyan 
'''
import os
import cv2
import fastdeploy as fd
from memory_profiler import profile

class PPOCRv3:
    def __init__(
            self,
            det_model_dir,
            cls_model_dir,
            rec_model_dir,
            rec_label_file,
            cpu_thread_num=9,
            backend="default"
        ) -> None:
        runtime_option = fd.RuntimeOption()
        runtime_option.set_cpu_thread_num(cpu_thread_num)
        cls_batch_size = 1
        rec_batch_size = 6
        det_model_file = os.path.join(det_model_dir, "inference.pdmodel")
        det_params_file = os.path.join(det_model_dir, "inference.pdiparams")
        cls_model_file = os.path.join(cls_model_dir, "inference.pdmodel")
        cls_params_file = os.path.join(cls_model_dir, "inference.pdiparams")
        rec_model_file = os.path.join(rec_model_dir, "inference.pdmodel")
        rec_params_file = os.path.join(rec_model_dir, "inference.pdiparams")

        det_option = runtime_option
        det_option.set_trt_input_shape("x", [1, 3, 64, 64], [1, 3, 640, 640], [1, 3, 960, 960])
        self.det_model = fd.vision.ocr.DBDetector(det_model_file, det_params_file, runtime_option=det_option)
        self.det_model.det_db_unclip_ratio = 2.0

        cls_option = runtime_option
        cls_option.set_trt_input_shape("x", [1, 3, 48, 10], [cls_batch_size, 3, 48, 320], [cls_batch_size, 3, 48, 1024])
        self.cls_model = fd.vision.ocr.Classifier(cls_model_file, cls_params_file, runtime_option=cls_option)

        rec_option = runtime_option
        rec_option.set_trt_input_shape("x", [1, 3, 48, 10], [rec_batch_size, 3, 48, 320], [rec_batch_size, 3, 48, 1024])
        self.rec_model = fd.vision.ocr.Recognizer(rec_model_file, rec_params_file, rec_label_file, runtime_option=rec_option)

        self.ppocr_v3 = fd.vision.ocr.PPOCRv3(det_model=self.det_model, cls_model=self.cls_model, rec_model=self.rec_model)
        self.ppocr_v3.cls_batch_size = cls_batch_size
        self.ppocr_v3.rec_batch_size = rec_batch_size
    
    # @profile
    # def run(self, im):
    #     return self.ppocr_v3.predict(im)



    def run(self, im):
    
        results = {}
        
        outputs = self.ppocr_v3.predict(im)


        # vis_im = fd.vision.vis_ppocr(im, outputs)
        # cv2.imwrite("vis.jpg", vis_im)

        results["boxes"] = outputs.boxes
        results["text"] = outputs.text
        results["rec_scores"] = outputs.rec_scores
        del outputs
        return results


def demo_one_img():
    
    det_model_dir = r"E:\models\PaddleOCR\ch_PP-OCRv3_xx_16.2M\inference_model\ch_PP-OCRv3_det_infer"
    cls_model_dir = r"E:\models\PaddleOCR\ch_PP-OCRv3_xx_16.2M\inference_model\ch_ppocr_mobile_v2.0_cls_infer"
    rec_model_dir = r"E:\models\PaddleOCR\ch_PP-OCRv3_xx_16.2M\inference_model\ch_PP-OCRv3_rec_infer"
    rec_label_file = r"E:\models\PaddleOCR\ch_PP-OCRv3_xx_16.2M\ppocr_keys_v1.txt"
    model = PPOCRv3(det_model_dir, cls_model_dir, rec_model_dir, rec_label_file)

    img_path = "zh_val_1.jpg"
    im = cv2.imread(img_path)
    results = model.run(im)
    # print(results)


def demo_for_batch():


    det_model_dir = r"E:\models\PaddleOCR\ch_PP-OCRv3_xx_16.2M\inference_model\ch_PP-OCRv3_det_infer"
    cls_model_dir = r"E:\models\PaddleOCR\ch_PP-OCRv3_xx_16.2M\inference_model\ch_ppocr_mobile_v2.0_cls_infer"
    rec_model_dir = r"E:\models\PaddleOCR\ch_PP-OCRv3_xx_16.2M\inference_model\ch_PP-OCRv3_rec_infer"
    rec_label_file = r"E:\models\PaddleOCR\ch_PP-OCRv3_xx_16.2M\ppocr_keys_v1.txt"
    
    model = PPOCRv3(det_model_dir, cls_model_dir, rec_model_dir, rec_label_file)

    img_dir = r"E:\DataSet\XFUND\images"
    img_list = os.listdir(img_dir)
    for ind, names in enumerate(img_list):
        print(f"loading images %s" % names)
        img_path = os.path.join(img_dir, names)
        assert os.path.exists(img_path), f"{img_path} not found!"
        im = cv2.imread(img_path)
        results = model.run(im)
        # print(results)
        




def demo_for_test():

    import psutil
    det_model_dir = r"E:\models\PaddleOCR\ch_PP-OCRv3_xx_16.2M\inference_model\ch_PP-OCRv3_det_infer"
    cls_model_dir = r"E:\models\PaddleOCR\ch_PP-OCRv3_xx_16.2M\inference_model\ch_ppocr_mobile_v2.0_cls_infer"
    rec_model_dir = r"E:\models\PaddleOCR\ch_PP-OCRv3_xx_16.2M\inference_model\ch_PP-OCRv3_rec_infer"
    rec_label_file = r"E:\models\PaddleOCR\ch_PP-OCRv3_xx_16.2M\ppocr_keys_v1.txt"
    runtime_option = fd.RuntimeOption()
    runtime_option.set_cpu_thread_num(4)
    cls_batch_size = 1
    rec_batch_size = 6
    det_model_file = os.path.join(det_model_dir, "inference.pdmodel")
    det_params_file = os.path.join(det_model_dir, "inference.pdiparams")
    cls_model_file = os.path.join(cls_model_dir, "inference.pdmodel")
    cls_params_file = os.path.join(cls_model_dir, "inference.pdiparams")
    rec_model_file = os.path.join(rec_model_dir, "inference.pdmodel")
    rec_params_file = os.path.join(rec_model_dir, "inference.pdiparams")
    det_option = runtime_option
    det_option.set_trt_input_shape("x", [1, 3, 64, 64], [1, 3, 640, 640], [1, 3, 960, 960])
    det_model = fd.vision.ocr.DBDetector(det_model_file, det_params_file, runtime_option=det_option)
    det_model.det_db_unclip_ratio = 2.0

    cls_option = runtime_option
    cls_option.set_trt_input_shape("x", [1, 3, 48, 10], [cls_batch_size, 3, 48, 320], [cls_batch_size, 3, 48, 1024])
    cls_model = fd.vision.ocr.Classifier(cls_model_file, cls_params_file, runtime_option=cls_option)

    rec_option = runtime_option
    rec_option.set_trt_input_shape("x", [1, 3, 48, 10], [rec_batch_size, 3, 48, 320], [rec_batch_size, 3, 48, 1024])
    rec_model = fd.vision.ocr.Recognizer(rec_model_file, rec_params_file, rec_label_file, runtime_option=rec_option)

    ppocr_v3 = fd.vision.ocr.PPOCRv3(det_model=det_model, cls_model=cls_model, rec_model=rec_model)
    ppocr_v3.cls_batch_size = cls_batch_size
    ppocr_v3.rec_batch_size = rec_batch_size


    img_dir = r"E:\DataSet\XFUND\images"
    img_list = os.listdir(img_dir)
    for ind, names in enumerate(img_list):
        print(f"loading images %s" % names)
        img_path = os.path.join(img_dir, names)
        assert os.path.exists(img_path), f"{img_path} not found!"
        im = cv2.imread(img_path)
        results = ppocr_v3.predict(im)
        print(results)
        print(u'当前进程的内存使用：%.4f GB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024 / 1024) )


def main():

    # demo_one_img() 
    # demo_for_layout()
    # demo_for_batch()
    demo_for_test()


    
if __name__ == '__main__':
    main()