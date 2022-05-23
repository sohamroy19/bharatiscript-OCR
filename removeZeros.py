import numpy as np


def removeZeros(img):
    # Sum along columns and extract row values
    sumAlongColumns = img.sum(axis=1)
    k = len(sumAlongColumns)
    thresh = sumAlongColumns[0]

    for i in range(k):
        sumAlongColumns[i] = thresh - sumAlongColumns[i]

    begPtr = 0
    endPtr = 0
    rowTable = np.zeros(100, 2)
    rowPoint = 0
    count = 0

    for i in range(k):
        if begPtr != 0 and i == k - 1:
            endPtr = begPtr + count
            rowTable[rowPoint, 0] = begPtr
            rowTable[rowPoint, 1] = endPtr
            rowPoint += 1
            begPtr = 0
            count = 0
        elif begPtr != 0 and sumAlongColumns[i] != 0:
            count += 1
        elif begPtr != 0 and sumAlongColumns[i] == 0:
            endPtr = begPtr + count
            rowTable[rowPoint, 0] = begPtr
            rowTable[rowPoint, 1] = endPtr
            rowPoint += 1
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
        for i in range(rowPoint - 1):
            if rowTable[i, 0] == 0:
                break
            elif abs(rowTable[i + 1, 0] - rowTable[i, 1]) <= 10:
                rowTable[i, 1] = rowTable[i + 1, 1]
                for j in range(i + 1, rowPoint - 1):
                    rowTable[j, 0] = rowTable[j + 1, 0]
                    rowTable[j, 1] = rowTable[j + 1, 1]
                cnt += 1
                rowTable[rowPoint - 1, 0] = 0
                rowTable[rowPoint - 1, 1] = 0
        rowPoint -= cnt

    # Segment the image
    for i in range(rowPoint):
        segImg = img[rowTable[i, 0] - 1 : rowTable[i, 1] - 1, :]

    return segImg
