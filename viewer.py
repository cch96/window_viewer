# coding: utf-8
import traceback
import time
import bitarray


import pyperclip
import win32clipboard
import win32api
import win32gui
import win32ui
import win32con
import cv2
import numpy as np

import timeit


class Viewer(object):
    """"""
    def __init__(self, project_name, hwnd=0):
        self.hwnd = hwnd  # 监控那个窗口, 默认是0即全屏
        self.project_name = project_name
        self.status = 0  # 0表示稳定，1表示变化

    @staticmethod
    def shot_screen():
        # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
        # 0表示全屏
        hwnd_dc = win32gui.GetWindowDC(0)
        # 根据窗口的DC获取mfcDC
        mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
        # mfcDC创建可兼容的DC
        window_dc = mfc_dc.CreateCompatibleDC()
        # 创建bigmap准备保存图片
        window_bitmap = win32ui.CreateBitmap()
        # 获取监控器信息
        moniter_dev = win32api.EnumDisplayMonitors(None, None)
        w = moniter_dev[0][2][2]
        h = moniter_dev[0][2][3]
        # 为bitmap开辟空间
        window_bitmap.CreateCompatibleBitmap(mfc_dc, w, h)
        window_dc.SelectObject(window_bitmap)
        # 截取从左上角（0，0）长宽为（w，h）的片段
        window_dc.BitBlt((0, 0), (w, h), mfc_dc, (0, 0), win32con.SRCCOPY)
        # 返回bitmap和窗口的设备上下文DC
        return ViewBitMap(window_bitmap, window_dc)

    @staticmethod
    def shot_window(hwnd):
        # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
        hwnd = win32gui.FindWindow(hwnd, 0)
        hwnd_dc = win32gui.GetWindowDC()
        # 根据窗口的DC获取mfcDC
        mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
        # mfcDC创建可兼容的DC
        window_dc = mfc_dc.CreateCompatibleDC()
        # 创建bigmap准备保存图片
        window_bitmap = win32ui.CreateBitmap()
        # 设置窗口宽高
        rat = win32gui.GetWindowRect(hwnd)
        w = rat[2] - rat[0]
        h = rat[3] - rat[1]
        # 为bitmap开辟空间
        window_bitmap.CreateCompatibleBitmap(mfc_dc, w, h)
        window_dc.SelectObject(window_bitmap)
        # 截取从左上角（0，0）长宽为（w，h）的片段
        window_dc.BitBlt((0, 0), (w, h), mfc_dc, (0, 0), win32con.SRCCOPY)
        # 返回viewBitMap类
        return ViewBitMap(window_bitmap, window_dc)

    @staticmethod
    def show_diff(a, b):
        ab = a.get_img_bits()
        bb = b.get_img_bits()
        v = 0
        for i in range(len(ab)):
            if ab[i] == bb[i]:
                v += 1
            return v

    def loop(self):
        if self.hwnd == 0:
            while True:
                a = self.shot_screen()
                b = self.shot_screen()
                self.show_diff(a, b)

        else:
            while True:
                self.shot_window(self.hwnd)


class ViewBitMap(object):

    def __init__(self, window_bitmap, window_dc):
        self.window_bitmap = window_bitmap
        self.window_dc = window_dc

    def save2file(self, path):
        self.window_bitmap.SaveBitmapFile(self.window_dc, path)

    def save2clipboard(self):
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32con.CF_BITMAP,
                                        self.window_bitmap.GetHandle())
        win32clipboard.CloseClipboard()

    def get_img_bits(self, type):
        return self.window_bitmap.GetBitmapBits(type)


def foo(hwnd, mouse):
    # 去掉下面这句就所有都输出了，但是我不需要那么多
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        titles.update({hwnd: win32gui.GetWindowText(hwnd)})


if __name__ == '__main__':
    viewer = Viewer('test')
    t1 = time.time() # 0.8s平均
    view = viewer.shot_screen()
    a = bitarray.bitarray(endian='little')
    a.frombytes(view.get_img_bits(1))
    view = viewer.shot_screen()
    b = bitarray.bitarray(endian='little')
    b.frombytes(view.get_img_bits(1))
    print(time.time()-t1)
    print((a ^ b).count())
    print(time.time()-t1)
    # b = np.asarray(view.get_img_bits(0), np.uint8)


