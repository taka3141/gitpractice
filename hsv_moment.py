# -*- coding: utf-8 -*-
import cv2
import numpy as np
import glob
import os

def main():
    outputfile = "output"
    outputfile2 = "output2"
    if not os.path.isdir(outputfile):
        os.mkdir(outputfile)
    if not os.path.isdir(outputfile2):
        os.mkdir(outputfile2)
    filelist = glob.glob("input/*.jpg")
    with open("greenratio.txt", "w") as gr:
        for fl in filelist:
            print(fl)
            im = cv2.imread(fl) # 画像の取得
            hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)   # HSV変換
            # 青色のHSV範囲
            #hsv_min = np.array([80, 150, 0])
            #hsv_max = np.array([150, 255, 255])
            # 緑色のHSV範囲
            hsv_min = np.array([10, 80, 0])
            hsv_max = np.array([80, 255, 255])
            mask = cv2.inRange(hsv, hsv_min,  hsv_max) # 条件に当てはまるピクセルの検出
            m = cv2.countNonZero(mask) # 緑のピクセルの数を数える
            h, w = mask.shape
            per = round(100*float(m)/(w * h),1)   # 緑の割合を計算
            cv2.imwrite(outputfile + "/" + os.path.splitext(os.path.basename(fl))[0] + "_" + str(per) +"_"+ ".jpg", mask) # マスクファイル（白黒）を書き出し
            gr.write(os.path.basename(fl) + " : " + str(per)+"%\n") # 緑の割合をファイルに出力
            maskedim = cv2.bitwise_and(im, im, mask=mask) # 元画像をマスク
            cv2.imwrite(outputfile2 + "/" + os.path.splitext(os.path.basename(fl))[0] + "_" + str(per) +"_"+ ".jpg", maskedim) # マスクされたファイルを書き出し
            

if __name__ == '__main__':
    main()
