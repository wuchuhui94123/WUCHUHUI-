#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抖音自动化机器人
功能: 自动刷视频、看直播、点赞、评论、关注
"""

import json
import time
import random
import sys
from datetime import datetime
from adb_controller import ADBController


class DouyinBot:
    """抖音自动化机器人"""

    def __init__(self, config_path: str = "config.json"):
        """
        初始化机器人

        Args:
            config_path: 配置文件路径
        """
        # 加载配置
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)

        # 初始化ADB控制器
        self.adb = ADBController(
            adb_path=self.config['adb_path'],
            device_name=self.config['device_name']
        )

        # 设置屏幕分辨率
        self.screen_width = self.config['screen_resolution']['width']
        self.screen_height = self.config['screen_resolution']['height']
        self.adb.screen_width = self.screen_width
        self.adb.screen_height = self.screen_height

        # 统计数据
        self.stats = {
            'videos_watched': 0,
            'lives_watched': 0,
            'likes_given': 0,
            'comments_sent': 0,
            'follows_made': 0,
            'start_time': datetime.now()
        }

    def log(self, message: str):
        """
        打印日志

        Args:
            message: 日志消息
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")

    def connect_and_start(self) -> bool:
        """
        连接设备并启动抖音

        Returns:
            是否成功
        """
        self.log("正在连接设备...")
        if not self.adb.connect_device():
            self.log("连接设备失败!")
            return False

        self.log("设备连接成功!")

        # 获取屏幕分辨率
        width, height = self.adb.get_screen_resolution()
        self.log(f"屏幕分辨率: {width}x{height}")

        # 启动抖音
        self.log("正在启动抖音...")
        self.adb.start_app(self.config['douyin_package'])
        time.sleep(5)

        return True

    def click_like_button(self):
        """点击点赞按钮(右侧爱心按钮)"""
        # 点赞按钮通常在右下角
        x = int(self.screen_width * 0.92)
        y = int(self.screen_height * 0.72)
        self.adb.tap_random((x - 30, x + 30), (y - 30, y + 30))
        self.stats['likes_given'] += 1
        self.log(f"点赞成功! 总计: {self.stats['likes_given']}")

    def click_comment_button(self):
        """点击评论按钮"""
        # 评论按钮在右侧,点赞按钮下方
        x = int(self.screen_width * 0.92)
        y = int(self.screen_height * 0.82)
        self.adb.tap_random((x - 30, x + 30), (y - 30, y + 30))
        time.sleep(1)

    def send_comment(self):
        """发送评论"""
        try:
            # 点击评论按钮
            self.click_comment_button()

            # 点击评论输入框
            x = int(self.screen_width * 0.5)
            y = int(self.screen_height * 0.93)
            self.adb.tap(x, y, delay=1)

            # 随机选择一条评论
            comment = random.choice(self.config['comments'])
            self.log(f"准备发送评论: {comment}")

            # 输入评论(由于中文输入复杂,这里使用简单的emoji或英文)
            # 实际使用时可能需要配置输入法或使用其他方法
            # 这里提供基础框架,实际需要根据设备调整
            time.sleep(1)

            # 点击发送按钮(通常在右下角)
            send_x = int(self.screen_width * 0.9)
            send_y = int(self.screen_height * 0.93)
            self.adb.tap(send_x, send_y, delay=1)

            self.stats['comments_sent'] += 1
            self.log(f"评论发送成功! 总计: {self.stats['comments_sent']}")

            # 返回
            self.adb.press_back(delay=1)

        except Exception as e:
            self.log(f"发送评论失败: {str(e)}")
            self.adb.press_back(delay=1)

    def click_follow_button(self):
        """点击关注按钮"""
        # 关注按钮通常在作者头像旁边或右侧
        x = int(self.screen_width * 0.92)
        y = int(self.screen_height * 0.35)
        self.adb.tap_random((x - 30, x + 30), (y - 30, y + 30))
        self.stats['follows_made'] += 1
        self.log(f"关注成功! 总计: {self.stats['follows_made']}")

    def watch_video(self):
        """观看一个视频"""
        # 随机观看时长
        duration = random.randint(
            self.config['video_settings']['watch_duration_min'],
            self.config['video_settings']['watch_duration_max']
        )

        self.log(f"观看视频 {duration} 秒...")
        time.sleep(duration)

        # 根据概率进行互动
        if random.random() < self.config['video_settings']['like_probability']:
            self.click_like_button()
            time.sleep(0.5)

        if random.random() < self.config['video_settings']['follow_probability']:
            self.click_follow_button()
            time.sleep(0.5)

        # 评论功能暂时禁用,因为中文输入较复杂
        # if random.random() < self.config['video_settings']['comment_probability']:
        #     self.send_comment()

        self.stats['videos_watched'] += 1

    def auto_watch_videos(self):
        """自动刷视频"""
        swipe_count = self.config['video_settings']['swipe_count']

        self.log(f"开始自动刷视频, 计划观看 {swipe_count} 个视频")

        for i in range(swipe_count):
            try:
                self.log(f"第 {i + 1}/{swipe_count} 个视频")

                # 观看当前视频
                self.watch_video()

                # 滑动到下一个视频
                self.adb.swipe_up()

                # 随机延迟,模拟真实用户行为
                delay = random.uniform(1, 3)
                time.sleep(delay)

            except KeyboardInterrupt:
                self.log("用户中断,停止刷视频")
                break
            except Exception as e:
                self.log(f"刷视频出错: {str(e)}")
                time.sleep(2)

        self.log("刷视频任务完成!")

    def enter_live_section(self):
        """进入直播页面"""
        self.log("正在进入直播页面...")

        # 点击顶部的"直播"标签
        # 通常在屏幕上方的导航栏
        x = int(self.screen_width * 0.3)  # 直播标签位置可能需要调整
        y = int(self.screen_height * 0.08)
        self.adb.tap(x, y, delay=2)

        self.log("已进入直播页面")

    def enter_random_live_room(self):
        """进入一个随机直播间"""
        # 点击屏幕中间的直播间
        x = int(self.screen_width * 0.5)
        y = int(self.screen_height * 0.4)
        self.adb.tap_random((x - 100, x + 100), (y - 100, y + 100), delay=3)
        self.log("进入直播间")

    def interact_in_live_room(self, duration: int):
        """
        在直播间互动

        Args:
            duration: 观看时长(秒)
        """
        self.log(f"在直播间观看 {duration} 秒...")

        start_time = time.time()
        next_like_time = time.time() + random.randint(
            self.config['live_settings']['like_interval_min'],
            self.config['live_settings']['like_interval_max']
        )

        while time.time() - start_time < duration:
            current_time = time.time()

            # 定期点赞
            if current_time >= next_like_time:
                self.click_like_button()
                next_like_time = current_time + random.randint(
                    self.config['live_settings']['like_interval_min'],
                    self.config['live_settings']['like_interval_max']
                )

            # 等待
            time.sleep(5)

        self.log("直播观看完成")

    def exit_live_room(self):
        """退出直播间"""
        self.adb.swipe_down(ratio=0.5)  # 向下滑动退出
        time.sleep(2)
        self.log("退出直播间")

    def auto_watch_lives(self):
        """自动看直播"""
        max_count = self.config['live_settings']['max_live_count']

        self.log(f"开始自动看直播, 计划观看 {max_count} 个直播间")

        # 先进入直播页面
        self.enter_live_section()

        for i in range(max_count):
            try:
                self.log(f"第 {i + 1}/{max_count} 个直播间")

                # 进入直播间
                self.enter_random_live_room()

                # 随机观看时长
                duration = random.randint(
                    self.config['live_settings']['watch_duration_min'],
                    self.config['live_settings']['watch_duration_max']
                )

                # 在直播间互动
                self.interact_in_live_room(duration)

                # 退出直播间
                self.exit_live_room()

                self.stats['lives_watched'] += 1

                # 随机延迟
                time.sleep(random.uniform(2, 5))

            except KeyboardInterrupt:
                self.log("用户中断,停止看直播")
                break
            except Exception as e:
                self.log(f"看直播出错: {str(e)}")
                self.adb.press_back(delay=2)
                time.sleep(2)

        self.log("看直播任务完成!")

    def print_statistics(self):
        """打印统计信息"""
        runtime = datetime.now() - self.stats['start_time']
        hours = runtime.seconds // 3600
        minutes = (runtime.seconds % 3600) // 60
        seconds = runtime.seconds % 60

        self.log("=" * 50)
        self.log("运行统计:")
        self.log(f"  运行时长: {hours}小时 {minutes}分钟 {seconds}秒")
        self.log(f"  观看视频: {self.stats['videos_watched']} 个")
        self.log(f"  观看直播: {self.stats['lives_watched']} 个")
        self.log(f"  点赞次数: {self.stats['likes_given']} 次")
        self.log(f"  评论次数: {self.stats['comments_sent']} 次")
        self.log(f"  关注次数: {self.stats['follows_made']} 次")
        self.log("=" * 50)

    def run(self, mode: str = "video"):
        """
        运行机器人

        Args:
            mode: 运行模式 - "video"(刷视频), "live"(看直播), "both"(两者都做)
        """
        try:
            # 连接设备并启动抖音
            if not self.connect_and_start():
                return

            # 根据模式执行任务
            if mode == "video":
                self.auto_watch_videos()
            elif mode == "live":
                self.auto_watch_lives()
            elif mode == "both":
                self.log("先刷视频,再看直播")
                self.auto_watch_videos()
                time.sleep(5)
                self.auto_watch_lives()
            else:
                self.log(f"未知模式: {mode}")
                return

            # 打印统计信息
            self.print_statistics()

        except KeyboardInterrupt:
            self.log("\n用户中断程序")
            self.print_statistics()
        except Exception as e:
            self.log(f"程序出错: {str(e)}")
            self.print_statistics()


def main():
    """主函数"""
    print("=" * 50)
    print("抖音自动化机器人 v1.0")
    print("=" * 50)
    print()

    if len(sys.argv) > 1:
        mode = sys.argv[1]
    else:
        print("请选择运行模式:")
        print("  1. 刷视频 (video)")
        print("  2. 看直播 (live)")
        print("  3. 两者都做 (both)")
        print()
        choice = input("请输入选择 (1/2/3): ").strip()

        mode_map = {"1": "video", "2": "live", "3": "both"}
        mode = mode_map.get(choice, "video")

    print(f"\n选择模式: {mode}\n")

    # 创建并运行机器人
    bot = DouyinBot()
    bot.run(mode)


if __name__ == "__main__":
    main()
