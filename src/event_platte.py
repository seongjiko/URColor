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
    # b, g, r = color
    # b_ = b / 255
    # g_ = g / 255
    # r_ = r / 255
    #
    # cmax = max([b_, g_, r_])
    # cmin = min([b_, g_, r_])
    # result = 0
    # temp = cmax - cmin
    #
    # if cmax == b_:
    #     result = 60 * ((r_ - g_) / temp + 4)
    #
    # if cmax == g_:
    #     result = 60 * ((b_ - r_) / temp + 2)
    #
    # if cmax == r_:
    #     result = 60 * (((g_ - b_) / temp) % 6)

    #return result

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
    if mode == PALETTE:
        print('select PALETTE')
        pixel = background[pt2[::-1]]
        x, y, w, h = icons[COLOR]
        background[y:y+h-1, x:x+w-1] = pixel
        Color = tuple(map(int, pixel))

    elif mode == HUE_IDX:
        create_colorPlatte(background, pt2[0], icons[PALETTE])

    elif mode == OPEN_IMAGE:
        print('open file')
        root = tk.Tk()
        filePath = filedialog.askopenfilename(initialdir='', title= 'Select file', filetypes=(('png files', '*.png'), ('jpg files', '*.jpg'), ('all files', '*.*')))
        root.destroy()

        color_img = cv2.imread(filePath)
        color_img_resize = cv2.resize(color_img, (680, 500))
        gray_img = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)
        gray_img = cv2.cvtColor(gray_img, cv2.COLOR_GRAY2BGR) # 색상 대입을 위해 3차원화
        gray_img_resize = cv2.resize(gray_img, (680, 500))
        hsv_img_resize = cv2.cvtColor(color_img_resize, cv2.COLOR_BGR2HSV)
        background[:, 120:] = gray_img_resize


    elif mode == EXTRACT_COLOR:
        HUE = BGR2H(Color)
        print(HUE)

        if usingStack:
            background[:, 120:] = gray_img_resize

        for i in range(500):
            for j in range(120, 800):
                p = hsv_img_resize[i][j-120]
                if HUE - 10 < p[0] <= HUE + 10 and p[1] != 0 and p[2] != 0:
                    background[i, j] = color_img_resize[i, j-120]
                    tempPos.append([i, j])

    elif mode == STACK_COLOR:
        if usingStack :
            usingStack = False
            print('Change stack mode : ON')

        else:
            usingStack = True
            print('Change stack mode : OFF')


    elif mode == CHANGE_COLOR:
        for pos in tempPos:
            r, c = pos
            background[r, c] = Color
            tempPos = []

    elif mode == RESET_IMAGE:
        background[:, 120:] = gray_img_resize


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
