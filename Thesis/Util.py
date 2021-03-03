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
        #TODO: fix center formula
        width = (bounds[2] - bounds[0] + 1)
        height = (bounds[3] - bounds[1] + 1)

        xcenter = (bounds[0] + width / 2) / 1200
        ycenter = (bounds[1] + height / 2) / 1824
        widthNorm = (bounds[2] - bounds[0] + 1) / 1200
        heightNorm = (bounds[3] - bounds[1] + 1) / 1824
        labelFile = path.format(count)
        with open(labelFile, 'w') as f:
            f.write('{} {} {} {} {}'.format(GUIClass[featClass], xcenter, ycenter, widthNorm, heightNorm))
        f.close()
        count = count + 1