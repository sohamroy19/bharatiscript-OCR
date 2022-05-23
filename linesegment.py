import cv2
import numpy as np
import matplotlib.pyplot as plt

# Read image
filename = "dataForTesting/images/whole/row1_col3.png"
testing = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
bw = 1 - cv2.threshold(testing, 0, 1, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1].astype(
    int
)

# Sum along columns and extract row values
sumAlongColumns = bw.sum(axis=1)
k = len(sumAlongColumns)
thresh = sumAlongColumns[0]

for i in range(k):
    sumAlongColumns[i] = thresh - sumAlongColumns[i]

begPtr = 0
endPtr = 0
rowTable = np.zeros((100, 2), dtype=int)
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
        elif abs(rowTable[i + 1, 0] - rowTable[i, 1]) < 7:
            rowTable[i, 1] = rowTable[i + 1, 1]
            for j in range(i + 1, rowPoint - 1):
                rowTable[j, 0] = rowTable[j + 1, 0]
                rowTable[j, 1] = rowTable[j + 1, 1]
            cnt += 1
            rowTable[rowPoint - 1, 0] = 0
            rowTable[rowPoint - 1, 1] = 0
    rowPoint -= cnt

# Segment rows of images
colTable = np.zeros((100, 2, rowPoint), dtype=int)
colPoint = np.zeros((rowPoint), dtype=int)
for i in range(rowPoint):
    segImg = bw[rowTable[i, 0] - 1 : rowTable[i, 1] - 1, :]

    # Segment along columns and extract column values
    sumAlongRows = segImg.sum(axis=0)
    colptr = 0
    endPtr = 0
    count = 0
    thresh = sumAlongRows[0]
    s = len(sumAlongRows)

    for j in range(s):
        sumAlongRows[j] = thresh - sumAlongRows[j]

    for j in range(s):
        if colptr != 0 and j == s:
            endPtr = colptr + count
            colTable[colPoint[i], 0, i] = colptr
            colTable[colPoint[i], 1, i] = endPtr
            colPoint[i] += 1
            colptr = 0
        elif colptr != 0 and sumAlongRows[j] != 0:
            count += 1
        elif colptr != 0 and sumAlongRows[j] == 0:
            endPtr = colptr + count
            colTable[colPoint[i], 0, i] = colptr
            colTable[colPoint[i], 1, i] = endPtr
            colPoint[i] += 1
            colptr = 0
        elif sumAlongRows[j] != 0:
            colptr = j
        else:
            colptr = 0
            count = 0

plt.imshow(testing)

# for i in range(rowPoint):
#     plt.plot([0, 2000], [rowTable[i, 0], rowTable[i, 0]], "white")
#     plt.plot([0, 2000], [rowTable[i, 1], rowTable[i, 1]], "white")
#     for j in range(colPoint[i]):
#         plt.plot([colTable[j, 0, i], colTable[j, 0, i]], [0, 1200], "white")
#         plt.plot([colTable[j, 1, i], colTable[j, 1, i]], [0, 1200], "white")

plt.show()
