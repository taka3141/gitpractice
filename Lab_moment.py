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
            img_Lab = cv2.cvtColor(im, cv2.COLOR_BGR2Lab) # Lab色空間に変換
            img_Lab_L, img_Lab_a, img_Lab_b = cv2.split(img_Lab) # 分割
            _thres, mask = cv2.threshold(img_Lab_a, 110, 255, cv2.THRESH_BINARY_INV) # マスク処理

            m = cv2.countNonZero(mask) # 緑のピクセルの数を数える
            h, w = mask.shape
            per = round(100*float(m)/(w * h),1)   # 緑の割合を計算
            cv2.imwrite(outputfile + "/" + os.path.splitext(os.path.basename(fl))[0] + "_" + str(per) +"_"+ ".jpg", mask) # マスクファイル（白黒）を書き出し
            gr.write(os.path.basename(fl) + " : " + str(per)+"%\n") # 緑の割合をファイルに出力
            maskedim = cv2.bitwise_and(im, im, mask=mask) # 元画像をマスク
            cv2.imwrite(outputfile2 + "/" + os.path.splitext(os.path.basename(fl))[0] + "_" + str(per) +"_"+ ".jpg", maskedim) # マスクされたファイルを書き出し
            

if __name__ == '__main__':
    main()
