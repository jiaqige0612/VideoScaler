import numpy as np
import cv2

def imgPad(img):
    
    lenY = len(img)
    lenX = len(img[0])

    padded = np.empty(shape = (lenX+10,lenY+10,3), dtype = int)
    padded[5:lenX+5,5:lenY+5,:] = img

    lenPY = lenY+10
    lenPX = lenX+10

    for i in range(5,0,-1):
      for x in range(i,lenPX-i):
        padded[i-1,x,:] = padded[i,x,:]
      for x in range(i,lenPX-i):
        padded[lenPY-i,x,:] = padded[lenPY-i-1,x,:]
      for y in range(i,lenPY-i):
        padded[y,i-1,:] = padded[y,i,:]
      for y in range(i,lenPY-i):
        padded[y,lenPX-i,:] = padded[y,lenPX-i-1,:]

      padded[i-1,i-1,:] = padded[i,i,:]
      padded[i-1,lenPX-i,:] = padded[i,lenPX-i-1,:]
      padded[lenPY-i,i-1,:] = padded[lenPY-i-1,i,:]
      padded[lenPY-i,lenPX-i,:] = padded[lenPY-i-1,lenPX-i-1,:]


    return padded

def imgExpand(img):
  
  lenX = len(img[0])*2
  lenY = len(img)*2

  scaled = np.zeros(shape = (lenX,lenY,3), dtype = int)

  for c in range(0,3):
    for x in range(0,lenY):
      for y in range(0,lenX):
        if((x%2 == 0) and (y%2 == 0)):

          scaled[x][y][c] = int(img[int(x/2)][int(y/2)][c])

  return scaled




def stage1weights(img, x, y, esf):

    coefs = [-0.125, 0.625, 0.625, -0.125]



    interpX45 =  coefs[0]*img[x-3][y-3] + coefs[1]*img[x-1][y-1] + coefs[2]*img[x+1][y+1] + coefs[3]*img[x+3][y+3]
    interpX135 = coefs[0]*img[x-3][y+3] + coefs[1]*img[x-1][y+1] + coefs[2]*img[x+1][y-1] + coefs[3]*img[x+3][y-3]

    interpA45 =  (coefs[0]*img[x-3][y-3]) + (coefs[1]*img[x-1][y-1]) + (coefs[2]*img[x+3][y+3]) + (coefs[3]*img[x+5][y+5])
    interpA135 = (coefs[0]*img[x+5][y-3]) + (coefs[1]*img[x+3][y-1]) + (coefs[2]*img[x-1][y+3]) + (coefs[3]*img[x-3][y+5])

    interpB45 =  (coefs[0]*img[x+5][y+3]) + (coefs[1]*img[x+3][y+1]) + (coefs[2]*img[x-1][y-3]) + (coefs[3]*img[x-3][y-5])
    interpB135 = (coefs[0]*img[x+5][y-5]) + (coefs[1]*img[x+3][y-3]) + (coefs[2]*img[x-1][y+1]) + (coefs[3]*img[x-3][y+3])

    interpC45 =  (coefs[0]*img[x+3][y+3]) + (coefs[1]*img[x+1][y+1]) + (coefs[2]*img[x-3][y-3]) + (coefs[3]*img[x-5][y-5])
    interpC135 = (coefs[0]*img[x+3][y-5]) +  (coefs[1]*img[x+1][y-3]) + (coefs[2]*img[x-3][y+1]) + (coefs[3]*img[x-5][y+3])

    interpD45 =  (coefs[0]*img[x+3][y+5]) + (coefs[1]*img[x+1][y+3]) + (coefs[2]*img[x-3][y-1]) + (coefs[3]*img[x-5][y-3])
    interpD135 = (coefs[0]*img[x-5][y+5]) + (coefs[1]*img[x-3][y+3]) + (coefs[2]*img[x+1][y-1]) + (coefs[3]*img[x+3][y-3])

    e45 = abs(interpA45-img[x+1][y+1]) + abs(interpB45 - img[x+1][y-1]) + abs(interpC45 - img[x-1][y-1]) + abs(interpD45 - img[x-1][y+1])
    e135 = abs(interpA135-img[x+1][y+1]) + abs(interpB135 - img[x+1][y-1]) + abs(interpC135 - img[x-1][y-1]) + abs(interpD135 - img[x-1][y+1])

    esf45 = pow(e45, esf)
    esf135 = pow(e135, esf)

    w45 = (esf135 + 0.001) / (esf135+esf45+0.002)
    w135 = 1 - w45

    #print(interpX45, interpX135)

    return w45*interpX45 + w135*interpX135



