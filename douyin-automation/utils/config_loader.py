"""
配置加载模块
"""
import os
import yaml


class ConfigLoader:
    """配置加载器"""

    def __init__(self, config_path='config/config.yaml'):
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self):
        """加载配置文件"""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"配置文件不存在: {self.config_path}")

        with open(self.config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        return config

    def get(self, key, default=None):
        """获取配置项"""
        keys = key.split('.')
        value = self.config

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default

            if value is None:
                return default

        return value

    def get_all(self):
        """获取所有配置"""
        return self.config
