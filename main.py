"""Main entry point for the PySide6 Notepad application."""

import codecs
import os
import sys
import subprocess
import time
from typing import Optional, Tuple
from chardet.universaldetector import UniversalDetector
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTabWidget,
    QFileDialog,
    QMessageBox,
    QLabel,
    QDialog,
    QMenu,
    QInputDialog,
    QColorDialog,
    QPushButton,
    QPlainTextEdit,
)
from PySide6.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog
from PySide6.QtCore import (
    QFile,
    QFileInfo,
    QEvent,
    QSize,
    QSettings,
    Qt,
    QRegularExpression,
    QTranslator,
)
from PySide6.QtGui import (
    QFont,
    QTextCursor,
    QPalette,
    QBrush,
    QAction,
    QColor,
    QTextDocument,
    QTextOption,
    QTextCharFormat,
    QSyntaxHighlighter,
    QFontMetricsF,
)
from ui.main_form import Ui_MainWindow
from codeeditor import CodeEditor
from ui.find_replace import Ui_Find
from ui.go_to import Ui_Goto
from ui.options import Ui_Opt
import ui.files_res
from constants import (
    EncodingType,
    LineEnding,
    TextFormat,
    ENCODING_NAMES,
    ENCODING_PYTHON_NAMES,
    LINE_ENDING_STRINGS,
    DEFAULT_FONT_FAMILY,
    DEFAULT_FONT_SIZE,
    DEFAULT_FONT_WEIGHT,
    DEFAULT_FONT_ITALIC,
    DEFAULT_ZOOM_INCREMENT,
    MIN_ZOOM_LEVEL,
    TAB_STOP_SPACES,
    DEFAULT_TEXT_COLOR,
    DEFAULT_BACKGROUND_COLOR,
    DEFAULT_LINE_COLOR,
    DEFAULT_LINE_NUMBER_AREA_TEXT,
    DEFAULT_LINE_NUMBER_AREA_BACKGROUND,
    DEFAULT_STYLE,
    DEFAULT_LANGUAGE,
    DEFAULT_MAX_RECENT_FILES,
    DEFAULT_ICON_SIZE,
    TEXT_FILE_EXTENSIONS,
    APP_VERSION,
    APP_RELEASE_DATE,
    APP_DEVELOPER,
)


class Editor(CodeEditor):
    """Extended code editor with file metadata and search highlighting."""

    def __init__(self):
        super().__init__()

        self.curName = ""
        self.zoomValue = 0
        self.encodingType = EncodingType.UTF8
        self.textFormat = TextFormat.TEXT_FILE
        self.lineEnding = LineEnding.WINDOWS_CRLF

        self.searchHighLight = SearchHighLight(self.document())
        self.setAcceptDrops(False)

    def zoom(self, delta: int) -> None:
        """Zoom in or out based on delta value."""
        zoom_increment = DEFAULT_ZOOM_INCREMENT if delta >= 0 else -DEFAULT_ZOOM_INCREMENT
        self.zoomIn(zoom_increment)
        self.zoomValue += zoom_increment

    def wheelEvent(self, event) -> None:
        """Handle wheel events, ignoring Ctrl+wheel for zoom."""
        if event.modifiers() & Qt.ControlModifier:
            event.ignore()
        else:
            QPlainTextEdit.wheelEvent(self, event)


class SearchHighLight(QSyntaxHighlighter):
    """Syntax highlighter for search text matches."""

    SEARCH_HIGHLIGHT_COLOR = "#9bff9b"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.pattern = QRegularExpression()
        self.format = QTextCharFormat()
        self.format.setBackground(QColor().fromString(self.SEARCH_HIGHLIGHT_COLOR))

    def highlightBlock(self, text: str) -> None:
        """Highlight matching text in the block."""
        match_iterator = self.pattern.globalMatch(text)
        while match_iterator.hasNext():
            match = match_iterator.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), self.format)

    def searchText(self, text: str) -> None:
        """Update search pattern and rehighlight."""
        self.pattern = QRegularExpression(text)
        self.rehighlight()


class Find(QDialog):
    def __init__(self, parent=None):
        super(Find, self).__init__(parent)
        self.ui = Ui_Find()
        self.ui.setupUi(self)
        self.setWindowIcon(self.parent().windowIcon())
        self.findReplaceActions()

    def changeEvent(self, event):
        if event.type() == QEvent.LanguageChange:
            self.ui.retranslateUi(self)
        super(Find, self).changeEvent(event)

    def findReplaceActions(self):

        self.ui.btnFind.clicked.connect(
            lambda: self.parent().find(
                self.ui.lineEditFind.text(),
                self.ui.checkCase.isChecked(),
                self.ui.checkWholeWord.isChecked(),
                self.ui.checkWrapAround.isChecked(),
            )
        )
        self.ui.btnReplace.clicked.connect(
            lambda: self.parent().replace(
                self.ui.lineEditFind.text(),
                self.ui.lineEditReplace.text(),
                self.ui.checkCase.isChecked(),
                self.ui.checkWholeWord.isChecked(),
                self.ui.checkWrapAround.isChecked(),
            )
        )
        self.ui.btnReplaceAll.clicked.connect(
            lambda: self.parent().replaceAll(
                self.ui.lineEditFind.text(),
                self.ui.lineEditReplace.text(),
                self.ui.checkCase.isChecked(),
                self.ui.checkWholeWord.isChecked(),
            )
        )


class Goto(QDialog):
    def __init__(self, parent=None):
        super(Goto, self).__init__(parent)
        self.ui = Ui_Goto()
        self.ui.setupUi(self)
        self.setWindowIcon(self.parent().windowIcon())

        self.ui.pushButton.clicked.connect(self.gotoClicked)

    def changeEvent(self, event):
        if event.type() == QEvent.LanguageChange:
            self.ui.retranslateUi(self)
        super(Goto, self).changeEvent(event)

    def gotoClicked(self):
        line = self.ui.spinBox.value() - 1
        doc = self.parent().tab.currentWidget()
        if line > doc.document().blockCount():
            doc.moveCursor(QTextCursor.End)
        else:
            cursor = QTextCursor(doc.document().findBlockByLineNumber(line))
            doc.setTextCursor(cursor)


