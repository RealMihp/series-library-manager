# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QFrame, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QMainWindow, QMenu, QMenuBar,
    QProgressBar, QPushButton, QSizePolicy, QSpacerItem,
    QSplitter, QTreeWidget, QTreeWidgetItem, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1280, 960)
        self.actionAdd_folder = QAction(MainWindow)
        self.actionAdd_folder.setObjectName(u"actionAdd_folder")
        self.actionPreferences = QAction(MainWindow)
        self.actionPreferences.setObjectName(u"actionPreferences")
        self.actionClose = QAction(MainWindow)
        self.actionClose.setObjectName(u"actionClose")
        self.actionScan_Folder = QAction(MainWindow)
        self.actionScan_Folder.setObjectName(u"actionScan_Folder")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_5 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.scanExplorerFrame = QFrame(self.splitter)
        self.scanExplorerFrame.setObjectName(u"scanExplorerFrame")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scanExplorerFrame.sizePolicy().hasHeightForWidth())
        self.scanExplorerFrame.setSizePolicy(sizePolicy)
        self.scanExplorerFrame.setMaximumSize(QSize(16777215, 16777215))
        self.scanExplorerFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.scanExplorerFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.scanExplorerFrame)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.splitter_2 = QSplitter(self.scanExplorerFrame)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Orientation.Vertical)
        self.searchFrame = QFrame(self.splitter_2)
        self.searchFrame.setObjectName(u"searchFrame")
        self.searchFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.searchFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.searchFrame)
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.addSeriesLabel = QLabel(self.searchFrame)
        self.addSeriesLabel.setObjectName(u"addSeriesLabel")

        self.verticalLayout.addWidget(self.addSeriesLabel)

        self.searchBarFrame = QFrame(self.searchFrame)
        self.searchBarFrame.setObjectName(u"searchBarFrame")
        self.searchBarFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.searchBarFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.searchBarFrame)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.searchLineEdit = QLineEdit(self.searchBarFrame)
        self.searchLineEdit.setObjectName(u"searchLineEdit")

        self.horizontalLayout_4.addWidget(self.searchLineEdit)

        self.SearchPushButton = QPushButton(self.searchBarFrame)
        self.SearchPushButton.setObjectName(u"SearchPushButton")

        self.horizontalLayout_4.addWidget(self.SearchPushButton)


        self.verticalLayout.addWidget(self.searchBarFrame)

        self.searchResults = QTreeWidget(self.searchFrame)
        self.searchResults.setObjectName(u"searchResults")
        self.searchResults.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.searchResults.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContentsOnFirstShow)
        self.searchResults.setUniformRowHeights(False)
        self.searchResults.setSortingEnabled(False)
        self.searchResults.setWordWrap(True)
        self.searchResults.setHeaderHidden(False)
        self.searchResults.header().setProperty(u"showSortIndicator", False)

        self.verticalLayout.addWidget(self.searchResults)

        self.addSeriesPushButton = QPushButton(self.searchFrame)
        self.addSeriesPushButton.setObjectName(u"addSeriesPushButton")

        self.verticalLayout.addWidget(self.addSeriesPushButton)

        self.splitter_2.addWidget(self.searchFrame)
        self.folderPreviewFrame = QFrame(self.splitter_2)
        self.folderPreviewFrame.setObjectName(u"folderPreviewFrame")
        self.folderPreviewFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.folderPreviewFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.folderPreviewFrame)
        self.verticalLayout_4.setSpacing(3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.folderPreviewLabel = QLabel(self.folderPreviewFrame)
        self.folderPreviewLabel.setObjectName(u"folderPreviewLabel")

        self.verticalLayout_4.addWidget(self.folderPreviewLabel)

        self.pathLine = QLineEdit(self.folderPreviewFrame)
        self.pathLine.setObjectName(u"pathLine")
        self.pathLine.setMinimumSize(QSize(0, 26))
        self.pathLine.setReadOnly(False)

        self.verticalLayout_4.addWidget(self.pathLine)

        self.fileExplorerListWidget = QListWidget(self.folderPreviewFrame)
        self.fileExplorerListWidget.setObjectName(u"fileExplorerListWidget")

        self.verticalLayout_4.addWidget(self.fileExplorerListWidget)

        self.splitter_2.addWidget(self.folderPreviewFrame)

        self.verticalLayout_6.addWidget(self.splitter_2)

        self.splitter.addWidget(self.scanExplorerFrame)
        self.mainFrame = QFrame(self.splitter)
        self.mainFrame.setObjectName(u"mainFrame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(3)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.mainFrame.sizePolicy().hasHeightForWidth())
        self.mainFrame.setSizePolicy(sizePolicy1)
        self.mainFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.mainFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.mainFrame)
        self.verticalLayout_2.setSpacing(3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.addedSeriesLabel = QLabel(self.mainFrame)
        self.addedSeriesLabel.setObjectName(u"addedSeriesLabel")

        self.verticalLayout_2.addWidget(self.addedSeriesLabel)

        self.treeWidget = QTreeWidget(self.mainFrame)
        self.treeWidget.setObjectName(u"treeWidget")
        self.treeWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.treeWidget.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContentsOnFirstShow)
        self.treeWidget.setUniformRowHeights(False)
        self.treeWidget.setSortingEnabled(True)
        self.treeWidget.setWordWrap(True)
        self.treeWidget.setHeaderHidden(False)
        self.treeWidget.header().setProperty(u"showSortIndicator", True)

        self.verticalLayout_2.addWidget(self.treeWidget)

        self.splitter.addWidget(self.mainFrame)
        self.showInfoFrame = QFrame(self.splitter)
        self.showInfoFrame.setObjectName(u"showInfoFrame")
        sizePolicy.setHeightForWidth(self.showInfoFrame.sizePolicy().hasHeightForWidth())
        self.showInfoFrame.setSizePolicy(sizePolicy)
        self.showInfoFrame.setMinimumSize(QSize(0, 0))
        self.showInfoFrame.setMaximumSize(QSize(16777215, 16777215))
        self.showInfoFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.showInfoFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.showInfoFrame)
        self.verticalLayout_7.setSpacing(3)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.seriesInfoLabel = QLabel(self.showInfoFrame)
        self.seriesInfoLabel.setObjectName(u"seriesInfoLabel")

        self.verticalLayout_7.addWidget(self.seriesInfoLabel)

        self.frame = QFrame(self.showInfoFrame)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.posterLabel = QLabel(self.frame)
        self.posterLabel.setObjectName(u"posterLabel")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(1)
        sizePolicy2.setHeightForWidth(self.posterLabel.sizePolicy().hasHeightForWidth())
        self.posterLabel.setSizePolicy(sizePolicy2)
        self.posterLabel.setMinimumSize(QSize(0, 340))
        self.posterLabel.setMaximumSize(QSize(16777215, 16777215))
        self.posterLabel.setScaledContents(True)
        self.posterLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_3.addWidget(self.posterLabel)

        self.titleLabel = QLabel(self.frame)
        self.titleLabel.setObjectName(u"titleLabel")
        self.titleLabel.setWordWrap(True)

        self.verticalLayout_3.addWidget(self.titleLabel)

        self.statusLabel = QLabel(self.frame)
        self.statusLabel.setObjectName(u"statusLabel")

        self.verticalLayout_3.addWidget(self.statusLabel)

        self.yearLabel = QLabel(self.frame)
        self.yearLabel.setObjectName(u"yearLabel")

        self.verticalLayout_3.addWidget(self.yearLabel)


        self.verticalLayout_7.addWidget(self.frame)

        self.seasonsLabel = QLabel(self.showInfoFrame)
        self.seasonsLabel.setObjectName(u"seasonsLabel")

        self.verticalLayout_7.addWidget(self.seasonsLabel)

        self.seasonsListWidget = QListWidget(self.showInfoFrame)
        self.seasonsListWidget.setObjectName(u"seasonsListWidget")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.seasonsListWidget.sizePolicy().hasHeightForWidth())
        self.seasonsListWidget.setSizePolicy(sizePolicy3)
        self.seasonsListWidget.setMaximumSize(QSize(16777215, 200))

        self.verticalLayout_7.addWidget(self.seasonsListWidget)

        self.verticalLayout_7.setStretch(1, 1)
        self.verticalLayout_7.setStretch(3, 1)
        self.splitter.addWidget(self.showInfoFrame)

        self.verticalLayout_5.addWidget(self.splitter)

        self.statusBarFrame = QFrame(self.centralwidget)
        self.statusBarFrame.setObjectName(u"statusBarFrame")
        self.statusBarFrame.setMaximumSize(QSize(16777215, 50))
        self.statusBarFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.statusBarFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.statusBarFrame)
        self.horizontalLayout_3.setSpacing(3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(3, 3, 3, 3)
        self.scanFrame = QFrame(self.statusBarFrame)
        self.scanFrame.setObjectName(u"scanFrame")
        self.scanFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.scanFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.scanFrame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.scanLabel = QLabel(self.scanFrame)
        self.scanLabel.setObjectName(u"scanLabel")

        self.horizontalLayout_2.addWidget(self.scanLabel)

        self.scanProgressBar = QProgressBar(self.scanFrame)
        self.scanProgressBar.setObjectName(u"scanProgressBar")
        self.scanProgressBar.setValue(0)
        self.scanProgressBar.setInvertedAppearance(False)

        self.horizontalLayout_2.addWidget(self.scanProgressBar)


        self.horizontalLayout_3.addWidget(self.scanFrame)

        self.statufBarHorizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.statufBarHorizontalSpacer)

        self.statusBarLabel = QLabel(self.statusBarFrame)
        self.statusBarLabel.setObjectName(u"statusBarLabel")
        self.statusBarLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.statusBarLabel.setMargin(9)

        self.horizontalLayout_3.addWidget(self.statusBarLabel)

        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 3)
        self.horizontalLayout_3.setStretch(2, 1)

        self.verticalLayout_5.addWidget(self.statusBarFrame)

        self.verticalLayout_5.setStretch(1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1280, 33))
        self.menubar.setNativeMenuBar(True)
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName(u"menuEdit")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menuFile.addAction(self.actionAdd_folder)
        self.menuFile.addAction(self.actionClose)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionScan_Folder)
        self.menuEdit.addAction(self.actionPreferences)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Library Manager", None))
        self.actionAdd_folder.setText(QCoreApplication.translate("MainWindow", u"Add folder", None))
