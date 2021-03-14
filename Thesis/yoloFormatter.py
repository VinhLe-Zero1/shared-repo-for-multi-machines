import os
import sys
from Util import GUIClass, xmlTraverse
import xml.etree.ElementTree as ET

img_width = 1200
img_height = 1920

def getYoloV3Format(feature):
    boxes = []
    for feat in feature:
        bounds = list(map(int, feat['bounds']))
        featClass = feat['class']
        #TODO: fix center formula
        width = (bounds[2] - bounds[0] + 1)
        height = (bounds[3] - bounds[1] + 1)

        xcenter = (bounds[0] + width / 2) / img_width
        ycenter = (bounds[1] + height / 2) / img_height

        widthNorm = width / img_width
        heightNorm = height / img_height

        boxes.append([GUIClass[featClass], xcenter, ycenter, widthNorm, heightNorm])
    return boxes

def formatter():
    baseDir = "D:\\Vinh\\School\\Thesis\\Data\\ReDraw-Final-Google-Play-Dataset\\ReDraw-Final-Google-Play-Dataset"
    subDir = [x[0] for x in os.walk(baseDir)][1:]
    print("Start extracting...")
    n = len(subDir)
    dirCount = 0
    targetDir = "D:\\Vinh\\Share\\shared-repo-for-multi-machines\\Thesis\\yolov3Boxes"

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
                boxes = getYoloV3Format(feature)
                xmlFile = fileName.split(("\\"))[-1]
                txtFile = xmlFile.replace("hierarchy", "screenshot")
                txtFile = txtFile.replace("xml", "txt")
                targetFile = os.path.join(targetDir, txtFile)
                with open(targetFile, "w") as f:
                    for box in boxes:
                        f.writelines("{} {} {} {} {}\n".format(box[0], box[1], box[2], box[3], box[4]))
                f.close()
        dirCount = dirCount + 1
        sys.stdout.write('\r')
        sys.stdout.write("{}".format(dirCount / n))
        sys.stdout.flush()


if __name__ == "__main__":
    formatter()