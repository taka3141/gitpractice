# -*- coding: utf-8 -*-
import cv2
import numpy as np
import glob
import os

def main():
    outputfile = "output"
    outputfile2 = "output2"
    # アウトプットするフォルダがなければ作成
    if not os.path.isdir(outputfile):
        os.mkdir(outputfile)
    if not os.path.isdir(outputfile2):
        os.mkdir(outputfile2)
    filelist = glob.glob("input/*") 
    with open("greenratio.csv", "w") as gr:
        for i, fl in enumerate(filelist):
            print(fl+"\t(%d / %d)" % (i+1, len(filelist)))
            im = cv2.imread(fl) # 画像の取得
            hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)   # HSV変換
            # 緑色のHSV範囲-
            hsv_min = np.array([60 / 360 * 179, 80, 0])
            hsv_max = np.array([170 / 360 * 179, 255, 255])
            mask = cv2.inRange(hsv, hsv_min,  hsv_max) # 条件に当てはまるピクセルの検出
            m = cv2.countNonZero(mask) # 緑のピクセルの数を数える
            h, w = mask.shape
            per = round(100*float(m)/(w * h),1)   # 緑の割合を計算
            cv2.imwrite(outputfile + "/" + os.path.splitext(os.path.basename(fl))[0] + "_" + str(per) +"_"+ ".jpg", mask) # 白黒画像を書き出し
            gr.write(os.path.basename(fl) + ", " + str(per)+"\n") # 緑の割合をファイルに出力
            maskedim = cv2.bitwise_and(im, im, mask=mask) # 緑色部分のみ抽出した画像を作成
            cv2.imwrite(outputfile2 + "/" + os.path.splitext(os.path.basename(fl))[0] + "_" + str(per) +"_"+ ".jpg", maskedim) # 緑色抽出画像を書き出し
            

if __name__ == '__main__':
    main()
