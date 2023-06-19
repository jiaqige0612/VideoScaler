import numpy as np
def bicubic_interpolation(image, scale=2):
    new_image = np.zeros((image.shape[0]*scale, image.shape[1]*scale, image.shape[2]), dtype=np.float32)

    for c in range(3):
        img = image[:, :, c]
        height, width = img.shape
        new_height = height * scale
        new_width = width * scale
        new_img = np.zeros((new_height, new_width), dtype=np.float32)

        for i in range(new_height):
            for j in range(new_width):
                x = i / scale
                y = j / scale

                # get floor number
                x_floor = int(np.floor(x))
                y_floor = int(np.floor(y))

                # Bicubic interpolation weights
                dx = x - x_floor
                dy = y - y_floor
                wx = np.array([cubic_weight(c) for c in cubic_neighbors(dx)])
                wy = np.array([cubic_weight(c) for c in cubic_neighbors(dy)])

                for k in range(-1, 3):
                    for l in range(-1, 3):
                        img_x = min(max(x_floor + k, 0), height - 1)
                        img_y = min(max(y_floor + l, 0), width - 1)
                        new_img[i, j] += img[img_x, img_y] * wx[k + 1] * wy[l + 1]

        new_image[:, :, c] = new_img[:, :, ]
    return new_image

# weight
def cubic_weight(t):
    if abs(t) <= 1:
        return 1.5 * abs(t)**3 - 2.5 * abs(t)**2 + 1
    # smaller weight away from the target
    elif abs(t) < 2:
        return -0.5 * abs(t)**3 + 2.5 * abs(t)**2 - 4 * abs(t) + 2
    else:
        return 0
#fixed range
def cubic_neighbors(t):
    return [t + 1, t, 1 - t, 2 - t]