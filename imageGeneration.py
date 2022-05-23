import cv2
import numpy as np

from imgSegment import imgSegment
from char_resize import char_resize
from generateData import generateData

# Read the image
images = np.zeros((28, 28, 52 * 42 * 17))
pointer = 1
baseBottom = [
    "091A",
    "091B",
    "091C",
    "091D",
    "091E",
    "091F",
    "092A",
    "092B",
    "092C",
    "092D",
    "092E",
    "092F",
    "095E",
    "0915",
    "0916",
    "0917",
    "0918",
    "0919",
    "0920",
    "0921",
    "0922",
    "0923",
    "0924",
    "0925",
    "0926",
    "0927",
    "0928",
    "0929",
    "0930",
    "0931",
    "0932",
    "0933",
    "0934",
    "0935",
    "0936",
    "0937",
    "0938",
    "0939",
]
upper = [
    "093E",
    "093F",
    "094A",
    "094B",
    "094C",
    "0905",
    "0940",
    "0941",
    "0942",
    "0943",
    "0944",
    "0946",
    "0947",
    "0948",
]

dirNamesArray = [baseBottom, upper]
dirNames = ["baseBottom", "upper"]

for i in range(len(dirNames)):
    dirName = dirNames[i]
    files = dirNamesArray[i]

    for classNum in range(len(files)):
        fileName = "dataForSegmenting/" + dirName + "/" + files[classNum] + ".png"
        tempImg = cv2.imread(fileName, cv2.IMREAD_GRAYSCALE)
        bwImg = 1 - cv2.threshold(tempImg, 0, 1, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[
            1
        ].astype(int)
        counter = 1

        # Getting the values for bounding box
        rowValues, noOfRows, colValues, noOfCols = imgSegment(bwImg)

        # Object extraction
        for j in range(noOfRows):
            for k in range(noOfCols(j)):
                segmentedImg = bwImg[
                    rowValues[j, 0] - 1 : rowValues[j, 1] - 1,
                    colValues[k, 0, j] : colValues[k, 1, j],
                ]
                segmentedImg, num = char_resize(segmentedImg)
                segmentedImg = cv2.threshold(
                    segmentedImg, 0, 1, cv2.THRESH_BINARY + cv2.THRESH_OTSU
                )[1].astype(int)
                counter, pointer, images = generateData(
                    segmentedImg, counter, dirName, files[classNum], pointer, images
                )
