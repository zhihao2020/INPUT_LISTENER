"""
Author:xuzhihao
2021-02-12:移动、点击已经完成；滚轮和键盘没有搞好
2021-02-19:大体已经完成，后续将会是细节上的改进
"""
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow,QApplication, QMessageBox,QWidget,QLabel
from PyQt5.QtCore import Qt,QThread,pyqtSignal
from PyQt5 import QtCore,QtGui
import pynput.mouse
from pynput.mouse import Button
import pynput.keyboard
import sys
import random
import time
import ast

from PyQt5 import QtCore, QtGui, QtWidgets

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
        self.menu.addAction(self.action)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "输入记录器 V0.2"))
        self.pushButton_3.setText(_translate("MainWindow", "执行"))
        self.pushButton_4.setText(_translate("MainWindow", "继续"))
        self.pushButton.setText(_translate("MainWindow", "开始记录"))
        self.pushButton_2.setText(_translate("MainWindow", "停止记录"))
        self.pushButton_2.setShortcut(_translate("MainWindow", "F4"))
        self.menu.setTitle(_translate("MainWindow", "关于"))
        self.action.setText(_translate("MainWindow", "软件简介"))

class reload_mainWin(QMainWindow, Ui_MainWindow):
    
    def __init__(self):
        super(reload_mainWin, self).__init__()
        self.setupUi(self)
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
        self.pushButton_2.hide()

        self.mouse= pynput.mouse.Controller()
       
    def about_it(self):
        QMessageBox.information(self,"介绍","此软件用于记录 鼠标事件和键盘事件\nF4为停止记录的快捷方式\n\n\n此程序为开源程序 绝无后门进程\n地址在我的github仓库zhihao2020\INPUT_RECORD",QMessageBox.Yes)

    def play_it(self):
        """
        鼠标移动 mouse_move,(x,y)qw
        鼠标点击 mouse_click,press or release|x+y|左键or右键
        鼠标滚轮 Scrolled,x|y
        """
        self.showMinimized()
        with open('dataini.io',"r") as fd:
            for line in fd.readlines():
                time.sleep(random.uniform(0,0.2))
                flag = line.split('=')[0]
                context = line.split('=')[1]
                if flag == "mouse_move":
                    print(context)
                    self.mouse_controller(context)
                elif flag == "mouse_click":
                    print(context)
                    self.mouse_Click(context)
                elif flag=="Scrolled":
                    print(context)
                    self.mouse_scroll(context)
                elif flag == "keyboard":
                    print(context)
                    self.keyboard_controller(context)
                
    def add_list_content(self,content):
        self.listWidget.addItem(content)

    def mouse_controller(self,content):
        
        x = int(content.split("+")[0])
        y = int(content.split("+")[1])
        self.mouse.position = (x,y)

    def mouse_Click(self,context):
        #鼠标点击 mouse_click,Pressed or Released|(x,y)|左键or右键
        first = context.split("|")[0]
        #second_location = context.split("|")[1]
        third = context.split("|")[2]
        if "Pressed" in  first:
            if "Button.left" in third:
                self.mouse.press(Button.left)
            elif  "Button.right" in third:
                print("按下右键")
                self.mouse.press(Button.right)
        elif  "Released" in first :
            if  "Button.left" in third:
                self.mouse.release(Button.left)
                
            elif "Button.right" in third :
                print("释放右键")
                self.mouse.release(Button.right)
            time.sleep(random.uniform(0,1))
        
    def mouse_scroll(self,content):
        # 鼠标滚轮 Scrolled,x|y
        mouse= pynput.mouse.Controller()
        x = content.split("|")[0]
        y = content.split("|")[1]
        mouse.scroll(int(x),int(y))
    
    def keyboard_controller(self,content):
        flag = content.split("|")[1].strip()
        try:
            button = ast.literal_eval(content.split("|")[0].strip())
        except:
            button = content.split("|")[0].strip()
        try:
            keyboard = pynput.keyboard.Controller()
            if "press" in flag:
                keyboard.press(button)
            elif "release" in flag:
                keyboard.release(button)
        except:
            pass

    def continue_start(self):
        print("恢复开始")
        self.keyboard_thread.start()
        self.mouse_thread.start()

    def start_record(self):
        #开始记录 鼠标位置、是否点击
        #判断 鼠标是否 拖动
        #判断键盘是否输入
        self.pushButton.setEnabled(False)
        self.pushButton_2.show()
        self.pushButton_3.hide()
        self.pushButton_4.hide()
        self.listWidget.clear()
        file = open('dataini.io',"w")
        file.close()
        self.keyboard_thread.start()
        self.mouse_thread.start()

    def end_record(self):
        #停止记录
        self.pushButton.setEnabled(True)
        self.keyboard_thread.cancel()
        self.mouse_thread.cancel()
        self.pushButton_3.show()
        self.pushButton_4.show()
      
class mouse_Thread(QThread,Ui_MainWindow):
    """
    io文件存储 “标识符,内容”
    鼠标移动 mouse_move,(x,y)
    鼠标点击 mouse_click,press or release|(x,y)|左键or右键
    鼠标滚轮 Scrolled,x|y23
    """
    mouse_signal = pyqtSignal(bool)
    mouse_information = pyqtSignal(str)
    
    def __init__(self):
        super(mouse_Thread,self).__init__()
       
    def on_move(self,x,y):
        with open('dataini.io',"a") as fd:
            fd.write('mouse_move='+ str(x) +"+" + str(y)+'\n')
        self.mouse_information.emit('鼠标移动到：{0}'.format((x,y)))

    def on_click(self,x,y,button,pressed):
        with open('dataini.io',"a") as fd:
            #存入格式为 按下去,右键或左键,(x,y)
            fd.write('mouse_click='+'%s|%s|%s'%('Pressed'if pressed else 'Released',
                            (x,y),button)+'\n')
           
        self.mouse_information.emit("鼠标点击 {0}".format('Pressed'if pressed else 'Released'))
        self.mouse_information.emit("鼠标点击 %s"%button)
    
    def on_scroll(self,x,y,dx,dy):
        with open('dataini.io',"a") as fd:
            fd.write('Scrolled={0}|{1}'.format(dx,dy)+'\n')
        self.mouse_information.emit("鼠标x轴滚动 %s"%dx)
        self.mouse_information.emit("鼠标y轴滚动 %s"%dy)
        
    def cancel(self):
        #用于线程暂停
        self.listener.stop()
   
    def run(self):     
        self.listener =  pynput.mouse.Listener(
            on_move = self.on_move,
            on_click = self.on_click,
            on_scroll=self.on_scroll)     
        self.listener.start()

class keyboard_Thread(QThread,Ui_MainWindow):
    """
    键盘 keyboard,按钮
   
    """
    keyboard_signal = pyqtSignal(bool)
    keyboard_information = pyqtSignal(str)
    def __init__(self):
        super(keyboard_Thread,self).__init__()
       
    def on_press(self,key):
        with open('dataini.io',"a") as fd:
            fd.write('keyboard='+str(key)+"|press"+'\n')
        self.keyboard_information.emit("按下 %s"%str(key))
        print('{0} pressed'.format(key))

    def on_release(self,key):
        with open('dataini.io',"a") as fd:
            fd.write('keyboard='+str(key)+"|release"+'\n')
        self.keyboard_information.emit('释放,{0}'.format(key))

    def cancel(self):
        #用于线程暂停
        self.listener.stop()

    def run(self):
        self.listener = pynput.keyboard.Listener(on_press = self.on_press,on_release=self.on_release) 
        self.listener.start()

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
