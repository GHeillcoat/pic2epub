# encoding:utf-8
# !/usr/bin/python3

import sys
import traceback
import turtle
import win32gui,win32con,win32api
from Ui_epub import *
from Ui_settings import *
from pic2epub import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class MainWindow(QMainWindow):
    filePath=""
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFixedSize(self.width(), self.height())
        self.setAcceptDrops(True)
        self.ui.progressBar.setVisible(False)
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setOffset(3, 3)
        self.shadow.setBlurRadius(10)
        self.shadow.setColor(QtGui.QColor(0, 0, 0, 100))
        self.setGraphicsEffect(self.shadow)
        self.ui.label_4.mousePressEvent = self.open_file
        self.ui.label_3.mousePressEvent = self.bilibili
        self.ui.pushButton.clicked.connect(self.to_epub)
        self.show()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self.isMaximized() == False:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, mouse_event):
        if QtCore.Qt.LeftButton and self.m_flag:
            self.move(mouse_event.globalPos() - self.m_Position)  # 更改窗口位置
            mouse_event.accept()

    def mouseReleaseEvent(self, mouse_event):
        self.m_flag = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
    
    def dragEnterEvent(self, evn):
        self.filePath=evn.mimeData().text()
        self.ui.label_4.setStyleSheet(".QLabel{\n"
"    \n"
"    \n"
"    background-image: url(:/1/src/4.png);\n"
"}\n"
".QLabel:hover{\n"
"    background-color: rgb(118,118,122);\n"
"    border-radius:10px;\n"
"    background-image: url(:/1/src/3.png);\n"
"    background-repeat:no-repeat\n"
"}")
        self.ui.label_2.setText(self.filePath[8:])
        evn.accept()
 
    # 鼠标放开执行
    def dropEvent(self, evn):
        print('鼠标放开了')
 
    def dragMoveEvent(self, evn):
        print('鼠标移入')

    
    def open_file(self,event):
        self.ui.label_4.setStyleSheet(".QLabel{\n"
"    \n"
"    \n"
"    background-image: url(:/1/src/3.png);\n"
"}\n"
".QLabel:hover{\n"
"    background-color: rgb(118,118,122);\n"
"    border-radius:10px;\n"
"    background-image: url(:/1/src/4.png);\n"
"    background-repeat:no-repeat\n"
"}")
        filePath=QFileDialog.getExistingDirectory(self, "选择文件夹", "C:/")
        self.filePath=filePath
        self.ui.label_2.setText(filePath[8:])

    def bilibili(self,event):
        QDesktopServices.openUrl(QUrl("https://space.bilibili.com/8804928"))

    def to_epub(self):
        self.ui.progressBar.setVisible(True)
        self.ui.progressBar.setValue(0)
        self.ui.progressBar.setMaximum(100)
        try:
            filePath=self.filePath[8:]
            self.ui.progressBar.setValue(15)
            #是否有子目录
            for root,dirs,files in os.walk(filePath):
                print(dirs)
            self.ui.progressBar.setValue(30)
            if len(dirs)==0:
                dir=filePath[filePath.rindex('/')+1:]
                self.ui.progressBar.setValue(45)
                epubObj = epub(dir)
                self.ui.progressBar.setValue(75)
                epubObj.create_pic(filePath)
                self.ui.progressBar.setValue(85)
                epubObj.close()
                self.ui.progressBar.setValue(100)
                win32api.MessageBox(0, "转换完成！\n已保存至根目录下output文件夹下", "提示", win32con.MB_OK)
                self.ui.progressBar.setVisible(False)
            else:
                fileList=os.listdir(filePath)
                fileList.sort()
                self.ui.progressBar.setValue(50)
                jindu=50/len(fileList)
                for i in fileList:
                    epubObj = epub(i)
                    epubObj.create_pic(filePath+"/"+i)
                    epubObj.close()
                    self.ui.progressBar.setValue(jindu)
                win32api.MessageBox(0, "转换完成！\n已保存至根目录下output文件夹下", "提示", win32con.MB_OK)
                self.ui.progressBar.setVisible(False)
        except:
            err=traceback.format_exc()
            self.ui.progressBar.setValue(100)
            win32api.MessageBox(0, err, "转换失败", win32con.MB_ICONERROR)
            self.ui.progressBar.setVisible(False)

