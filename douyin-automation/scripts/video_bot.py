"""
抖音视频自动化脚本
"""
import time
import random
from utils.logger import Logger


class VideoBot:
    """视频刷取机器人"""

    def __init__(self, device_manager, config, logger=None):
        self.device = device_manager
        self.config = config
        self.logger = logger or Logger()
        self.action_count = 0

    def run(self):
        """运行视频刷取任务"""
        self.logger.info("=" * 50)
        self.logger.info("开始刷视频任务")
        self.logger.info("=" * 50)

        duration = self.config.get('video.duration', 300)
        start_time = time.time()
        video_count = 0

        try:
            while time.time() - start_time < duration:
                # 检查是否需要休息
                if self._should_rest():
                    self._take_rest()

                # 观看视频
                watch_time = self._watch_video()
                video_count += 1

                self.logger.info(f"已观看第 {video_count} 个视频，耗时 {watch_time:.1f}s")

                # 随机互动
                self._random_interaction()

                # 滑动到下一个视频
                self._swipe_next()

                # 随机等待
                self.device.random_sleep(
                    self.config.get('randomization.action_interval_min', 1),
                    self.config.get('randomization.action_interval_max', 3)
                )

                self.action_count += 1

            self.logger.info(f"刷视频任务完成! 共观看 {video_count} 个视频")

        except KeyboardInterrupt:
            self.logger.warning("用户中断任务")
        except Exception as e:
            self.logger.error(f"任务执行出错: {str(e)}")

    def _watch_video(self):
        """观看视频"""
        min_time = self.config.get('video.watch_time_min', 10)
        max_time = self.config.get('video.watch_time_max', 30)

        watch_time = random.uniform(min_time, max_time)

        # 模拟真人观看：随机在视频中间点击暂停/播放
        if random.random() < 0.1:  # 10% 概率暂停
            pause_time = watch_time * random.uniform(0.3, 0.7)
            time.sleep(pause_time)

            # 点击暂停
            self.device.tap_center()
            self.logger.debug("暂停视频")

            # 暂停一小会
            time.sleep(random.uniform(1, 3))

            # 点击继续播放
            self.device.tap_center()
            self.logger.debug("继续播放")

            time.sleep(watch_time - pause_time)
        else:
            time.sleep(watch_time)

        return watch_time

    def _random_interaction(self):
        """随机互动（点赞、评论、分享）"""

        # 点赞
        if random.random() < self.config.get('video.like_probability', 0.3):
            self._like_video()

        # 评论
        if random.random() < self.config.get('video.comment_probability', 0.1):
            self._comment_video()

        # 分享（较少使用）
        if random.random() < self.config.get('video.share_probability', 0.05):
            self._share_video()

    def _like_video(self):
        """点赞视频"""
        try:
            # 抖音点赞按钮通常在屏幕右侧中下方
            x = self.device.screen_width * 0.9
            y = self.device.screen_height * 0.65

            self.device.tap(x, y)
            self.logger.info("✓ 点赞")

            self.device.random_sleep(0.5, 1.5)
            return True

        except Exception as e:
            self.logger.error(f"点赞失败: {str(e)}")
            return False

    def _comment_video(self):
        """评论视频"""
        try:
            # 点击评论按钮（右侧下方）
            x = self.device.screen_width * 0.9
            y = self.device.screen_height * 0.75

            self.device.tap(x, y)
            self.device.random_sleep(1, 2)

            # 查找评论输入框
            comment_input = self.device.find_element(
                className="android.widget.EditText"
            )

            if comment_input and comment_input.exists:
                # 点击输入框
                comment_input.click()
                self.device.random_sleep(0.5, 1)

                # 随机选择评论内容
                comments = self.config.get('comments', ['666'])
                comment_text = random.choice(comments)

                # 输入评论
                self.device.input_text(comment_text)
                self.device.random_sleep(0.5, 1)

                # 查找发送按钮
                send_btn = self.device.find_element(text="发送")
                if send_btn and send_btn.exists:
                    send_btn.click()
                    self.logger.info(f"✓ 评论: {comment_text}")
                    self.device.random_sleep(1, 2)

            # 返回视频界面
            self.device.press_back()
            self.device.random_sleep(0.5, 1)

            return True

        except Exception as e:
            self.logger.error(f"评论失败: {str(e)}")
            # 确保返回视频界面
            self.device.press_back()
            return False

    def _share_video(self):
        """分享视频（收藏）"""
        try:
            # 点击分享按钮（右侧下方）
            x = self.device.screen_width * 0.9
            y = self.device.screen_height * 0.85

            self.device.tap(x, y)
            self.device.random_sleep(1, 2)

            # 点击收藏（避免真正分享到其他平台）
            collect_btn = self.device.find_element(text="收藏")
            if collect_btn and collect_btn.exists:
                collect_btn.click()
                self.logger.info("✓ 收藏视频")
                self.device.random_sleep(0.5, 1)

            # 返回
            self.device.press_back()
            self.device.random_sleep(0.5, 1)

            return True

        except Exception as e:
            self.logger.error(f"分享失败: {str(e)}")
            self.device.press_back()
            return False

    def _swipe_next(self):
        """滑动到下一个视频"""
        duration = random.uniform(
            self.config.get('randomization.swipe_duration_min', 300) / 1000,
            self.config.get('randomization.swipe_duration_max', 800) / 1000
        )
        self.device.swipe_up(duration)

    def _should_rest(self):
        """判断是否需要休息"""
        max_actions = self.config.get('safety.max_continuous_actions', 50)
        return self.action_count > 0 and self.action_count % max_actions == 0

    def _take_rest(self):
        """休息一段时间"""
        rest_duration = self.config.get('safety.rest_duration', 60)
        self.logger.info(f"⏸️  休息 {rest_duration}s，模拟真人行为...")

        # 随机按Home键或只是停留
        if random.random() < 0.5:
            self.device.press_home()
            time.sleep(rest_duration)
            # 重新打开抖音
            package_name = self.config.get('douyin.package_name')
            self.device.start_app(package_name)
        else:
            time.sleep(rest_duration)
