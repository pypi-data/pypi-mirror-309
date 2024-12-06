from pathlib import Path

from PySide6.QtCore import QTranslator, QLocale, Signal, QObject, QDirIterator, QLibraryInfo
from PySide6.QtWidgets import QApplication

from .logging import logger


class TransItem(QTranslator):
    def __init__(self, directory, filename, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.directory = directory
        self.filename = filename


class TransManager(QObject):
    signal_apply = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self._items = []
        self.add(QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath), 'qt')  # 注册Qt内置翻译文件

    def apply(self, locale):
        logger.debug(f"Apply locale: {locale}")
        locale = QLocale.system() if locale == "Auto" else QLocale(locale)
        for item in self._items:
            item.load(locale, item.filename, "_", item.directory)
        self.signal_apply.emit()

    def add(self, path, name):
        """添加指定文件名前缀的翻译文件"""
        exist_trans = next((item for item in self._items if item.directory == path and item.filename == name), None)
        if exist_trans:
            logger.debug(f"Translator {path}/{name} already added")
        else:
            logger.debug(f'Add translator file: {path}/{name}')
            assert QApplication.instance(), "No QApplication instance found"
            trans = TransItem(path, name)
            QApplication.instance().installTranslator(trans)
            self._items.append(trans)

    def add_dir(self, path):
        """用QDir实现的目录遍历，添加该目录下的翻译文件"""
        if isinstance(path, Path):
            path = str(path)

        logger.debug(f'Add translator files in directory: {path}')
        it = QDirIterator(path, ['*.qm'])
        while it.hasNext():
            item = it.next()
            name = Path(item).stem.rsplit('_', 2)[0]
            if name:
                self.add(path, name)


trans_manager = TransManager()
