#!/usr/bin/env python3
"""
抖音自动化脚本主程序
Author: Claude
Description: 自动刷视频、看直播、点赞、评论等功能
"""

import sys
import os
import argparse
import time

# 添加项目路径到系统路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.logger import Logger
from utils.config_loader import ConfigLoader
from utils.device_manager import DeviceManager
from scripts.video_bot import VideoBot
from scripts.live_bot import LiveBot


def print_banner():
    """打印欢迎横幅"""
    banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║           🎬 抖音自动化脚本 Douyin Bot 🎬                  ║
║                                                           ║
║           自动刷视频 | 看直播 | 点赞互动                   ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='抖音自动化脚本 - 自动刷视频、看直播、互动'
    )

    parser.add_argument(
        '-m', '--mode',
        choices=['video', 'live', 'both'],
        default='both',
        help='运行模式：video(仅刷视频)、live(仅看直播)、both(两者都执行，默认)'
    )

    parser.add_argument(
        '-c', '--config',
        default='config/config.yaml',
        help='配置文件路径（默认：config/config.yaml）'
    )

    parser.add_argument(
        '-d', '--device',
        help='设备ID（覆盖配置文件中的设置）'
    )

    parser.add_argument(
        '--duration',
        type=int,
        help='运行时长（秒）'
    )

    parser.add_argument(
        '--debug',
        action='store_true',
        help='启用调试模式'
    )

    return parser.parse_args()


def check_environment():
    """检查运行环境"""
    try:
        import uiautomator2
        import yaml
        return True
    except ImportError as e:
        print(f"❌ 缺少必要的依赖库: {str(e)}")
        print("请运行: pip install -r requirements.txt")
        return False


def main():
    """主函数"""
    # 打印横幅
    print_banner()

    # 解析参数
    args = parse_arguments()

    # 检查环境
    if not check_environment():
        return 1

    try:
        # 加载配置
        print(f"📋 加载配置文件: {args.config}")
        config = ConfigLoader(args.config)

        # 初始化日志
        log_level = 'DEBUG' if args.debug else config.get('logging.level', 'INFO')
        log_dir = config.get('logging.log_dir', 'logs') if config.get('logging.save_to_file', True) else None
        logger = Logger(level=log_level, log_dir=log_dir)

        logger.info("=" * 60)
        logger.info("抖音自动化脚本启动")
        logger.info("=" * 60)

        # 获取设备ID
        device_id = args.device or config.get('adb.device_id')
        if not device_id:
            logger.error("未指定设备ID，请在配置文件或命令行中指定")
            return 1

        # 初始化设备管理器
        logger.info(f"🔌 初始化设备管理器...")
        device_manager = DeviceManager(device_id, logger)

        # 连接设备
        if not device_manager.connect():
            logger.error("设备连接失败，请检查：")
            logger.error("1. 模拟器是否已启动")
            logger.error("2. ADB是否已安装并配置")
            logger.error("3. 设备ID是否正确")
            return 1

        # 启动抖音
        package_name = config.get('douyin.package_name')
        logger.info(f"🚀 启动抖音应用: {package_name}")

        if not device_manager.start_app(package_name):
            logger.error("启动抖音失败，请确保抖音已安装")
            return 1

        # 等待应用完全启动
        time.sleep(5)

        # 根据模式运行
        mode = args.mode

        if mode in ['video', 'both']:
            if config.get('video.enabled', True):
                logger.info("\n" + "=" * 60)
                logger.info("🎬 开始视频任务")
                logger.info("=" * 60)
                video_bot = VideoBot(device_manager, config, logger)
                video_bot.run()

                # 如果还要执行直播任务，休息一会
                if mode == 'both' and config.get('live.enabled', True):
                    logger.info("\n⏸️  视频任务完成，休息30秒后开始直播任务...")
                    time.sleep(30)

        if mode in ['live', 'both']:
            if config.get('live.enabled', True):
                logger.info("\n" + "=" * 60)
                logger.info("📺 开始直播任务")
                logger.info("=" * 60)
                live_bot = LiveBot(device_manager, config, logger)
                live_bot.run()

        # 任务完成
        logger.info("\n" + "=" * 60)
        logger.info("✅ 所有任务执行完成！")
        logger.info("=" * 60)

        return 0

    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断执行")
        return 0

    except Exception as e:
        print(f"\n\n❌ 发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
