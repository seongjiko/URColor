import numpy as np
import cv2

def place_icons(image, size):
    icon_name = ["addIcon", "changeIcon", "originIcon", "removeIcon", "resetIcon", "colorIcon", "colorIcon", "colorIcon", "colorIcon", "colorIcon", "colorIcon", "colorIcon"]

    icons = [(i % 2, i//2, 1, 1) for i in range(len(icon_name))]
    icons = np.multiply(icons, size*2)

    for roi, name in zip(icons, icon_name):
        icon = cv2.imread("../images/%s.png" % name, cv2.IMREAD_COLOR)
        if icon is None:
            print("Can't load img")
            continue

        else:
            print(f"success load {name} img file.")

        x, y, w, h = roi
        image[y:y+h, x:x+w] = cv2.resize(icon, size)
    return list(icons)

def create_hueIndex(image, roi):
    x, y, w, h = roi
    index = [[(j, 1, 1) for j in range(w)] for i in range(h)]
    ratios = (180/w, 255, 255)
    hueIndex = np.multiply(index, ratios).astype('uint8')
    image[y:y+h, x:x+w] = cv2.cvtColor(hueIndex, cv2.COLOR_HSV2BGR)

def create_colorPlatte(image, idx, roi):
    x, y, w, h = roi
    hue = idx-x
    palette = [[(hue, j, h-i-1) for j in range(w)] for i in range(h)]

    ratios = (180/w, 255/w, 255/h)
    palette = np.multiply(palette, ratios).astype('uint8')

    image[y:y+h, x:x+w] = cv2.cvtColor(palette, cv2.COLOR_HSV2BGR)

# image = np.full((500, 800, 3), 255, np.uint8)
# icons = place_icons(image, (60, 60))
# cv2.imshow("PaintCV", image)
# cv2.waitKey(0)
