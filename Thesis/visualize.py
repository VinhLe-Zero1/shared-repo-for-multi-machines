from Config import *
import cv2
import numpy as np
import json

colorDict = {
    "red": (255,0,0),
    "orange": (255,128,0),
    "yellow": (255,255,0),
    "lightGreen": (128,255,0),
    "green": (0,255,0),
    "darkGreen": (0,255,128),
    "cyan": (0,255,255),
    "skyBlue": (0,128,255),
    "blue": (0,0,255),
    "indigo":  (127,0,255),
    "purple": (255,0,255),
    "pink": (255,0,127),
    "grey": (128,128,128),
    "white": (255,255,255),
    "black": (0,0,0)
}

colorTable = [
"orange",
"yellow",
"black",
"lightGreen",
"green",
"darkGreen",
"cyan",
"skyBlue",
"blue",
"indigo",
"purple",
"pink",
"grey",
"white",
"red"
]

resultFile = "ricotext_test_results.json"
with open(resultFile, "r") as f:
    data_json = f.read()
f.close()

resultList = json.loads(data_json)
boxes = []
for res in resultList:
    if res['image_id'] == "a2dp.Vol-screens_screenshot_1.":
        boxes.append(res)

img = "D:\\Vinh\\School\\Thesis\\Data\\ReDraw-Final-Google-Play-Dataset\\ReDraw-Final-Google-Play-Dataset\\a2dp.Vol-screens\\screenshot_1.png"

screen = cv2.imread(img)
result = screen.copy()

for box in boxes:
    if box["score"] >= 0.8:
        bbox = box["bbox"]
        objectId = box["category_id"]
        color = colorDict[colorTable[objectId]]
        cv2.rectangle(result, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), color, thickness=2)

cv2.imshow("result", result)
cv2.waitKey(0)
cv2.destroyAllWindows()