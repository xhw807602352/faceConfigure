#! usr/bin/python3
# -*-coding: utf-8-*-
# Author: frankle
# Date: 2019/4/22 20:07
# FileName: week7day1.py
# Software: PyCharm
import cv2
import numpy
import face_recognition
import dlib

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    print(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
    print(int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    # save = cv2.VideoWriter('save.avi', fourcc, cap.get(cv2.CAP_PROP_XI_FRAMERATE), (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
    save = cv2.VideoWriter('save.avi', fourcc, 20.0, (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

    while 1:
        if cap.isOpened():
            ret, frame = cap.read()
            cv2.imshow('face', frame)
            save.write(frame)
            k = cv2.waitKey(1)
            if k == 27:
                cv2.destroyAllWindows()
                break

    cap.release()

