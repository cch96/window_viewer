# coding: utf-8
import traceback
import time
import io

import bitarray
import pyscreeze
import lackey
import numpy
import cv2
import pyscreeze


class Viewer(object):
    """"""
    def __init__(self, project_name, hwnd=0):
        self.hwnd = hwnd  # 监控那个窗口, 默认是0即全屏
        self.project_name = project_name
        self.status = 0  # 0表示稳定，1表示变化

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


if __name__ == '__main__':
    for i in range(1000):
        bit1 = bitarray.bitarray()
        a = pyscreeze.screenshot(region=[0, 0, 600, 200])
        bit1.frombytes(a.tobytes())
        t1 = time.time()
        bit2 = bitarray.bitarray()
        b = pyscreeze.screenshot(region=[0, 0, 600, 200])
        bit2.frombytes(b.tobytes())
        print((bit1^bit2).count(1))
        print(time.time()-t1)
