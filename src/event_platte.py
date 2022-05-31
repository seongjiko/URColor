from header.paint_init import *
from header.paint_utils import *

def onMouse(event, x, y, flags, param):
    global pt1, pt2, mouse_mode, draw_mode

    if event == cv2.EVENT_LBUTTONUP: # 왼쪽 버튼 떼기
        pt2 = (x, y) # 종료 좌표 저장
        mouse_mode = 1 # 버튼 떼기 상태 지정

        for i, (x0, y0, w, h) in enumerate(icons):
            if x0 <= x < x0+w and y0 <= y < y0+h:
                if i < 6:
                    mouse_mode = 0
                    draw_mode = i

                else: command(i)
                return
    elif event == cv2.EVENT_LBUTTONDOWN:
        pt1 = (x, y)
        mouse_mode = 2

    if mouse_mode >= 2:
        mouse_mode = 0 if x < 125 else 3
        pt2 = (x, y)

def command(mode):
    global icons, image, Color, hue

    if mode == PALETTE:
        pixel = image[pt2[::-1]]
        x, y, w, h = icons[COLOR]
        image[y:y+h-1, x:x+w-1] = pixel
        Color = tuple(map(int, pixel))

    elif mode == HUE_IDX:
        create_colorPlatte(image, pt2[0], icons[PALETTE])

    cv2.imshow("PaintCV", image)

image = np.full((500, 800, 3), 255, np.uint8)
icons = place_icons(image, (60, 60))
x, y, w, h = icons[-1]

PALETTE_roi = (0, y+h+2, 120, 120)
hueIndex_roi = (0, y+h+124, 120, 15)
icons.append(PALETTE_roi)
icons.append(hueIndex_roi)
create_colorPlatte(image, 0, icons[PALETTE])
create_hueIndex(image, icons[HUE_IDX])

cv2.imshow("PaintCV", image)
cv2.setMouseCallback("PaintCV", onMouse)
cv2.waitKey(0)