def stage2weights(img, x, y, esf):

  coefs = [-0.125, 0.625, 0.625, -0.125]

  interpX0 =  (coefs[0]*img[x+3][y]) + (coefs[1]*img[x+1][y]) + (coefs[2]*img[x-1][y]) + (coefs[3]*img[x-3][y])
  interpX90 = (coefs[0]*img[x][y+3]) + (coefs[1]*img[x][y+1]) + (coefs[2]*img[x][y-1]) + (coefs[3]*img[x][y-3])

  interpA0 = (coefs[0]*img[x-3][y]) + (coefs[1]*img[x-1][y]) + (coefs[2]*img[x+3][y]) + (coefs[3]*img[x+5][y])
  interpA90 = (coefs[0]*img[x+1][y+4]) + (coefs[1]*img[x+1][y+2]) + (coefs[2]*img[x+1][y-2]) + (coefs[3]*img[x+1][y-4])

  interpB0 = (coefs[0]*img[x-4][y-1]) + (coefs[1]*img[x-2][y-1]) + (coefs[2]*img[x+2][y-1]) + (coefs[3]*img[x+4][y-1])
  interpB90 = (coefs[0]*img[x][y+3]) + (coefs[1]*img[x][y+1]) + (coefs[2]*img[x][y-3]) + (coefs[3]*img[x][y-5])

  interpC0 = (coefs[0]*img[x-5][y]) + (coefs[1]*img[x-3][y]) + (coefs[2]*img[x+1][y]) + (coefs[3]*img[x+3][y])
  interpC90 = (coefs[0]*img[x-1][y+4]) + (coefs[1]*img[x-1][y+2]) + (coefs[2]*img[x-1][y-2]) + (coefs[3]*img[x-1][y-4])

  interpD0 = (coefs[0]*img[x-4][y+1]) + (coefs[1]*img[x-2][y+1]) + (coefs[2]*img[x+2][y+1]) + (coefs[3]*img[x+4][y+1])
  interpD90 = (coefs[0]*img[x][y+5]) + (coefs[1]*img[x][y+3]) + (coefs[2]*img[x][y-1]) + (coefs[3]*img[x][y-3])

  e0 = abs(interpA0-img[x+1][y+1]) + abs(interpB0 - img[x+1][y-1]) + abs(interpC0 - img[x-1][y-1]) + abs(interpD0 - img[x-1][y+1])
  e90 = abs(interpA90-img[x+1][y+1]) + abs(interpB90 - img[x+1][y-1]) + abs(interpC90 - img[x-1][y-1]) + abs(interpD90 - img[x-1][y+1])

  esf0 = pow(e0, esf)
  esf90 = pow(e90, esf)

  w0 = (esf0 + 0.001) / ((esf90+esf0) + 0.002)
  w90 = 1 - w0

  return w0*interpX0 + w90*interpX90






def stage1(img, esf):
  for x in range(5,len(img)-5):
    for y in range(5,len(img)-5):
      if((x%2 == 0) or (y%2 == 0)):
        continue
      else:
        img[x][y] = stage1weights(img, x, y, esf)
  return img


