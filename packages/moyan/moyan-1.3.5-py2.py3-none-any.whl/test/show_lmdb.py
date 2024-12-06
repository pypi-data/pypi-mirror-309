# 可视化lmdb文件

import cv2
import lmdb
import numpy as np


lmdb_file = "E:/DataSet/OCR/gen_idcard_dict3k_600w_moyan_230823/test/"
# lmdb_file = "E:/DataSet/OCR/gen_text_char9k_600w_moyan_230816/test"
env = lmdb.open(lmdb_file, readonly=True, lock=False)
print(env)

with env.begin(write=False) as txn:
    i = 0
    for key, value in txn.cursor():
        '''
        origin-key :  image-000008671
            img-key:   image-000008671
            label-key: label-000008671
        
            get_label = txt.get(label-key.encode())
            get_image = txt.get(img-key.encode())
        '''

        label_key = key.decode('utf-8').replace('image', 'label').encode()
        label = txn.get(label_key).decode('utf-8')


        image_buf = np.frombuffer(value, dtype=np.uint8)     
        # 将数据转换(解码)成图像格式
        # cv2.IMREAD_GRAYSCALE为灰度图，cv2.IMREAD_COLOR为彩色图
        img = cv2.imdecode(image_buf, cv2.IMREAD_COLOR)
        # cv2.imwrite('show.jpg',img)
        print(i, label)
        i+=1


    # # 获取图像数据
    # image_bin = txn.get('image-000004358'.encode())
    # label = txn.get('label-000004358'.encode()).decode()  # 解码

    # # 将二进制文件转为十进制文件（一维数组）
    # image_buf = np.frombuffer(image_bin, dtype=np.uint8)
    
    # # 将数据转换(解码)成图像格式
    # # cv2.IMREAD_GRAYSCALE为灰度图，cv2.IMREAD_COLOR为彩色图
    # img = cv2.imdecode(image_buf, cv2.IMREAD_COLOR)
    # cv2.imwrite('show.jpg',img)
    # print(label)


# import cv2
# import lmdb
# import numpy as np
 
# env = lmdb.open('./data/test/cute80_288')
# txn = env.begin()
 
# for key, value in txn.cursor(): #遍历 
#    key = key.decode('utf-8')
#    value = value.decode('utf-8')
#    with open('ct80_crop/'+key+'.txt', 'w') as f:
#      f.write(value)

# env.close()