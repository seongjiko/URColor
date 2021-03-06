import cv2

from header.paint_init import *
from header.paint_utils import *
import tkinter as tk
from tkinter import filedialog

def BGR2H(color):
    V = max(color)
    B, G, R = color
    minGBR = min(color)
    if V == B:
        result = 240 + (60*(R-G)) / (V - minGBR)

    if V == G:
        result = 120 + (60*(B-R)) / (V - minGBR)

    if V == R:
        result = (60*(G-B) / (V - minGBR))

    result = (result/360) * 170

    if result < 0:
        result += 170

    return result

def onMouse(event, x, y, flags, param):
    global pt1, pt2, mouse_mode, draw_mode

    if event == cv2.EVENT_LBUTTONUP: # 왼쪽 버튼 떼기
        pt2 = (x, y) # 종료 좌표 저장
        mouse_mode = 1 # 버튼 떼기 상태 지정

        for i, (x0, y0, w, h) in enumerate(icons):
            if x0 <= x < x0+w and y0 <= y < y0+h:
                if i < 0:
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

color_img = np.array([])
gray_img = np.array([])

tempPos = []
usingStack = False # 스택모드

def command(mode):
    global icons, background, Color, hue, color_img, gray_img, color_img_resize, hsv_img_resize #hsv_img
    global tempPos, gray_img_resize, usingStack
    update = False

    if mode == PALETTE: # HUE에 따른 팔레트
        print('select PALETTE')
        pixel = background[pt2[::-1]]
        x, y, w, h = icons[COLOR]
        background[y:y+h-1, x:x+w-1] = pixel
        Color = tuple(map(int, pixel))

    elif mode == HUE_IDX: # HUE
        create_colorPlatte(background, pt2[0], icons[PALETTE])

    elif mode == OPEN_IMAGE: # 파일 열기
        print('open file')
        root = tk.Tk()
        filePath = filedialog.askopenfilename(initialdir='', title= 'Select file', filetypes=(('jpg files', '*.jpg'), ('png files', '*.png'), ('all files', '*.*')))
        root.destroy()

        color_img = cv2.imread(filePath)
        color_img_resize = cv2.resize(color_img, (680, 500))
        gray_img = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)
        gray_img = cv2.cvtColor(gray_img, cv2.COLOR_GRAY2BGR) # 색상 대입을 위해 3차원화
        gray_img_resize = cv2.resize(gray_img, (680, 500))
        hsv_img_resize = cv2.cvtColor(color_img_resize, cv2.COLOR_BGR2HSV)
        background[:, 120:] = gray_img_resize

        cv2.imwrite('../temp/log.jpg', background)
    elif mode == EXTRACT_COLOR:
        HUE = BGR2H(Color)
        print(HUE)

        if usingStack:
            background[:, 120:] = gray_img_resize

        for i in range(500):
            for j in range(120, 800):
                p = hsv_img_resize[i][j-120]
                if HUE - 20 < p[0] <= HUE + 20 and p[1] != 0 and p[2] != 0:
                    background[i, j] = color_img_resize[i, j-120]
                    tempPos.append([i, j])

        cv2.imwrite('../temp/log.jpg', background)

    elif mode == STACK_COLOR:
        if usingStack :
            usingStack = False
            print('Change stack mode : ON')

        else:
            usingStack = True
            print('Change stack mode : OFF')


    elif mode == CHANGE_COLOR:
        cv2.imwrite('../temp/log.jpg', background)
        for pos in tempPos:
            r, c = pos
            background[r, c] = Color
            tempPos = []


    elif mode == RESET_IMAGE:
        print('reset')
        cv2.imwrite('../temp/log.jpg', background)
        background[:, 120:] = gray_img_resize

    elif mode == SHOW_ORIGIN:
        print('show origin')
        cv2.imwrite('../temp/log.jpg', background)
        for i in range(500):
            for j in range(120, 800):
                background[i, j] = color_img_resize[i, j-120]
        background[:, 120:] = color_img_resize

    elif mode == UNDO:
        background = cv2.imread('../temp/log.jpg')


    elif mode == BLURRING_IMAGE:
        filter = np.ones((5, 5), np.float32) / 25
        background[:, 120:] = cv2.filter2D(background[:, 120:], -1, filter)

    elif mode == SHARPNING_IMAGE:
        filter = np.array([[1, -2, 1], [-2, 5, -2], [1, -2, 1]], np.float32)
        background[:, 120:] = cv2.filter2D(background[:, 120:], -1, filter)

    # elif mode == INVERSION_COLOR:
    #     background[:, 120:] = 255 - background[:, 120:]

    elif mode == SAVE_IMAGE:
        cv2.imwrite('result.png', background[:, 120:])
        print("save!")

    elif mode == EXIT:
        cv2.destroyAllWindows()
        return

    cv2.imshow("PaintCV", background)

background = np.full((500, 800, 3), 255, np.uint8)
icons = place_icons(background, (60, 60))
x, y, w, h = icons[-1]

PALETTE_roi = (0, y+h+2, 120, 120)
hueIndex_roi = (0, y+h+124, 120, 15)
icons.append(PALETTE_roi)
icons.append(hueIndex_roi)
create_colorPlatte(background, 0, icons[PALETTE])
create_hueIndex(background, icons[HUE_IDX])

cv2.imshow("PaintCV", background)
cv2.setMouseCallback("PaintCV", onMouse)
cv2.waitKey(0)
