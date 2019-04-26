#! usr/bin/python3
# Author:Frankle
# -*-coding:utf-8-*-
# @Time:2019/4/25.11:42
# @site:
# @name:qtTest.py
# @software:PyCharm
from face import *
import sys
from PyQt5.QtWidgets import (QWidget, QToolTip,QMainWindow,
    QPushButton, QApplication)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
import cv2
import face_recognition as fr
import time
import numpy as np

def facelib(face):
    tmp = []
    for i in face:
        tmp.append(fr.face_encodings(fr.api.load_image_file(i))[0])
    return tmp

class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        self.initUI()
    
    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))
        self.playvideo.clicked.connect(self.cb_videocap)
        self.picplay.clicked.connect(self.cb_picread)
        self.display.setGeometry(0, 0, 500, 300)
        self.videorecord.clicked.connect(self.cb_videorecord)
        self.encoding.clicked.connect(self.cb_encoding)
        # self.close.clicked.connect(self.cb_encoding)
        
        self.setGeometry(0, 0, 600, 600)
        self.show()
        
    def cb_videocap(self):
        reader = cv2.VideoCapture('save1.avi')
        # facetxt = cv2.putText()
        while True:
            ret, frame = reader.read()
            if ret:
                frame = cv2.resize(frame, (300, 300))
                w, h, d = frame.shape
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                locations = fr.api.face_locations(frame)
                # print(locations)
                for i in locations:
                    top, right, bottom, left = i
                    cv2.rectangle(frame, (left * w // 300, top * w // 300), (right * h // 300, bottom * h // 300),
                                  (0, 255, 255), thickness=2)
                    cv2.putText(frame, 'beautyFace', (right * h // 300, bottom * h // 300), cv2.FONT_HERSHEY_COMPLEX, 0.5,(0, 255, 255),1)
                Qimg = QImage(frame.data, w, h, w * d, QImage.Format_RGB888)
                self.display.setPixmap(QPixmap.fromImage(Qimg))
                cv2.imshow('cv2', 0)
                k = cv2.waitKey(1)
                if k != -1:
                    break
            else:
                break
        reader.release()
        cv2.destroyAllWindows()

    def cb_videorecord(self):
        reader = cv2.VideoCapture(0)
        while reader.isOpened():
            ret, frame = reader.read()
            if ret:
                frame = cv2.resize(frame, (300, 300))
                w, h, d = frame.shape
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                locations = fr.api.face_locations(frame)
                for i in locations:
                    top, right, bottom, left = i
                    cv2.rectangle(frame, (left * w // 300, top * w // 300), (right * h // 300, bottom * h // 300),
                                  (0, 255, 255), thickness=2)
                    cv2.putText(frame, 'beautyFace', (right * h // 300, bottom * h // 300), cv2.FONT_HERSHEY_COMPLEX,
                                0.5, (0, 255, 255), 1)
                Qimg = QImage(frame.data, w, h, w * d, QImage.Format_RGB888)
                self.display.setPixmap(QPixmap.fromImage(Qimg))
                cv2.imshow('cv2', 0)
                k = cv2.waitKey(1)
                if k != -1:
                    break
            else:
                break
        reader.release()
        cv2.destroyAllWindows()
        if not reader.isOpened():
            pass
            self.display.setText('没能打开摄像头，请重试！')
        
    def cb_encoding(self):

        encoding_my = []
        facefile = []
        # 读取成员名字
        try:
            with open('facefile.txt', 'r') as f:
                for i in f:
                    facefile.append(f)
        except:
            with open('facefile.txt', 'w'):
                pass
        # 读取人脸特征数据
        for i in facefile:
            encoding_my.append(np.loadtxt(i + '.txt'))

        newMem = 'u'
        reader = cv2.VideoCapture('save1.avi')
        while True:
            ret, frame = reader.read()
            if ret:
                frame = cv2.resize(frame, (300, 300))
                w, h, d = frame.shape
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                locations = fr.api.face_locations(frame)
                saved = 0
                for i in locations:
                    top, right, bottom, left = i
                    now = fr.api.face_encodings(frame, locations)[0]
                    out = fr.api.compare_faces(encoding_my, now, tolerance=0.6)
                    print(out)
                    cv2.rectangle(frame, (left * w // 300, top * w // 300), (right * h // 300, bottom * h // 300),
                                  (0, 255, 255), thickness=2)
                    # 新的脸就保存
                    if True not in out:
                            with open('facefile.txt', 'r') as f:
                                f.write(newMem)
                            f = open(newMem, 'w')
                            np.savetxt(newMem + '.txt', now)
                            saved = 1
                    
                Qimg = QImage(frame.data, w, h, w * d, QImage.Format_RGB888)
                self.display.setPixmap(QPixmap.fromImage(Qimg))
                cv2.imshow('cv2', 0)
                k = cv2.waitKey(1)
                if k == 27:
                    break
                if saved:
                    break
            else:
                break
        reader.release()
        cv2.destroyAllWindows()
        
    def cb_picread(self):
         img = cv2.imread('timg.jpg')
         img = cv2.resize(img, (300, 300))
         w, h, d = img.shape
         locations = fr.api.face_locations(img, 2)
         
         for i in locations:
             top, right, bottom, left = i
             cv2.rectangle(img, (left * w // 300, top * w // 300), (right * h // 300, bottom * h // 300),
                           (0, 255, 255), thickness=2)

         Qimg = QImage(img.data, w, h,  # 创建QImage格式的图像，并读入图像信息
                w * d,
                QImage.Format_RGB888)
         self.display.setPixmap(QPixmap.fromImage(Qimg))
         
        
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    def mouseMoveEvent(self, e):
        x = e.x()
        y = e.y()
        text = "x: {0},  y: {1}".format(x, y)
        print(text)
        # self.label.setText(text)

    def buttonClicked(self):
        # sender = self.picread.sender()
        sender = self.sender()
        print(sender.text() + 'button click')
        # self.statusBar().showMessage(sender.text() + ' was pressed')
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.setWindowTitle('人脸识别')
    sys.exit(app.exec_())
