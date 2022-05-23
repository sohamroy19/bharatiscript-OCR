import tensorflow as tf
from tensorflow import keras
from imgSegment import imgSegment
import cv2
from char_resize import char_resize
from imgSegmentTesting import imgSegmentTesting
import numpy as np


model = keras.models.load_model("convnetBaseBottom.h5")
model1 = keras.models.load_model("convnetUpper.h5")
baseBottomTest = np.zeros((3, 49))
upperTest = np.zeros((3, 49))


fileName = "dataForTesting/Panchatantra _Bharati/Panchatantra _Bharati-02.jpg"
img = cv2.imread(fileName)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
bwImg = 1 - cv2.threshold(img, 0, 1, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1].astype(int)
[rowValues, noOfRows, colValues, noOfCols] = imgSegment(bwImg)

for i in range(noOfRows):
    for j in range(noOfCols):
        segmentedImg = bwImg[
            rowValues[i, 1] : rowValues[i, 2], colValues[j, 1, i] : colValues[j, 2, i]
        ]
        segmentedImg, num = char_resize(segmentedImg)
        fileAdd = "dataForTesting/images/whole/row" + str(i) + "_col" + str(j) + ".png"
        cv2.imwrite(fileAdd, segmentedImg)

        [upperImg, baseBottomImg, baseRow] = imgSegmentTesting(segmentedImg)
        [upperImg, num] = char_resize(upperImg)
        [baseBottomImg, num] = char_resize(baseBottomImg)
        upperImg = upperImg.astype(np.uint8)
        fileAddUp = (
            "dataForTesting/images/upper/row" + str(i) + "_col" + str(j) + ".png"
        )
        cv2.imwrite(fileAddUp, float(upperImg))
        fileAddBase = (
            "dataForTesting/images/base/row" + str(i),
            "_col" + str(j) + ".png",
        )
        cv2.imwrite(fileAddBase, float(baseBottomImg))

        if baseRow == 1:
            baseBottomTest[i, j] = model.predict(baseBottomImg)

        else:
            baseBottomTest[i, j] = model.predict(baseBottomImg)
            upperTest[i, j] = model1.predict(upperImg)
