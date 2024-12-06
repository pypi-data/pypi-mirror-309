from onnx import load_model, save_model
from onnxmltools.utils import float16_converter


def main():

    onnx_model_dir = "./outputs/layoutlmv3_xfund_hg_221026/checkpoint-1000/model.onnx"
    onnx_model = load_model(onnx_model_dir)
    trans_model = float16_converter.convert_float_to_float16(onnx_model, keep_io_types=True)
    save_model(trans_model, "model_fp16.onnx")
    
if __name__ == '__main__':
    main()