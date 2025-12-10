#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ADB控制模块 - 用于控制Android虚拟机
"""

import subprocess
import time
import random
import re
from typing import Tuple, Optional


class ADBController:
    """ADB控制器类"""

    def __init__(self, adb_path: str = "adb", device_name: str = "127.0.0.1:5555"):
        """
        初始化ADB控制器

        Args:
            adb_path: ADB可执行文件路径
            device_name: 设备名称或IP:端口
        """
        self.adb_path = adb_path
        self.device_name = device_name
        self.screen_width = 1080
        self.screen_height = 2340

    def execute_adb_command(self, command: str) -> str:
        """
        执行ADB命令

        Args:
            command: ADB命令

        Returns:
            命令输出结果
        """
        try:
            full_command = f"{self.adb_path} -s {self.device_name} {command}"
            result = subprocess.run(
                full_command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.stdout.strip()
        except Exception as e:
            print(f"执行ADB命令失败: {command}, 错误: {str(e)}")
            return ""

    def connect_device(self) -> bool:
        """
        连接设备

        Returns:
            是否连接成功
        """
        try:
            result = subprocess.run(
                f"{self.adb_path} connect {self.device_name}",
                shell=True,
                capture_output=True,
                text=True,
                timeout=10
            )
            output = result.stdout.strip()
            print(f"连接设备: {output}")
            return "connected" in output or "already connected" in output
        except Exception as e:
            print(f"连接设备失败: {str(e)}")
            return False

    def check_device(self) -> bool:
        """
        检查设备是否连接

        Returns:
            设备是否连接
        """
        try:
            result = subprocess.run(
                f"{self.adb_path} devices",
                shell=True,
                capture_output=True,
                text=True,
                timeout=10
            )
            return self.device_name in result.stdout
        except Exception as e:
            print(f"检查设备失败: {str(e)}")
            return False

    def get_screen_resolution(self) -> Tuple[int, int]:
        """
        获取屏幕分辨率

        Returns:
            (宽度, 高度)
        """
        try:
            output = self.execute_adb_command("shell wm size")
            match = re.search(r'(\d+)x(\d+)', output)
            if match:
                width = int(match.group(1))
                height = int(match.group(2))
                self.screen_width = width
                self.screen_height = height
                return width, height
        except Exception as e:
            print(f"获取屏幕分辨率失败: {str(e)}")

        return self.screen_width, self.screen_height

    def tap(self, x: int, y: int, delay: float = 0.5):
        """
        点击屏幕坐标

        Args:
            x: X坐标
            y: Y坐标
            delay: 点击后延迟时间(秒)
        """
        self.execute_adb_command(f"shell input tap {x} {y}")
        time.sleep(delay)

    def tap_random(self, x_range: Tuple[int, int], y_range: Tuple[int, int], delay: float = 0.5):
        """
        在指定范围内随机点击

        Args:
            x_range: X坐标范围 (min, max)
            y_range: Y坐标范围 (min, max)
            delay: 点击后延迟时间(秒)
        """
        x = random.randint(x_range[0], x_range[1])
        y = random.randint(y_range[0], y_range[1])
        self.tap(x, y, delay)

    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration: int = 300):
        """
        滑动屏幕

        Args:
            x1: 起始X坐标
            y1: 起始Y坐标
            x2: 结束X坐标
            y2: 结束Y坐标
            duration: 滑动持续时间(毫秒)
        """
        self.execute_adb_command(f"shell input swipe {x1} {y1} {x2} {y2} {duration}")
        time.sleep(0.5)

    def swipe_up(self, ratio: float = 0.7):
        """
        向上滑动(刷下一个视频)

        Args:
            ratio: 滑动距离比例(0-1)
        """
        x = self.screen_width // 2
        y_start = int(self.screen_height * 0.8)
        y_end = int(self.screen_height * (0.8 - ratio))
        duration = random.randint(300, 500)

        # 添加一些随机性，让滑动更自然
        x_offset = random.randint(-50, 50)
        self.swipe(x + x_offset, y_start, x + x_offset, y_end, duration)

    def swipe_down(self, ratio: float = 0.7):
        """
        向下滑动(刷上一个视频)

        Args:
            ratio: 滑动距离比例(0-1)
        """
        x = self.screen_width // 2
        y_start = int(self.screen_height * 0.2)
        y_end = int(self.screen_height * (0.2 + ratio))
        duration = random.randint(300, 500)

        x_offset = random.randint(-50, 50)
        self.swipe(x + x_offset, y_start, x + x_offset, y_end, duration)

    def swipe_left(self):
        """向左滑动"""
        x_start = int(self.screen_width * 0.8)
        x_end = int(self.screen_width * 0.2)
        y = self.screen_height // 2
        duration = random.randint(300, 500)
        self.swipe(x_start, y, x_end, y, duration)

    def swipe_right(self):
        """向右滑动"""
        x_start = int(self.screen_width * 0.2)
        x_end = int(self.screen_width * 0.8)
        y = self.screen_height // 2
        duration = random.randint(300, 500)
        self.swipe(x_start, y, x_end, y, duration)

    def input_text(self, text: str, delay: float = 0.5):
        """
        输入文本

        Args:
            text: 要输入的文本
            delay: 输入后延迟时间(秒)
        """
        # 处理特殊字符和中文
        text = text.replace(' ', '%s')
        text = text.replace('&', '\\&')
        self.execute_adb_command(f'shell input text "{text}"')
        time.sleep(delay)

    def press_back(self, delay: float = 0.5):
        """
        按返回键

        Args:
            delay: 按键后延迟时间(秒)
        """
        self.execute_adb_command("shell input keyevent KEYCODE_BACK")
        time.sleep(delay)

    def press_home(self, delay: float = 0.5):
        """
        按Home键

        Args:
            delay: 按键后延迟时间(秒)
        """
        self.execute_adb_command("shell input keyevent KEYCODE_HOME")
        time.sleep(delay)

    def start_app(self, package_name: str, activity: Optional[str] = None, delay: float = 3):
        """
        启动应用

        Args:
            package_name: 应用包名
            activity: Activity名称(可选)
            delay: 启动后延迟时间(秒)
        """
        if activity:
            self.execute_adb_command(f"shell am start -n {package_name}/{activity}")
        else:
            self.execute_adb_command(f"shell monkey -p {package_name} -c android.intent.category.LAUNCHER 1")
        time.sleep(delay)

    def stop_app(self, package_name: str, delay: float = 1):
        """
        停止应用

        Args:
            package_name: 应用包名
            delay: 停止后延迟时间(秒)
        """
        self.execute_adb_command(f"shell am force-stop {package_name}")
        time.sleep(delay)

    def is_app_running(self, package_name: str) -> bool:
        """
        检查应用是否运行

        Args:
            package_name: 应用包名

        Returns:
            应用是否运行
        """
        output = self.execute_adb_command("shell dumpsys window | grep mCurrentFocus")
        return package_name in output

    def screenshot(self, save_path: str = "/sdcard/screenshot.png") -> bool:
        """
        截屏

        Args:
            save_path: 保存路径

        Returns:
            是否成功
        """
        try:
            self.execute_adb_command(f"shell screencap -p {save_path}")
            return True
        except Exception as e:
            print(f"截屏失败: {str(e)}")
            return False

    def get_current_activity(self) -> str:
        """
        获取当前Activity

        Returns:
            当前Activity名称
        """
        output = self.execute_adb_command("shell dumpsys window | grep mCurrentFocus")
        return output
