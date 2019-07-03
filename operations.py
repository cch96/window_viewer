import cv2
import pyscreeze
import numpy as np
from application import AppExecutor


class FindImgError(Exception):
    """找不到图片"""

class OpenImgError(Exception):
    """打开图片失败"""

class WaitTimeOutError(Exception):
    """等待元素超时"""


def async_operation():

    def wrapper(opeartion):
        opeartion()
        AppExecutor.


class Element(object):

    def __init__(self, find_img_name, confidence=0.85):
        self.name = find_img_name
        self.confidence = confidence
        try:
            self.find_img = cv2.imread(find_img_name)
        except Exception:
            raise OpenImgError('找不到指定图像: %s' % find_img_name)

    def local_all(self, source_img):
        """
        返回所有识别准确的图片,的横坐标和纵坐标
        :return: [(int(x1), int(y1)), (int(x2), int(y2))...]
        """
        all_result = pyscreeze.locateAll(self.find_img, source_img, confidence=self.confidence)
        print(self.find_img)
        print(all_result)
        if all_result:
            # 结构化数据，返回结果集[(int(x1), int(y1)), (int(x2), int(y2))...
            element_positions = []
            for x in all_result:
                element_positions.append(tuple(map(int, x['result'])))
            return element_positions
        raise FindImgError('无法识别图片')


    def local_one(self, source_img, dirction=1, index=0):
        """
        返回符合条件的从左到右指定图片坐标
        :param dirction: 以水平方向找，还是垂直方向。0表水平，1表垂直
        :param index: 从左到右第几个, index可以是负数
        :return: (int(x), int(y))
        """
        all_element = self.local_all(source_img)
        sorted_result = sorted(all_element, key=lambda x: x[dirction])
        return sorted_result[index]

    @async_operation
    def wait_get(self, source_img, dirction=1, index=0, attempts=999999, fun=None, f_kwargs=None):
        """等待识别的元素出现, 并返回坐标

        :param source_img PIL: 原图, 即屏幕截图
        :param dirction int: 方向, 1为纵向，0为横向
        :param index int: 顺序 例如0表示找到底第一个元素
        :param attempts int: 尝试次数，识别找图尝试多少次
        :param fun function: 找图失败时调用的函数
        :param f_kwargs dict: 找图失败执行函数所需的参数
        :return: [(x, y), ......] 图的坐标
        """
        result = None
        for i in range(attempts):
            try:
                result = self.local_one(source_img, dirction, index)
            except FindImgError:
                if callable(fun) and isinstance(f_kwargs, dict):
                    fun(**f_kwargs)
            return result
        else:
            raise WaitTimeOutError('等待 %s 失败 ' % self.name)

    @async_operation
    def wait_disapper(self, source_img, attempts=999999, fun=None, f_kwargs=None):
        """等待，直到目标元素消失

        :param source_img PIL: 原图，即屏幕截图
        :param attempts int: 尝试次数
        :param fun function: 找到目标元素时，调用的函数
        :param f_kwargs dict: 找到元素时调用函数所需参数
        :return bool: True
        """
        for i in range(attempts):
            try:
               self.local_all(source_img)
            except FindImgError:
                return True
            else:
                if callable(fun) and isinstance(f_kwargs, dict):
                    fun(**f_kwargs)
        else:
            raise WaitTimeOutError('等待 %s 失败' % self.name)

    @async_operation
    def wait_move(self, before_position, source_img, attempts=999999):
        """等待, 直到元素出现移动

        :param before_position tuple: 之前元素出现的坐标
        :param source_img PIL: 原图，即屏幕截图
        :param attempts int: 尝试次数
        :return bool: True
        """
        for i in range(attempts):
            try:
                result = self.local_one(source_img)
                if before_position != result:
                    return True
            except FindImgError:
                return True
        else:
            raise WaitTimeOutError('等待 %s 移动失败' % self.name)


class Window(object):
    def __init__(self, window_name):
        self.name = window_name
        from collections import deque
        self.window_history = deque(maxlen=3)

    def get_average_gray(self, window_img, threshold=180):
        im_gray = cv2.cvtColor(window_img, cv2.COLOR_BGR2GRAY)
        im_binary = cv2.threshold(im_gray, threshold, 255, cv2.THRESH_BINARY)
        height, weigh = im_gray.shape
        sum = 0
        for i in im_binary[1]:
            sum += np.sum(i)
        return sum / (height * weigh)

    def wait_stable(self, window_img, before_average_gray, attempts=999999):
        for i in range(attempts):
            now_average_gray = self.get_average_gray(window_img)
            print(before_average_gray, now_average_gray)
            if abs(now_average_gray - before_average_gray) < 1.2:
                return True
        else:
            raise WaitTimeOutError('等待页面 %s 稳定失败' % self.name)

    def wait_change(self, window_img, before_average_gray, attempts=999999):
        for i in range(attempts):
            now_average_gray = self.get_average_gray(window_img)
            self.window_history.append(now_average_gray)
            print(before_average_gray, now_average_gray)
            if abs(now_average_gray - before_average_gray) > 1.2:
                return
        else:
            return None

