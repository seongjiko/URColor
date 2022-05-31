import numpy as np, cv2

def place_icons(image, size):
    icon_name = ["addIcon", "changeIcon", "originIcon", "removeIcon", "resetIcon"]

    icons = [(i%2, i//2, 1, 1) for i in range(len(icon_name))]
    icons = np.multiply(icons, size*2)

    for roi, name in zip(icons, icon_name):
        icon = cv2.imread("images/%s.png" % name, cv2.IMREAD_COLOR)
        if icon is None:
            print("Can't load img")
            continue
        x, y, w, h = roi
        image[y:y+h, x:x+w] = cv2.resize(icon, size)
        return list(icons)

image = np.full((500, 800, 3), 255, np.uint8)
icons = place_icons(image, (60, 60))
cv2.imshow("PaintCV", image)
cv2.waitKey(0)


