import numpy as np
import cv2
import numpy as np
import cv2


def imgPad(img):
    lenY = len(img)
    lenX = len(img[0])

    print(lenY)
    print(lenX)

    padded = np.empty(shape=(lenY + 10, lenX + 10, 3), dtype=int)
    padded[5:lenY + 5, 5:lenX + 5, :] = img

    lenPY = lenY + 10
    lenPX = lenX + 10

    for i in range(5, 0, -1):
        for x in range(i, lenPX - i):
            padded[i - 1, x, :] = padded[i, x, :]
        for x in range(i, lenPX - i):
            padded[lenPY - i, x, :] = padded[lenPY - i - 1, x, :]
        for y in range(i, lenPY - i):
            padded[y, i - 1, :] = padded[y, i, :]
        for y in range(i, lenPY - i):
            padded[y, lenPX - i, :] = padded[y, lenPX - i - 1, :]

        padded[i - 1, i - 1, :] = padded[i, i, :]
        padded[i - 1, lenPX - i, :] = padded[i, lenPX - i - 1, :]
        padded[lenPY - i, i - 1, :] = padded[lenPY - i - 1, i, :]
        padded[lenPY - i, lenPX - i, :] = padded[lenPY - i - 1, lenPX - i - 1, :]

    print(np.shape(padded))

    return padded


def imgExpand(img):
    lenX = len(img[0]) * 2
    lenY = len(img) * 2

    scaled = np.zeros(shape=(lenY, lenX, 3), dtype=int)

    for c in range(0, 3):
        for x in range(0, lenY):
            for y in range(0, lenX):
                if ((x % 2 == 0) and (y % 2 == 0)):
                    scaled[x][y][c] = int(img[int(x / 2)][int(y / 2)][c])

    print(np.shape(scaled))
    return scaled


def stage1weights(img, x, y, esf):
    coefs = [-0.125, 0.625, 0.625, -0.125]

    interpX45 = coefs[0] * img[x - 3][y - 3] + coefs[1] * img[x - 1][y - 1] + coefs[2] * img[x + 1][y + 1] + coefs[3] * \
                img[x + 3][y + 3]
    interpX135 = coefs[0] * img[x - 3][y + 3] + coefs[1] * img[x - 1][y + 1] + coefs[2] * img[x + 1][y - 1] + coefs[3] * \
                 img[x + 3][y - 3]

    interpA45 = (coefs[0] * img[x - 3][y - 3]) + (coefs[1] * img[x - 1][y - 1]) + (coefs[2] * img[x + 3][y + 3]) + (
                coefs[3] * img[x + 5][y + 5])
    interpA135 = (coefs[0] * img[x + 5][y - 3]) + (coefs[1] * img[x + 3][y - 1]) + (coefs[2] * img[x - 1][y + 3]) + (
                coefs[3] * img[x - 3][y + 5])

    interpB45 = (coefs[0] * img[x + 5][y + 3]) + (coefs[1] * img[x + 3][y + 1]) + (coefs[2] * img[x - 1][y - 3]) + (
                coefs[3] * img[x - 3][y - 5])
    interpB135 = (coefs[0] * img[x + 5][y - 5]) + (coefs[1] * img[x + 3][y - 3]) + (coefs[2] * img[x - 1][y + 1]) + (
                coefs[3] * img[x - 3][y + 3])

    interpC45 = (coefs[0] * img[x + 3][y + 3]) + (coefs[1] * img[x + 1][y + 1]) + (coefs[2] * img[x - 3][y - 3]) + (
                coefs[3] * img[x - 5][y - 5])
    interpC135 = (coefs[0] * img[x + 3][y - 5]) + (coefs[1] * img[x + 1][y - 3]) + (coefs[2] * img[x - 3][y + 1]) + (
                coefs[3] * img[x - 5][y + 3])

    interpD45 = (coefs[0] * img[x + 3][y + 5]) + (coefs[1] * img[x + 1][y + 3]) + (coefs[2] * img[x - 3][y - 1]) + (
                coefs[3] * img[x - 5][y - 3])
    interpD135 = (coefs[0] * img[x - 5][y + 5]) + (coefs[1] * img[x - 3][y + 3]) + (coefs[2] * img[x + 1][y - 1]) + (
                coefs[3] * img[x + 3][y - 3])

    e45 = abs(interpA45 - img[x + 1][y + 1]) + abs(interpB45 - img[x + 1][y - 1]) + abs(
        interpC45 - img[x - 1][y - 1]) + abs(interpD45 - img[x - 1][y + 1])
    e135 = abs(interpA135 - img[x + 1][y + 1]) + abs(interpB135 - img[x + 1][y - 1]) + abs(
        interpC135 - img[x - 1][y - 1]) + abs(interpD135 - img[x - 1][y + 1])

    esf45 = pow(e45, esf)
    esf135 = pow(e135, esf)

    w45 = (esf135 + 0.001) / (esf135 + esf45 + 0.002)
    w135 = 1 - w45

    # print(interpX45, interpX135)

    return w45 * interpX45 + w135 * interpX135


