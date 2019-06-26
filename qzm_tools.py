# coding: utf-8
import aircv as ac
import traceback
import os
import win32api, win32con, win32gui, win32ui
import time
from win32api import GetSystemMetrics

SCREENIMG = 'img'

class ImgFinder(object):
    """识别图像位置
    	:params imsrc: 原始图片名, 默认保存在img文件夹中
    	:params imsch: 目标图片名 
        1.方法window_capture,截全屏并且保存到文件夹中,默认是img文件夹
        2.方法get_position, 返回目标在原图的中位置(只识别唯一的一个)
	"""
    def __init__(self, imsch, imsrc='screen.png'):
        try:
            self.imsrc = ac.imread(os.path.join(SCREENIMG, imsrc))
            self.imsch = ac.imread(os.path.join(SCREENIMG, imsch))
        except:
            print('无法找到图片')
            traceback.print_exc()

    @staticmethod
    def window_capture():
        hwnd = 0 # 窗口的编号，0号表示当前活跃窗口
        # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
        hwndDC = win32gui.GetWindowDC(hwnd)
        # 根据窗口的DC获取mfcDC
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        # mfcDC创建可兼容的DC
        saveDC = mfcDC.CreateCompatibleDC()
        # 创建bigmap准备保存图片
        saveBitMap = win32ui.CreateBitmap()
        # 获取监控器信息
        MoniterDev = win32api.EnumDisplayMonitors(None, None)
        w = MoniterDev[0][2][2]
        h = MoniterDev[0][2][3]
        # print w,h　　　#图片大小
        # 为bitmap开辟空间
        saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
        # 高度saveDC，将截图保存到saveBitmap中
        saveDC.SelectObject(saveBitMap)
        # 截取从左上角（0，0）长宽为（w，h）的图片
        saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
        saveBitMap.SaveBitmapFile(saveDC, os.path.join(SCREENIMG, 'screen.png'))

    def get_all_element(self):
        """
        返回所有识别准确的图片,的横坐标和纵坐标
        :return: [(int(x1), int(y1)), (int(x2), int(y2))...]
        """
        results = ac.find_all_template(self.imsrc, self.imsch)
        real_result = tuple(filter(lambda x: x['confidence'] > 0.90, results))
        print(results)
        if real_result:
            # 结构化数据，返回结果集[(int(x1), int(y1)), (int(x2), int(y2))...
            element_positions = []
            for x in real_result:
                element_positions.append(tuple(map(int, x['result'])))
            return element_positions
        raise Exception('识别失败')


    def get_element(self, dirction=1, index=0):
        """
        返回符合条件的从左到右指定图片坐标
        :param dirction: 以水平方向找，还是垂直方向。0表水平，1表垂直
        :param index: 从左到右第几个, index可以是负数
        :return: (int(x), int(y))
        """
        all_element = self.get_all_element()
        sorted_result = sorted(all_element, key=lambda x: x[dirction])
        return sorted_result[index]


if __name__ == '__main__':
    t1 = time.time()

    showRegionOnScreen
    print(time.time()-t1)




