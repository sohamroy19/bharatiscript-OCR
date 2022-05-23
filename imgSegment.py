import cv2
import numpy as np


def imgSegment(img):
    # Sum along columns and segment
    img = cv2.threshold(img, 0, 1, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1].astype(int)
    sumAlongColumns = img.sum(1)
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

    # Replace with proper row values
    for k in range(2):
        cnt = 0
        for i in range(noOfRows - 1):
            if rowValues[i, 0] == 0:
                break
            elif abs(rowValues[i + 1, 0] - rowValues[i, 1]) < 7:
                rowValues[i, 1] = rowValues[i + 1, 1]
                for j in range(i + 1, noOfRows - 1):
                    rowValues[j, 0] = rowValues[j + 1, 0]
                    rowValues[j, 1] = rowValues[j + 1, 1]
                cnt += 1
                rowValues[noOfRows, 0] = 0
                rowValues[noOfRows, 1] = 0
        noOfRows = noOfRows - cnt

    # Segmenting the image into rows
    colValues = np.zeros((100, 2, noOfRows))
    noOfCols = np.zeros((1, noOfRows))

    for i in range(noOfRows):
        segImg = img[rowValues[i, 0] : rowValues[i, 1], :]

        # Sum along rows
        sumAlongRows = sum(segImg, 1)
        begPtr = 0
        endPtr = 0
        count = 0

        for j in range(len(sumAlongRows)):
            if begPtr != 0 and sumAlongRows(j) != 0:
                count += 1
            elif begPtr != 0 and sumAlongRows(j) == 0:
                endPtr = begPtr + count
                colValues[noOfCols[i], 0, i] = begPtr
                colValues[noOfCols[i], 1, i] = endPtr
                noOfCols[i] += 1
                begPtr = 0
            elif sumAlongRows(j) != 0:
                begPtr = j
            else:
                begPtr = 0
                count = 0

    return rowValues, noOfRows, colValues, noOfCols
