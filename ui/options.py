# Auto-generated UI module; linting is intentionally disabled.
from PySide6.QtCore import (QCoreApplication, QMetaObject, QSize, Qt)
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (QCheckBox, QComboBox, QFontComboBox,
    QFormLayout, QGridLayout, QGroupBox, QLabel, QPushButton,
    QRadioButton, QSizePolicy, QSpacerItem, QTabWidget, QVBoxLayout, QWidget)

class Ui_Opt(object):
    def setupUi(self, Opt):
        if not Opt.objectName():
            Opt.setObjectName(u"Opt")
        Opt.resize(400, 400)
        Opt.setMinimumSize(QSize(400, 400))
        Opt.setLayoutDirection(Qt.LeftToRight)
        Opt.setStyleSheet(u"")
        self.verticalLayout_4 = QVBoxLayout(Opt)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.tabWidget = QTabWidget(Opt)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabMain = QWidget()
        self.tabMain.setObjectName(u"tabMain")
        self.gridLayout_3 = QGridLayout(self.tabMain)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.comboStyle = QComboBox(self.tabMain)
        self.comboStyle.addItem("")
        self.comboStyle.addItem("")
        self.comboStyle.addItem("")
        self.comboStyle.setObjectName(u"comboStyle")

        self.gridLayout_3.addWidget(self.comboStyle, 0, 1, 1, 1)

        self.labelStyle = QLabel(self.tabMain)
        self.labelStyle.setObjectName(u"labelStyle")

        self.gridLayout_3.addWidget(self.labelStyle, 0, 0, 1, 1)

        self.labelLocalization = QLabel(self.tabMain)
        self.labelLocalization.setObjectName(u"labelLocalization")

        self.gridLayout_3.addWidget(self.labelLocalization, 1, 0, 1, 1)

        self.comboLocalization = QComboBox(self.tabMain)
        self.comboLocalization.addItem("")
        self.comboLocalization.addItem("")
        self.comboLocalization.setObjectName(u"comboLocalization")

        self.gridLayout_3.addWidget(self.comboLocalization, 1, 1, 1, 1)

        self.checkShowMenu = QCheckBox(self.tabMain)
        self.checkShowMenu.setObjectName(u"checkShowMenu")
        self.checkShowMenu.setChecked(False)

        self.gridLayout_3.addWidget(self.checkShowMenu, 2, 0, 1, 1)

        self.checkShowStatusBar = QCheckBox(self.tabMain)
        self.checkShowStatusBar.setObjectName(u"checkShowStatusBar")
        self.checkShowStatusBar.setChecked(False)

        self.gridLayout_3.addWidget(self.checkShowStatusBar, 2, 1, 1, 1)

        self.groupTabBar = QGroupBox(self.tabMain)
        self.groupTabBar.setObjectName(u"groupTabBar")
        self.groupTabBar.setAlignment(Qt.AlignCenter)
        self.verticalLayout = QVBoxLayout(self.groupTabBar)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.checkShowTabBar = QCheckBox(self.groupTabBar)
        self.checkShowTabBar.setObjectName(u"checkShowTabBar")
        self.checkShowTabBar.setChecked(False)

        self.verticalLayout.addWidget(self.checkShowTabBar)

        self.checkTabBarVertical = QCheckBox(self.groupTabBar)
        self.checkTabBarVertical.setObjectName(u"checkTabBarVertical")
        self.checkTabBarVertical.setChecked(False)

        self.verticalLayout.addWidget(self.checkTabBarVertical)

        self.checkTabBarCloseBtn = QCheckBox(self.groupTabBar)
        self.checkTabBarCloseBtn.setObjectName(u"checkTabBarCloseBtn")
        self.checkTabBarCloseBtn.setChecked(False)

        self.verticalLayout.addWidget(self.checkTabBarCloseBtn)


        self.gridLayout_3.addWidget(self.groupTabBar, 3, 0, 1, 1)

        self.groupToolBar = QGroupBox(self.tabMain)
        self.groupToolBar.setObjectName(u"groupToolBar")
        self.groupToolBar.setAlignment(Qt.AlignCenter)
        self.verticalLayout_2 = QVBoxLayout(self.groupToolBar)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.checkShowToolBar = QCheckBox(self.groupToolBar)
        self.checkShowToolBar.setObjectName(u"checkShowToolBar")
        self.checkShowToolBar.setChecked(False)

        self.verticalLayout_2.addWidget(self.checkShowToolBar)

        self.radioToolBarIconsSmall = QRadioButton(self.groupToolBar)
        self.radioToolBarIconsSmall.setObjectName(u"radioToolBarIconsSmall")

        self.verticalLayout_2.addWidget(self.radioToolBarIconsSmall)

        self.radioToolBarIconsMedium = QRadioButton(self.groupToolBar)
        self.radioToolBarIconsMedium.setObjectName(u"radioToolBarIconsMedium")
        self.radioToolBarIconsMedium.setChecked(True)

        self.verticalLayout_2.addWidget(self.radioToolBarIconsMedium)

        self.radioToolBarIconsLarge = QRadioButton(self.groupToolBar)
        self.radioToolBarIconsLarge.setObjectName(u"radioToolBarIconsLarge")
        self.radioToolBarIconsLarge.setChecked(False)

        self.verticalLayout_2.addWidget(self.radioToolBarIconsLarge)


        self.gridLayout_3.addWidget(self.groupToolBar, 3, 1, 1, 1)

        self.tabWidget.addTab(self.tabMain, "")
        self.tabColoursFont = QWidget()
        self.tabColoursFont.setObjectName(u"tabColoursFont")
        self.gridLayout_4 = QGridLayout(self.tabColoursFont)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.groupFont = QGroupBox(self.tabColoursFont)
        self.groupFont.setObjectName(u"groupFont")
        self.groupFont.setAlignment(Qt.AlignCenter)
        self.formLayout_2 = QFormLayout(self.groupFont)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.labelFontName = QLabel(self.groupFont)
        self.labelFontName.setObjectName(u"labelFontName")
        self.labelFontName.setMinimumSize(QSize(100, 20))

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.labelFontName)

        self.fontComboBox = QFontComboBox(self.groupFont)
        self.fontComboBox.setObjectName(u"fontComboBox")
        self.fontComboBox.setMinimumSize(QSize(150, 21))
        self.fontComboBox.setMaximumSize(QSize(200, 21))
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(12)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.fontComboBox.setCurrentFont(font)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.fontComboBox)

        self.labelFontSize = QLabel(self.groupFont)
        self.labelFontSize.setObjectName(u"labelFontSize")
        self.labelFontSize.setMinimumSize(QSize(100, 20))

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.labelFontSize)

        self.checkFontBold = QCheckBox(self.groupFont)
        self.checkFontBold.setObjectName(u"checkFontBold")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.checkFontBold)

        self.checkFontItalic = QCheckBox(self.groupFont)
        self.checkFontItalic.setObjectName(u"checkFontItalic")

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.checkFontItalic)

        self.comboFontSize = QComboBox(self.groupFont)
        self.comboFontSize.addItem("")
        self.comboFontSize.addItem("")
        self.comboFontSize.addItem("")
        self.comboFontSize.addItem("")
        self.comboFontSize.addItem("")
        self.comboFontSize.addItem("")
        self.comboFontSize.addItem("")
        self.comboFontSize.addItem("")
        self.comboFontSize.addItem("")
        self.comboFontSize.addItem("")
        self.comboFontSize.addItem("")
        self.comboFontSize.addItem("")
        self.comboFontSize.addItem("")
        self.comboFontSize.addItem("")
        self.comboFontSize.addItem("")
        self.comboFontSize.addItem("")
        self.comboFontSize.setObjectName(u"comboFontSize")
        self.comboFontSize.setMaximumSize(QSize(80, 16777215))

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.comboFontSize)


        self.gridLayout_4.addWidget(self.groupFont, 2, 0, 1, 1)

        self.groupColor = QGroupBox(self.tabColoursFont)
        self.groupColor.setObjectName(u"groupColor")
        self.groupColor.setAlignment(Qt.AlignCenter)
        self.formLayout = QFormLayout(self.groupColor)
        self.formLayout.setObjectName(u"formLayout")
        self.labelDocText = QLabel(self.groupColor)
        self.labelDocText.setObjectName(u"labelDocText")
        self.labelDocText.setMinimumSize(QSize(0, 0))

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelDocText)

        self.btnTextColor = QPushButton(self.groupColor)
        self.btnTextColor.setObjectName(u"btnTextColor")
        self.btnTextColor.setMinimumSize(QSize(30, 20))
        self.btnTextColor.setMaximumSize(QSize(30, 20))
        self.btnTextColor.setStyleSheet(u"QPushButton {\n"
"background-color: #000000;\n"
"border-style: outset;\n"
"border-width: 1px;\n"
"border-color: #000000;\n"
"} ")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.btnTextColor)

        self.labelBackground = QLabel(self.groupColor)
        self.labelBackground.setObjectName(u"labelBackground")
        self.labelBackground.setMinimumSize(QSize(0, 0))

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelBackground)

        self.btnBackgroundColor = QPushButton(self.groupColor)
        self.btnBackgroundColor.setObjectName(u"btnBackgroundColor")
        self.btnBackgroundColor.setMinimumSize(QSize(30, 20))
        self.btnBackgroundColor.setMaximumSize(QSize(30, 20))
        self.btnBackgroundColor.setStyleSheet(u"QPushButton {\n"
"background-color: #ffffff;\n"
"border-style: outset;\n"
"border-width: 1px;\n"
"border-color: #000000;\n"
"} ")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.btnBackgroundColor)

        self.labelLineColor = QLabel(self.groupColor)
        self.labelLineColor.setObjectName(u"labelLineColor")
        self.labelLineColor.setMinimumSize(QSize(0, 0))

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelLineColor)

        self.btnLineColor = QPushButton(self.groupColor)
        self.btnLineColor.setObjectName(u"btnLineColor")
        self.btnLineColor.setMinimumSize(QSize(30, 20))
        self.btnLineColor.setMaximumSize(QSize(30, 20))
        self.btnLineColor.setStyleSheet(u"QPushButton {\n"
"background-color: #e8e8ff;\n"
"border-style: outset;\n"
"border-width: 1px;\n"
"border-color: #000000;\n"
"} ")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.btnLineColor)

        self.labelLineNumbAreaText = QLabel(self.groupColor)
        self.labelLineNumbAreaText.setObjectName(u"labelLineNumbAreaText")
        self.labelLineNumbAreaText.setMinimumSize(QSize(0, 0))

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.labelLineNumbAreaText)

        self.btnLineNumbAreaText = QPushButton(self.groupColor)
        self.btnLineNumbAreaText.setObjectName(u"btnLineNumbAreaText")
        self.btnLineNumbAreaText.setMinimumSize(QSize(30, 20))
        self.btnLineNumbAreaText.setMaximumSize(QSize(30, 20))
        self.btnLineNumbAreaText.setStyleSheet(u"QPushButton {\n"
"background-color: #000000;\n"
"border-style: inset;\n"
"border-width: 1px;\n"
"border-color: #000000;\n"
"} ")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.btnLineNumbAreaText)

        self.labelLineNumbAreaBackgrnd = QLabel(self.groupColor)
        self.labelLineNumbAreaBackgrnd.setObjectName(u"labelLineNumbAreaBackgrnd")
        self.labelLineNumbAreaBackgrnd.setMinimumSize(QSize(200, 20))

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.labelLineNumbAreaBackgrnd)

        self.btnLineNumbAreaBackgrnd = QPushButton(self.groupColor)
        self.btnLineNumbAreaBackgrnd.setObjectName(u"btnLineNumbAreaBackgrnd")
        self.btnLineNumbAreaBackgrnd.setMinimumSize(QSize(30, 20))
        self.btnLineNumbAreaBackgrnd.setMaximumSize(QSize(30, 20))
        self.btnLineNumbAreaBackgrnd.setStyleSheet(u"QPushButton {\n"
"background-color: #c0c0c0;\n"
"border-style: outset;\n"
"border-width: 1px;\n"
"border-color: #000000;\n"
"} ")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.btnLineNumbAreaBackgrnd)


        self.gridLayout_4.addWidget(self.groupColor, 0, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer_2, 4, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer, 1, 0, 1, 1)

        self.tabWidget.addTab(self.tabColoursFont, "")

        self.verticalLayout_4.addWidget(self.tabWidget)

        self.btnClose = QPushButton(Opt)
        self.btnClose.setObjectName(u"btnClose")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnClose.sizePolicy().hasHeightForWidth())
        self.btnClose.setSizePolicy(sizePolicy)
        self.btnClose.setMinimumSize(QSize(75, 23))
        self.btnClose.setMaximumSize(QSize(75, 23))
        self.btnClose.setLayoutDirection(Qt.RightToLeft)

        self.verticalLayout_4.addWidget(self.btnClose)

        QWidget.setTabOrder(self.tabWidget, self.comboStyle)
        QWidget.setTabOrder(self.comboStyle, self.comboLocalization)
        QWidget.setTabOrder(self.comboLocalization, self.checkShowMenu)
        QWidget.setTabOrder(self.checkShowMenu, self.checkShowStatusBar)
        QWidget.setTabOrder(self.checkShowStatusBar, self.checkShowTabBar)
        QWidget.setTabOrder(self.checkShowTabBar, self.checkTabBarVertical)
        QWidget.setTabOrder(self.checkTabBarVertical, self.checkTabBarCloseBtn)
        QWidget.setTabOrder(self.checkTabBarCloseBtn, self.checkShowToolBar)
        QWidget.setTabOrder(self.checkShowToolBar, self.radioToolBarIconsSmall)
        QWidget.setTabOrder(self.radioToolBarIconsSmall, self.radioToolBarIconsMedium)
        QWidget.setTabOrder(self.radioToolBarIconsMedium, self.radioToolBarIconsLarge)
        QWidget.setTabOrder(self.radioToolBarIconsLarge, self.btnTextColor)
        QWidget.setTabOrder(self.btnTextColor, self.btnBackgroundColor)
        QWidget.setTabOrder(self.btnBackgroundColor, self.btnLineColor)
        QWidget.setTabOrder(self.btnLineColor, self.btnLineNumbAreaText)
        QWidget.setTabOrder(self.btnLineNumbAreaText, self.btnLineNumbAreaBackgrnd)
        QWidget.setTabOrder(self.btnLineNumbAreaBackgrnd, self.fontComboBox)
        QWidget.setTabOrder(self.fontComboBox, self.comboFontSize)
        QWidget.setTabOrder(self.comboFontSize, self.checkFontBold)
        QWidget.setTabOrder(self.checkFontBold, self.checkFontItalic)

        self.retranslateUi(Opt)
        self.btnClose.clicked.connect(Opt.close)

        self.tabWidget.setCurrentIndex(0)
        self.comboFontSize.setCurrentIndex(7)


        QMetaObject.connectSlotsByName(Opt)
    # setupUi

    def retranslateUi(self, Opt):
        Opt.setWindowTitle(QCoreApplication.translate("Opt", u"Options", None))
        self.comboStyle.setItemText(0, QCoreApplication.translate("Opt", u"windowsvista", None))
        self.comboStyle.setItemText(1, QCoreApplication.translate("Opt", u"Windows", None))
        self.comboStyle.setItemText(2, QCoreApplication.translate("Opt", u"Fusion", None))

        self.labelStyle.setText(QCoreApplication.translate("Opt", u"Select Style App:", None))
        self.labelLocalization.setText(QCoreApplication.translate("Opt", u"Localization:", None))
        self.comboLocalization.setItemText(0, QCoreApplication.translate("Opt", u"English", None))
        self.comboLocalization.setItemText(1, QCoreApplication.translate("Opt", u"Russian", None))

        self.checkShowMenu.setText(QCoreApplication.translate("Opt", u"Show Menu", None))
        self.checkShowStatusBar.setText(QCoreApplication.translate("Opt", u"Show Status Bar", None))
        self.groupTabBar.setTitle(QCoreApplication.translate("Opt", u"Tab Bar", None))
        self.checkShowTabBar.setText(QCoreApplication.translate("Opt", u"Show Tab Bar", None))
        self.checkTabBarVertical.setText(QCoreApplication.translate("Opt", u"Vertical Tab Bar", None))
        self.checkTabBarCloseBtn.setText(QCoreApplication.translate("Opt", u"Show Close Button", None))
        self.groupToolBar.setTitle(QCoreApplication.translate("Opt", u"Tool Bar", None))
        self.checkShowToolBar.setText(QCoreApplication.translate("Opt", u"Show Tool Bar", None))
        self.radioToolBarIconsSmall.setText(QCoreApplication.translate("Opt", u"Small Icons (16)", None))
        self.radioToolBarIconsMedium.setText(QCoreApplication.translate("Opt", u"Medium Icons (24)", None))
        self.radioToolBarIconsLarge.setText(QCoreApplication.translate("Opt", u"Large Icons (32)", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabMain), QCoreApplication.translate("Opt", u"Main", None))
        self.groupFont.setTitle(QCoreApplication.translate("Opt", u"Font Style", None))
        self.labelFontName.setText(QCoreApplication.translate("Opt", u"Font Name:", None))
        self.labelFontSize.setText(QCoreApplication.translate("Opt", u"Font Size:", None))
        self.checkFontBold.setText(QCoreApplication.translate("Opt", u"Bold", None))
        self.checkFontItalic.setText(QCoreApplication.translate("Opt", u"Italic", None))
        self.comboFontSize.setItemText(0, QCoreApplication.translate("Opt", u"5", None))
        self.comboFontSize.setItemText(1, QCoreApplication.translate("Opt", u"6", None))
        self.comboFontSize.setItemText(2, QCoreApplication.translate("Opt", u"7", None))
        self.comboFontSize.setItemText(3, QCoreApplication.translate("Opt", u"8", None))
        self.comboFontSize.setItemText(4, QCoreApplication.translate("Opt", u"9", None))
        self.comboFontSize.setItemText(5, QCoreApplication.translate("Opt", u"10", None))
        self.comboFontSize.setItemText(6, QCoreApplication.translate("Opt", u"11", None))
        self.comboFontSize.setItemText(7, QCoreApplication.translate("Opt", u"12", None))
        self.comboFontSize.setItemText(8, QCoreApplication.translate("Opt", u"14", None))
        self.comboFontSize.setItemText(9, QCoreApplication.translate("Opt", u"16", None))
        self.comboFontSize.setItemText(10, QCoreApplication.translate("Opt", u"18", None))
        self.comboFontSize.setItemText(11, QCoreApplication.translate("Opt", u"20", None))
        self.comboFontSize.setItemText(12, QCoreApplication.translate("Opt", u"22", None))
        self.comboFontSize.setItemText(13, QCoreApplication.translate("Opt", u"24", None))
        self.comboFontSize.setItemText(14, QCoreApplication.translate("Opt", u"26", None))
        self.comboFontSize.setItemText(15, QCoreApplication.translate("Opt", u"28", None))

        self.groupColor.setTitle(QCoreApplication.translate("Opt", u"Colour Style", None))
        self.labelDocText.setText(QCoreApplication.translate("Opt", u"Document Text:", None))
        self.btnTextColor.setText("")
        self.labelBackground.setText(QCoreApplication.translate("Opt", u"Document Background:", None))
        self.btnBackgroundColor.setText("")
        self.labelLineColor.setText(QCoreApplication.translate("Opt", u"Current Line Background:", None))
        self.btnLineColor.setText("")
        self.labelLineNumbAreaText.setText(QCoreApplication.translate("Opt", u"Line Number Area Text:", None))
        self.btnLineNumbAreaText.setText("")
        self.labelLineNumbAreaBackgrnd.setText(QCoreApplication.translate("Opt", u"Line Number Area Background:", None))
        self.btnLineNumbAreaBackgrnd.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabColoursFont), QCoreApplication.translate("Opt", u"Colours/Font", None))
        self.btnClose.setText(QCoreApplication.translate("Opt", u"Close", None))
    # retranslateUi

