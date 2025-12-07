"""
设备管理模块
"""
import time
import random
import uiautomator2 as u2
from utils.logger import Logger


class DeviceManager:
    """Android 设备管理器"""

    def __init__(self, device_id, logger=None):
        self.device_id = device_id
        self.logger = logger or Logger()
        self.device = None
        self.screen_width = 0
        self.screen_height = 0

    def connect(self):
        """连接设备"""
        try:
            self.logger.info(f"正在连接设备: {self.device_id}")
            self.device = u2.connect(self.device_id)

            # 获取屏幕分辨率
            info = self.device.info
            self.screen_width = info.get('displayWidth', 1080)
            self.screen_height = info.get('displayHeight', 1920)

            self.logger.info(f"设备连接成功! 分辨率: {self.screen_width}x{self.screen_height}")
            return True

        except Exception as e:
            self.logger.error(f"设备连接失败: {str(e)}")
            return False

    def is_connected(self):
        """检查设备是否连接"""
        try:
            if self.device:
                self.device.info
                return True
        except:
            pass
        return False

    def start_app(self, package_name):
        """启动应用"""
        try:
            self.logger.info(f"启动应用: {package_name}")
            self.device.app_start(package_name)
            time.sleep(3)
            return True
        except Exception as e:
            self.logger.error(f"启动应用失败: {str(e)}")
            return False

    def stop_app(self, package_name):
        """停止应用"""
        try:
            self.logger.info(f"停止应用: {package_name}")
            self.device.app_stop(package_name)
            return True
        except Exception as e:
            self.logger.error(f"停止应用失败: {str(e)}")
            return False

    def swipe_up(self, duration=None):
        """向上滑动（刷下一个视频）"""
        if duration is None:
            duration = random.uniform(0.3, 0.8)

        start_x = self.screen_width / 2
        start_y = self.screen_height * 0.8
        end_x = self.screen_width / 2
        end_y = self.screen_height * 0.2

        # 添加随机偏移，模拟真人操作
        start_x += random.randint(-50, 50)
        end_x += random.randint(-50, 50)

        self.device.swipe(start_x, start_y, end_x, end_y, duration)
        self.logger.debug("执行向上滑动")

    def swipe_down(self, duration=None):
        """向下滑动（刷上一个视频）"""
        if duration is None:
            duration = random.uniform(0.3, 0.8)

        start_x = self.screen_width / 2
        start_y = self.screen_height * 0.2
        end_x = self.screen_width / 2
        end_y = self.screen_height * 0.8

        start_x += random.randint(-50, 50)
        end_x += random.randint(-50, 50)

        self.device.swipe(start_x, start_y, end_x, end_y, duration)
        self.logger.debug("执行向下滑动")

    def tap(self, x, y):
        """点击屏幕"""
        # 添加随机偏移
        x += random.randint(-10, 10)
        y += random.randint(-10, 10)

        self.device.click(x, y)
        self.logger.debug(f"点击坐标: ({x}, {y})")

    def tap_center(self):
        """点击屏幕中心"""
        x = self.screen_width / 2
        y = self.screen_height / 2
        self.tap(x, y)

    def double_tap(self, x=None, y=None):
        """双击（点赞）"""
        if x is None:
            x = self.screen_width / 2
        if y is None:
            y = self.screen_height / 2

        self.device.double_click(x, y, 0.1)
        self.logger.debug(f"双击点赞: ({x}, {y})")

    def input_text(self, text):
        """输入文本"""
        try:
            self.device.send_keys(text)
            self.logger.debug(f"输入文本: {text}")
            return True
        except Exception as e:
            self.logger.error(f"输入文本失败: {str(e)}")
            return False

    def press_back(self):
        """按返回键"""
        self.device.press("back")
        self.logger.debug("按返回键")

    def press_home(self):
        """按Home键"""
        self.device.press("home")
        self.logger.debug("按Home键")

    def screenshot(self, filename=None):
        """截图"""
        try:
            if filename:
                img = self.device.screenshot(filename)
            else:
                img = self.device.screenshot()
            return img
        except Exception as e:
            self.logger.error(f"截图失败: {str(e)}")
            return None

    def find_element(self, **kwargs):
        """查找元素"""
        try:
            return self.device(**kwargs)
        except Exception as e:
            self.logger.error(f"查找元素失败: {str(e)}")
            return None

    def wait_element(self, timeout=10, **kwargs):
        """等待元素出现"""
        try:
            return self.device(**kwargs).wait(timeout=timeout)
        except Exception as e:
            self.logger.debug(f"等待元素超时: {kwargs}")
            return False

    def random_sleep(self, min_sec=1, max_sec=3):
        """随机等待"""
        sleep_time = random.uniform(min_sec, max_sec)
        time.sleep(sleep_time)
        return sleep_time
