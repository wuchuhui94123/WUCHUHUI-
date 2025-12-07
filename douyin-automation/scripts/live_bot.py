"""
抖音直播自动化脚本
"""
import time
import random
from utils.logger import Logger


class LiveBot:
    """直播互动机器人"""

    def __init__(self, device_manager, config, logger=None):
        self.device = device_manager
        self.config = config
        self.logger = logger or Logger()
        self.action_count = 0

    def run(self):
        """运行直播观看任务"""
        self.logger.info("=" * 50)
        self.logger.info("开始直播观看任务")
        self.logger.info("=" * 50)

        duration = self.config.get('live.duration', 600)
        start_time = time.time()
        live_count = 0

        try:
            # 进入直播广场
            if not self._enter_live_section():
                self.logger.error("无法进入直播区域")
                return

            while time.time() - start_time < duration:
                # 检查是否需要休息
                if self._should_rest():
                    self._take_rest()

                # 进入一个直播间
                if self._enter_live_room():
                    live_count += 1

                    # 观看直播
                    watch_time = self._watch_live()
                    self.logger.info(f"已观看第 {live_count} 个直播间，耗时 {watch_time:.1f}s")

                    # 随机互动
                    self._random_interaction()

                    # 退出直播间
                    self._exit_live_room()

                # 滑动寻找下一个直播
                self._swipe_next()

                # 随机等待
                self.device.random_sleep(2, 5)

                self.action_count += 1

            self.logger.info(f"直播观看任务完成! 共观看 {live_count} 个直播间")

        except KeyboardInterrupt:
            self.logger.warning("用户中断任务")
        except Exception as e:
            self.logger.error(f"任务执行出错: {str(e)}")

    def _enter_live_section(self):
        """进入直播区域"""
        try:
            self.logger.info("尝试进入直播区域...")

            # 方法1：查找"直播"标签
            live_tab = self.device.find_element(text="直播")
            if live_tab and live_tab.exists:
                live_tab.click()
                self.device.random_sleep(2, 3)
                self.logger.info("✓ 已进入直播区域")
                return True

            # 方法2：滑动到直播页面（如果直播在推荐旁边）
            # 向左滑动
            self.device.device.swipe(
                self.device.screen_width * 0.8,
                self.device.screen_height * 0.1,
                self.device.screen_width * 0.2,
                self.device.screen_height * 0.1,
                0.3
            )
            self.device.random_sleep(1, 2)

            # 再次检查
            live_tab = self.device.find_element(text="直播")
            if live_tab and live_tab.exists:
                self.logger.info("✓ 已进入直播区域")
                return True

            self.logger.warning("未找到直播区域，将在当前页面寻找直播间")
            return True

        except Exception as e:
            self.logger.error(f"进入直播区域失败: {str(e)}")
            return False

    def _enter_live_room(self):
        """进入直播间"""
        try:
            # 点击屏幕中心区域进入直播间
            x = self.device.screen_width * random.uniform(0.3, 0.7)
            y = self.device.screen_height * random.uniform(0.3, 0.6)

            self.device.tap(x, y)
            self.device.random_sleep(2, 4)

            self.logger.info("✓ 进入直播间")
            return True

        except Exception as e:
            self.logger.error(f"进入直播间失败: {str(e)}")
            return False

    def _watch_live(self):
        """观看直播"""
        min_time = self.config.get('live.watch_time_min', 60)
        max_time = self.config.get('live.watch_time_max', 300)

        watch_time = random.uniform(min_time, max_time)

        # 在观看过程中随机滚动查看评论
        intervals = int(watch_time / 20)  # 每20秒左右一次互动
        interval_time = watch_time / max(intervals, 1)

        for i in range(intervals):
            time.sleep(interval_time)

            # 随机滚动评论区
            if random.random() < 0.3:
                self._scroll_comments()

        # 剩余时间
        remaining = watch_time - (intervals * interval_time)
        if remaining > 0:
            time.sleep(remaining)

        return watch_time

    def _random_interaction(self):
        """随机互动"""

        # 点赞
        if random.random() < self.config.get('live.like_probability', 0.5):
            self._like_live()

        # 评论
        if random.random() < self.config.get('live.comment_probability', 0.3):
            self._comment_live()

        # 送礼物（谨慎使用，默认关闭）
        if random.random() < self.config.get('live.gift_probability', 0.0):
            self._send_gift()

    def _like_live(self):
        """点赞直播"""
        try:
            # 直播间点赞通常在右下角
            x = self.device.screen_width * 0.9
            y = self.device.screen_height * 0.85

            # 连续点击多次（类似真人快速点赞）
            tap_count = random.randint(3, 8)
            for _ in range(tap_count):
                self.device.tap(x, y)
                time.sleep(random.uniform(0.1, 0.3))

            self.logger.info(f"✓ 点赞 {tap_count} 次")
            return True

        except Exception as e:
            self.logger.error(f"点赞失败: {str(e)}")
            return False

    def _comment_live(self):
        """评论直播"""
        try:
            # 查找评论输入框（通常在底部）
            comment_input = self.device.find_element(
                className="android.widget.EditText"
            )

            if comment_input and comment_input.exists:
                # 点击输入框
                comment_input.click()
                self.device.random_sleep(1, 2)

                # 随机选择评论内容
                comments = self.config.get('comments', ['666'])
                comment_text = random.choice(comments)

                # 输入评论
                self.device.input_text(comment_text)
                self.device.random_sleep(0.5, 1)

                # 查找发送按钮
                send_btn = self.device.find_element(text="发送")
                if not send_btn or not send_btn.exists:
                    # 尝试其他可能的文本
                    send_btn = self.device.find_element(
                        className="android.widget.TextView",
                        textContains="发送"
                    )

                if send_btn and send_btn.exists:
                    send_btn.click()
                    self.logger.info(f"✓ 评论: {comment_text}")
                    self.device.random_sleep(1, 2)
                else:
                    # 如果找不到发送按钮，尝试按回车
                    self.device.device.press("enter")
                    self.logger.info(f"✓ 评论: {comment_text}")
                    self.device.random_sleep(1, 2)

                return True

        except Exception as e:
            self.logger.error(f"评论失败: {str(e)}")
            return False

    def _send_gift(self):
        """送礼物（默认禁用）"""
        self.logger.warning("送礼物功能已禁用，避免消费")
        return False

    def _scroll_comments(self):
        """滚动评论区"""
        try:
            # 在评论区域向上滑动
            start_x = self.device.screen_width * 0.3
            start_y = self.device.screen_height * 0.7
            end_x = start_x
            end_y = self.device.screen_height * 0.5

            self.device.device.swipe(start_x, start_y, end_x, end_y, 0.3)
            self.logger.debug("滚动评论区")

        except Exception as e:
            self.logger.debug(f"滚动评论失败: {str(e)}")

    def _exit_live_room(self):
        """退出直播间"""
        try:
            # 点击左上角或向下滑动退出
            if random.random() < 0.5:
                # 方法1：点击返回按钮
                self.device.press_back()
            else:
                # 方法2：向下滑动退出
                self.device.swipe_down()

            self.device.random_sleep(1, 2)
            self.logger.debug("退出直播间")
            return True

        except Exception as e:
            self.logger.error(f"退出直播间失败: {str(e)}")
            return False

    def _swipe_next(self):
        """滑动到下一个直播"""
        # 在直播列表中向上滑动
        duration = random.uniform(0.3, 0.8)
        self.device.swipe_up(duration)
        self.logger.debug("滑动到下一个直播")

    def _should_rest(self):
        """判断是否需要休息"""
        max_actions = self.config.get('safety.max_continuous_actions', 50)
        return self.action_count > 0 and self.action_count % max_actions == 0

    def _take_rest(self):
        """休息一段时间"""
        rest_duration = self.config.get('safety.rest_duration', 60)
        self.logger.info(f"⏸️  休息 {rest_duration}s，模拟真人行为...")

        # 返回主页休息
        self.device.press_home()
        time.sleep(rest_duration)

        # 重新打开抖音
        package_name = self.config.get('douyin.package_name')
        self.device.start_app(package_name)
        self.device.random_sleep(2, 3)

        # 重新进入直播区域
        self._enter_live_section()
