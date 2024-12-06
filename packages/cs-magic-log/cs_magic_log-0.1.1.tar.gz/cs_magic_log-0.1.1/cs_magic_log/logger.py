import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

from loguru import logger as _logger


@dataclass
class LogConfig:
    console_level: str = "INFO"
    file_level: str = "DEBUG"
    log_file: Optional[Path] = None
    log_format: str = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
    console_format: str = "<green>{time:HH:mm:ss}</green> | {message}"
    rotation: str = "5 MB"
    output_dir: Path = Path("logs")

    def __post_init__(self):
        if self.log_file is None:
            self.output_dir.mkdir(exist_ok=True)
            self.log_file = self.output_dir / f"{datetime.now().isoformat()}.log"


def setup_logger(config: Optional[LogConfig] = None) -> _logger.__class__:
    """
    设置并返回配置好的logger实例
    """
    if config is None:
        config = LogConfig()

    # 移除默认的 stderr 处理器
    _logger.remove()

    # 添加控制台处理器
    _logger.add(
        sys.stderr,
        level=config.console_level,
        format=config.console_format,
        colorize=True
    )
    
    # 添加文件处理器
    _logger.add(
        str(config.log_file),
        level=config.file_level,
        format=config.log_format,
        rotation=config.rotation
    )

    return _logger


# 默认logger实例
logger = setup_logger() 