#if QT_CONFIG(shortcut)
        self.actionAdd_folder.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.actionPreferences.setText(QCoreApplication.translate("MainWindow", u"Preferences", None))
        self.actionClose.setText(QCoreApplication.translate("MainWindow", u"Close", None))
#if QT_CONFIG(shortcut)
        self.actionClose.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+W", None))
#endif // QT_CONFIG(shortcut)
        self.actionScan_Folder.setText(QCoreApplication.translate("MainWindow", u"Scan Folder", None))
        self.addSeriesLabel.setText(QCoreApplication.translate("MainWindow", u"Add series", None))
        self.SearchPushButton.setText(QCoreApplication.translate("MainWindow", u"Search", None))
        ___qtreewidgetitem = self.searchResults.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("MainWindow", u"Info", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"Title", None));
        self.addSeriesPushButton.setText(QCoreApplication.translate("MainWindow", u"Add selected series", None))
        self.folderPreviewLabel.setText(QCoreApplication.translate("MainWindow", u"Folder", None))
        self.pathLine.setInputMask("")
        self.pathLine.setText("")
        self.pathLine.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Library folder path", None))
        self.addedSeriesLabel.setText(QCoreApplication.translate("MainWindow", u"Added series", None))
        ___qtreewidgetitem1 = self.treeWidget.headerItem()
        ___qtreewidgetitem1.setText(1, QCoreApplication.translate("MainWindow", u"Info", None));
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("MainWindow", u"Title", None));
        self.seriesInfoLabel.setText(QCoreApplication.translate("MainWindow", u"Series info", None))
        self.posterLabel.setText("")
        self.titleLabel.setText("")
        self.statusLabel.setText("")
        self.yearLabel.setText("")
        self.seasonsLabel.setText(QCoreApplication.translate("MainWindow", u"Seasons", None))
        self.scanLabel.setText(QCoreApplication.translate("MainWindow", u"Scan", None))
        self.statusBarLabel.setText("")
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
    # retranslateUi

