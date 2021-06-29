# -*- coding: utf-8 -*-
import cv2
import os
import numpy as np
import time
import serial
ser = serial.Serial('/dev/cu.usbmodem1401', 9600, timeout=None)
not_used = ser.readline()

# カスケード型識別器の読み込み
cascade = cv2.CascadeClassifier(
    "/Users/satoutakumi/Documents/face-blur/haarcascade_frontalface_default.xml")

#画面のテキスト情報
def text_information(frame,up_to_down_range , LorR,mode,top_text_x,top_texts_list,width,height,shutter_f,shutter_cnt):
    if(shutter_f != 2):
        #全モード表示
        top_texts(frame,top_text_x,top_texts_list)
        #文字表示
        cv2.putText(frame, top_texts_list[mode], (top_text_x[mode], 50),cv2.FONT_ITALIC, 1, (255, 255, 255), 3)
        #スライド状態表示
        slide_mode(LorR,frame)
        #距離表示
        distance_text(up_to_down_range ,frame,width,height)
    else:
        #カウントダウン表示
        countdown_save(shutter_cnt,frame,width,height)

#全モード表示
def top_texts(frame,x,texts):
    for i in range(len(x)):
        cv2.putText(frame, texts[i], (x[i], 50),cv2.FONT_ITALIC, 1, (0, 0, 0), 5)

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
def countdown_save(shutter_cnt,frame,width,height):
    if(shutter_cnt == 10): #カウントダウン10のとき
        text_x = int(width / 2 - width / 4  - width / 16)
        text_y = int(height / 2 + height / 4)
        cv2.putText(frame, str(shutter_cnt), (text_x, text_y),cv2.FONT_ITALIC, 20, (0, 0, 0), 50)
        cv2.putText(frame, str(shutter_cnt), (text_x, text_y),cv2.FONT_ITALIC, 20, (255, 255, 255), 48)
    elif(shutter_cnt >= 1 and shutter_cnt < 10): #カウントダウン1 ~ 9のとき
        text_x = int(width / 2 - width / 4 + width / 8 - width / 16)
        text_y = int(height / 2 + height / 4)
        cv2.putText(frame, str(shutter_cnt), (text_x, text_y),cv2.FONT_ITALIC, 20, (0, 0, 0), 50)
        cv2.putText(frame, str(shutter_cnt), (text_x, text_y),cv2.FONT_ITALIC, 20, (255, 255, 255), 48)
    elif(shutter_cnt == 0): #カウントダウン終了時
        frame = cv2.circle(frame,(int((width - 1) / 2),int((height - 1) / 2)), int(width), (32,32,32), -1)

#距離表示
def distance_text(up_to_down_range ,frame,width,height):
    if(up_to_down_range == 300):
        cv2.putText(frame, "Push(30cm -> 15cm)", (0, 100),cv2.FONT_ITALIC, 1, (0, 0, 0), 5)
        cv2.putText(frame, "Push(30cm -> 15cm)", (0, 100),cv2.FONT_ITALIC, 1, (255, 255, 255), 3)
    else:
        cv2.putText(frame, "more push!", (0, 100),cv2.FONT_ITALIC, 1, (0, 0, 0), 5)
        cv2.putText(frame, "more push!", (0, 100),cv2.FONT_ITALIC, 1, (255, 255, 255), 3)

# モザイク処理
def mosaic(img, alpha):
    # 画像の高さと幅
    w = img.shape[1]
    h = img.shape[0]

    # 最近傍法で縮小→拡大することでモザイク加工
    img = cv2.resize(img, (int(w*alpha), int(h*alpha)))
    img = cv2.resize(img, (w, h), interpolation=cv2.INTER_NEAREST)

    return img

# モード別の処理
def image_processing(mode,img):
    if mode == 1:
        #モード処理(グレー化)
        img= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    elif mode == 2:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 二値化(閾値100を超えた画素を255にする。)
        ret, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        #ノイズ除去処理
        ksize=3
        #中央値フィルタ
        img = cv2.medianBlur(img,ksize)

    elif mode == 3:
        # グレースケール変換
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 顔領域の探索
        face = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(30, 30))
        # 顔領域を赤色の矩形で囲む
        for (x, y, w, h) in face:
            # 顔部分を切り出してモザイク処理
            img[y:y+h, x:x+w] = mosaic(img[y:y+h, x:x+w], 0.05)
    elif mode == 4:
        #モード処理(色反転)
        img = 255 - img
    elif mode == 5:
        img = cv2.Canny(img,127,127)
    
    return img

