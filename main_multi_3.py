from cgi import print_directory
from concurrent.futures.process import _process_worker
import glob
import json
import math
import os
import time
from tkinter import N
from traceback import print_tb
import cv2
import numpy as np
from multiprocessing import Process,Manager

planks = {
    "planks_oak":"planks 0",
    "planks_spruce":"planks 1",
    "planks_birch":"planks 2",
    "planks_jungle":"planks 3",
    "planks_acacia":"planks 4",
    "planks_big_oak":"planks 5",
    "crimson_planks":"crimson_planks",
    "warped_planks":"warped_planks"
}
log = {
    "log_oak":"log 0",
    "log_spruce":"log 1",
    "log_birch":"log 2",
    "log_jungle":"log 3",
}
log2 = {
    "log_acacia":"log2 0",
    "log_big_oak":"log2 1"
}
concrete = {
"concrete_white":"concrete 0",
"concrete_orange":"concrete 1",
"concrete_magenta":"concrete 2",
"concrete_light_blue":"concrete 3",
"concrete_yellow":"concrete 4",
"concrete_lime":"concrete 5",
"concrete_pink":"concrete 6",
"concrete_gray":"concrete 7",
"concrete_silver":"concrete 8",
"concrete_cyan":"concrete 9",
"concrete_purple":"concrete 10",
"concrete_blue":"concrete 11",
"concrete_brown":"concrete 12",
"concrete_green":"concrete 13",
"concrete_red":"concrete 14",
"concrete_black":"concrete 15"
}

wool = {
    "wool_colored_white":"wool 0",
    "wool_colored_orange":"wool 1",
    "wool_colored_magenta":"wool 2",
    "wool_colored_light_blue":"wool 3",
    "wool_colored_yellow":"wool 4",
    "wool_colored_lime":"wool 5",
    "wool_colored_pink":"wool 6",
    "wool_colored_gray":"wool 7",
    "wool_colored_silver":"wool 8",
    "wool_colored_cyan":"wool 9",
    "wool_colored_purple":"wool 10",
    "wool_colored_blue":"wool 11",
    "wool_colored_brown":"wool 12",
    "wool_colored_green":"wool 13",
    "wool_colored_red":"wool 14",
    "wool_colored_black":"wool 15"
}

concrete_powder = {
    "concrete_powder_white":"concretepowder 0",
    "concrete_powder_orange":"concretepowder 1",
    "concrete_powder_magenta":"concretepowder 2",
    "concrete_powder_light_blue":"concretepowder 3",
    "concrete_powder_yellow":"concretepowder 4",
    "concrete_powder_lime":"concretepowder 5",
    "concrete_powder_pink":"concretepowder 6",
    "concrete_powder_gray":"concretepowder 7",
    "concrete_powder_silver":"concretepowder 8",
    "concrete_powder_cyan":"concretepowder 9",
    "concrete_powder_purple":"concretepowder 10",
    "concrete_powder_blue":"concretepowder 11",
    "concrete_powder_brown":"concretepowder 12",
    "concrete_powder_green":"concretepowder 13",
    "concrete_powder_red":"concretepowder 14",
    "concrete_powder_black":"concretepowder 15"
}

texturesPath = [
    "./texture/concrete",
    "./texture/log",
    "./texture/ore",
    "./texture/ore_block",
    "./texture/planks",
    "./texture/produce",
    "./texture/wool"
]

process_worker_num = 8
# x = 455
# y = 300
# x = 128
# y = 96
# y = 72 #16:9
#y = 85 #3:2
#y = 96 #4:3
x = 128
y = 128

def mosaic(img, alpha, w, h):
    # 画像の高さ、幅、チャンネル数
    # h, w, ch = img.shape

    # 縮小→拡大でモザイク加工
    img = cv2.resize(img,(int(w*alpha), int(h*alpha)))
    img = cv2.resize(img,(w, h), interpolation=cv2.INTER_NEAREST)

    return img

def rgbAve(img):
    x, y, ch = img.shape
    r,g,b = 0,0,0
    for y_ in range(0,y,1):
        for x_ in range(0,x,1):
            r, g, b = img[y_,x_][2]+r, img[y_,x_][1]+g, img[y_,x_][0]+b
    return [math.floor(r/(x*y)),math.floor(g/(x*y)),math.floor(b/(x*y))]
            
