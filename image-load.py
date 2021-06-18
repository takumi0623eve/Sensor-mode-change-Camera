# -*- coding: utf-8 -*-
import cv2
import os
import numpy as np
import serial
ser = serial.Serial('/dev/cu.usbmodem1201', 9600, timeout=None)
not_used = ser.readline()


def anime_filter(img):
    # グレースケール変換
    gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)

    # ぼかしでノイズ低減
    edge = cv2.blur(gray, (3, 3))

    # Cannyアルゴリズムで輪郭抽出
    edge = cv2.Canny(edge, 50, 150, apertureSize=3)

    # 輪郭画像をRGB色空間に変換
    edge = cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR)

    # 画像の領域分割
    img = cv2.pyrMeanShiftFiltering(img, 5, 20)

    # 差分を返す
    return cv2.subtract(img, edge)

def top_texts(frame):
    cv2.putText(frame, 'Basic', (0, 50),
                        cv2.FONT_ITALIC, 1, (0, 0, 0), 3)
    cv2.putText(frame, 'Gray', (110, 50),
                        cv2.FONT_ITALIC, 1, (0, 0, 0), 3)
    cv2.putText(frame, 'Mirror', (200, 50),
                        cv2.FONT_ITALIC, 1, (0, 0, 0), 3)
    cv2.putText(frame, 'Bura', (310, 50),
                        cv2.FONT_ITALIC, 1, (0, 0, 0), 3)
    cv2.putText(frame, 'Color_inversion', (400, 50),
                        cv2.FONT_ITALIC, 1, (0, 0, 0), 3)

def slide_mode(LorR ,frame):
    if (LorR == 71):
                cv2.putText(frame, ' <--', (0, 150),
                            cv2.FONT_ITALIC, 1, (255, 255, 255), 3)
    elif (LorR == 72):
                cv2.putText(frame, ' -->', (0, 150),
                            cv2.FONT_ITALIC, 1, (255, 255, 255), 3)
    elif(LorR == 70):
                cv2.putText(frame, ' Waiting', (0, 150),
                            cv2.FONT_ITALIC, 1, (255, 255, 255), 3)

def countdown_save(save_photo,frame):
    if(save_photo >= 10 and save_photo <50):
                cv2.putText(frame, str(24 - save_photo), (0, 100),cv2.FONT_ITALIC, 1, (255, 255, 255), 3)






def save_frame_camera_key(device_num, dir_path, basename, ext='jpg', delay=1, window_name='frame'):  # カメラ保存用
    cap = cv2.VideoCapture(device_num)

    if not cap.isOpened():
        return

    os.makedirs(dir_path, exist_ok=True)
    base_path = os.path.join(dir_path, basename)
    mode = 0
    n = 0
    save_photo = 0
    LorR = 70

    while True:
        # print(f)

        if mode == 0:
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)

            cv2.putText(frame, 'Basic', (0, 50),
                        cv2.FONT_ITALIC, 1, (255, 255, 255), 7)

            top_texts(frame)

            slide_mode(LorR,frame)

            countdown_save(save_photo,frame)

            cv2.imshow(window_name, frame)
        elif mode == 1:
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            cv2.putText(frame, 'Gray', (110, 50),
                        cv2.FONT_ITALIC, 1, (255, 255, 255), 7)

            top_texts(frame)
            

            slide_mode(LorR,frame)
            
            countdown_save(save_photo,frame)

            cv2.imshow(window_name, frame)
        elif mode == 2:
            ret, frame = cap.read()

            cv2.putText(frame, 'Mirror', (200, 50),
                        cv2.FONT_ITALIC, 1, (255, 255, 255), 7)

            top_texts(frame)
            

            slide_mode(LorR,frame)
            
            countdown_save(save_photo,frame)

            cv2.imshow(window_name, frame)

        elif mode == 3:
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)
            frame = cv2.GaussianBlur(frame, (21, 21), 10)

            cv2.putText(frame, 'Bura', (310, 50),
                        cv2.FONT_ITALIC, 1, (255, 255, 255), 7)
            
            top_texts(frame)
            

            slide_mode(LorR,frame)
            
            countdown_save(save_photo,frame)

            cv2.imshow(window_name, frame)

        elif mode == 4:
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)
            frame = 255 - frame

            cv2.putText(frame, 'Color_inversion', (400, 50),
                        cv2.FONT_ITALIC, 1, (255, 255, 255), 7)

            top_texts(frame)
            

            slide_mode(LorR,frame)
            
            countdown_save(save_photo,frame)

            cv2.imshow(window_name, frame)
        elif mode == 5:
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)
            # 画像のアニメ絵化
            frame = anime_filter(frame)
            cv2.putText(frame, ' anime', (0, 50),
                        cv2.FONT_ITALIC, 1, (255, 255, 255), 7)

            slide_mode(LorR,frame)

            countdown_save(save_photo,frame)


            cv2.imshow(window_name, frame)

        key = cv2.waitKey(delay) & 0xFF
        # if key == ord('c'):

        if save_photo == 50:
            cv2.putText(frame, ' Saved', (0, 100),cv2.FONT_ITALIC, 1, (255, 255, 255), 3)
            ret, frame = cap.read()
            cv2.imwrite('{}_{}.{}'.format(base_path, n, ext), frame)
            img_path = "/Users/satoutakumi/Desktop/Censor-mode-change-Camera/Sensor-mode-change-Camera/img/camera_capture_" + \
                str(n) + ".jpg"
            if mode == 0:
                img = cv2.imread(img_path, -1)
                img = cv2.flip(img, 1)
            elif mode == 1:
                img = cv2.imread(img_path, 0)
                img = cv2.flip(img, 1)
            elif mode == 2:
                img = cv2.imread(img_path, -1)
            elif mode == 3:
                img = cv2.imread(img_path, -1)
                img = cv2.flip(img, 1)
                img = cv2.GaussianBlur(img, (25, 25), 0)
            elif mode == 4:
                img = cv2.imread(img_path, -1)
                img = cv2.flip(img, 1)
                img = 255 - img
            elif mode == 5:
                img = cv2.imread(img_path, -1)
                img = cv2.flip(img, 1)
                img = pixel_art(img, 0.5, 4)

            cv2.imwrite(img_path, img)
            #cv2.imshow('image', img)
            n += 1
            save_photo = 9

        elif key == ord('q'):
            break

        val_arduino = ser.readline()
        data = int(repr(val_arduino.decode())[1:-5])
        if(data < 10):
            mode = data
        elif(data >= 10 and data < 70):
            save_photo = data
            #cv2.putText(frame, str(25 - save_photo), (0, 100),cv2.FONT_ITALIC, 1, (255, 255, 255), 3)
        elif(data >= 70):
            LorR = data

    cv2.destroyWindow(window_name)


save_frame_camera_key(
    0, '/Users/satoutakumi/Desktop/Censor-mode-change-Camera/Sensor-mode-change-Camera/img', 'camera_capture')
ser.close()
