#! usr/bin/python3
# -*-coding: utf-8-*-
# Author: frankle
# Date: 2019/4/23 21:06
# FileName: test.py
# Software: PyCharm
from PIL import ImageDraw, Image
import face_recognition as fr
import numpy as np
import cv2

def loadnpArray(filename):
    return np.loadtxt(filename)

def savenpArray(tofile,npArray):
        np.savetxt(tofile, npArray)


facelib = loadnpArray('face.txt')
print(facelib)
reader = cv2.VideoCapture('save1.avi')
w = int(reader.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(reader.get(cv2.CAP_PROP_FRAME_HEIGHT))


while 1:
    ret, frame = reader.read()
    if ret:
        # gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        # small_gray = cv2.resize(gray, (160, 120), interpolation=2)
        small_frame = cv2.resize(frame, (160, 120), interpolation=2)
        location = fr.api.face_locations(small_frame)
        for loction in location:
            top, right, bottom, left = loction
            # head = frame[top:bottom, left:right]
            now = fr.api.face_encodings(small_frame, [loction])[0]
            cv2.rectangle(frame, (left*w//160, top*w//160), (right*h//120, bottom*h//120), (0, 255, 255), thickness=2)
            # cv2.imshow('ss', head)
            # fr.api.compare_faces(0,now)
        else:
            cv2.imshow('sss', frame)
        k = cv2.waitKey(1)
        if k == 27:
            break
        elif k == ord('s'):
            if len(now):
                savenpArray('face.txt', now)
                break


    else:
        break
cv2.destroyAllWindows()
# def func():
#     cv2.destroyAllWindows()
#     img = fr.api.load_image_file('2.jpg')
#     loction = fr.api.face_locations(img)
#
#     top, right, bottom, left = loction[0]
#     head = img[top:bottom, left:right]
#     pilimg = Image.fromarray(img)
#     pilimg1 = Image.fromarray(head)
#     dr = ImageDraw.Draw(pilimg)
#     dr.rectangle([ right,left, bottom, top], width=5)
#     pilimg.show('123')
#     pilimg1.show('123')
