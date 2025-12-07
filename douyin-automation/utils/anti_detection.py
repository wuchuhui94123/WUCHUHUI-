"""
防检测工具模块
"""
import random
import time
from utils.logger import Logger


class AntiDetection:
    """防检测工具类"""

    def __init__(self, config, logger=None):
        self.config = config
        self.logger = logger or Logger()

    def random_sleep(self, min_sec=None, max_sec=None):
        """
        随机等待
        模拟人类操作的不确定性
        """
        if min_sec is None:
            min_sec = self.config.get('randomization.action_interval_min', 1)
        if max_sec is None:
            max_sec = self.config.get('randomization.action_interval_max', 5)

        sleep_time = random.uniform(min_sec, max_sec)

        # 添加微小的随机抖动
        if self.config.get('randomization.human_like_delay', True):
            jitter = random.uniform(-0.1, 0.1)
            sleep_time += jitter

        time.sleep(max(0, sleep_time))
        return sleep_time

    def get_random_swipe_duration(self):
        """
        获取随机滑动持续时间
        """
        min_duration = self.config.get('randomization.swipe_duration_min', 300)
        max_duration = self.config.get('randomization.swipe_duration_max', 800)

        duration = random.uniform(min_duration, max_duration) / 1000  # 转换为秒

        return duration

    def add_coordinate_jitter(self, x, y, max_jitter=20):
        """
        为坐标添加随机抖动
        模拟人类点击的不精确性
        """
        jitter_x = random.randint(-max_jitter, max_jitter)
        jitter_y = random.randint(-max_jitter, max_jitter)

        return x + jitter_x, y + jitter_y

    def should_perform_action(self, probability):
        """
        根据概率决定是否执行某个操作
        """
        return random.random() < probability

    def get_random_comment(self):
        """
        获取随机评论内容
        """
        comments = self.config.get('comments', ['666'])
        return random.choice(comments)

    def get_behavior_pattern(self):
        """
        生成类人行为模式
        返回一系列随机的操作序列
        """
        patterns = [
            'watch_only',      # 只看不互动
            'active_liker',    # 积极点赞
            'casual_browser',  # 随意浏览
            'commenter',       # 爱评论
        ]

        return random.choice(patterns)

    def simulate_reading_time(self, content_length=100):
        """
        模拟阅读时间
        根据内容长度估算合理的阅读时间
        """
        # 假设平均阅读速度：每秒2-4个字
        reading_speed = random.uniform(2, 4)
        base_time = content_length / reading_speed

        # 添加随机浮动
        variation = random.uniform(0.8, 1.5)
        reading_time = base_time * variation

        return max(1, reading_time)  # 至少1秒

    def check_rest_needed(self, action_count):
        """
        检查是否需要休息
        """
        max_actions = self.config.get('safety.max_continuous_actions', 50)
        return action_count > 0 and action_count % max_actions == 0

    def get_rest_duration(self):
        """
        获取休息时长
        添加随机性以避免检测
        """
        base_duration = self.config.get('safety.rest_duration', 60)
        variation = random.uniform(0.8, 1.2)

        return int(base_duration * variation)

    def randomize_action_order(self, actions):
        """
        随机化操作顺序
        """
        shuffled = actions.copy()
        random.shuffle(shuffled)
        return shuffled

    def get_human_like_tap_pattern(self):
        """
        获取类人点击模式
        有时会误触，有时会双击
        """
        patterns = {
            'single_tap': 0.85,      # 85% 单次点击
            'double_tap': 0.10,      # 10% 双击
            'miss_then_tap': 0.05,   # 5% 先点偏再修正
        }

        rand = random.random()
        cumulative = 0

        for pattern, probability in patterns.items():
            cumulative += probability
            if rand < cumulative:
                return pattern

        return 'single_tap'

    def apply_typing_rhythm(self, text):
        """
        模拟打字节奏
        返回每个字符间的延迟时间列表
        """
        delays = []

        for i, char in enumerate(text):
            # 基础打字速度：每个字符100-300ms
            base_delay = random.uniform(0.1, 0.3)

            # 特殊情况调整
            if char in ['。', '！', '？', ',', '.', '!', '?']:
                # 标点符号后稍微停顿
                base_delay += random.uniform(0.1, 0.3)

            if i > 0 and i % 5 == 0:
                # 每5个字符偶尔停顿
                if random.random() < 0.3:
                    base_delay += random.uniform(0.2, 0.5)

            delays.append(base_delay)

        return delays

    def get_watch_time(self, content_type='video'):
        """
        获取观看时长
        根据内容类型返回合理的观看时长
        """
        if content_type == 'video':
            min_time = self.config.get('video.watch_time_min', 10)
            max_time = self.config.get('video.watch_time_max', 30)
        elif content_type == 'live':
            min_time = self.config.get('live.watch_time_min', 60)
            max_time = self.config.get('live.watch_time_max', 300)
        else:
            min_time, max_time = 5, 15

        # 使用正态分布而非均匀分布，更符合真实情况
        mean = (min_time + max_time) / 2
        std_dev = (max_time - min_time) / 6

        watch_time = random.gauss(mean, std_dev)

        # 确保在范围内
        watch_time = max(min_time, min(max_time, watch_time))

        return watch_time