def saving_move(mode,img,img_path): #画像保存
    #画像読み込み
    img = cv2.imread(img_path, 1)
    #画像反転
    img = cv2.flip(img,1)
    #画像加工
    img = image_processing(mode,img)

    #画像書き出し
    cv2.imwrite(img_path, img)

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
    mode = 0 #モード数(0 ~ 4)
    n = 0 #保存枚数
    LorR = 5 #左右スライド情報(5:通常 6:右スライド 7:左スライド)
    up_to_down_range = 300 #上下スライドの検出距離(300:検出リセット)
    up_to_down_range_prev  = 300 #前回のup_to_down_rangeの検出範囲
    up_to_down_range_cnt  = 0 #同距離の回数カウント
    shutter_f = 0 #シャッター(上下スライド)の検出フラグ
    shutter_loop_cnt = 0 #シャッター開始してからのループ回数
    width = cap.get(3) #画面の横幅
    height = cap.get(4) #画面の縦幅
    top_text_x = [0, 110, 200, 410, 480] #top_textの各X軸
    top_texts_list = ["Basic","Gray","Monochrome","Blur","Color_inversion"] #top_textの文字
    shutter_cnt = 10 #シャッターのカウントダウン

    while True:
        #動画読み込み
        ret, frame = cap.read()
        #動画反転
        frame = cv2.flip(frame, 1)
        #画像加工
        frame = image_processing(mode,frame)
        #文字情報追加
        text_information(frame,up_to_down_range , LorR,mode,top_text_x,top_texts_list,width,height,shutter_f,shutter_cnt)
        #動画表示
        cv2.imshow(window_name, frame)

        #カメラ撮影
        if (shutter_cnt == 0):
            #動画読み込み
            ret, frame = cap.read()
            #動画書き出し
            cv2.imwrite('{}_{}.{}'.format(base_path, n, ext), frame)
            #画像保存パス
            img_path = "/Users/satoutakumi/Desktop/Censor-mode-change-Camera/Sensor-mode-change-Camera/img/camera_capture_" + \
                        str(n) + ".jpg"
            saving_move(mode,frame,img_path)
            #動画表示
            cv2.imshow(window_name, frame)
            #枚数カウント
            n += 1
            #距離のリセット
            up_to_down_range = 300
            #距離の判定リセット
            shutter_f = 0
            #カウントダウンのリセット
            shutter_cnt = 10

        #arduino IDEから値取得
        val_arduino = ser.readline()
        data = int(repr(val_arduino.decode())[1:-5])
        if(shutter_f!= 2): #撮影モードではないなら
            
            if(data >= 0 and data < 5): #0 ~ 4 なら撮影モードに代入
                mode = data
            elif(data >= 5 and data < 8): #5 ~ 7 なら左右モードに代入
                LorR = data

            if(shutter_f == 0 and up_to_down_range > (int)(data / 100) and (int)(data / 100) >= 200): #20cm以上で検出され上下判定がなく、以前の入力より短いなら
                #検出距離の更新
                up_to_down_range = (int)(data / 100)
                #上下スライド判定開始
                shutter_f = 1
                #前の検出距離情報の更新(代入)
                up_to_down_range_prev  = up_to_down_range
            elif(shutter_f == 1): #上下スライド判定があるなら
                if((int)(data / 100) >= 140 and (int)(data / 100) <= 180): #15cm ~ 19cm なら
                    #上下スライド検出
                   shutter_f = 2
                if (up_to_down_range == up_to_down_range_prev ): #前の検出距離と現在の検出距離が同じなら
                    #同距離の検出回数を増加
                    up_to_down_range_cnt  +=1
                    if(up_to_down_range_cnt  == 20): #20回同距離なら
                        #検出距離のリセット
                        up_to_down_range = 300
                        #同距離の検出回数のリセット
                        up_to_down_range_cnt  = 0
        else: #撮影カウントダウン
            if(data == 6 or data == 7): #6 or 7ならキャンセル
                shutter_f = 0
                shutter_cnt = 10
                shutter_loop_cnt = 0
                up_to_down_range = 300
            else:
                shutter_loop_cnt += 1
                if(shutter_loop_cnt % 15  == 0):
                    shutter_cnt -=1
        
        #キー入力情報
        key = cv2.waitKey(delay) & 0xFF
        if key == ord('q'): #処理終了
            break

    cv2.destroyWindow(window_name)

save_frame_camera_key(
    0, '/Users/satoutakumi/Desktop/Censor-mode-change-Camera/Sensor-mode-change-Camera/img', 'camera_capture')
ser.close()
