import cv2
import numpy as np


def generateData(A, counter, dir, className, pointer, images):
    # move character vertically
    for j in range(-2, 3):
        # count += 1
        J = cv2.warpAffine(A, np.float32([[1, 0, 0], [0, 1, j]]), A.shape)
        cv2.imwrite(
            J,
            "dataForTrainingbn/"
            + dir
            + "/"
            + className
            + "/"
            + className
            + "_"
            + str(counter)
            + ".png",
        )
        images[:, :, pointer] = J
        pointer += 1
        counter += 1
        # figure
        # cv2.imshow(J)

    # move character horizontally
    for i in [-2, -1, 1, 2]:
        # count += 1
        J = cv2.warpAffine(A, np.float32([[1, 0, i], [0, 1, 0]]), A.shape)
        cv2.imwrite(
            J,
            "dataForTrainingbn/"
            + dir
            + "/"
            + className
            + "/"
            + className
            + "_"
            + str(counter)
            + ".png",
        )
        images[:, :, pointer] = J
        pointer += 1
        counter += 1
        # figure
        # cv2.imshow(J)

    # move character diagonally
    for i in [-2, -1, 1, 2]:
        # count += 1
        J = cv2.warpAffine(A, np.float32([[1, 0, i], [0, 1, i]]), A.shape)
        cv2.imwrite(
            J,
            "dataForTrainingbn/"
            + dir
            + "/"
            + className
            + "/"
            + className
            + "_"
            + str(counter)
            + ".png",
        )
        images[:, :, pointer] = J
        pointer += 1
        counter += 1
        # figure
        # cv2.imshow(J)

        # count += 1
        J = cv2.warpAffine(A, np.float32([[1, 0, i], [0, 1, -i]]), A.shape)
        cv2.imwrite(
            J,
            "dataForTrainingbn/"
            + dir
            + "/"
            + className
            + "/"
            + className
            + "_"
            + str(counter)
            + ".png",
        )
        images[:, :, pointer] = J
        pointer += 1
        counter += 1
        # figure
        # cv2.imshow(J)

    return counter, pointer, images