def xLineLoad(process_worker_num,process_num,w,outImg,returned_dict,texture_rgbAveList):
    yRange = math.floor(y / process_worker_num)
    yStart = yRange * process_num
    yEnd = yStart+yRange
    print("process : "+str(process_num)+" is START")
    blockList = []
    # for i in range(yStart,yEnd,1):
    #     print("prcIN : "+str(process_num) + " i => "+str(i))
    h__ = 0
    for h_ in range(yStart,yEnd,1):
        print("prcIN : "+str(process_num) + " h_ => "+str(h_))
        blockList.append([])
        for w_ in range(0,w,1):
            blockList[h__].append([])
            rgbAveDifferenceList = []
            textureList = []
            for textureName in texture_rgbAveList.keys():
                textureList.append(textureName)
                # print("\nX:"+str(w_)+" Y:"+str(h_))
                # print(textureName)
                # print("R:"+str(outImg[h_,w_][2])+" | "+str(texture_rgbAveList[textureName][0]))
                # print("G:"+str(outImg[h_,w_][1])+" | "+str(texture_rgbAveList[textureName][1]))
                # print("B:"+str(outImg[h_,w_][0])+" | "+str(texture_rgbAveList[textureName][2]))
                # print(((outImg[h_,w_][2]-texture_rgbAveList[textureName][0])**2+(outImg[h_,w_][1]-texture_rgbAveList[textureName][1])**2+(outImg[h_,w_][0]-texture_rgbAveList[textureName][2])**2)**1/2)
                rgbAveDifferenceList.append(math.floor(((outImg[h_,w_][2]-texture_rgbAveList[textureName][0])**2+(outImg[h_,w_][1]-texture_rgbAveList[textureName][1])**2+(outImg[h_,w_][0]-texture_rgbAveList[textureName][2])**2)**1/2))
                # outImg[h_,w_]
            for num in range(0,len(rgbAveDifferenceList),1):
                if min(rgbAveDifferenceList) == rgbAveDifferenceList[num]:
                    # print(rgbAveDifferenceList[num])
                    break
            # print(textureList[num])
            if textureList[num] in planks:
                blockList[h__][w_].append(planks[textureList[num]])
            elif textureList[num] in log:
                blockList[h__][w_].append(log[textureList[num]])
            elif textureList[num] in log2:
                blockList[h__][w_].append(log2[textureList[num]])
            elif textureList[num] in concrete:
                blockList[h__][w_].append(concrete[textureList[num]])
            elif textureList[num] in concrete_powder:
                blockList[h__][w_].append(concrete_powder[textureList[num]])
            elif textureList[num] in wool.keys():
                blockList[h__][w_].append(wool[textureList[num]])
            else:
                blockList[h__][w_].append(textureList[num])
        h__ = h__ + 1
    # print(blockList)
    returned_dict[process_num] = blockList
    print("process : "+str(process_num)+" DONE")


if __name__ == '__main__':
    img = cv2.imread(input("画像を選択してください\n> "))
    h, w, ch = img.shape
    process_worker_num_input = input("処理するスレッド数(変更する場合は入力をしてください) : "+str(process_worker_num)+"\n>")
    x_input = input("画像のサイズ X(変更する場合は入力をしてください) : "+str(w)+"\n>")
    y_input = input("画像のサイズ Y(変更する場合は入力をしてください) : "+str(h)+"\n>")
    if process_worker_num_input == "":
        process_worker_num_input = process_worker_num
    process_worker_num = int(process_worker_num_input)

    if x_input == "":
        x_input = w
    if y_input == "":
        y_input = h
    x = int(x_input)
    y = int(y_input)
    print(x)
    print(y)

    print("Comparing the difference with texture RGB average...")
    texture_rgbAveList = {}
    for texturePath in texturesPath:
        print("loading RGB average of"+texturePath+" of")
        for imgPath in glob.glob(texturePath+"/*"):
            imgPath = imgPath.replace("\\","/")
            print(" "+os.path.split(imgPath)[1].replace(".png",""))
            texture_rgbAve = rgbAve(cv2.imread(imgPath))
            texture_rgbAveList[os.path.split(imgPath)[1].replace(".png","")] = texture_rgbAve

    print("DONE")
    outImg = mosaic(img, 1, x, y)

    h, w, ch = outImg.shape
   

    print("create Manager")
    manager = Manager()
    print("DONE")

    print("create dict")
    returned_dict = manager.dict()
    print("DONE")

    print("create process loop")
    
    for process_num in range(0,process_worker_num,1):
        # print("process : "+str(process_num)+" is ON")
        process = Process(
            target=xLineLoad,
            kwargs={
                'process_worker_num': process_worker_num,
                'process_num': process_num,
                'w': w,
                'outImg':outImg,
                'returned_dict': returned_dict,
                'texture_rgbAveList':texture_rgbAveList
            })
        process.start()
    process.join()

    print("ALL process serialize...")
    blockData = []
    # print(str(returned_dict))
    for process_num in range(0,process_worker_num,1):
        print(process_num)
        for x_ in range(0,len(returned_dict[process_num]),1):
            blockData.append(returned_dict[process_num][x_])
    print("DONE")

    
    print("ALL dot inversioning...")
    blockList = []
    for b in range(len(blockData)-1,-1,-1):
        # print(b)
        blockList.append(blockData[b])
    print("DONE")

    outPut = {}
    outPut["blockList"] = blockList
    with open('out.json', 'w') as file:
        json.dump(outPut["blockList"], file)
    # print(blockList)




