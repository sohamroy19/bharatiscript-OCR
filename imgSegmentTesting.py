import cv2
import numpy as np


def imgSegmentTesting(segImg):
    segImg = cv2.threshold(segImg, 0, 1, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1].astype(
        int
    )

    # Sum along columns and segment
    sumAlongColumns = segImg.sum(axis=1)
    begPtr = 0
    endPtr = 0
    count = 0
    rowValues = np.zeros(50, 2)
    noOfRows = 0

    for i in range(len(sumAlongColumns)):
        if begPtr != 0 and sumAlongColumns[i] != 0:
            count += 1
        elif begPtr != 0 and sumAlongColumns[i] == 0:
            endPtr = begPtr + count
            rowValues[noOfRows, 0] = begPtr
            rowValues[noOfRows, 1] = endPtr
            noOfRows += 1
            begPtr = 0
            count = 0
        elif sumAlongColumns[i] != 0:
            begPtr = i
        else:
            begPtr = 0
            count = 0

    # Find the base character
    biggest = 0
    baseRow = 0
    for i in range(noOfRows):
        if rowValues[i, 1] - rowValues[i, 0] >= biggest:
            biggest = rowValues[i, 1] - rowValues[i, 0]
            baseRow = i

    # Return baseBottom and upper images
    if baseRow == 1:
        baseBottomImg = segImg
        # imshow(baseBottomImg)
        upperImg = np.zeros(28, 28)
    else:
        upperImg = segImg[rowValues[0, 0] : rowValues[baseRow - 2, 1], :]
        # imshow(upperImg)
        baseBottomImg = segImg[
            rowValues[baseRow - 1, 0] : rowValues[noOfRows - 1, 1], :
        ]
        # imshow(baseBottomImg)

    return upperImg, baseBottomImg, baseRow
