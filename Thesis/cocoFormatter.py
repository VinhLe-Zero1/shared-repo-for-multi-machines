import sys

from Util import xmlTraverse, GUIClass
import xml.etree.ElementTree as ET
import os
import json
import cv2
import numpy as np
from Config import *

categories = [
    {"id": 0, "name": "Button"},
    {"id": 1, "name": "CheckBox"},
    {"id": 2, "name": "Chronometer"},
    {"id": 3, "name": "EditText"},
    {"id": 4, "name": "ImageButton"},
    {"id": 5, "name": "ImageView"},
    {"id": 6, "name": "ProgressBar"},
    {"id": 7, "name": "RadioButton"},
    {"id": 8, "name": "RatingBar"},
    {"id": 9, "name": "SeekBar"},
    {"id": 10, "name": "Spinner"},
    {"id": 11, "name": "Switch"},
    {"id": 12, "name": "ToggleButton"},
    {"id": 13, "name": "VideoView"},
    {"id": 14, "name": "TextView"}
]

# sampleXML = 'hierarchy_1.xml'
# tree = ET.parse(sampleXML)
# root = tree.getroot()
#
# feature = []
# for child in root:
#     xmlTraverse(child, feature)

def build_annotation(annotation, feature, imageId, count):
    for feat in feature:
        bounds = list(map(int, feat['bounds']))
        featClass = feat['class']
        segmentation = [[bounds[0], bounds[1], bounds[2], bounds[1], bounds[0],bounds[3], bounds[2], bounds[3]]]
        width = (bounds[2] - bounds[0] + 1)
        height = (bounds[3] - bounds[1] + 1)
        area = width * height
        bbox = [bounds[0], bounds[1], width, height]
        annotation.append({
            "segmentation": segmentation,
            "area": area,
            "iscrowd": 0,
            "image_id": imageId,
            "bbox": bbox,
            "category_id": GUIClass[featClass],
            "id": count
        })
        count = count + 1

def googleDriveCenterNetFormat(dir, fileName, images, imageCount):
    appName = dir.split("\\")[-1]
    imagePath = "/content/drive/MyDrive/Thesis/ReDraw-Final-Google-Play-Dataset/" + appName
    xmlFile = fileName.split(("\\"))[-1]
    imageFile = xmlFile.replace("hierarchy", "screenshot")
    imageFile = imageFile.replace("xml", "png")
    images.append({
        "id": imageCount,
        "width": 1200,
        "height": 1920,
        "file_name": imagePath + "/" + imageFile
    })

def localCenterNetFormat(fileName, images, imageCount):
    imageName = fileName.replace("xml", "png")
    imageName = imageName.replace("hierarchy", "screenshot")
    images.append({
        "id": imageCount,
        "width": 1200,
        "height": 1920,
        "file_name": imageName
    })

def localFasterRCNNFormat(fileName, images, imageCount):
    originalImageName = fileName.replace("xml", "png")
    originalImageName = originalImageName.replace("hierarchy", "screenshot")
    originalImage = cv2.imread(originalImageName)
    copiedImage = np.copy()

def formatter(isGoogleDrive, netType):
    subDir = [x[0] for x in os.walk(baseDir)][1:]
    annotations = []
    images = []
    annoCount = 0
    imageCount = 0
    print("Start extracting...")
    n = len(subDir)
    dirCount = 0
    for dir in subDir[0:1]:
        for file in os.listdir(dir):
            if file.endswith(".xml") and not file.startswith("."):
                fileName = os.path.join(dir, file)
                tree = ET.parse(fileName)
                root = tree.getroot()
                feature = []
                for child in root:
                    try:
                        xmlTraverse(child, feature)
                    except Exception:
                        print(Exception.with_traceback())
                        print(fileName)
                        SystemExit
                build_annotation(annotations, feature, imageCount, annoCount)
                if isGoogleDrive:
                    googleDriveCenterNetFormat(dir, fileName, images, imageCount)
                    break
                else:
                    if netType == "CenterNet":
                        localCenterNetFormat(fileName, images, imageCount)
                    else:
                        pass
                imageCount = imageCount + 1
        dirCount = dirCount + 1
        sys.stdout.write('\r')
        sys.stdout.write("{}".format(dirCount / n))
        sys.stdout.flush()


    ricoAnnotation = {
        "info": "",
        "licenses": "",
        "categories": categories,
        "images": images,
        "annotations": annotations
    }

    dumpPath = "D:\\Vinh\\Share\\shared-repo-for-multi-machines\\Thesis\\annotations\\instances_test.json"
    with open(dumpPath, 'w') as fp:
        json.dump(ricoAnnotation, fp)



if __name__ == "__main__":
    formatter(True, "CenterNet")