class SettingsWindows(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setOffset(0, 0)
        self.shadow.setBlurRadius(10)
        self.shadow.setColor(QtGui.QColor(255, 255, 255, 50))
        self.setGraphicsEffect(self.shadow)
        self.ui.label_2.mousePressEvent = self.setting1
        self.ui.label_3.mousePressEvent = self.setting2
        self.ui.label_4.mousePressEvent = self.setting3
        self.ui.label_5.mousePressEvent = self.setting4
        self.ui.label_6.mousePressEvent = self.setting5
        self.ui.label_7.mousePressEvent = self.setting6
        self.ui.pushButton.clicked.connect(self.close)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self.isMaximized() == False:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, mouse_event):
        if QtCore.Qt.LeftButton and self.m_flag:
            self.move(mouse_event.globalPos() - self.m_Position)  # 更改窗口位置
            mouse_event.accept()

    def mouseReleaseEvent(self, mouse_event):
        self.m_flag = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    def setting1(self,event):
        self.ui.stackedWidget.setCurrentIndex(0)
        #设置背景颜色
        self.ui.label_2.setStyleSheet('background-color: rgb(51,51,51);')
        self.ui.label_3.setStyleSheet('color: rgb(255, 255, 255);')
        self.ui.label_4.setStyleSheet('color: rgb(255, 255, 255);')
        self.ui.label_5.setStyleSheet('color: rgb(255, 255, 255);')
        self.ui.label_6.setStyleSheet('color: rgb(255, 255, 255);')
        self.ui.label_7.setStyleSheet('color: rgb(255, 255, 255);')
    
    def setting2(self,event):
        self.ui.stackedWidget.setCurrentIndex(1)
        self.ui.label_3.setStyleSheet('background-color: rgb(51,51,51);')
        self.ui.label_2.setStyleSheet('color: rgb(255, 255, 255);')
        self.ui.label_4.setStyleSheet('color: rgb(255, 255, 255);')
        self.ui.label_5.setStyleSheet('color: rgb(255, 255, 255);')
        self.ui.label_6.setStyleSheet('color: rgb(255, 255, 255);')
        self.ui.label_7.setStyleSheet('color: rgb(255, 255, 255);')

    def setting3(self,event):
        self.ui.stackedWidget.setCurrentIndex(2)
        self.ui.label_4.setStyleSheet('background-color: rgb(51,51,51);')
        self.ui.label_3.setStyleSheet('color: rgb(255, 255, 255);')
        self.ui.label_2.setStyleSheet('color: rgb(255, 255, 255);')
        self.ui.label_5.setStyleSheet('color: rgb(255, 255, 255);')
        self.ui.label_6.setStyleSheet('color: rgb(255, 255, 255);')
        self.ui.label_7.setStyleSheet('color: rgb(255, 255, 255);')

    def setting4(self,event):
        self.ui.stackedWidget.setCurrentIndex(3)
        self.ui.label_5.setStyleSheet('background-color: rgb(51,51,51);')
        self.ui.label_3.setStyleSheet('color: rgb(255, 255, 255);')
        self.ui.label_4.setStyleSheet('color: rgb(255, 255, 255);')
        self.ui.label_2.setStyleSheet('color: rgb(255, 255, 255);')
        self.ui.label_6.setStyleSheet('color: rgb(255, 255, 255);')
        self.ui.label_7.setStyleSheet('color: rgb(255, 255, 255);')

    def setting5(self,event):
        self.ui.stackedWidget.setCurrentIndex(4)
        self.ui.label_6.setStyleSheet('background-color: rgb(51,51,51);')
        self.ui.label_3.setStyleSheet('color: rgb(255, 255, 255);')
        self.ui.label_4.setStyleSheet('color: rgb(255, 255, 255);')
        self.ui.label_5.setStyleSheet('color: rgb(255, 255, 255);')
        self.ui.label_2.setStyleSheet('color: rgb(255, 255, 255);')
        self.ui.label_7.setStyleSheet('color: rgb(255, 255, 255);')

    def setting6(self,event):
        self.ui.stackedWidget.setCurrentIndex(5)
        self.ui.label_7.setStyleSheet('background-color: rgb(51,51,51);')
        self.ui.label_3.setStyleSheet('color: rgb(255, 255, 255);')
        self.ui.label_4.setStyleSheet('color: rgb(255, 255, 255);')
        self.ui.label_5.setStyleSheet('color: rgb(255, 255, 255);')
        self.ui.label_2.setStyleSheet('color: rgb(255, 255, 255);')
        self.ui.label_6.setStyleSheet('color: rgb(255, 255, 255);')

if __name__ == "__main__":
 app = QApplication(sys.argv)
 window = MainWindow()
 window2 = SettingsWindows()
 window.show()
 window.ui.pushButton_5.clicked.connect(window2.show)
 sys.exit(app.exec_())