class Options(QDialog):
    def __init__(self, parent=None):
        super(Options, self).__init__(parent)
        self.ui = Ui_Opt()
        self.ui.setupUi(self)
        self.setWindowIcon(self.windowIcon())

        self.loadOpt()
        self.optionsActions()

    def changeEvent(self, event):
        if event.type() == QEvent.LanguageChange:
            self.ui.retranslateUi(self)
        super(Options, self).changeEvent(event)

    def loadOpt(self):

        self.ui.comboStyle.setCurrentText(self.parent().currentStyle)
        self.ui.comboLocalization.setCurrentText(self.parent().language)

        self.ui.checkShowMenu.setChecked(self.parent().menuVisible)
        self.ui.checkShowStatusBar.setChecked(self.parent().statusBarVisible)
        self.ui.checkShowToolBar.setChecked(self.parent().toolBarVisible)
        self.ui.checkShowTabBar.setChecked(self.parent().tabBarVisible)
        self.ui.checkTabBarVertical.setChecked(self.parent().tabVertical)
        self.ui.checkTabBarCloseBtn.setChecked(self.parent().tab.tabsClosable())

        if self.parent().iSize == 16:
            self.ui.radioToolBarIconsSmall.setChecked(True)
        if self.parent().iSize == 24:
            self.ui.radioToolBarIconsMedium.setChecked(True)
        if self.parent().iSize == 32:
            self.ui.radioToolBarIconsLarge.setChecked(True)

        for i in range(self.ui.formLayout.count()):
            w = self.ui.formLayout.itemAt(i).widget()
            if isinstance(w, QPushButton):
                if w.objectName() == "btnTextColor":
                    text = self.parent().colorText
                if w.objectName() == "btnBackgroundColor":
                    text = self.parent().backgroundColor
                if w.objectName() == "btnLineColor":
                    text = self.parent().lineColor
                if w.objectName() == "btnLineNumbAreaText":
                    text = self.parent().lineNumberAreaText
                if w.objectName() == "btnLineNumbAreaBackgrnd":
                    text = self.parent().lineNumberAreaBackgrnd
                w.setStyleSheet(
                    "QPushButton {\n"
                    "background-color: %s;\n"
                    "border-style: outset;\n"
                    "border-width: 1px;\n"
                    "border-color: #000000;\n"
                    "} " % text
                )

        self.ui.fontComboBox.setCurrentText(self.parent().fontFamily)
        self.ui.comboFontSize.setCurrentText(str(self.parent().sizeTxt))

        self.ui.checkFontBold.setChecked(self.parent().fontWeight == 800)

        self.ui.checkFontItalic.setChecked(self.parent().fontItalic)

    def optionsActions(self):
        # General
        self.ui.comboStyle.currentIndexChanged.connect(self.changeStyleApp)
        self.ui.comboLocalization.currentIndexChanged.connect(self.changelang)
        self.ui.checkShowMenu.stateChanged.connect(self.showMenu)
        self.ui.checkShowStatusBar.stateChanged.connect(self.showStatusBar)

        self.ui.checkShowTabBar.stateChanged.connect(self.showTabBar)
        self.ui.checkTabBarVertical.stateChanged.connect(self.changeTabBarPos)
        self.ui.checkTabBarCloseBtn.stateChanged.connect(self.showTabCloseBtn)

        self.ui.checkShowToolBar.stateChanged.connect(self.showToolBar)
        self.ui.radioToolBarIconsSmall.toggled.connect(
            lambda: self.parent().iconSizeToolBar(16)
        )
        self.ui.radioToolBarIconsMedium.toggled.connect(
            lambda: self.parent().iconSizeToolBar(24)
        )
        self.ui.radioToolBarIconsLarge.toggled.connect(
            lambda: self.parent().iconSizeToolBar(32)
        )

        # Colour/Font

        self.ui.btnTextColor.clicked.connect(
            lambda: self.colorDialog(self.ui.btnTextColor, self.parent().colorText)
        )
        self.ui.btnBackgroundColor.clicked.connect(
            lambda: self.colorDialog(
                self.ui.btnBackgroundColor, self.parent().backgroundColor
            )
        )
        self.ui.btnLineColor.clicked.connect(
            lambda: self.colorDialog(self.ui.btnLineColor, self.parent().lineColor)
        )
        self.ui.btnLineNumbAreaText.clicked.connect(
            lambda: self.colorDialog(
                self.ui.btnLineNumbAreaText, self.parent().lineNumberAreaText
            )
        )
        self.ui.btnLineNumbAreaBackgrnd.clicked.connect(
            lambda: self.colorDialog(
                self.ui.btnLineNumbAreaBackgrnd, self.parent().lineNumberAreaBackgrnd
            )
        )

        self.ui.fontComboBox.currentIndexChanged.connect(self.changeFontName)
        self.ui.comboFontSize.currentIndexChanged.connect(self.changeFontSize)
        self.ui.checkFontBold.stateChanged.connect(self.changeFontBold)
        self.ui.checkFontItalic.stateChanged.connect(self.changeFontItalic)

    def changeStyleApp(self, idx):
        text = self.ui.comboStyle.itemText(idx)
        self.parent().currentStyle = text
        app.setStyle(text)
        self.update()

    def changelang(self, idx):
        self.parent().translateApp(idx)
        self.parent().update_window_title()
        self.parent().updateRecentFileActions()

    def showMenu(self, visible: bool) -> None:
        """Toggle menu bar visibility."""
        self.parent().menuVisible = visible
        self.parent().ui.menubar.setVisible(visible)

    def showStatusBar(self, visible: bool) -> None:
        """Toggle status bar visibility."""
        self.parent().statusBarVisible = visible
        self.parent().ui.statusbar.setVisible(visible)

    def showTabBar(self, visible: bool) -> None:
        """Toggle tab bar visibility."""
        self.parent().tabBarVisible = visible
        self.parent().tab.tabBar().setVisible(visible)

    def changeTabBarPos(self, vertical: bool) -> None:
        """Change tab bar position."""
        self.parent().tabVertical = vertical
        position = QTabWidget.West if vertical else QTabWidget.North
        self.parent().tab.setTabPosition(position)

    def showTabCloseBtn(self, visible: bool) -> None:
        """Toggle tab close button visibility."""
        self.parent().tabCloseBtn = visible
        self.parent().tab.setTabsClosable(visible)

    def showToolBar(self, visible: bool) -> None:
        """Toggle toolbar visibility."""
        self.parent().toolBarVisible = visible
        toolbars = [
            self.parent().ui.toolBarFile,
            self.parent().ui.toolBarEdit,
            self.parent().ui.toolBarView,
        ]
        for toolbar in toolbars:
            toolbar.setVisible(visible)

    def colorDialog(self, btn, text):
        col = QColorDialog.getColor(QColor().fromString(text), self)
        if not col.isValid():
            return
        btn.setStyleSheet(
            "QPushButton {\n"
            "background-color: %s;\n"
            "border-style: outset;\n"
            "border-width: 1px;\n"
            "border-color: #000000;\n"
            "} " % col.name()
        )
        if btn == self.ui.btnTextColor:
            self.parent().colorText = col.name()
        if btn == self.ui.btnBackgroundColor:
            self.parent().backgroundColor = col.name()
        if btn == self.ui.btnLineColor:
            self.parent().lineColor = col.name()
        if btn == self.ui.btnLineNumbAreaText:
            self.parent().lineNumberAreaText = col.name()
        if btn == self.ui.btnLineNumbAreaBackgrnd:
            self.parent().lineNumberAreaBackgrnd = col.name()
        self.changeColor()

    def changeColor(self):
        palette = QPalette()
        palette.setColor(QPalette.Text, QColor().fromString(self.parent().colorText))
        palette.setColor(
            QPalette.Base, QColor().fromString(self.parent().backgroundColor)
        )
        for idx in range(self.parent().tab.count()):
            w = self.parent().tab.widget(idx)
            w.setPalette(palette)
            w.lineColor = QColor().fromString(self.parent().lineColor)
            w.lineNumberAreaText = QColor().fromString(self.parent().lineNumberAreaText)
            w.lineNumberAreaBackground = QColor().fromString(
                self.parent().lineNumberAreaBackgrnd
            )
            w.highlight_current_line()
            w.line_number_area.repaint()

    def changeFontName(self, idx):
        self.parent().fontFamily = self.ui.fontComboBox.itemText(idx)
        self.parent().changeFont()

    def changeFontSize(self, idx):
        self.parent().sizeTxt = int(self.ui.comboFontSize.itemText(idx))
        self.parent().changeFont()

    def changeFontBold(self, checked: bool) -> None:
        """Toggle font bold weight."""
        self.parent().fontWeight = 800 if checked else 500
        self.parent().changeFont()

    def changeFontItalic(self, checked: bool) -> None:
        """Toggle font italic style."""
        self.parent().fontItalic = checked
        self.parent().changeFont()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.settings = QSettings("config.ini", QSettings.IniFormat)
        self.trans = QTranslator()
        self.loadSettings()
        self.createUi()
        self.newFile()
        self.optionsDlg = Options(self)
        self.findDlg = Find(self)
        self.gotoDlg = Goto(self)
        self.createRecentList()
        self.connectActions()
        self.update_window_title()
        self.setAcceptDrops(True)

    def loadSettings(self):
        # Glob zoom
        self.zoomGlob = 0
        # New document count
        self.numbDoc = 0
        # Rename dialog selected text
        self.textFromDlg = ""
        # Style window (windowsvista; Windows; Fusion)
        self.currentStyle = self.settings.value("MAIN/CURRENT_STYLE", DEFAULT_STYLE)
        app.setStyle(self.currentStyle)
        self.update()
        # Language (English; Russian)
        self.language = self.settings.value("MAIN/LANGUAGE", DEFAULT_LANGUAGE)
        if self.language == "English":
            self.translateApp(0)
        else:
            self.translateApp(1)
        # Menu
        self.menuVisible = self.settings.value("MAIN/SHOW_MENU", True, type=bool)
        self.ui.menubar.setVisible(self.menuVisible)
        # StatusBar
        self.statusBarVisible = self.settings.value(
            "MAIN/SHOW_STATUSBAR", True, type=bool
        )
        self.ui.statusbar.setVisible(self.statusBarVisible)
        # TabBar
        self.tabBarVisible = self.settings.value("MAIN/SHOW_TABBAR", True, type=bool)
        self.tabVertical = self.settings.value("MAIN/VERTICAL_TABBAR", False, type=bool)
        self.tabCloseBtn = self.settings.value("MAIN/TAB_CLOSE_BTN", True, type=bool)
        # ToolBar
        self.toolBarVisible = self.settings.value("MAIN/SHOW_TOOLBAR", True, type=bool)
        self.ui.toolBarFile.setVisible(self.toolBarVisible)
        self.ui.toolBarEdit.setVisible(self.toolBarVisible)
        self.ui.toolBarView.setVisible(self.toolBarVisible)
        # Icon size ToolBar (16-Small; 24-Medium; 32-Large)
        self.iSize = self.settings.value("MAIN/TOOLBAR_ICONS_SIZE", DEFAULT_ICON_SIZE, type=int)
        self.iconSizeToolBar(self.iSize)
        # Color
        self.colorText = self.settings.value("COLOUR/TEXT_COLOUR", DEFAULT_TEXT_COLOR)
        self.backgroundColor = self.settings.value(
            "COLOUR/BACKGROUND_COLOUR", DEFAULT_BACKGROUND_COLOR
        )
        self.lineColor = self.settings.value("COLOUR/LINE_COLOUR", DEFAULT_LINE_COLOR)
        self.lineNumberAreaText = self.settings.value(
            "COLOUR/LINE_NUMBER_AREA_TEXT", DEFAULT_LINE_NUMBER_AREA_TEXT
        )
        self.lineNumberAreaBackgrnd = self.settings.value(
            "COLOUR/LINE_NUMBER_AREA_BACKGROUND", DEFAULT_LINE_NUMBER_AREA_BACKGROUND
        )
        # Font
        self.fontFamily = self.settings.value("FONT/FONT_FAMILY", DEFAULT_FONT_FAMILY)
        self.sizeTxt = self.settings.value("FONT/FONT_SIZE", DEFAULT_FONT_SIZE, type=int)
        self.fontWeight = self.settings.value("FONT/FONT_WEIGHT", DEFAULT_FONT_WEIGHT, type=int)
        self.fontItalic = self.settings.value("FONT/FONT_ITALIC", DEFAULT_FONT_ITALIC, type=bool)
        # Geometry
        max = self.settings.value("GEOMETRY/APP_MAXIMIZED", False, type=bool)
        heightApp = self.settings.value("GEOMETRY/APP_HEIGHT", 500, type=int)
        widthApp = self.settings.value("GEOMETRY/APP_WIDTH", 730, type=int)
        x = self.settings.value("GEOMETRY/START_POS_X", 475, type=int)
        y = self.settings.value("GEOMETRY/START_POS_Y", 224, type=int)
        if max:
            self.setWindowState(Qt.WindowState.WindowMaximized)
        self.resize(widthApp, heightApp)
        self.move(x, y)
        # Recent files
        self.maxRecentFiles = DEFAULT_MAX_RECENT_FILES
        self.recentFileActs = []
        self.files = self.settings.value("RECENT_FILE_LIST/FILES", [], type=list)

    def saveSettings(self):
        self.settings.beginGroup("MAIN")
        self.settings.setValue("CURRENT_STYLE", self.currentStyle)
        self.settings.setValue("LANGUAGE", self.language)
        self.settings.setValue("SHOW_MENU", self.menuVisible)
        self.settings.setValue("SHOW_STATUSBAR", self.statusBarVisible)
        self.settings.setValue("SHOW_TABBAR", self.tabBarVisible)
        self.settings.setValue("VERTICAL_TABBAR", self.tabVertical)
        self.settings.setValue("TAB_CLOSE_BTN", self.tabCloseBtn)
        self.settings.setValue("SHOW_TOOLBAR", self.toolBarVisible)
        self.settings.setValue("TOOLBAR_ICONS_SIZE", self.iSize)
        self.settings.endGroup()
        self.settings.beginGroup("COLOUR")
        self.settings.setValue("TEXT_COLOUR", self.colorText)
        self.settings.setValue("BACKGROUND_COLOUR", self.backgroundColor)
        self.settings.setValue("LINE_COLOUR", self.lineColor)
        self.settings.setValue("LINE_NUMBER_AREA_TEXT", self.lineNumberAreaText)
        self.settings.setValue(
            "LINE_NUMBER_AREA_BACKGROUND", self.lineNumberAreaBackgrnd
        )
        self.settings.endGroup()
        self.settings.beginGroup("FONT")
        self.settings.setValue("FONT_FAMILY", self.fontFamily)
        self.settings.setValue("FONT_SIZE", self.sizeTxt)
        self.settings.setValue("FONT_WEIGHT", self.fontWeight)
        self.settings.setValue("FONT_ITALIC", self.fontItalic)
        self.settings.endGroup()
        self.settings.beginGroup("GEOMETRY")
        self.settings.setValue("APP_MAXIMIZED", self.isMaximized())
        if not self.isMaximized():
            self.settings.setValue("APP_HEIGHT", self.size().height())
            self.settings.setValue("APP_WIDTH", self.size().width())
            self.settings.setValue("START_POS_X", self.pos().x())
            self.settings.setValue("START_POS_Y", self.pos().y())
        self.settings.endGroup()
        self.settings.beginGroup("RECENT_FILE_LIST")
        if len(self.files) == 0:
            self.settings.remove("")
        else:
            self.settings.setValue("FILES", self.files)
        self.settings.endGroup()

    def translateApp(self, idx):
        if idx == 0:
            app1 = QApplication.instance()
            app1.removeTranslator(self.trans)
            self.ui.retranslateUi(self)
            self.language = "English"
        else:
            self.trans.load("ru_Ru")
            app1 = QApplication.instance()
            app1.installTranslator(self.trans)
            self.ui.retranslateUi(self)
            self.language = "Russian"

    def createUi(self):
        # StatusBar
        self.textFormatLabel = QLabel("Text File")
        self.textFormatLabel.setMinimumWidth(50)
        self.ui.statusbar.addPermanentWidget(self.textFormatLabel)
        self.chrCountLabel = QLabel("Length: 1")
        self.chrCountLabel.setMinimumWidth(80)
        self.ui.statusbar.addPermanentWidget(self.chrCountLabel)
        self.cursorPosLabel = QLabel("Ln: 1 Col: 1")
        self.cursorPosLabel.setMinimumWidth(100)
        self.ui.statusbar.addPermanentWidget(self.cursorPosLabel)
        self.symbNewLineLabel = QLabel("Windows (CR LF)")
        self.symbNewLineLabel.setMinimumWidth(100)
        self.ui.statusbar.addPermanentWidget(self.symbNewLineLabel)
        self.encTxtLabel = QLabel("UTF-8")
        self.encTxtLabel.setMinimumWidth(80)
        self.ui.statusbar.addPermanentWidget(self.encTxtLabel)
        self.zoomLabel = QLabel("Zoom: 100%")
        self.zoomLabel.setMinimumWidth(80)
        self.ui.statusbar.addPermanentWidget(self.zoomLabel)
        # Tabpanel
        self.tab = QTabWidget()
        self.setCentralWidget(self.tab)
        self.tab.setMovable(True)
        self.tab.setDocumentMode(True)

        self.tab.tabBar().setVisible(self.tabBarVisible)
        if self.tabVertical:
            self.tab.setTabPosition(QTabWidget.West)
        else:
            self.tab.setTabPosition(QTabWidget.North)
        self.tab.setTabsClosable(self.tabCloseBtn)

    def createRecentList(self):
        self.separatorAct = self.ui.menuFile.insertSeparator(self.ui.actionExit)
        for i in range(self.maxRecentFiles):
            self.recentFileActs.append(
                QAction(self, visible=False, triggered=self.openRecentFile)
            )
            self.ui.menuFile.insertAction(self.ui.actionExit, self.recentFileActs[i])
        self.emptyRecentListAction = QAction(
            self, visible=False, triggered=self.emptyRecentList
        )
        self.emptyRecentListAction.setText("Empty Recent Files List")
        self.ui.menuFile.insertAction(self.ui.actionExit, self.emptyRecentListAction)
        self.updateRecentFileActions()

    def openRecentFile(self):
        action = self.sender()
        if action:
            self.openFile(action.data())

    def emptyRecentList(self):
        self.files.clear()
        for widget in QApplication.topLevelWidgets():
            if isinstance(widget, MainWindow):
                widget.updateRecentFileActions()

        self.separatorAct.setVisible(False)
        self.emptyRecentListAction.setVisible(False)

    def updateRecentFileActions(self):
        if self.language == "English":
            txt1 = "Empty Recent Files List"
        else:
            txt1 = "Очистить список недавних файлов"

        numRecentFiles = min(len(self.files), self.maxRecentFiles)

        for i in range(numRecentFiles):
            text = "&%d: %s" % (i + 1, os.path.basename(self.files[i]))
            self.recentFileActs[i].setText(text)
            self.recentFileActs[i].setData(self.files[i])
            self.recentFileActs[i].setVisible(True)

        for j in range(numRecentFiles, self.maxRecentFiles):
            self.recentFileActs[j].setVisible(False)

        if numRecentFiles > 0:
            self.separatorAct.setVisible(True)
            self.emptyRecentListAction.setVisible(True)
            self.emptyRecentListAction.setText(txt1)

    def connectActions(self):
        # Tabs
        self.tab.tabBarClicked.connect(self.tabClick)
        self.tab.tabCloseRequested.connect(self.closeFile)
        self.tab.currentChanged.connect(self.tab_changed)
        self.tab.customContextMenuRequested.connect(self.contextTab)
        # File-menu
        self.ui.actionNew.triggered.connect(self.newFile)
        self.ui.actionOpen.triggered.connect(self.openDialog)
        self.ui.actionSave.triggered.connect(self.save)
        self.ui.actionSaveAs.triggered.connect(self.saveAs)
        self.ui.actionPrint.triggered.connect(self.printFile)
        self.ui.actionPrintPreview.triggered.connect(self.printPreview)
        self.ui.actionClose.triggered.connect(
            lambda: self.closeFile(self.tab.currentIndex())
        )
        self.ui.actionCloseAll.triggered.connect(self.closeAllFiles)
        self.ui.actionOptions.triggered.connect(lambda: self.optionsDlg.show())

        self.ui.actionExit.triggered.connect(self.close)

        # Edit-menu
        self.ui.actionUndo.triggered.connect(lambda: self.tab.currentWidget().undo())
        self.ui.actionRedo.triggered.connect(lambda: self.tab.currentWidget().redo())
        self.ui.actionCut.triggered.connect(lambda: self.tab.currentWidget().cut())
        self.ui.actionCopy.triggered.connect(lambda: self.tab.currentWidget().copy())
        self.ui.actionPaste.triggered.connect(lambda: self.tab.currentWidget().paste())
        self.ui.actionSelectAll.triggered.connect(
            lambda: self.tab.currentWidget().selectAll()
        )
        self.ui.actionFindReplace.triggered.connect(self.runFindDlg)
        self.ui.actionGoto.triggered.connect(lambda: self.gotoDlg.show())
        self.ui.actionDateTime.triggered.connect(self.insertDateTime)
        self.ui.actionUPPERCASE.triggered.connect(self.uppercase)
        self.ui.actionLowercase.triggered.connect(self.lowercase)
        self.ui.actionProperCase.triggered.connect(self.propercase)
        self.ui.actionTrimTrailingSpace.triggered.connect(self.trim_trailing_space)
        self.ui.actionTrimLeadingSpace.triggered.connect(self.trim_leading_space)
        self.ui.actionTabToSpace.triggered.connect(self.tab_to_space)
        self.ui.actionRemoveSpace.triggered.connect(self.remove_space)
        self.ui.actionJoinLines.triggered.connect(self.join_lines)
        self.ui.actionRemoveEmptyLines.triggered.connect(self.remove_empty_lines)
        self.ui.actionRemoveDuplicateLines.triggered.connect(self.remove_duplicate_lines)
        self.ui.actionSortLinesAscendingOrder.triggered.connect(
            self.sort_lines_ascending_order
        )
        self.ui.actionSortLinesDescendingOrder.triggered.connect(
            self.sort_lines_descending_order
        )
        self.ui.actionWindowsCRLF.triggered.connect(self.windows_crlf)
        self.ui.actionUnixLF.triggered.connect(self.unix_lf)

        # View-menu
        self.ui.actionAlwaysTop.toggled.connect(self.window_on_top)
        self.ui.actionShowSpaceTab.triggered.connect(self.show_space_tab)
        self.ui.actionWrapText.toggled.connect(self.wrap_text)
        self.ui.actionZoomIn.triggered.connect(self.zoom_in)
        self.ui.actionZoomOut.triggered.connect(self.zoom_out)
        self.ui.actionZoomRestore.triggered.connect(self.zoom_restore)
        self.ui.actionSummary.triggered.connect(self.summary_doc)

        # Encoding
        self.ui.actionUTF8.toggled.connect(self.change_encoding)
        self.ui.actionUTF8BOM.toggled.connect(self.change_encoding)
        self.ui.actionUTF16BE.toggled.connect(self.change_encoding)
        self.ui.actionUTF16LE.toggled.connect(self.change_encoding)
        self.ui.actionWindows1251.toggled.connect(self.change_encoding)
        self.ui.actionOEM866.toggled.connect(self.change_encoding)

        # Help-menu
        self.ui.actionAbout.triggered.connect(self.about)

    def runFindDlg(self):
        text = self.tab.currentWidget().textCursor().selectedText()
        if text:
            self.findDlg.ui.lineEditFind.setText(text)
        self.findDlg.show()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            self.openFile(f)

    def closeEvent(self, event):
        if self.maybeSave():
            self.saveSettings()
            event.accept()
        else:
            event.ignore()

    def tabClick(self, idx):
        if idx == -1:
            self.tab.setContextMenuPolicy(Qt.NoContextMenu)
        else:
            self.tab.setCurrentIndex(idx)
            self.tab.setContextMenuPolicy(Qt.CustomContextMenu)

    def contextTab(self, point):
        if self.language == "English":
            txt1 = "Close"
            txt2 = "Rename"
            txt3 = "Open Containing Folder"
            txt4 = "Reload"
        else:
            txt1 = "Закрыть"
            txt2 = "Переименовать"
            txt3 = "Открыть папку файла"
            txt4 = "Перезагрузить"

        menu = QMenu()
        closeAction = QAction(txt1, menu)
        closeAction.triggered.connect(lambda: self.closeFile(self.tab.currentIndex()))
        menu.addAction(closeAction)

        renameAction = QAction(txt2, menu)
        renameAction.triggered.connect(lambda: self.renameTab(self.tab.currentIndex()))
        menu.addAction(renameAction)

        openFolderAction = QAction(txt3, menu)
        openFolderAction.triggered.connect(self.openFolder)
        menu.addAction(openFolderAction)

        reloadFileAction = QAction(txt4, menu)
        reloadFileAction.triggered.connect(self.reloadFile)
        menu.addAction(reloadFileAction)

        if self.tab.currentWidget().curName:
            openFolderAction.setVisible(True)
            reloadFileAction.setVisible(True)
        else:
            openFolderAction.setVisible(False)
            reloadFileAction.setVisible(False)

        menu.exec(self.tab.mapToGlobal(point))

    def renameTab(self, idx: int) -> None:
        """Rename the file in the specified tab."""
        if self.language == "English":
            dialog_title = "Rename Current File:"
            label_text = "New Name:"
            ok_text = "Ok"
            cancel_text = "Cancel"
            error_msg = "Cannot rename file "
        else:
            dialog_title = "Переименовать файл:"
            label_text = "Новое имя:"
            ok_text = "Да"
            cancel_text = "Нет"
            error_msg = "Невозможно переименовать файл "

        dlg = QInputDialog(self)
        dlg.setWindowTitle(dialog_title)
        dlg.setLabelText(label_text)
        dlg.setTextValue(self.tab.tabText(idx))
        dlg.setOkButtonText(ok_text)
        dlg.setCancelButtonText(cancel_text)
        dlg.textValueSelected.connect(self.textInputDlg)
        dlg.exec()
        newName = self.textFromDlg

        if not newName:
            return

        doc = self.tab.widget(idx)
        info = QFileInfo(doc.curName)
        if info.exists():
            path = info.absolutePath()
            filePath = info.absoluteFilePath()
            fileName = info.fileName()
            file = QFile(filePath)
            new_path = os.path.join(path, newName)
            if not file.rename(filePath, new_path):
                QMessageBox.warning(
                    self,
                    "Notepad",
                    f"{error_msg}{fileName}:\n{file.errorString()}.",
                )
                return
            doc.curName = new_path

        self.tab.setTabText(idx, newName)
        self.update_window_title()

    def textInputDlg(self, txt):
        self.textFromDlg = txt

    def openFolder(self) -> None:
        """Open the folder containing the current file in Windows Explorer."""
        doc = self.tab.currentWidget()
        if not doc.curName:
            return
            
        info = QFileInfo(doc.curName)
        if info.exists():
            path = info.absolutePath().replace("/", "\\")
            try:
                subprocess.Popen(f'explorer.exe "{path}"')
            except Exception as e:
                if self.language == "English":
                    error_msg = "Cannot open folder"
                else:
                    error_msg = "Невозможно открыть папку"
                QMessageBox.warning(self, "Notepad", f"{error_msg}:\n{str(e)}.")

    def reloadFile(self) -> None:
        """Reload current file from disk."""
        doc = self.tab.currentWidget()
        path = doc.curName
        if not path:
            return
        
        try:
            enc = self.detector(path)
            with open(path, "r", encoding=enc, errors="replace") as file:
                txt = file.read()
            doc.setPlainText(txt)
            doc.document().setModified(False)
            self.update_status_bar()
        except Exception as e:
            if self.language == "English":
                error_msg = "Cannot reload file "
            else:
                error_msg = "Невозможно перезагрузить файл "
            QMessageBox.warning(self, "Notepad", f"{error_msg}{path}:\n{str(e)}.")

    def iconSizeToolBar(self, size):
        self.iSize = size
        self.ui.toolBarFile.setIconSize(QSize(size, size))
        self.ui.toolBarEdit.setIconSize(QSize(size, size))
        self.ui.toolBarView.setIconSize(QSize(size, size))

    def changeFont(self):
        for idx in range(self.tab.count()):
            self.tab.widget(idx).setFont(
                QFont(self.fontFamily, self.sizeTxt, self.fontWeight, self.fontItalic)
            )
            self.tab.widget(idx).zoomValue = 0
        self.zoomGlob = 0
        self.update_status_bar()

    def documentWasModified(self):
        if self.tab.count() >= 1:
            self.setWindowModified(self.tab.currentWidget().document().isModified())

    def maybeSave(self):
        if self.tab.currentWidget().document().isModified():
            if self.language == "English":
                msg = (
                    "The document has been modified.\nDo you want to save your changes?"
                )
                txt1 = "Save"
                txt2 = "Discard"
                txt3 = "Cancel"
            else:
                msg = "Документ был изменен.\nХотите сохранить измнения?"
                txt1 = "Сохранить"
                txt2 = "Нет"
                txt3 = "Отмена"
            msgBox = QMessageBox(self)
            msgBox.setText(msg)
            msgBox.setIcon(QMessageBox.Question)
            msgBox.setWindowTitle("Notepad")
            saveBtn = msgBox.addButton(txt1, QMessageBox.AcceptRole)
            msgBox.addButton(txt2, QMessageBox.DestructiveRole)
            cancelBtn = msgBox.addButton(txt3, QMessageBox.RejectRole)
            msgBox.exec()
            if msgBox.clickedButton() == saveBtn:
                return self.save()
            if msgBox.clickedButton() == cancelBtn:
                return False
        return True

    def createTab(self, fileName, path, txt):
        doc = Editor()

        doc.document().contentsChanged.connect(self.documentWasModified)
        doc.cursorPositionChanged.connect(self.cursorChanged)
        doc.setContextMenuPolicy(Qt.CustomContextMenu)
        doc.customContextMenuRequested.connect(self.context_doc)

        # Text format
        if path:
            doc.curName = path
            fi = QFileInfo(path)
            ext = fi.suffix()
            doc.textFormat = TextFormat.TEXT_FILE if ext in TEXT_FILE_EXTENSIONS else TextFormat.OTHER
        elif fileName.find(".txt") == -1:
            doc.textFormat = TextFormat.OTHER

        # Endline symbol
        if txt:
            doc.setPlainText(txt)
            line_ending = self.lineEndingsOpt(txt)
            if line_ending == LINE_ENDING_STRINGS[LineEnding.WINDOWS_CRLF]:
                doc.lineEnding = LineEnding.WINDOWS_CRLF
            elif line_ending == LINE_ENDING_STRINGS[LineEnding.UNIX_LF]:
                doc.lineEnding = LineEnding.UNIX_LF
            else:
                doc.lineEnding = LineEnding.WINDOWS_CRLF

        # Color
        palette = QPalette()
        brush = QBrush(QColor(0, 120, 215))
        brush.setStyle(Qt.SolidPattern)
        brush1 = QBrush(QColor(255, 255, 255))
        brush1.setStyle(Qt.SolidPattern)
        # Highlight Text inactive
        palette.setBrush(QPalette.Inactive, QPalette.Highlight, brush)
        palette.setBrush(QPalette.Inactive, QPalette.HighlightedText, brush1)
        # Text
        palette.setColor(QPalette.Text, QColor().fromString(self.colorText))
        # Background
        palette.setColor(QPalette.Base, QColor().fromString(self.backgroundColor))
        doc.setPalette(palette)
        doc.lineColor = QColor().fromString(self.lineColor)
        doc.lineNumberAreaText = QColor().fromString(self.lineNumberAreaText)
        doc.lineNumberAreaBackground = QColor().fromString(self.lineNumberAreaBackgrnd)
        doc.highlight_current_line()
        doc.line_number_area.repaint()

        # Font
        doc.setFont(
            QFont(self.fontFamily, self.sizeTxt, self.fontWeight, self.fontItalic)
        )

        # Zoom
        if self.zoomGlob <= (0 - self.sizeTxt):
            self.zoom_restore()
        else:
            doc.zoomValue = self.zoomGlob
            doc.zoomIn(doc.zoomValue)

        # Wrapline
        if self.ui.actionWrapText.isChecked():
            doc.setLineWrapMode(Editor.WidgetWidth)
        else:
            doc.setLineWrapMode(Editor.NoWrap)

        # Show space and tabs
        option = QTextOption()
        if self.ui.actionShowSpaceTab.isChecked():
            option.setFlags(option.flags() | QTextOption.ShowTabsAndSpaces)
        else:
            option.setFlags(option.flags() & QTextOption.ShowTabsAndSpaces)
        doc.document().setDefaultTextOption(option)
        doc.setTabStopDistance(QFontMetricsF(doc.font()).horizontalAdvance(" ") * TAB_STOP_SPACES)

        idx = self.tab.addTab(doc, fileName)
        self.tab.setCurrentIndex(idx)
        self.update_window_title()
        self.update_status_bar()
        self.update_encoding_menu()
        self.update_eol()

    def context_doc(self, point):
        if self.language == "English":
            txt1 = "Undo"
            txt2 = "Redo"
            txt3 = "Cut"
            txt4 = "Copy"
            txt5 = "Paste"
            txt6 = "Select All"
        else:
            txt1 = "Отменить"
            txt2 = "Повторить"
            txt3 = "Вырезать"
            txt4 = "Копировать"
            txt5 = "Вставить"
            txt6 = "Выделить все"

        menu = QMenu()
        undoAction = QAction(txt1, menu)
        undoAction.triggered.connect(lambda: self.tab.currentWidget().undo())
        menu.addAction(undoAction)

        redoAction = QAction(txt2, menu)
        redoAction.triggered.connect(lambda: self.tab.currentWidget().redo())
        menu.addAction(redoAction)

        cutAction = QAction(txt3, menu)
        cutAction.triggered.connect(lambda: self.tab.currentWidget().cut())
        menu.addAction(cutAction)

        copyAction = QAction(txt4, menu)
        copyAction.triggered.connect(lambda: self.tab.currentWidget().copy())
        menu.addAction(copyAction)

        pasteAction = QAction(txt5, menu)
        pasteAction.triggered.connect(lambda: self.tab.currentWidget().paste())
        menu.addAction(pasteAction)

        selectAction = QAction(txt6, menu)
        selectAction.triggered.connect(lambda: self.tab.currentWidget().selectAll())
        menu.addAction(selectAction)

        menu.exec(self.tab.currentWidget().mapToGlobal(point))

    def newFile(self):
        self.numbDoc += 1
        fileName = "Untitled" + str(self.numbDoc) + ".txt"
        path = ""
        txt = ""
        self.createTab(fileName, path, txt)

    def openDialog(self):
        if self.language == "English":
            txt1 = "Open File"
            txt2 = "Text Files (*.txt);; All Files (*)"
        else:
            txt1 = "Открыть файл"
            txt2 = "Текстовые файлы (*.txt);; Все файлы (*)"

        path, _ = QFileDialog.getOpenFileName(self, txt1, "", txt2)
        if path:
            return self.openFile(path)

    def openFile(self, path: str) -> bool:
        """Open a file in a new tab. Returns True if successful."""
        if self.language == "English":
            txt1 = "Cannot read file "
            txt2 = "The file is open"
            txt3 = "The file is already opened in Notepad"
        else:
            txt1 = "Невозможно прочитать файл "
            txt2 = "Файл открыт"
            txt3 = "Файл уже открыт в Notepad"

        # Check if file is already open
        existing_tab = self.fileIsNotOpen(path)
        if existing_tab != -1:
            self.tab.setCurrentIndex(existing_tab)
            QMessageBox.critical(self, "Notepad", txt3)
            return False

        # Try to read the file
        try:
            enc = self.detector(path)
            with open(
                file=path, mode="r", encoding=enc, errors="replace", newline=""
            ) as file:
                txt = file.read()
        except Exception as e:
            QMessageBox.warning(self, "Notepad", f"{txt1}{path}:\n{str(e)}.")
            return False

        # Create tab and update recent files
        fileName = os.path.basename(path)
        self.createTab(fileName, path, txt)
        self.ui.statusbar.showMessage(txt2, 3000)

        # Update recent files list
        if path in self.files:
            self.files.remove(path)
        self.files.insert(0, path)
        del self.files[self.maxRecentFiles:]

        # Update recent file actions in all windows
        for widget in QApplication.topLevelWidgets():
            if isinstance(widget, MainWindow):
                widget.updateRecentFileActions()

        return True

    def detector(self, path: str) -> str:
        """Detect file encoding using chardet."""
        detector = UniversalDetector()
        try:
            with open(path, "rb") as f:
                for line in f:
                    detector.feed(line)
                    if detector.done:
                        break
            detector.close()
            
            detected_encoding = detector.result.get("encoding", "utf-8")
            # Map detected encodings to Python encoding names
            encoding_map = {
                "UTF-8-SIG": "utf_8_sig",
                "UTF-16": "utf_16",
                "windows-1251": "cp1251",
                "IBM866": "cp866",
            }
            return encoding_map.get(detected_encoding, "utf_8")
        except Exception:
            return "utf_8"  # Default fallback

    def lineEndingsOpt(self, txt: str) -> Optional[str]:
        """Detect line ending type in text."""
        if LINE_ENDING_STRINGS[LineEnding.WINDOWS_CRLF] in txt:
            return LINE_ENDING_STRINGS[LineEnding.WINDOWS_CRLF]
        if LINE_ENDING_STRINGS[LineEnding.UNIX_LF] in txt:
            return LINE_ENDING_STRINGS[LineEnding.UNIX_LF]
        return None

    def fileIsNotOpen(self, path: str) -> int:
        """Check if file is already open. Returns tab index or -1 if not found."""
        for idx in range(self.tab.count()):
            if path == self.tab.widget(idx).curName:
                return idx
        return -1

    def save(self) -> bool:
        """Save current document. Returns True if successful."""
        idx = self.tab.currentIndex()
        path = self.tab.widget(idx).curName
        if path:
            return self.saveFile(path)
        return self.saveAs()

    def saveAs(self) -> bool:
        """Save current document with new name. Returns True if successful."""
        if self.language == "English":
            dialog_title = "Save File"
            error_msg = "The file is already opened in Notepad"
        else:
            dialog_title = "Сохранить файл"
            error_msg = "Файл уже открыт в Notepad"

        idx = self.tab.currentIndex()
        fileName = self.tab.tabText(idx)
        if self.tab.widget(idx).curName:
            fileName = self.tab.widget(idx).curName
        path, _ = QFileDialog.getSaveFileName(self, dialog_title, fileName)
        if not path:
            return False

        # Check if file is already open in another tab
        existing_tab = self.fileIsNotOpen(path)
        if existing_tab != -1 and path != fileName:
            self.tab.setCurrentIndex(existing_tab)
            QMessageBox.critical(self, "Notepad", error_msg)
            return False

        return self.saveFile(path)

    def saveFile(self, path: str) -> bool:
        """Save current document to file. Returns True if successful."""
        if self.language == "English":
            error_msg = "Cannot write file "
            success_msg = "File saved"
        else:
            error_msg = "Невозможно записать файл "
            success_msg = "Файл сохранен"

        tb = self.tab
        idx = tb.currentIndex()
        doc = tb.widget(idx)

        # Convert line endings
        if doc.lineEnding == LineEnding.WINDOWS_CRLF:
            txt = doc.toPlainText().replace("\n", LINE_ENDING_STRINGS[LineEnding.WINDOWS_CRLF])
        else:
            txt = doc.toPlainText()

        # Encode text according to selected encoding
        encoding_name = ENCODING_PYTHON_NAMES.get(doc.encodingType, "utf_8")
        encoded_text = txt.encode(encoding_name, "replace")

        try:
            with open(path, "wb") as f:
                # Write BOM for UTF-16 encodings
                if doc.encodingType == EncodingType.UTF16_BE:
                    f.write(codecs.BOM_UTF16_BE)
                elif doc.encodingType == EncodingType.UTF16_LE:
                    f.write(codecs.BOM_UTF16_LE)
                f.write(encoded_text)
        except Exception as e:
            QMessageBox.warning(self, "Notepad", f"{error_msg}{path}:\n{str(e)}.")
            return False

        # Update document state
        doc.curName = path
        doc.document().setModified(False)
        name = os.path.basename(path)
        tb.setTabText(idx, name)
        self.ui.statusbar.showMessage(success_msg, 3000)
        self.update_window_title()
        return True

    def closeFile(self, idx):
        if self.maybeSave():
            self.tab.widget(idx).close()
            self.tab.removeTab(idx)
        if self.tab.count() == 0:
            self.numbDoc = 0
            self.newFile()

    def closeAllFiles(self):
        while self.tab.count() > 0:
            idx = self.tab.currentIndex()
            if self.maybeSave():
                self.tab.widget(idx).close()
                self.tab.removeTab(idx)
            else:
                return False
        self.numbDoc = 0
        self.newFile()

    def printFile(self):
        self.zoom_restore()
        printer = QPrinter(QPrinter.HighResolution)
        dlg = QPrintDialog(printer, self)
        if dlg.exec() == QDialog.Accepted:
            idx = self.tab.currentIndex()
            self.tab.widget(idx).print_(printer)

    def printPreview(self):
        if self.language == "English":
            txt1 = "Print Preview"
        else:
            txt1 = "Предварительный просмотр"

        self.zoom_restore()
        printer = QPrinter(QPrinter.HighResolution)
        preview = QPrintPreviewDialog(printer, self)
        preview.setWindowTitle(txt1)
        idx = self.tab.currentIndex()
        preview.paintRequested.connect(self.tab.widget(idx).print_)
        preview.exec()

    def cursorChanged(self):
        doc = self.tab.currentWidget()
        text = doc.textCursor().selectedText()
        doc.searchHighLight.searchText(text)
        self.update_status_bar()

    def find(self, findText, checkCase, checkWholeWord, wrapAround):
        idx = self.tab.currentIndex()
        doc = self.tab.widget(idx)
        flags = QTextDocument.FindFlag(0)
        if checkCase:
            flags |= QTextDocument.FindCaseSensitively
        if checkWholeWord:
            flags |= QTextDocument.FindWholeWords
        if findText:
            if not doc.find(findText, flags):
                if wrapAround:
                    doc.moveCursor(QTextCursor.Start)
                    if not doc.find(findText, flags):
                        QMessageBox.information(
                            self, "Notepad", "Cannot find text:\n'%s'" % findText
                        )
                else:
                    QMessageBox.information(
                        self, "Notepad", "Cannot find text:\n'%s'" % findText
                    )

    def replace(self, findText, replaceText, checkCase, checkWholeWord, wrapAround):
        idx = self.tab.currentIndex()
        doc = self.tab.widget(idx)
        if findText == doc.textCursor().selectedText():
            doc.textCursor().insertText(replaceText)
        self.find(findText, checkCase, checkWholeWord, wrapAround)

    def replaceAll(self, findText, replaceText, checkCase, checkWholeWord):
        if findText:
            idx = self.tab.currentIndex()
            doc = self.tab.widget(idx)
            flags = QTextDocument.FindFlag(0)
            if checkCase:
                flags |= QTextDocument.FindCaseSensitively
            if checkWholeWord:
                flags |= QTextDocument.FindWholeWords
            doc.textCursor().beginEditBlock()
            cursor = QTextCursor(doc.document())
            while True:
                cursor = doc.document().find(findText, cursor, flags)
                if cursor.isNull():
                    break
                cursor.insertText(replaceText)
            doc.textCursor().endEditBlock()

    def insertDateTime(self):
        datetime = time.strftime("%H:%M %d.%m.%Y", time.localtime())
        self.tab.currentWidget().textCursor().insertText(datetime)

    def _get_selected_or_all_text(self) -> Tuple[QTextCursor, str]:
        """Get selected text or all document text."""
        doc = self.tab.currentWidget()
        cursor = doc.textCursor()
        text = cursor.selectedText()
        if not text:
            cursor.select(QTextCursor.Document)
            text = cursor.selectedText()
        return cursor, text

    def uppercase(self) -> None:
        """Convert selected or all text to uppercase."""
        doc = self.tab.currentWidget()
        if not doc.toPlainText():
            return
        cursor, text = self._get_selected_or_all_text()
        cursor.insertText(text.upper())

    def lowercase(self) -> None:
        """Convert selected or all text to lowercase."""
        doc = self.tab.currentWidget()
        if not doc.toPlainText():
            return
        cursor, text = self._get_selected_or_all_text()
        cursor.insertText(text.lower())

    def propercase(self) -> None:
        """Convert selected or all text to title case."""
        doc = self.tab.currentWidget()
        if not doc.toPlainText():
            return
        cursor, text = self._get_selected_or_all_text()
        cursor.insertText(text.title())

    def trim_trailing_space(self) -> None:
        """Strip trailing spaces from the selection or the whole document."""
        doc = self.tab.currentWidget()
        if not doc.toPlainText():
            return
        cursor, text = self._get_selected_or_all_text()
        lines = text.splitlines(True)
        for line in lines:
            cursor.insertText(line.rstrip() + "\u2029")
        cursor.deletePreviousChar()

    def trim_leading_space(self) -> None:
        """Strip leading spaces from the selection or the whole document."""
        doc = self.tab.currentWidget()
        if not doc.toPlainText():
            return
        cursor, text = self._get_selected_or_all_text()
        lines = text.splitlines(True)
        for line in lines:
            if line.lstrip() == "":
                cursor.insertText("\u2029")
            else:
                cursor.insertText(line.lstrip())

    def tab_to_space(self) -> None:
        """Replace tabs with spaces in the selection or document."""
        doc = self.tab.currentWidget()
        if not doc.toPlainText():
            return
        cursor, text = self._get_selected_or_all_text()
        spaces = " " * TAB_STOP_SPACES
        lines = text.splitlines(True)
        for line in lines:
            cursor.insertText(line.replace("\t", spaces))

    def remove_space(self) -> None:
        """Remove spaces from the selection or entire document."""
        doc = self.tab.currentWidget()
        if not doc.toPlainText():
            return
        cursor, text = self._get_selected_or_all_text()
        lines = text.splitlines(True)
        for line in lines:
            cursor.insertText(line.replace(" ", ""))

    def join_lines(self) -> None:
        """Join selected lines by removing paragraph separators."""
        doc = self.tab.currentWidget()
        if not doc.toPlainText():
            return
        cursor, text = self._get_selected_or_all_text()
        cursor.insertText(text.replace("\u2029", ""))

    def remove_empty_lines(self) -> None:
        """Remove empty lines in the current selection or document."""
        doc = self.tab.currentWidget()
        if not doc.toPlainText():
            return
        cursor, text = self._get_selected_or_all_text()
        lines = text.splitlines(True)
        for line in lines:
            if line.strip():  # Only keep non-empty lines
                cursor.insertText(line)

    def remove_duplicate_lines(self) -> None:
        """Remove duplicate lines while preserving order."""
        doc = self.tab.currentWidget()
        if not doc.toPlainText():
            return
        cursor, text = self._get_selected_or_all_text()
        lines = text.splitlines(True)
        seen = set()
        unique_lines = []
        for line in lines:
            if line not in seen:
                seen.add(line)
                unique_lines.append(line)
        for line in unique_lines:
            cursor.insertText(line)

    def sort_lines_ascending_order(self) -> None:
        """Sort selected lines in ascending order."""
        doc = self.tab.currentWidget()
        if not doc.toPlainText():
            return
        cursor, text = self._get_selected_or_all_text()
        lines = text.splitlines(True)
        if lines:
            lines[-1] = lines[-1] + "\u2029"
            lines.sort()
            for line in lines:
                cursor.insertText(line)
            cursor.deletePreviousChar()

    def sort_lines_descending_order(self) -> None:
        """Sort selected lines in descending order."""
        doc = self.tab.currentWidget()
        if not doc.toPlainText():
            return
        cursor, text = self._get_selected_or_all_text()
        lines = text.splitlines(True)
        if lines:
            lines[-1] = lines[-1] + "\u2029"
            lines.sort(reverse=True)
            for line in lines:
                cursor.insertText(line)
            cursor.deletePreviousChar()

    def windows_crlf(self) -> None:
        """Switch line endings to Windows style."""
        doc = self.tab.currentWidget()
        if doc.lineEnding == LineEnding.UNIX_LF:
            doc.lineEnding = LineEnding.WINDOWS_CRLF
            self.ui.actionWindowsCRLF.setEnabled(False)
            self.ui.actionUnixLF.setEnabled(True)
            if doc.toPlainText():
                doc.document().setModified(True)
            self.update_status_bar()

    def unix_lf(self) -> None:
        """Switch line endings to Unix style."""
        doc = self.tab.currentWidget()
        if doc.lineEnding == LineEnding.WINDOWS_CRLF:
            doc.lineEnding = LineEnding.UNIX_LF
            self.ui.actionWindowsCRLF.setEnabled(True)
            self.ui.actionUnixLF.setEnabled(False)
            if doc.toPlainText():
                doc.document().setModified(True)
            self.update_status_bar()

    def update_eol(self) -> None:
        """Refresh the line-ending UI state for the current tab."""
        doc = self.tab.currentWidget()
        if doc.lineEnding == LineEnding.WINDOWS_CRLF:
            self.ui.actionWindowsCRLF.setEnabled(False)
            self.ui.actionUnixLF.setEnabled(True)
        else:
            self.ui.actionWindowsCRLF.setEnabled(True)
            self.ui.actionUnixLF.setEnabled(False)

    def zoom_in(self):
        """Increase zoom level for all tabs."""
        for idx in range(self.tab.count()):
            self.tab.widget(idx).zoom(+2)
            self.zoomGlob = self.tab.widget(idx).zoomValue
            self.update_tab_distance()
        self.update_status_bar()

    def zoom_out(self) -> None:
        """Decrease zoom level for all tabs."""
        for idx in range(self.tab.count()):
            if self.zoomGlob > MIN_ZOOM_LEVEL:
                self.tab.widget(idx).zoom(-2)
                self.zoomGlob = self.tab.widget(idx).zoomValue
            self.update_tab_distance()
        self.update_status_bar()

    def wheelEvent(self, event) -> None:  # pylint: disable=invalid-name
        """Handle mouse wheel zooming with the Ctrl modifier."""
        if event.modifiers() & Qt.ControlModifier:
            for idx in range(self.tab.count()):
                if self.zoomGlob > MIN_ZOOM_LEVEL:
                    self.tab.widget(idx).zoom(event.angleDelta().y())
                elif self.zoomGlob == MIN_ZOOM_LEVEL:
                    self.zoom_in()
                    self.zoomGlob = self.tab.widget(idx).zoomValue
                else:
                    event.ignore()
                self.zoomGlob = self.tab.widget(idx).zoomValue
                self.update_tab_distance()
            self.update_status_bar()

    def zoom_restore(self):
        """Reset zoom for all tabs to the base font size."""
        for idx in range(self.tab.count()):
            self.tab.widget(idx).setFont(
                QFont(self.fontFamily, self.sizeTxt, self.fontWeight, self.fontItalic)
            )
            self.update_tab_distance()
            self.tab.widget(idx).zoomValue = 0
        self.zoomGlob = 0
        self.update_status_bar()

    def wrap_text(self):
        """Toggle line wrapping on all tabs."""
        for idx in range(self.tab.count()):
            if self.ui.actionWrapText.isChecked():
                self.tab.widget(idx).setLineWrapMode(Editor.WidgetWidth)
            else:
                self.tab.widget(idx).setLineWrapMode(Editor.NoWrap)

    def window_on_top(self):
        """Keep window always on top when toggled."""
        flags = Qt.WindowFlags()
        if self.ui.actionAlwaysTop.isChecked():
            flags |= Qt.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        pos = self.pos()
        if pos.x() < 0:
            pos.setX(0)
        if pos.y() < 0:
            pos.setY(0)
        self.move(pos)
        self.show()

    def summary_doc(self):  # pylint: disable=too-many-locals,too-many-statements
        """Show statistics about the current document."""
        doc = self.tab.currentWidget()
        text_doc = doc.toPlainText()
        text_select = doc.textCursor().selectedText()
        selection_ranges = 1 if text_select else 0

        if self.language == "English":
            txt1 = "Characters(without line endings): "
            txt2 = "Words: "
            txt3 = "Lines: "
            txt4 = "Document length: "
            txt5 = " selected characters"
            bytes_select = f" ({len(text_select.encode('utf_8'))} bytes) in {selection_ranges} ranges"
            txt6 = "Full file path: "
            txt7 = "Created: "
            txt8 = "Modified: "
            txt9 = "Summary"
        else:
            txt1 = "Символов(без окончания строки): "
            txt2 = "Слов: "
            txt3 = "Строк: "
            txt4 = "Длина: "
            txt5 = " выделенных символов"
            bytes_select = (
                f" ({len(text_select.encode('utf_8'))} байт) в {selection_ranges} диапазоне(ах)"
            )
            txt6 = "Полный путь к файлу: "
            txt7 = "Создан: "
            txt8 = "Изменен: "
            txt9 = "Информация о файле"

        char_count = txt1 + str(len(text_doc.replace("\n", "")))
        word_count = txt2 + str(len(text_doc.split()))
        lines = txt3 + str(doc.document().lineCount())

        if doc.lineEnding == LineEnding.WINDOWS_CRLF:
            length = txt4 + str(len(text_doc.replace("\n", LINE_ENDING_STRINGS[LineEnding.WINDOWS_CRLF])))
            text_select = text_select.replace("\u2029", LINE_ENDING_STRINGS[LineEnding.WINDOWS_CRLF])
            char_select = str(len(text_select.replace(LINE_ENDING_STRINGS[LineEnding.WINDOWS_CRLF], ""))) + txt5
        else:
            length = txt4 + str(doc.document().characterCount() - 1)
            text_select = text_select.replace("\u2029", LINE_ENDING_STRINGS[LineEnding.UNIX_LF])
            char_select = str(len(text_select.replace(LINE_ENDING_STRINGS[LineEnding.UNIX_LF], ""))) + txt5

        info = QFileInfo(doc.curName)
        if info.exists():
            path = txt6 + info.absoluteFilePath().replace("/", "\\")
            created = txt7 + info.birthTime().toString("dd.MM.yyyy HH:mm:ss")
            modified = txt8 + info.lastModified().toString("dd.MM.yyyy HH:mm:ss")
            msg = (
                path
                + "\n"
                + created
                + "\n"
                + modified
                + "\n"
                + char_count
                + "\n"
                + word_count
                + "\n"
                + lines
                + "\n"
                + length
                + "\n"
                + char_select
                + bytes_select
            )
        else:
            msg = (
                char_count
                + "\n"
                + word_count
                + "\n"
                + lines
                + "\n"
                + length
                + "\n"
                + char_select
                + bytes_select
            )

        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(txt9)
        msg_box.setText(msg)
        msg_box.exec()

    def show_space_tab(self):
        """Toggle drawing of tabs and spaces across all documents."""
        option = QTextOption()
        for idx in range(self.tab.count()):
            if self.ui.actionShowSpaceTab.isChecked():
                option.setFlags(option.flags() | QTextOption.ShowTabsAndSpaces)
            else:
                option.setFlags(option.flags() & QTextOption.ShowTabsAndSpaces)
            self.tab.widget(idx).document().setDefaultTextOption(option)
            self.update_tab_distance()

    def update_tab_distance(self) -> None:
        """Update tab stop distance according to the current font."""
        current_widget = self.tab.currentWidget()
        if current_widget:
            current_widget.setTabStopDistance(
                QFontMetricsF(current_widget.font()).horizontalAdvance(" ") * TAB_STOP_SPACES
            )

    def change_encoding(self) -> None:
        """Set encoding flags for the current document based on menu selection."""
        doc = self.tab.currentWidget()
        encoding_map = {
            self.ui.actionUTF8: EncodingType.UTF8,
            self.ui.actionUTF8BOM: EncodingType.UTF8_BOM,
            self.ui.actionUTF16BE: EncodingType.UTF16_BE,
            self.ui.actionUTF16LE: EncodingType.UTF16_LE,
            self.ui.actionWindows1251: EncodingType.WINDOWS_1251,
            self.ui.actionOEM866: EncodingType.OEM_866,
        }
        for action, encoding_type in encoding_map.items():
            if action.isChecked():
                doc.encodingType = encoding_type
                break
        self.update_status_bar()
        if doc.toPlainText():
            doc.document().setModified(True)

    def update_encoding_menu(self) -> None:
        """Sync encoding menu check marks with the current document."""
        doc = self.tab.currentWidget()
        encoding_map = {
            EncodingType.UTF8: self.ui.actionUTF8,
            EncodingType.UTF8_BOM: self.ui.actionUTF8BOM,
            EncodingType.UTF16_BE: self.ui.actionUTF16BE,
            EncodingType.UTF16_LE: self.ui.actionUTF16LE,
            EncodingType.WINDOWS_1251: self.ui.actionWindows1251,
            EncodingType.OEM_866: self.ui.actionOEM866,
        }
        # Uncheck all first
        for action in encoding_map.values():
            action.setChecked(False)
        # Check the current encoding
        if doc.encodingType in encoding_map:
            encoding_map[doc.encodingType].setChecked(True)

    def about(self):
        QMessageBox.about(
            self,
            "Notepad",
            f"This program is free software\nDeveloper: {APP_DEVELOPER}\nVersion: {APP_VERSION}\n{APP_RELEASE_DATE}",
        )

    def update_status_bar(self) -> None:
        """Refresh the status bar with the current document metadata."""
        doc = self.tab.currentWidget()
        cursor = doc.textCursor()
        text = doc.toPlainText()

        # Update encoding label
        encoding_name = ENCODING_NAMES.get(doc.encodingType, "UTF-8")
        self.encTxtLabel.setText(encoding_name)

        # Update text format label
        if doc.textFormat == TextFormat.TEXT_FILE:
            self.textFormatLabel.setText("Text File")
        else:
            self.textFormatLabel.setText("")

        # Update line ending and length
        if doc.lineEnding == LineEnding.WINDOWS_CRLF:
            self.symbNewLineLabel.setText("Windows (CR LF)")
            length = f"Length: {len(text.replace(chr(10), LINE_ENDING_STRINGS[LineEnding.WINDOWS_CRLF]))}"
        else:
            self.symbNewLineLabel.setText("Unix (LF)")
            length = f"Length: {doc.document().characterCount() - 1}"

        self.chrCountLabel.setText(length)
        self.cursorPosLabel.setText(
            f"Ln: {1 + cursor.blockNumber()} Col: {1 + cursor.positionInBlock()}"
        )
        self.zoomLabel.setText(
            f"Zoom: {int(100 * (self.sizeTxt + self.zoomGlob) / self.sizeTxt)}%"
        )

    def update_window_title(self):
        """Update the window title to reflect the active document."""
        tb = self.tab
        idx = tb.currentIndex()
        doc = tb.widget(idx)
        if doc.curName:
            name = doc.curName
        else:
            name = tb.tabText(idx)
        self.setWindowTitle(f"{name}[*] - Notepad")
        self.setWindowModified(doc.document().isModified())

    def tab_changed(self):
        """Update UI elements when the active tab changes."""
        if self.tab.count() > 1:
            self.update_window_title()
            self.update_status_bar()
            self.update_encoding_menu()
            self.update_eol()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
