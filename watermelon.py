import cv2
import numpy as np

# 人脸分类器
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')  

# 眼睛分类器 
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')  

# 读取视频
video = cv2.VideoCapture('input_video.mp4')  

# 获取视频尺寸
size = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), 
        int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))

# 定义mask    
mask = np.zeros(size, dtype=np.uint8)  

# 视频编辑器
video_editor = cv2.VideoWriter('output_video.avi',  
                               cv2.VideoWriter_fourcc(*'XVID'), 
                               30, size) 

while True:
    ret, frame = video.read()  
    if ret == False: 
        break  
    
    # 人脸检测        
    faces = face_cascade.detectMultiScale(frame, 1.1, 4)  
    
    # 对每张人脸,检测眼睛,并计算嘴部位置
    for face in faces: 
        x, y, w, h = face  
        
        # 检测眼睛
        eyes = eye_cascade.detectMultiScale(frame[y:y+h, x:x+w]) 
        
        # 计算嘴部位置,人脸的2/3位置
        mouth_y = int(y + h * 2 / 3)  
        
        # 在mask中画出人脸区域,眼睛和嘴部,其他部分设置为黑
        cv2.rectangle(mask, (x, y), (x+w, y+h), 255, -1) 
        for ex, ey, ew, eh in eyes:
            cv2.rectangle(mask, (x+ex, y+ey), (x+ex+ew, y+ey+eh), 255, -1)
        cv2.rectangle(mask, (x, mouth_y), (x+w, mouth_y + 10), 255, -1)
        
        # 将frame中的人脸区域外的部分设置为透明
        frame = cv2.seamlessClone(np.zeros(frame.shape, frame.dtype),  
                                  frame, mask, (x, y), cv2.NORMAL_CLONE)
        
    # 写入编辑后的帧
    video_editor.write(frame)
    
# 释放资源
video.release() 
video_editor.release()