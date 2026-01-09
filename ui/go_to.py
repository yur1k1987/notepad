# Auto-generated UI module; linting is intentionally disabled.
from PySide6.QtCore import QCoreApplication, QMetaObject, QSize
from PySide6.QtWidgets import (QGridLayout, QLabel,
    QPushButton, QSpinBox)

class Ui_Goto(object):
    def setupUi(self, Goto):
        if not Goto.objectName():
            Goto.setObjectName(u"Goto")
        Goto.resize(250, 50)
        Goto.setMinimumSize(QSize(250, 50))
        self.gridLayout_2 = QGridLayout(Goto)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.pushButton = QPushButton(Goto)
        self.pushButton.setObjectName(u"pushButton")

        self.gridLayout.addWidget(self.pushButton, 0, 2, 1, 1)

        self.label = QLabel(Goto)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.spinBox = QSpinBox(Goto)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(999999999)

        self.gridLayout.addWidget(self.spinBox, 0, 1, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)


        self.retranslateUi(Goto)

        QMetaObject.connectSlotsByName(Goto)
    # setupUi

    def retranslateUi(self, Goto):
        Goto.setWindowTitle(QCoreApplication.translate("Goto", u"Go to", None))
        self.pushButton.setText(QCoreApplication.translate("Goto", u"Go to", None))
        self.label.setText(QCoreApplication.translate("Goto", u"Go to Line:", None))
    # retranslateUi

