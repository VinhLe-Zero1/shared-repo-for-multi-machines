import cv2
import re

GUIClass = {'Button':0,
'CheckBox':1,
'Chronometer':2,
'EditText':3,
'ImageButton':4,
'ImageView':5,
'ProgressBar':6,
'RadioButton':7,
'RatingBar':8,
'SeekBar':9,
'Spinner':10,
'Switch':11,
'ToggleButton':12,
'VideoView':13,
'TextView':14}

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

def xmlTraverse(node, feature):
    nodeClass = node.attrib['class'].split('.')[2]
    if nodeClass in GUIClass:
        feature.append({
            'class': nodeClass,
            'bounds': re.findall('\d+',node.attrib['bounds'])})
    for child in node:
        xmlTraverse(child, feature)

def showImg(title, img):
    cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def writeYolov3Labels(feature, path):
    count = 0
    for feat in feature:
        bounds = list(map(int, feat['bounds']))
        featClass = feat['class']

        xcenter = ((bounds[2] - bounds[0] + 1) / 2) / 1200
        ycenter = ((bounds[3] - bounds[1] + 1) / 2) / 1824
        width = (bounds[2] - bounds[0] + 1) / 1200
        height = (bounds[3] - bounds[1] + 1) / 1824
        labelFile = path.format(count)
        with open(labelFile, 'w') as f:
            f.write('{} {} {} {} {}'.format(GUIClass[featClass], xcenter, ycenter, width, height))
        f.close()
        count = count + 1