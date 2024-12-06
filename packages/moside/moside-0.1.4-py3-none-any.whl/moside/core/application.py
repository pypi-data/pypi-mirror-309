import sys

from PySide6.QtCore import Qt, QLibraryInfo
from PySide6.QtWidgets import QApplication

from .logging import logger


def create_modern_app():
    logger.debug('Creating Modern Application...')

    # 高分屏支持
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # 如果是已存在的app实例
    logger.debug('Use exist app instance or create new app instance')
    _app = QApplication.instance() or QApplication(sys.argv)

    # 解决子窗口关闭后鼠标指针样式失效的问题
    _app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)

    # 资源和翻译
    from ..assets import resources  # noqa 载入资源文件
    from .translation import trans_manager
    # trans_manager.add(':i18n/', 'modern_main_window')  # 注册资源中的翻译文件
    trans_manager.add_dir(':i18n')

    return _app


app = create_modern_app()