def stage2(img, esf):
  for x in range(10, len(img)-10):
    for y in range(10, len(img)-10):
      if((x+y)%2 ==0):
        continue
      else:
        img[x][y] = stage2weights(img, x, y, esf)
  return img

def SRwLocalStructEst(img, esf = 2):

  padded = imgPad(img)
  scaled = imgExpand(padded)

  stage1(scaled[:,:,0], esf)
  stage1(scaled[:,:,1], esf)
  stage1(scaled[:,:,2], esf)

  stage2(scaled[:,:,0], esf)
  stage2(scaled[:,:,1], esf)
  stage2(scaled[:,:,2], esf)

  return scaled[10:len(scaled[0])-10,10:len(scaled)-10,:]


def divide_image_into_blocks(image, block_size):
    #divide into 64 by 64 blocks
    #output 128 by 128 blocks
    height, width, _ = image.shape
    num_row_blocks = height // block_size
    num_col_blocks = width // block_size

    blocks = []
    for i in range(num_row_blocks):
        for j in range(num_col_blocks):
            block = image[i * block_size:(i + 1) * block_size, j * block_size:(j + 1) * block_size, :]
            blocks.append(block)

    return blocks

def combine_blocks(blocks, image_shape):
    height, width, _ = image_shape
    block_size = blocks[0].shape[0]
    num_row_blocks = height // block_size
    num_col_blocks = width // block_size

    combined_image = np.zeros(image_shape, dtype=np.float32)
    index = 0
    for i in range(num_row_blocks):
        for j in range(num_col_blocks):
            block = blocks[index]
            index += 1
            combined_image[i * block_size:(i + 1) * block_size, j * block_size:(j + 1) * block_size] = block

    return combined_image

def SRwLocalStruct(img, esf = 2):
    blocks = []
    sr_blocks = []
    blocks = divide_image_into_blocks(img, 64)
    sr_image = np.zeros([img.shape[0]*esf, img.shape[1]*esf, img.shape[2]], dtype = np.float32)

    for i in range(np.shape(blocks)[0]):
      sr_blocks.append(SRwLocalStructEst(blocks[i], esf))
      print(i)

    combined_image = combine_blocks(sr_blocks, (img.shape[0]*esf, img.shape[1]*esf, img.shape[2]))

    return combined_image

def zero_pad_image(image, desired_size = 64):
    height, width, _ = image.shape
    padded_height = int(np.ceil(height / desired_size) * desired_size)
    padded_width = int(np.ceil(width / desired_size) * desired_size)

    pad_height_top = int((padded_height - height) / 2)
    pad_height_bottom = padded_height - height - pad_height_top
    pad_width_left = int((padded_width - width) / 2)
    pad_width_right = padded_width - width - pad_width_left

    padded_image = cv2.copyMakeBorder(image, pad_height_top, pad_height_bottom, pad_width_left, pad_width_right, cv2.BORDER_CONSTANT, value=0)

    return padded_image

def remove_zero_padding(padded_image, original_height, original_width):
    padded_height, padded_width, _ = padded_image.shape

    pad_height_top = int((padded_height - original_height) / 2)
    pad_height_bottom = padded_height - original_height - pad_height_top
    pad_width_left = int((padded_width - original_width) / 2)
    pad_width_right = padded_width - original_width - pad_width_left

    cropped_image = padded_image[pad_height_top:pad_height_top+original_height, pad_width_left:pad_width_left+original_width]

    return cropped_image

def LocalStruct(img, scale):
    pad_img = zero_pad_image(img, desired_size=64)
    if scale % 2 != 0:
        print("Scale not supported by this mode, change to bicubic mode")
        return cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
    else:
        print("Local Structure")
        combined_image = pad_img
        for i in range (scale//2):
            combined_image = SRwLocalStruct(combined_image, esf=2)

        combined_image_cropped = remove_zero_padding(combined_image, np.shape(img)[0] * scale,
                                                         np.shape(img)[1] * scale)

        return combined_image_cropped




