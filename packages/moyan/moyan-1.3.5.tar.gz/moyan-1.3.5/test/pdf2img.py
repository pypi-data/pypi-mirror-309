import fitz
import os
import moyan

'''
    pip install fitz 
    pip install pymupdf==1.18.14
'''

def mkdir(path):
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
    else:
        pass


def pdf_image(pdfPath, save_dir, zoom_x, zoom_y, rotation_angle):
    """
    :param pdfPath: pdf文件的路径
    :param save_dir: 图像要保存的文件夹
    :param zoom_x: x方向的缩放系数
    :param zoom_y: y方向的缩放系数
    :param rotation_angle: 旋转角度
    :return: None
    """

    names = os.path.basename(pdfPath)
    name, stuffix = os.path.splitext(names)

    # 打开PDF文件
    pdf = fitz.open(pdfPath)

    # 逐页读取PDF
    for pg in range(0, pdf.pageCount):
        page = pdf[pg]
        # 设置缩放和旋转系数
        trans = fitz.Matrix(zoom_x, zoom_y).preRotate(rotation_angle)
        pm = page.getPixmap(matrix=trans, alpha=False)
        save_path = os.path.join(save_dir, name+f"_{pg+1}.jpg")
        pm.writePNG(save_path)
    pdf.close()


# pdf_image(r"pdfs/01.pdf", r"images/", 10, 10, 0)

file_dir = r'C:\Users\ice_m\Desktop\体检报告\pdf'

save_dir = r'C:\Users\ice_m\Desktop\体检报告_save'
moyan.pathExit(save_dir)

file_list = moyan.walkDir2List(file_dir, filter_postfix=[".pdf"])

for file_name in file_list:
    pdf_path = os.path.join(file_dir, file_name)
    pdf_image(pdf_path, save_dir, 5, 5, 0)

