#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ADB测试工具
用于测试设备连接、获取屏幕信息、测试点击位置等
"""

import json
import time
from adb_controller import ADBController


def load_config():
    """加载配置"""
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("错误: 找不到config.json文件")
        return None


def test_connection(adb):
    """测试设备连接"""
    print("\n=== 测试设备连接 ===")

    print("正在连接设备...")
    if adb.connect_device():
        print("✓ 设备连接成功")
        return True
    else:
        print("✗ 设备连接失败")
        print("\n请检查:")
        print("  1. 模拟器是否已启动")
        print("  2. USB调试是否已开启")
        print("  3. config.json中的device_name是否正确")
        return False


def test_device_info(adb):
    """获取设备信息"""
    print("\n=== 设备信息 ===")

    # 屏幕分辨率
    width, height = adb.get_screen_resolution()
    print(f"屏幕分辨率: {width}x{height}")

    # 当前Activity
    activity = adb.get_current_activity()
    print(f"当前界面: {activity}")

    # 检查抖音是否运行
    douyin_package = "com.ss.android.ugc.aweme"
    is_running = adb.is_app_running(douyin_package)
    print(f"抖音是否运行: {'是' if is_running else '否'}")


def test_tap_positions(adb):
    """测试点击位置"""
    print("\n=== 测试点击位置 ===")
    print("将在屏幕上测试几个关键位置的点击")
    print("请观察模拟器屏幕,确认点击位置是否正确")
    print()

    width = adb.screen_width
    height = adb.screen_height

    positions = {
        "屏幕中心": (width // 2, height // 2),
        "点赞按钮位置": (int(width * 0.92), int(height * 0.72)),
        "评论按钮位置": (int(width * 0.92), int(height * 0.82)),
        "关注按钮位置": (int(width * 0.92), int(height * 0.35)),
    }

    for name, (x, y) in positions.items():
        print(f"点击: {name} ({x}, {y})")
        input("按Enter继续...")
        adb.tap(x, y)
        time.sleep(1)


def test_swipe(adb):
    """测试滑动"""
    print("\n=== 测试滑动 ===")
    print("将测试向上滑动(刷下一个视频)")
    print()

    input("按Enter开始测试向上滑动...")
    print("向上滑动...")
    adb.swipe_up()

    time.sleep(1)

    input("按Enter开始测试向下滑动...")
    print("向下滑动...")
    adb.swipe_down()


def test_app_control(adb, package):
    """测试应用控制"""
    print("\n=== 测试应用控制 ===")

    print(f"正在启动应用: {package}")
    adb.start_app(package)
    time.sleep(3)

    is_running = adb.is_app_running(package)
    print(f"应用是否运行: {'是' if is_running else '否'}")

    input("\n按Enter停止应用...")
    adb.stop_app(package)
    print("应用已停止")


def interactive_test(adb):
    """交互式测试"""
    print("\n=== 交互式测试 ===")
    print("输入坐标测试点击,格式: x,y")
    print("输入 'q' 退出")
    print()

    while True:
        try:
            user_input = input("请输入坐标 (如: 540,1170): ").strip()

            if user_input.lower() == 'q':
                break

            x, y = map(int, user_input.split(','))
            print(f"点击位置: ({x}, {y})")
            adb.tap(x, y)

        except ValueError:
            print("输入格式错误,请使用 'x,y' 格式")
        except KeyboardInterrupt:
            break


def main():
    """主函数"""
    print("=" * 50)
    print("ADB测试工具")
    print("=" * 50)

    # 加载配置
    config = load_config()
    if not config:
        return

    # 创建ADB控制器
    adb = ADBController(
        adb_path=config['adb_path'],
        device_name=config['device_name']
    )
    adb.screen_width = config['screen_resolution']['width']
    adb.screen_height = config['screen_resolution']['height']

    # 测试菜单
    while True:
        print("\n" + "=" * 50)
        print("请选择测试项目:")
        print("  1. 测试设备连接")
        print("  2. 获取设备信息")
        print("  3. 测试点击位置")
        print("  4. 测试滑动")
        print("  5. 测试应用控制(抖音)")
        print("  6. 交互式测试")
        print("  7. 全部测试")
        print("  0. 退出")
        print("=" * 50)

        choice = input("\n请输入选择: ").strip()

        if choice == '0':
            print("\n再见!")
            break
        elif choice == '1':
            test_connection(adb)
        elif choice == '2':
            if test_connection(adb):
                test_device_info(adb)
        elif choice == '3':
            if test_connection(adb):
                test_tap_positions(adb)
        elif choice == '4':
            if test_connection(adb):
                test_swipe(adb)
        elif choice == '5':
            if test_connection(adb):
                test_app_control(adb, config['douyin_package'])
        elif choice == '6':
            if test_connection(adb):
                interactive_test(adb)
        elif choice == '7':
            if test_connection(adb):
                test_device_info(adb)
                input("\n按Enter继续测试点击位置...")
                test_tap_positions(adb)
                input("\n按Enter继续测试滑动...")
                test_swipe(adb)
        else:
            print("无效的选择")


if __name__ == "__main__":
    main()
