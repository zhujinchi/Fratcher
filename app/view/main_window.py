# coding: utf-8
from PyQt6.QtCore import Qt, pyqtSignal, QEasingCurve, QUrl, QSize
from PyQt6.QtGui import QIcon, QDesktopServices
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QFrame, QWidget

from qfluentwidgets import NavigationAvatarWidget, NavigationItemPosition, MessageBox, FluentWindow, SplashScreen
from qfluentwidgets import FluentIcon as FIF

from app.view.gallery_interface import GalleryInterface

# from .folder_interface import FolderInterface
from app.view.folder_interface import FolderInterface
from app.view.list_interface import ListInterface
from app.view.match_interface import MatchInterface
from app.view.output_interface import OutputInterface
from app.view.setting_interface import SettingInterface
from app.view.mark_interface import MarkInterface
from app.common.icon import Icon
from app.common.signal_bus import signalBus
from app.common.translator import Translator


class MainWindow(FluentWindow):

    def __init__(self):
        super().__init__()
        self.initWindow()

        # create sub interface
        self.folderInterface = FolderInterface(self)
        self.listInterface = ListInterface(self)
        self.matchInterface = MatchInterface(self)
        self.outputInterface = OutputInterface(self)
        self.settingInterface = SettingInterface(self)
        self.markInterface = MarkInterface(self)
        self.markInterface.setObjectName("markInterface")  # 设置 objectName

        # initialize layout
        self.initLayout()

        # add items to navigation interface
        self.initNavigation()
        self.splashScreen.finish()

    def initLayout(self):
        signalBus.switchToSampleCard.connect(self.switchToSample)
        signalBus.supportSignal.connect(self.onSupport)

    def initNavigation(self):
        # add navigation items
        t = Translator()
        self.addSubInterface(self.folderInterface, FIF.FOLDER, t.folder)
        self.navigationInterface.addSeparator()

        pos = NavigationItemPosition.SCROLL
        self.addSubInterface(self.listInterface, FIF.ALIGNMENT,t.list, pos)
        self.addSubInterface(self.matchInterface, FIF.BACK_TO_WINDOW, t.match, pos)
        self.addSubInterface(self.outputInterface, FIF.DOWNLOAD, t.output, pos)
        self.addSubInterface(self.markInterface,FIF.LABEL,t.mark,pos)

        # add custom widget to bottom
        self.navigationInterface.addWidget(
            routeKey='avatar',
            widget=NavigationAvatarWidget('作者', 'app/resource/images/avator.png'),
            onClick=self.onSupport,
            position=NavigationItemPosition.BOTTOM
        )
        self.addSubInterface(
            self.settingInterface, FIF.SETTING, t.setting, NavigationItemPosition.BOTTOM)

    def initWindow(self):
        self.resize(1280, 1010)
        self.setMinimumWidth(960)
        self.setMinimumHeight(760)
        self.setWindowIcon(QIcon('app/resource/images/logo.png'))
        self.setWindowTitle('Fragment Matcher')

        # create splash screen
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(106, 106))
        self.splashScreen.raise_()

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
        self.show()
        QApplication.processEvents()

    def onSupport(self):
        w = MessageBox(
            '注意事项',
            '本项目仅限学习交流，禁止商用。\n联系作者：Angzeng@iCloud.com',
            self
        )
        w.width = 300
        w.yesButton.setText('作者主页')
        w.cancelButton.setText('关闭')
        if w.exec():
            QDesktopServices.openUrl(QUrl("https://github.com/zhujinchi/"))

    def switchToSample(self, routeKey, index):
        """ switch to sample """
        interfaces = self.findChildren(GalleryInterface)
        for w in interfaces:
            if w.objectName() == routeKey:
                self.stackedWidget.setCurrentWidget(w, False)
                w.scrollToCard(index)
