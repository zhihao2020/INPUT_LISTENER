from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QMutex,QWaitCondition
from PyQt5.QtWidgets import QMainWindow,QApplication,QWidget,QLabel
from PyQt5.QtCore import Qt,QThread,pyqtSignal
from PyQt5 import QtCore,QtGui
import logging
import pyautogui
import pynput.mouse
import pynput.keyboard
import sys,os
import webbrowser
import requests
import json
import zipfile
import shutil
import time
import psutil
import subprocess

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(450, 378)
        MainWindow.setMaximumSize(QtCore.QSize(450, 378))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setObjectName("listWidget")
        self.horizontalLayout.addWidget(self.listWidget)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout.addWidget(self.pushButton_3)
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout.addWidget(self.pushButton_4)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 450, 26))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.action_2 = QtWidgets.QAction(MainWindow)
        self.action_2.setObjectName("action_2")
        self.menu.addAction(self.action_2)
        self.menu.addAction(self.action)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "输入记录器@zhihao"))
        self.pushButton_3.setText(_translate("MainWindow", "执行"))
        self.pushButton_4.setText(_translate("MainWindow", "恢复"))
        self.pushButton.setText(_translate("MainWindow", "开始记录"))
        self.pushButton_2.setText(_translate("MainWindow", "停止记录"))
        self.menu.setTitle(_translate("MainWindow", "关于"))
        self.action.setText(_translate("MainWindow", "软件简介"))
        self.action_2.setText(_translate("MainWindow", "关于作者"))

class reload_mainWin(QMainWindow, Ui_MainWindow):
    
    def __init__(self):
        super(reload_mainWin, self).__init__()
        self.setupUi(self)
        self.action_2.triggered.connect(self.about_me)
        self.action.triggered.connect(self.about_it)
        self.pushButton.clicked.connect(self.start_record)
        self.pushButton_2.clicked.connect(self.end_record)
        self.pushButton_4.clicked.connect(self.continue_start)
        self.pushButton_3.clicked.connect(self.play_it)

        self.keyboard_thread = keyboard_Thread()
        self.mouse_thread = mouse_Thread()
        self.mouse_thread.mouse_information.connect(self.add_list_content)
        self.keyboard_thread.keyboard_information.connect(self.add_list_content)
        #隐藏按钮
        self.pushButton_3.hide()
        self.pushButton_4.hide()
       
    def about_me(self):
        print("介绍作者")
        webbrowser.open_new_tab('https://xuzhihao.top/about/')
    
    def about_it(self):
        #展示一个新窗口 用于介绍软件信息
        pass

    def play_it(self):
        #mouse_click mouse_move Scrolled 
        #keyboard_press keyboard_release
        with open('dataini.io',"r") as fd:
            for line in fd.readable:
                flag = line.split(',')[0]
                context = line.split(',')[1]
                if flag == "mouse_move":
                    pass
                elif flag == "mouse_click":
                    pass
                elif flag == "keyboard":
                    pass
                
    def add_list_content(self,content):
        self.listWidget.addItem(content)

    def mouse_controller(self):
        mouse= pynput.mouse.Controller()
        mouse.set(x,y)
        mouse.press()
        mouse.release()
        mouse.scroll(0,2)
        
    def keyboard_controller(self):
        keyboard = pynput.keyboard.Controller()
    
    def continue_start(self):
        print("恢复开始")
        self.keyboard_thread.start()
        self.mouse_thread.start()

    def start_record(self):
        #开始记录 鼠标位置、是否点击
        #判断 鼠标是否 拖动
        #判断键盘是否输入
        self.pushButton_3.hide()
        self.pushButton_4.hide()
        print("开始")
        self.listWidget.clear()
        file = open('dataini.io',"w")
        file.close()
        self.keyboard_thread.start()
        self.mouse_thread.start()

    def end_record(self):
        #停止记录
        self.keyboard_thread.cancel()
        self.mouse_thread.cancel()
        self.pushButton_3.show()
        self.pushButton_4.show()

class mouse_Thread(QThread,Ui_MainWindow):
    mouse_signal = pyqtSignal(bool)
    mouse_information = pyqtSignal(str)
    
    def __init__(self):
        super(mouse_Thread,self).__init__()
       
    def on_move(self,x,y):
        with open('dataini.io',"a") as fd:
            fd.write('mouse_move,'+str((x,y))+'\n')
        self.mouse_information.emit('鼠标移动到：{0}'.format((x,y)))

    def on_click(self,x,y,button,pressed):
        with open('dataini.io',"a") as fd:
            #存入格式为 按下去,右键或左键,(x,y)
            fd.write('mouse_click,'+'%s %s %s'%('Pressed'if pressed else 'Released',
                            (x,y),button)+'\n')
           
        self.mouse_information.emit("鼠标点击 {0}".format('Pressed'if pressed else 'Released'))
        self.mouse_information.emit("鼠标点击 %s"%button)
    
    def on_scroll(self,x,y,dx,dy):
        with open('dataini.io',"a") as fd:
            fd.write('Scrolled,{0} {1}'.format(dx,dy)+'\n')
        self.mouse_information.emit("鼠标x轴滚动 %s"%dx)
        self.mouse_information.emit("鼠标y轴滚动 %s"%dy)
    
    def pause(self):
        print("线程暂停")
        
    def cancel(self):
        print("线程取消")
        self.listener.stop()
    def run(self):
        
        self.listener =  pynput.mouse.Listener(
            on_move = self.on_move,
            on_click = self.on_click,
            on_scroll=self.on_scroll)     
        
        self.listener.start()

