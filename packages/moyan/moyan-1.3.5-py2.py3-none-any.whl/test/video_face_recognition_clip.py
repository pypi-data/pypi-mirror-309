#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   video_face_recognition_clip.py
@Time    :   2023/12/20 09:42:37
@Author  :   moyan 
@Contact :   ice_moyan@163.com
'''
import os
import cv2
import dlib
import face_recognition
import moviepy.editor as mp

def main():

    # 加载需要跟踪的人脸图像
    target_face_path = "/mnt/e/DataSet/Avater_data/xwlb/known_id/01.png"
    target_image = face_recognition.load_image_file(target_face_path)
    target_face_encoding = face_recognition.face_encodings(target_image)[0]

    video_path = "/mnt/e/DataSet/Avater_data/xwlb/1080p/0a1a2bafde91c0b13799011432685484.mp4"
    video = cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
   
    # tracker = cv2.TrackerKCF_create()
    
    # 初始化跟踪器
    tracker = dlib.correlation_tracker()

    # 初始化目标人脸编码
    target_encoding = None
    
    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame, model="cnn")
        # face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left)  in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), thickness=2)
            # cv2.putText(frame, name, (left+6, bottom-6), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        # 显示图像
        cv2.imshow("Video", frame)
        
        # 按下 'q' 键退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break       



    video.release()
    cv2.destroyAllWindows()

if __name__=='__main__':
    main()
