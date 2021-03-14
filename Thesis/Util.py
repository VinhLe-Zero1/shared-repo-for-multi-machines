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


def xmlTraverse(node, feature):
    nodeClass = node.attrib['class'].split('.')[-1]
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

