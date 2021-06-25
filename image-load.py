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
    if (LorR == 71):
                cv2.putText(frame, ' <--', (0, 150),
                            cv2.FONT_ITALIC, 1, (0, 0, 0), 5)
                cv2.putText(frame, ' <--', (0, 150),
                            cv2.FONT_ITALIC, 1, (255, 255, 255), 3)
    elif (LorR == 72):
                cv2.putText(frame, ' -->', (0, 150),
                            cv2.FONT_ITALIC, 1, (0, 0, 0), 5)
                cv2.putText(frame, ' -->', (0, 150),
                            cv2.FONT_ITALIC, 1, (255, 255, 255), 3)
    elif(LorR == 70):
                cv2.putText(frame, 'Ready', (0, 150),
                            cv2.FONT_ITALIC, 1, (0, 0, 0), 5)
                cv2.putText(frame, 'Ready', (0, 150),
                            cv2.FONT_ITALIC, 1, (255, 255, 255), 3)

#カウントダウン表示
def countdown_save(save_range,frame):
    if (save_range > 100 or save_range < 40):
        cv2.putText(frame, "Distance:" + str(save_range), (0, 100),cv2.FONT_ITALIC, 1, (0, 0, 0), 5)
        cv2.putText(frame, "Distance:" + str(save_range), (0, 100),cv2.FONT_ITALIC, 1, (255, 255, 255), 3)
    elif(save_range  >= 40 and save_range < 91):
        cv2.putText(frame, "ShutterTime:" + str(100 - save_range), (0, 100),cv2.FONT_ITALIC, 1, (0, 0, 0), 5)
        cv2.putText(frame, "ShutterTime:" + str(100 - save_range), (0, 100),cv2.FONT_ITALIC, 1, (255, 255, 255), 3)
    elif(save_range >= 91 and save_range < 100):
        cv2.putText(frame, str(100 - save_range), (640 - 320 , 520),cv2.FONT_ITALIC, 20, (0, 0, 0), 50)
        cv2.putText(frame, str(100 - save_range), (640 - 320, 520),cv2.FONT_ITALIC, 16, (255, 255, 255), 50)
    else:
        cv2.putText(frame, 'Saved', (0, 100),cv2.FONT_ITALIC, 1, (0, 0, 0), 5)
        cv2.putText(frame, 'Saved', (0, 100),cv2.FONT_ITALIC, 1, (255, 255, 255), 3)

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
    LorR = 70
    save_range = 300
    f = 0
    cnt = 0

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
            
            #全モード表示
            top_texts(frame)
            #文字表示
            cv2.putText(frame, 'Basic', (0, 50),
                        cv2.FONT_ITALIC, 1, (255, 255, 255), 3)
            #スライド状態表示
            slide_mode(LorR,frame)
            #距離 and カウントダウン表示
            countdown_save(save_range,frame)
            #動画表示
            cv2.imshow(window_name, frame)
        elif mode == 1:
            #動画読み込み
            ret, frame = cap.read()
            #動画反転
            frame = cv2.flip(frame, 1)
            #モード処理(グレー化)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            #全モード表示
            top_texts(frame)
            #文字表示
            cv2.putText(frame, 'Gray', (110, 50),
                        cv2.FONT_ITALIC, 1, (255, 255, 255), 3)
            #スライド状態表示
            slide_mode(LorR,frame)
            #距離 and カウントダウン表示
            countdown_save(save_range,frame)
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

            #全モード表示
            top_texts(frame)
            #モード表示
            cv2.putText(frame, 'Monochrome', (200, 50),
                        cv2.FONT_ITALIC, 1, (255, 255, 255), 3)
            #スライド状態表示
            slide_mode(LorR,frame)
            #距離 and カウントダウン表示
            countdown_save(save_range,frame)

            #動画表示
            cv2.imshow(window_name, frame)
        elif mode == 3:
            #動画読み込み
            ret, frame = cap.read()
            #動画反転
            frame = cv2.flip(frame, 1)
            #モード処理(ブラー)
            frame = cv2.GaussianBlur(frame, (21, 21), 10)
            #全モード表示
            top_texts(frame)
            #文字表示
            cv2.putText(frame, 'Blur', (410, 50),
                        cv2.FONT_ITALIC, 1, (255, 255, 255), 3)
            #スライド状態表示
            slide_mode(LorR,frame)
            #距離 and カウントダウン表示
            countdown_save(save_range,frame)
            #動画表示
            cv2.imshow(window_name, frame)
        elif mode == 4:
            #動画読み込み
            ret, frame = cap.read()
            #動画反転
            frame = cv2.flip(frame, 1)
            #モード処理(色反転)
            frame = 255 - frame
            #全モード表示
            top_texts(frame)
            #文字表示
            cv2.putText(frame, 'Color_inversion', (480, 50),
                        cv2.FONT_ITALIC, 1, (255, 255, 255), 3)
            #スライド状態表示
            slide_mode(LorR,frame)
            #距離 and カウントダウン表示
            countdown_save(save_range,frame)
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
            countdown_save(save_range,frame)
            #動画表示
            cv2.imshow(window_name, frame)
        
        elif mode == 5:
            #動画読み込み
            ret, frame = cap.read()
            #動画反転
            frame = cv2.flip(frame, 1)
            
            frame = cv2.Canny(frame,127,127)
            #文字表示
            cv2.putText(frame, ' Edge', (0, 50),
                        cv2.FONT_ITALIC, 1, (0, 0, 0), 3)
            #スライド状態表示
            slide_mode(LorR,frame)
            #距離 and カウントダウン表示
            countdown_save(save_range,frame)
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

            #動画書き出し
            cv2.imwrite(img_path, img)
            #cv2.imshow('image', img)

            #枚数カウント
            n += 1
            #距離のリセット
            save_range = 300
            #距離の判定リセット
            f = 0
            #処理停止
            time.sleep(0.5)

        #処理終了
        elif key == ord('q'):
            break

        #arduino IDEから値取得
        val_arduino = ser.readline()
        data = int(repr(val_arduino.decode())[1:-5])

        #0~3なら動画モードに代入
        if(data >= 0 and data < 6):
            mode = data
        #70~73なら左右スライドモードに代入
        elif(data >= 70 and data <= 72 ):
            LorR = data
        #100以上で前回の距離より小さいならなら距離(save_range)に代入
        elif(save_range > (int)(data / 100) and (int)(data / 100) > 100):
            save_range = (int)(data / 100)

            #200 ~ 250なら距離判定のフラグを立てる
            if(f == 0 and save_range >= 250 and save_range <= 200):
                f = 1
            #140 ~ 190で距離判定のフラグが立っているなら
            elif(save_range < 190 and save_range > 140):
                #カウントダウン用(60)を代入
                save_range = 80
        #100以上で前回の距離より大きいなら距離(save_range)をリセット
        elif(save_range >= (int)(data / 100) and (int)(data / 100) > 200):
            save_range = 300
            #距離判定フラグリセット
            f = 0
        #撮影カウントダウン
        if(save_range >= 40 and save_range < 100):
            save_range +=1
            cnt += 1
            if(cnt % 2 == 0):
                save_range -=1
    

    cv2.destroyWindow(window_name)


save_frame_camera_key(
    0, '/Users/satoutakumi/Desktop/Censor-mode-change-Camera/Sensor-mode-change-Camera/img', 'camera_capture')
ser.close()
