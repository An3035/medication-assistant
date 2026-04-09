"""日志配置"""

from loguru import logger
import sys
from pathlib import Path


def setup_logger(log_level: str = "INFO"):
    """配置日志"""
    # 移除默认handler
    logger.remove()

    # 添加控制台输出
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        level=log_level,
        colorize=True,
    )

    # 添加文件输出
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    logger.add(
        log_dir / "app_{time:YYYY-MM-DD}.log",
        rotation="500 MB",
        retention="10 days",
        level=log_level,
        encoding="utf-8",
    )

    return logger


# 创建全局logger实例
log = setup_logger()