def stage2weights(img, x, y, esf):
    coefs = [-0.125, 0.625, 0.625, -0.125]

    interpX0 = (coefs[0] * img[x + 3][y]) + (coefs[1] * img[x + 1][y]) + (coefs[2] * img[x - 1][y]) + (
                coefs[3] * img[x - 3][y])
    interpX90 = (coefs[0] * img[x][y + 3]) + (coefs[1] * img[x][y + 1]) + (coefs[2] * img[x][y - 1]) + (
                coefs[3] * img[x][y - 3])

    interpA0 = (coefs[0] * img[x - 3][y]) + (coefs[1] * img[x - 1][y]) + (coefs[2] * img[x + 3][y]) + (
                coefs[3] * img[x + 5][y])
    interpA90 = (coefs[0] * img[x + 1][y + 4]) + (coefs[1] * img[x + 1][y + 2]) + (coefs[2] * img[x + 1][y - 2]) + (
                coefs[3] * img[x + 1][y - 4])

    interpB0 = (coefs[0] * img[x - 4][y - 1]) + (coefs[1] * img[x - 2][y - 1]) + (coefs[2] * img[x + 2][y - 1]) + (
                coefs[3] * img[x + 4][y - 1])
    interpB90 = (coefs[0] * img[x][y + 3]) + (coefs[1] * img[x][y + 1]) + (coefs[2] * img[x][y - 3]) + (
                coefs[3] * img[x][y - 5])

    interpC0 = (coefs[0] * img[x - 5][y]) + (coefs[1] * img[x - 3][y]) + (coefs[2] * img[x + 1][y]) + (
                coefs[3] * img[x + 3][y])
    interpC90 = (coefs[0] * img[x - 1][y + 4]) + (coefs[1] * img[x - 1][y + 2]) + (coefs[2] * img[x - 1][y - 2]) + (
                coefs[3] * img[x - 1][y - 4])

    interpD0 = (coefs[0] * img[x - 4][y + 1]) + (coefs[1] * img[x - 2][y + 1]) + (coefs[2] * img[x + 2][y + 1]) + (
                coefs[3] * img[x + 4][y + 1])
    interpD90 = (coefs[0] * img[x][y + 5]) + (coefs[1] * img[x][y + 3]) + (coefs[2] * img[x][y - 1]) + (
                coefs[3] * img[x][y - 3])

    e0 = abs(interpA0 - img[x + 1][y + 1]) + abs(interpB0 - img[x + 1][y - 1]) + abs(
        interpC0 - img[x - 1][y - 1]) + abs(interpD0 - img[x - 1][y + 1])
    e90 = abs(interpA90 - img[x + 1][y + 1]) + abs(interpB90 - img[x + 1][y - 1]) + abs(
        interpC90 - img[x - 1][y - 1]) + abs(interpD90 - img[x - 1][y + 1])

    esf0 = pow(e0, esf)
    esf90 = pow(e90, esf)

    w0 = (esf0 + 0.001) / ((esf90 + esf0) + 0.002)
    w90 = 1 - w0

    return w0 * interpX0 + w90 * interpX90


def stage1(img, esf):
  for x in range(5,len(img)-5,2):
    for y in range(5,len(img)-5,2):
      img[x][y] = stage1weights(img, x, y, esf)
        
  return img


def stage2(img, esf):
  for y in range(10, len(img)-10,1):
    if(y%2 == 0):
      p = 11
    else:
      p = 10
    for x in range(p, len(img)-10, 2):
      img[x][y] = stage2weights(img, x, y, esf)
      
  return img


def SRwLocalStructEst(img, esf=3):
    padded = imgPad(img)
    scaled = imgExpand(padded)

    stage1(scaled[:, :, 0], esf)
    stage1(scaled[:, :, 1], esf)
    stage1(scaled[:, :, 2], esf)

    stage2(scaled[:, :, 0], esf)
    stage2(scaled[:, :, 1], esf)
    stage2(scaled[:, :, 2], esf)

    return scaled[10:len(scaled[0]) - 10, 10:len(scaled) - 10, :]
def LocalStruct(img, scale):
    if scale % 2 != 0:
        print("Scale not supported by this mode, change to bicubic mode")
        return cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
    else:
        print("Local Structure")
        final_image = img
        for i in range (scale//2):
            final_image = SRwLocalStructEst(final_image, esf=3)

        return final_image




