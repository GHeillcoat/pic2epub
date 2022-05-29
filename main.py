import sys
import traceback
import win32gui,win32con,win32api
from Ui_epub import *
from pic2epub import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import QDir, QUrl
from PyQt5.QtGui import QDesktopServices

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
        try:
            filePath=self.filePath[8:]
            #是否有子目录
            for root,dirs,files in os.walk(filePath):
                print(dirs)
            if len(dirs)==0:
                dir=filePath[filePath.rindex('/')+1:]
                epubObj = epub(dir)
                epubObj.create_pic(filePath)
                epubObj.close()
                win32api.MessageBox(0, "转换完成！\n已保存至根目录下output文件夹下", "提示", win32con.MB_OK)
            else:
                fileList=os.listdir(filePath)
                fileList.sort()
                for i in fileList:
                    epubObj = epub(i)
                    epubObj.create_pic(filePath+"/"+i)
                    epubObj.close()
                win32api.MessageBox(0, "转换完成！\n已保存至根目录下output文件夹下", "提示", win32con.MB_OK)
        except:
            err=traceback.format_exc()
            win32api.MessageBox(0, err, "转换失败", win32con.MB_ICONERROR)
            #win32api.MessageBox(0, "转换失败\n"+e, "提示", win32con.MB_OK)

if __name__ == "__main__":
 app = QApplication(sys.argv)
 window = MainWindow()
 sys.exit(app.exec_())