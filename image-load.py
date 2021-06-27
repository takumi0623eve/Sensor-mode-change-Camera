# -*- coding: utf-8 -*-
import cv2
import os
import numpy as np
import time
import serial
import random
ser = serial.Serial('/dev/cu.usbmodem1401', 9600, timeout=None)
not_used = ser.readline()

#アニメフィルター加工
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

#全モード表示
def top_texts(frame):
    cv2.putText(frame, 'Basic', (0, 50),
                        cv2.FONT_ITALIC, 1, (0, 0, 0), 5)
    cv2.putText(frame, 'Gray', (110, 50),
                        cv2.FONT_ITALIC, 1, (0, 0, 0), 5)
    cv2.putText(frame, 'Monochrome', (200, 50),
                        cv2.FONT_ITALIC, 1, (0, 0, 0), 5)
    cv2.putText(frame, 'Blur', (410, 50),
                        cv2.FONT_ITALIC, 1, (0, 0, 0), 5)
    cv2.putText(frame, 'Color_inversion', (480, 50),
                        cv2.FONT_ITALIC, 1, (0, 0, 0), 5)

#スライドモード表示
def slide_mode(LorR ,frame):
    if(LorR == 5):
        cv2.putText(frame, 'Ready', (0, 150),cv2.FONT_ITALIC, 1, (0, 0, 0), 5)
        cv2.putText(frame, 'Ready', (0, 150),cv2.FONT_ITALIC, 1, (255, 255, 255), 3)
    elif (LorR == 6):
        cv2.putText(frame, ' <--', (0, 150),cv2.FONT_ITALIC, 1, (0, 0, 0), 5)
        cv2.putText(frame, ' <--', (0, 150),cv2.FONT_ITALIC, 1, (255, 255, 255), 3)
    elif (LorR == 7):
        cv2.putText(frame, ' -->', (0, 150),cv2.FONT_ITALIC, 1, (0, 0, 0), 5)
        cv2.putText(frame, ' -->', (0, 150),cv2.FONT_ITALIC, 1, (255, 255, 255), 3)

#カウントダウン表示
def countdown_save(save_range,frame,width,height):
    if(save_range == 90): #カウントダウン10のとき
        text_x = int(width / 2 - width / 4  - width / 16)
        text_y = int(height / 2 + height / 4)
        cv2.putText(frame, str(100 - save_range), (text_x, text_y),cv2.FONT_ITALIC, 20, (0, 0, 0), 50)
        cv2.putText(frame, str(100 - save_range), (text_x, text_y),cv2.FONT_ITALIC, 20, (255, 255, 255), 48)
    elif(save_range >= 91 and save_range < 100): #カウントダウン1 ~ 9のとき
        text_x = int(width / 2 - width / 4 + width / 8 - width / 16)
        text_y = int(height / 2 + height / 4)
        cv2.putText(frame, str(100 - save_range), (text_x, text_y),cv2.FONT_ITALIC, 20, (0, 0, 0), 50)
        cv2.putText(frame, str(100 - save_range), (text_x, text_y),cv2.FONT_ITALIC, 20, (255, 255, 255), 48)
    elif(save_range == 100): #カウントダウン終了時
        frame = cv2.circle(frame,(int((width - 1) / 2),int((height - 1) / 2)), int(width), (32,32,32), -1)
        for num in range(int(width)):
                frame = cv2.circle(frame,(int((width - 1) / 2),int((height - 1) / 2)),int(width  - num),(int(63 * (width / (num + 1)) - 63),int(63 * (width / (num + 1)) - 63),int(63 * (width / (num + 1)) - 63)),0)
    else:
        cv2.putText(frame, "Distance:" + str(save_range), (0, 100),cv2.FONT_ITALIC, 1, (0, 0, 0), 5)
        cv2.putText(frame, "Distance:" + str(save_range), (0, 100),cv2.FONT_ITALIC, 1, (255, 255, 255), 3)

