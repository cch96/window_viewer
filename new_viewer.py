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

VIEWER_FINDED = 0
VIEWER_STABLE = 0
DIFF_THRESHOLD = 0.03
STABLE_COUNT = 3
APP_INIT = 0
APP_BUSY = 1
APP_FREE = 2


class AppManager(object):
    """
    这里使用唯一的manager去调用其他viewer方法，因为，pc就只有一台，若是并行,操作可能会更慢
    所以只由一个manager去控制
    """
    def __init__(self):
        self.app_viewer_dict = {}

    def _change_app_status(self):
        """改变appview状态， 当状态为busy时忽略操作"""
        pass

    def accpet(self):
        """从逻辑处理模块接受消息"""
        pass
    def send(self):
        """给逻辑处理模块发消息 """
        pass
    def execute(self):
        """调用appview执行操作"""
        pass

    def looking(self):
        for app, app_viewer in self.app_viewer_dict:
            if app_viewer.status == APP_FREE:
                app.send()

    def run(self):
        """创建appview实例， 监听是否稳定"""
        for app in app_list:
            self.app_viewer_dict[app] = app_viewer
        while True:
            screen = pyscreeze.screenshot()
            for app_viewer in self.app_viewer_dict.keys():
                app_viewer.shot(screen)


class AppViewer(object):

    def __init__(self, app, window_area):
        self.app = app
        self.window_area = window_area
        self.status = APP_INIT
        self.window_history = deque(maxlen=3)

    def _has_changed(self, before_window, now_window):
        before_window_bit = numpy.array(before_window)
        after_window_bit = numpy.array(now_window)
        diff_bits = numpy.sum(before_window == after_window_bit)
        diff_rate = diff_bits/before_window.size
        if diff_rate > DIFF_THRESHOLD:
            return True
        return False

    def shot(self, screen):
        app_window = screen.crop(self.window_area)
        self.window_history.append(app_window)

    def isstabled(self):
        """过滤掉切换动画"""
        changed = self._has_changed(self.window_history[-1], self.window_history[-2])
        if not changed:
            return True
        return False

    def ischanged(self, screen):
        if len(self.window_history) > 1:
            changed = self._has_changed(self.window_history[-1], self.window_history[-2])
            if changed:
                self.app.send({'status': VIEWER_STABLE})

    def find_pic(self, target_pic):
        last_window = self.window_history[-1]
        result = list(pyscreeze.locateAll(target_pic, last_window))
        self.app.send({'status': VIEWER_FINDED, 'data': result})
        # TODO 这里还是想把self.app.send改为return 由loop去处理发送, 这样在拓展appview的时候会更加的符合习惯
    # TODO 把我一些有关图像识别的方法


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
    a = list(pyscreeze.locateAll('img/find.png', 'img/screen.png'))
    print(a)
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

