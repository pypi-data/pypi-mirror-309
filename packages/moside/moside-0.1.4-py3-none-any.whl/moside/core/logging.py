import logging

import colorlog


def get_logger(name, level='INFO'):
    handler = colorlog.StreamHandler()  # 创建控制台日志处理器
    handler.setFormatter(
        colorlog.ColoredFormatter(  # 设置格式化器
            "%(log_color)s%(asctime)s | %(levelname)s | %(name)s - %(filename).s%(module)s:%(funcName)s:%(lineno)d - %(message)s",
        ))

    _logger = colorlog.getLogger(name)  # 创建logger对象
    _logger.setLevel(level)  # 设置日志级别
    _logger.addHandler(handler)  # 添加处理器

    return _logger


logger = get_logger('moside', 'INFO')
logger.debug(f'Current log level: {logging.getLevelName(logger.level)}')