def save_frame_camera_key(device_num, dir_path, basename, ext='jpg', delay=1, window_name='frame'):  # カメラ保存用
    #動画ファイル読み込み
    cap = cv2.VideoCapture(device_num)

    #動画を読み込めないなら終了
    if not cap.isOpened():
        return

    #ディレクトリ作成
    os.makedirs(dir_path, exist_ok=True)
    #パズ文字列からファイル作成
    base_path = os.path.join(dir_path, basename)

    #各初期値設定
    mode = 0
    n = 0
    save_photo = 0
    LorR = 5
    save_range = 300
    save_range_prev = 300
    save_range_cnt = 0
    f = 0
    cnt = 0
    width = 0
    height = 0
    width = cap.get(3)
    height = cap.get(4)

    while True:
        '''
        mode+=random.randint(0,4)
        if(mode > 4):
            mode = 0'''
            
        if mode == 0:
            #動画読み込み
            ret, frame = cap.read()
            #動画反転
            frame = cv2.flip(frame, 1)
            
            if(save_range < 90 or save_range >= 100):
                #全モード表示
                top_texts(frame)
                #文字表示
                cv2.putText(frame, 'Basic', (0, 50),
                            cv2.FONT_ITALIC, 1, (255, 255, 255), 3)
                #スライド状態表示
                slide_mode(LorR,frame)
            
            #距離 and カウントダウン表示
            countdown_save(save_range,frame,width,height)
            
            #動画表示
            cv2.imshow(window_name, frame)
        elif mode == 1:
            #動画読み込み
            ret, frame = cap.read()
            #動画反転
            frame = cv2.flip(frame, 1)
            #モード処理(グレー化)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            if(save_range < 90 or save_range >= 100):
                #全モード表示
                top_texts(frame)
                #文字表示
                cv2.putText(frame, 'Gray', (110, 50),
                            cv2.FONT_ITALIC, 1, (255, 255, 255), 3)
                #スライド状態表示
                slide_mode(LorR,frame)
            #距離 and カウントダウン表示
            countdown_save(save_range,frame,width,height)
            #動画表示
            cv2.imshow(window_name, frame)
        elif mode == 2:
            #動画読み込み
            ret, frame = cap.read()
            #動画反転
            frame = cv2.flip(frame, 1)
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # 二値化(閾値100を超えた画素を255にする。)
            ret, frame = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY)

            #ノイズ除去処理
            ksize=3
            #中央値フィルタ
            frame = cv2.medianBlur(frame,ksize)

            if(save_range < 90 or save_range >= 100):
                #全モード表示
                top_texts(frame)
                #モード表示
                cv2.putText(frame, 'Monochrome', (200, 50),
                            cv2.FONT_ITALIC, 1, (255, 255, 255), 3)
                #スライド状態表示
                slide_mode(LorR,frame)
            
            #距離 and カウントダウン表示
            countdown_save(save_range,frame,width,height)

            #動画表示
            cv2.imshow(window_name, frame)
        elif mode == 3:
            #動画読み込み
            ret, frame = cap.read()
            #動画反転
            frame = cv2.flip(frame, 1)
            #モード処理(ブラー)
            frame = cv2.GaussianBlur(frame, (21, 21), 10)
            
            if(save_range < 90 or save_range >= 100):
                #全モード表示
                top_texts(frame)
                #文字表示
                cv2.putText(frame, 'Blur', (410, 50),
                            cv2.FONT_ITALIC, 1, (255, 255, 255), 3)
                #スライド状態表示
                slide_mode(LorR,frame)
            
            #距離 and カウントダウン表示
            countdown_save(save_range,frame,width,height)
            #動画表示
            cv2.imshow(window_name, frame)
        elif mode == 4:
            #動画読み込み
            ret, frame = cap.read()
            #動画反転
            frame = cv2.flip(frame, 1)
            #モード処理(色反転)
            frame = 255 - frame
            if(save_range < 90 or save_range >= 100):
                #全モード表示
                top_texts(frame)
                #文字表示
                cv2.putText(frame, 'Color_inversion', (480, 50),
                            cv2.FONT_ITALIC, 1, (255, 255, 255), 3)
                #スライド状態表示
                slide_mode(LorR,frame)
            #距離 and カウントダウン表示
            countdown_save(save_range,frame,width,height)
            #動画表示
            cv2.imshow(window_name, frame)

        
        elif mode == 5:
            #動画読み込み
            ret, frame = cap.read()
            #動画反転
            frame = cv2.flip(frame, 1)
            frame = cv2.Canny(frame,127,127)
            # 画像のアニメ絵化
            #frame = anime_filter(frame)
            #文字表示
            cv2.putText(frame, ' anime', (0, 50),
                        cv2.FONT_ITALIC, 1, (0, 0, 0), 3)
            #スライド状態表示
            slide_mode(LorR,frame)
            #距離 and カウントダウン表示
            countdown_save(save_range,frame,width,height)
            #動画表示
            cv2.imshow(window_name, frame)
        
        elif mode == 6:
            #動画読み込み
            ret, frame = cap.read()
            #動画反転
            frame = cv2.flip(frame, 1)
            
            frame = cv2.Canny(frame,127,127)
            
            if(save_range < 90 or save_range >= 100):
                #文字表示
                cv2.putText(frame, ' Edge', (0, 50),
                            cv2.FONT_ITALIC, 1, (0, 0, 0), 3)
                #スライド状態表示
                slide_mode(LorR,frame)
            
            #距離 and カウントダウン表示
            countdown_save(save_range,frame,width,height)
            #動画表示
            cv2.imshow(window_name, frame)

        #キー入力情報
        key = cv2.waitKey(delay) & 0xFF
        # if key == ord('c'):

        #カメラ撮影
        if save_range == 100:
            #動画読み込み
            ret, frame = cap.read()
            #動画書き出し
            cv2.imwrite('{}_{}.{}'.format(base_path, n, ext), frame)
            #画像保存パス
            img_path = "/Users/satoutakumi/Desktop/Censor-mode-change-Camera/Sensor-mode-change-Camera/img/camera_capture_" + \
                str(n) + ".jpg"
            #モード別画像処理
            if mode == 0:
                #画像読み込み
                img = cv2.imread(img_path, 1)
                #画像反転
                img = cv2.flip(img,1)

            elif mode == 1:
                #画像読み込み
                img = cv2.imread(img_path, 0)
                #画像反転
                img = cv2.flip(img,1)

            elif mode == 2:
                #画像読み込み
                img = cv2.imread(img_path, 0)
                #画像反転
                img = cv2.flip(img,1)
                # 二値化(閾値100を超えた画素を255にする。)
                ret, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

                #ノイズ除去処理
                ksize=3
                #中央値フィルタ
                img = cv2.medianBlur(img,ksize)

            elif mode == 3:
                #画像読み込み
                img = cv2.imread(img_path, 1)
                #画像反転
                img = cv2.flip(img,1)
                #モード処理(ブラー)
                img = cv2.GaussianBlur(img, (25, 25), 0)

            elif mode == 4:
                #画像読み込み
                img = cv2.imread(img_path, 1)
                #画像反転
                img = cv2.flip(img,1)
                #色反転
                img = 255 - img

            elif mode == 5:
                #画像読み込み
                img = cv2.imread(img_path, -1)
                #画像反転
                img = cv2.flip(img,1)
                #モード処理(アニメ化)
                #img = pixel_art(img, 0.5, 4)
                img = cv2.Canny(img,127,127)
            elif mode == 6:
                #画像読み込み
                img = cv2.imread(img_path, -1)
                #画像反転
                img = cv2.flip(img,1)
                img = cv2.Canny(img,127,127)

            #画像書き出し
            cv2.imwrite(img_path, img)

            #枚数カウント
            n += 1
            #距離のリセット
            save_range = 300
            #距離の判定リセット
            f = 0
            #動画表示
            cv2.imshow(window_name, frame)
            time.sleep(0.00001)
            cv2.imshow('image', img)

        #処理終了
        elif key == ord('q'):
            break

        #arduino IDEから値取得
        if(f != 2):
            val_arduino = ser.readline()
            data = int(repr(val_arduino.decode())[1:-5])

        #0~4なら動画モードに代入
        if(f != 2 and data >= 0 and data < 5):
            mode = data
        #5~7なら左右スライドモードに代入
        elif(f != 2 and data >= 5 and data <= 7 ):
            LorR = data
        #200以上で前回の距離より小さいならなら距離(save_range)に代入
        elif(f == 0 and save_range >= 200 and save_range > (int)(data / 100) and (int)(data / 100) >= 200):
            save_range = (int)(data / 100)
            #200 ~ 240なら距離判定のフラグを立てる
            if(save_range <= 240):
                f = 1
                save_range_prev = save_range
        elif(f == 1 and (int)(data / 100) >= 140 and (int)(data / 100) <= 190):
            #カウントダウン用を代入
                save_range = 90
                f = 2
        
        if(f == 1 and save_range == save_range_prev):
            save_range_cnt +=1
            if(save_range_cnt == 10):
                save_range = 300
                save_range_cnt = 0
                f = 0
        
        #撮影カウントダウン
        if(f == 2 and save_range >= 90 and save_range < 100):
            cnt += 1
            if(cnt % 30 * 10 == 0):
                save_range +=1

    cv2.destroyWindow(window_name)


save_frame_camera_key(
    0, '/Users/satoutakumi/Desktop/Censor-mode-change-Camera/Sensor-mode-change-Camera/img', 'camera_capture')
ser.close()
