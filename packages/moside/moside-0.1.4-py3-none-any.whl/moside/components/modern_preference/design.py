# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'design.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFormLayout,
    QFrame, QGroupBox, QLabel, QSizePolicy,
    QTextBrowser, QVBoxLayout, QWidget)

class Ui_ModernPreference(object):
    def setupUi(self, ModernPreference):
        if not ModernPreference.objectName():
            ModernPreference.setObjectName(u"ModernPreference")
        self.ly_modern_preference = QVBoxLayout(ModernPreference)
        self.ly_modern_preference.setObjectName(u"ly_modern_preference")
        self.grp_appearance = QGroupBox(ModernPreference)
        self.grp_appearance.setObjectName(u"grp_appearance")
        self.ly_appearance = QVBoxLayout(self.grp_appearance)
        self.ly_appearance.setObjectName(u"ly_appearance")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.lbl_lang = QLabel(self.grp_appearance)
        self.lbl_lang.setObjectName(u"lbl_lang")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.lbl_lang)

        self.cmb_lang = QComboBox(self.grp_appearance)
        self.cmb_lang.setObjectName(u"cmb_lang")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.cmb_lang)

        self.lbl_style = QLabel(self.grp_appearance)
        self.lbl_style.setObjectName(u"lbl_style")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.lbl_style)

        self.cmb_style = QComboBox(self.grp_appearance)
        self.cmb_style.setObjectName(u"cmb_style")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.cmb_style)

        self.lbl_theme = QLabel(self.grp_appearance)
        self.lbl_theme.setObjectName(u"lbl_theme")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.lbl_theme)

        self.cmb_theme = QComboBox(self.grp_appearance)
        self.cmb_theme.setObjectName(u"cmb_theme")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.cmb_theme)


        self.ly_appearance.addLayout(self.formLayout)

        self.chk_colorful = QCheckBox(self.grp_appearance)
        self.chk_colorful.setObjectName(u"chk_colorful")

        self.ly_appearance.addWidget(self.chk_colorful)

        self.chk_expand = QCheckBox(self.grp_appearance)
        self.chk_expand.setObjectName(u"chk_expand")

        self.ly_appearance.addWidget(self.chk_expand)


        self.ly_modern_preference.addWidget(self.grp_appearance)

        self.textBrowser = QTextBrowser(ModernPreference)
        self.textBrowser.setObjectName(u"textBrowser")

        self.ly_modern_preference.addWidget(self.textBrowser)


        self.retranslateUi(ModernPreference)

        QMetaObject.connectSlotsByName(ModernPreference)
    # setupUi

    def retranslateUi(self, ModernPreference):
        self.grp_appearance.setTitle(QCoreApplication.translate("ModernPreference", u"Appearance", None))
        self.lbl_lang.setText(QCoreApplication.translate("ModernPreference", u"Language", None))
        self.lbl_style.setText(QCoreApplication.translate("ModernPreference", u"Style", None))
        self.lbl_theme.setText(QCoreApplication.translate("ModernPreference", u"Theme", None))
        self.chk_colorful.setText(QCoreApplication.translate("ModernPreference", u"Colorful", None))
        self.chk_expand.setText(QCoreApplication.translate("ModernPreference", u"Expand", None))
        self.textBrowser.setHtml(QCoreApplication.translate("ModernPreference", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Microsoft YaHei UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600; color:#ff79c6;\">MoSide</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Means <span style=\" color:#ff79c6;\">mo</span>dern py<span style=\" color:#ff79c6;\">side</span><br />No learning cost, fool-like use, quickly add "
                        "modern UI and practical functions to your PySide6 project,<br />and with colors based on the Dracula theme created by Zeno Rocha.</p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">GPL-3.0 License</p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#bd93f9;\">Created by: \u6c5f\u767d\u6cb3</span></p></body></html>", None))
        pass
    # retranslateUi

