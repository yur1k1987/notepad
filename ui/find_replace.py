# Auto-generated UI module; linting is intentionally disabled.
from PySide6.QtCore import QCoreApplication, QMetaObject, QSize
from PySide6.QtWidgets import (QCheckBox, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_Find(object):
    def setupUi(self, Find):
        if not Find.objectName():
            Find.setObjectName(u"Find")
        Find.setEnabled(True)
        Find.resize(420, 150)
        Find.setMinimumSize(QSize(420, 150))
        self.horizontalLayout = QHBoxLayout(Find)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(6)
        self.gridLayout.setContentsMargins(-1, -1, 6, -1)
        self.label = QLabel(Find)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.lineEditFind = QLineEdit(Find)
        self.lineEditFind.setObjectName(u"lineEditFind")

        self.gridLayout.addWidget(self.lineEditFind, 0, 1, 1, 1)

        self.checkWholeWord = QCheckBox(Find)
        self.checkWholeWord.setObjectName(u"checkWholeWord")

        self.gridLayout.addWidget(self.checkWholeWord, 3, 0, 1, 1)

        self.label_2 = QLabel(Find)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.lineEditReplace = QLineEdit(Find)
        self.lineEditReplace.setObjectName(u"lineEditReplace")

        self.gridLayout.addWidget(self.lineEditReplace, 1, 1, 1, 1)

        self.checkCase = QCheckBox(Find)
        self.checkCase.setObjectName(u"checkCase")

        self.gridLayout.addWidget(self.checkCase, 2, 0, 1, 1)

        self.checkWrapAround = QCheckBox(Find)
        self.checkWrapAround.setObjectName(u"checkWrapAround")

        self.gridLayout.addWidget(self.checkWrapAround, 2, 1, 1, 1)


        self.horizontalLayout.addLayout(self.gridLayout)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.btnFind = QPushButton(Find)
        self.btnFind.setObjectName(u"btnFind")

        self.verticalLayout.addWidget(self.btnFind)

        self.btnReplace = QPushButton(Find)
        self.btnReplace.setObjectName(u"btnReplace")

        self.verticalLayout.addWidget(self.btnReplace)

        self.btnReplaceAll = QPushButton(Find)
        self.btnReplaceAll.setObjectName(u"btnReplaceAll")

        self.verticalLayout.addWidget(self.btnReplaceAll)

        self.verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.btnCancel = QPushButton(Find)
        self.btnCancel.setObjectName(u"btnCancel")

        self.verticalLayout.addWidget(self.btnCancel)


        self.horizontalLayout.addLayout(self.verticalLayout)

#if QT_CONFIG(shortcut)
        self.label.setBuddy(self.lineEditFind)
        self.label_2.setBuddy(self.lineEditReplace)
#endif // QT_CONFIG(shortcut)
        QWidget.setTabOrder(self.lineEditFind, self.lineEditReplace)
        QWidget.setTabOrder(self.lineEditReplace, self.btnFind)
        QWidget.setTabOrder(self.btnFind, self.btnReplace)
        QWidget.setTabOrder(self.btnReplace, self.btnReplaceAll)
        QWidget.setTabOrder(self.btnReplaceAll, self.checkCase)
        QWidget.setTabOrder(self.checkCase, self.checkWholeWord)
        QWidget.setTabOrder(self.checkWholeWord, self.checkWrapAround)
        QWidget.setTabOrder(self.checkWrapAround, self.btnCancel)

        self.retranslateUi(Find)
        self.btnCancel.clicked.connect(Find.reject)

        QMetaObject.connectSlotsByName(Find)
    # setupUi

    def retranslateUi(self, Find):
        Find.setWindowTitle(QCoreApplication.translate("Find", u"Find and Replace", None))
        self.label.setText(QCoreApplication.translate("Find", u"Find:", None))
        self.checkWholeWord.setText(QCoreApplication.translate("Find", u"Match Whole Word", None))
        self.label_2.setText(QCoreApplication.translate("Find", u"Replace:", None))
        self.checkCase.setText(QCoreApplication.translate("Find", u"Match Case", None))
        self.checkWrapAround.setText(QCoreApplication.translate("Find", u"Wrap Around", None))
        self.btnFind.setText(QCoreApplication.translate("Find", u"&Find", None))
        self.btnReplace.setText(QCoreApplication.translate("Find", u"&Replace", None))
        self.btnReplaceAll.setText(QCoreApplication.translate("Find", u"Replace All", None))
        self.btnCancel.setText(QCoreApplication.translate("Find", u"&Cancel", None))
    # retranslateUi
