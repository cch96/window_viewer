# coding: utf-8
import traceback
import time
import asyncio
import io
import os
from collections import deque, UserDict
from typing import List, Tuple, Deque, Dict, NewType

import keyboard
import pyscreeze
import pywinauto
from pywinauto.application import Application, WindowSpecification
from pywinauto.base_wrapper import BaseWrapper
from pywinauto.win32structures import RECT
import PIL
import numpy
import pyscreeze

import settings

VIEWER_FINDED = 0
VIEWER_STABLE = 0
DIFF_THRESHOLD = 0.03
STABLE_COUNT = 3
APP_INIT = 0
APP_BUSY = 1
APP_FREE = 2


class NotBindApps(Exception):
    """没有绑定app"""


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

    def __init__(self, app: Application, active: WindowSpecification,
                 wrapper: BaseWrapper, rect: RECT):
        self.app = app
        self.active = active
        self.wrapper = wrapper
        self.rect = rect
        self.status = APP_INIT
        self.window_history: Deque[PIL.Image.Image]= deque(maxlen=3)

    def _has_changed(self, before_window, now_window):
        before_window_bit = numpy.array(before_window)
        after_window_bit = numpy.array(now_window)
        diff_bits = numpy.sum(before_window == after_window_bit)
        diff_rate = diff_bits/before_window.size
        if diff_rate > DIFF_THRESHOLD:
            return True
        return False

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



class AppScriptMap(object):
    instance = None
    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super().__new__(cls, *args, **kwargs)
        return cls.instance

    def __init__(self):
        self.app_script = {}
        self.script_app = {}

    def __len__(self):
        return len(self.app_script)

    def __iter__(self):
        for key, value in self.app_script:
            yield (key, value)

    def app_to_script(self, app: AppViewer):
        return self.app_script[app]

    def script_to_app(self, script: str):
        return self.script_app[script]

    def save(self, app: AppViewer, script_name: str):
        self.app_script[app] = script_name
        self.script_app[script_name] = app


class Viewer(object):

    def __init__(self, project_name):
        self.project_name = project_name
        self.app_script_map: AppScriptMap = AppScriptMap()
        self.appview_list: List[AppViewer] = []

    def accept(self):


    # async def send(self, result):
    #     pass
    #
    # def excute_loop_events(self):
    #     for loop_event in self.loop_events:
    #         loop_event.run()
    #
    # @classmethod
    # def execute(task):
    #     pass
    #
    #
    # def _ischanged(self, screen1, screen2, threshold):
    #     screen1_bit = numpy.array(screen1)
    #     screen2_bit = numpy.array(screen1)
    #     diff = numpy.sum(screen1_bit == screen2_bit)
    #     diff_rate = diff/screen2_bit.size
    #     if diff_rate > threshold:
    #         return True
    #     elif diff_rate <= threshold:
    #         return False

    def _get_focus_app(self):
        app = Application().connect(active_only=True)
        active_window = app.active()
        wrapper = active_window.wrapper_object()
        app_view = AppViewer(app=app, active=active_window,
                             wrapper=wrapper, rect=wrapper.rectangle())
        return app_view

    def bind_apps(self):
        for script in os.listdir('script'):
            print('请点击SCRIPT:%s需要绑定的窗口后，按ctrl+x' % script)
            keyboard.wait('ctrl+x')
            app_view = self._get_focus_app()
            self.app_script_map.save(app=app_view, script_name=script)
            self.appview_list.append(app_view)
            print('您已绑定窗口 %s' % app_view.wrapper.element_info)
            print('请继续')

    def run(self):
        if self.appview_list == []:
            raise NotBindApps("您还没有绑定app")
        while True:
            screen = pyscreeze.screenshot()
            for app_view in self.appview_list:
                rect = app_view.rect
                app_shot = screen.crop((rect.left, rect.top, rect.right, rect.bottom))
                app_view.window_history.append(app_shot)


def main():
    viewer = Viewer('1')
    viewer.bind_apps()
    viewer.run()


if __name__ == '__main__':
    main()

