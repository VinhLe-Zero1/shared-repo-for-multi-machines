from Util import xmlTraverse, GUIClass
import xml.etree.ElementTree as ET
import os
import json

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
        featClass = feat['Class']
        segmentation = [[bounds[0], bounds[1], bounds[2], bounds[1], bounds[0],bounds[3], bounds[2], bounds[3]]]
        width = (bounds[2] - bounds[0] + 1)
        height = (bounds[3] - bounds[1] + 1)
        area = width * height
        bbox = [bounds[0], bounds[1], width, height]
        annotation.append({
            "segmentation": segmentation,
            "area": area,
            "iscrowd": 0,
            "image_id": id,
            "bbox": bbox,
            "category_id": GUIClass[featClass],
            "id": count
        })
        count = count + 1


baseDir = "D:\\Vinh\\School\\Thesis\\Data\\ReDraw-Final-Google-Play-Dataset\\ReDraw-Final-Google-Play-Dataset"
subDir = [x[0] for x in os.walk(baseDir)]
annotations = []
images = []
annoCount = 0
imageCount = 0
for dir in subDir:
    path = os.path.join(baseDir, dir)
    for file in os.listdir(path):
        if file.endswith(".xml"):
            fileName = os.path.join(path, file)
            tree = ET.parse(fileName)
            root = tree.getroot()
            feature = []
            xmlTraverse(root, feature)
            build_annotation(annotations, feature, imageCount, annoCount)
            images.append({
                "id": imageCount,
                "width": 1200,
                "height": 1824,
                "file_name": fileName.replace("xml","jpg")
            })
            imageCount = imageCount + 1



ricoAnnotation = {
    "info": "",
    "licenses": "",
    "categories": categories,
    "images": images,
    "annotations": annotations
}

dumpPath = ""
with open(dumpPath, 'w') as fp:
    json.dump(ricoAnnotation, fp)