class keyboard_Thread(QThread,Ui_MainWindow):
    keyboard_signal = pyqtSignal(bool)
    keyboard_information = pyqtSignal(str)
    def __init__(self):
        super(keyboard_Thread,self).__init__()
       
    def on_press(self,key):
        with open('dataini.io',"a") as fd:
            fd.write('keyboard_press,'+str(key)+'\n')
        self.keyboard_information.emit("按下 %s"%str(key))
        print('{0} pressed'.format(key))

    def on_release(self,key):
        with open('dataini.io',"a") as fd:
            fd.write('keyboard_release,'+str(key)+'\n')
        self.keyboard_information.emit('释放,{0}'.format(key))

    def pause(self):
        print("线程暂停")
        self.isPause = True

    def cancel(self):
        print("线程取消")
        self.listener.stop()

    def run(self):
        self.listener = pynput.keyboard.Listener(on_press = self.on_press,on_release=self.on_release) 
        
        self.listener.start()

class update_Thread(QThread,Ui_MainWindow):
    update_Signal = pyqtSignal(bool)

    def __init__(self):
        super(update_Thread,self).__init__()
   
    def check_latest(self):
    # 确定当前软件是否为最新版
        params = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
            "Host": "api.github.com"}
        try:
            response = requests.get("https://api.github.com/repos/zhihao2020/INPUT_LISTENER/releases/latest", params=params)
            if response.status_code != 200:
                raise Exception("网络异常")
            temp = json.loads(response.text)
            self.latest_tag = temp["tag_name"]
            print(self.latest_tag)
            if not os.path.exists("softID.io"):
                file = open("softID.io","w")
                file.close()
            with open("softID.io",'r') as f:
                previous_tag = f.readline()
            if self.latest_tag != previous_tag:
                download_url = temp["assets"][0]['browser_download_url']
                file_size = temp['assets'][0]['size']
                return download_url,file_size
            else:
                pass
                #self.New_signal.emit(3)
        except requests.exceptions.ConnectionError:
            print("请求被拒绝")
        except Exception as e:
            print("158行，%s"%e)
            #self.Error_signal.emit(2)

    def kill_process(self):
        for proc in psutil.process_iter():
            if proc.name()=='Input_Record.exe':
                proc.kill()            
                    
    def download(self,download_url,file_size):
        print("downloading ....")
        temp_file = os.path.join(self.download_path,'update.zip')
        params = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"}
        with open(temp_file,'wb') as self.fileobj:
            f = requests.get(download_url,stream=True,params=params)
            offset = 0
            for chunk in f.iter_content(chunk_size=1024):
                if not chunk:
                    break
                self.fileobj.seek(offset)
                self.fileobj.write(chunk)
                offset = offset+len(chunk)
                proess = offset/int(file_size) * 100
                self.trigger.emit(int(proess))

    def unzip(self):
        self.kill_process()
        current_path = os.path.dirname(os.path.abspath(__file__))
        update_file_path = os.path.join(self.download_path, 'update.zip')
        with zipfile.ZipFile(update_file_path) as fd:
            for n in fd.namelist():
                try:
                    os.remove(n)
                except:
                    try:
                        shutil.rmtree(n)
                    except:
                        print(n)
        shutil.unpack_archive(
            filename=update_file_path,
            extract_dir=current_path
        )
        os.remove(update_file_path)

    def run(self):
        # 确定当前软件是否为最新版
        try:
            download_url, file_size = self.check_latest()
            print(download_url)
            self.download(download_url, file_size)
            self.Button_signal.emit(True)
            self.unzip()
            with open("softID.io", 'w') as f:
                f.write(self.latest_tag)
           
        except Exception as e:
            print(e)



class Information(QWidget):
    def __init__(self):
        super(Information,self).__init__()
        self.initUI()
    def initUI(self):
        label = QLabel(self)
        label.resize(700, 100)
        label.setText("还有5秒钟，记录启动")
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QtGui.QFont("Arial", 40))
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = reload_mainWin()
    myWin.show()
    sys.exit(app.exec_())
