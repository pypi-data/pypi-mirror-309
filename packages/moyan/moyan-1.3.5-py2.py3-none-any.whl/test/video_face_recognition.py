#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   video_face_recognition.py
@Time    :   2023/12/19 16:57:56
@Author  :   moyan 
@Contact :   ice_moyan@163.com
'''
import os
import cv2
import moyan
import numpy as np
import face_recognition


import cv2

def get_frame_from_video(video_path, frame_index):
    # 打开视频文件
    video = cv2.VideoCapture(video_path)

    # 逐帧读取视频直到目标帧
    current_frame_index = 0
    while current_frame_index < frame_index:
        ret, frame = video.read()
        if not ret:
            # 视频读取结束或出现错误
            break
        current_frame_index += 1

    # 检查是否成功读取到目标帧
    if current_frame_index == frame_index:
        # 在这里可以对获取到的帧进行进一步处理，例如保存为图像文件或返回图像
        return frame

    # 关闭视频文件
    video.release()

    # 如果未成功读取到目标帧，则返回None
    return None


def main():
    
    known_face_dir = "/mnt/e/DataSet/Avater_data/xwlb/known_id/"
    known_face_encodings = []
    known_face_names = []

    for file_names in os.listdir(known_face_dir):
        name = os.path.splitext(file_names)[0]
        img_path = os.path.join(known_face_dir, file_names)
        assert os.path.exists(img_path), f"{img_path} not exist!"
        image = face_recognition.load_image_file(img_path)
        # face_locations = face_recognition.face_locations(image)
        # print(face_locations)
        # encoding = face_recognition.face_encodings(image, face_locations)[0]
        encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(encoding)
        known_face_names.append(name)
    

    video_dir = "/mnt/e/DataSet/Avater_data/xwlb/1080p/"
    video_list = moyan.walkDir2List(video_dir, filter_postfix=[".mp4"])


    for ind, names in enumerate(video_list):
        print(f"loading {ind}, {names}")
        video_path = os.path.join(video_dir, names)
        assert os.path.exists(video_path), f"{video_path} not exist!"
        frame = get_frame_from_video(video_path, frame_index=120)
        if frame is not None:
            # cv2.imwrite(f"{names}_frame_120.png", frame)

            # rgb_frame = frame[:,:,::-1]
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # rgb_frame = np.ascontiguousarray(frame[:, :, ::-1])
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)


            for (top, right, bottom, left), face_encoding  in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.38) # 0.38
                name = "Unknown"
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), thickness=2)
            cv2.putText(frame, name, (left+6, bottom-6), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imwrite(f"{names}_frame_120.png", frame)

        # cv2.imshow(f"video_{name}", frame)

        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

if __name__=='__main__':
    main()
