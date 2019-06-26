# coding: utf-8
import traceback
import time
import asyncio
import io
from collections import deque

import pyscreeze
import numpy
import cv2
import pyscreeze
import settings

VIEWER_STABLE = 0
DIFF_THRESHOLD = 0.03
STABLE_WAIT = 0.5
APP_INIT = 0
APP_BUSY = 1
APP_FREE = 2

class Windows(object):
    pass

class BaseApp(object):
    pass

class AppViewer(object):

    def __init__(self, app, window_area):
        self.app = app
        self.window_area = window_area
        self.status = APP_INIT
        self.window_history = deque(maxlen=3)

    def _get_window(self, screen):
        app_window = screen.copy(self.window_area)
        self.window_history.append(app_window)

    def _has_changed(self, before_window, now_window):
        before_window_bit = numpy.array(before_window)
        after_window_bit = numpy.array(now_window)
        diff_bits = numpy.sum(before_window == after_window_bit)
        diff_rate = diff_bits/before_window.size
        if diff_rate > DIFF_THRESHOLD:
            return True
        return False

    def _has_stable(self):
        """过滤掉切换动画"""
        window_changed_history = deque(maxlen=3)
        changed = self._has_changed(self.window_history[-1], self.window_history[-2])
        window_changed_history.append(changed)


    def wait_stable(self, screen):
        self._get_window(screen)
        if len(self.window_history) > 1:
            changed = self._has_changed(self.window_history[-1], self.window_history[-2])
            if changed:
                self.app.send({'status': VIEWER_STABLE})

    def find_pic(self, ):




class Viewer(object):
    """"""
    def __init__(self, project_name, hwnd=0):
        self.project_name = project_name
        self.status = 0  # 0表示稳定，1表示变化
        self.loop_envents = [x() for x in settings.loop_events]
        self.loop = asyncio.get_event_loop()
        self.apps = []

    async def accpet(self):
            pass

    async def send(self, result):
        pass

    def excute_loop_events(self):
        for loop_event in self.loop_events:
            loop_event.run()

    @classmethod
    def execute(task):
        pass

    def loop(self):
        while True:
            screen = pyscreeze.screenshot()
        # numpy.array(screen)
        # self.excute_loop_events()
        # sender, data = self.loop.run_until_complete(asyncio.wait(self.accpet()))
        # result = self.execute(data)
        # self.send(sender, data)

    def _ischanged(self, screen1, screen2, threshold):
        screen1_bit = numpy.array(screen1)
        screen2_bit = numpy.array(screen1)
        diff = numpy.sum(screen1_bit == screen2_bit)
        diff_rate = diff/screen2_bit.size
        if diff_rate > threshold:
            return True
        elif diff_rate <= threshold:
            return False


if __name__ == '__main__':
    #
    # im = pyscreeze.screenshot()
    # i1 = numpy.array(im)
    # time.sleep(1)
    # t1 = time.time()
    # im = pyscreeze.screenshot()
    # i2 = numpy.array(im)
    # total = numpy.sum(i1 == i2)
    # t2 = time.time()
    # print(total/i2.size)
    # print(t2-t1)

