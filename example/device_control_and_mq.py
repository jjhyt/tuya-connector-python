"""This module has components that are used for testing tuya's device control and Pulsar massage queue."""
import logging
import json
from tkinter import *
from tuya_connector import (
    TuyaOpenAPI,
    TuyaOpenPulsar,
    TuyaCloudPulsarTopic,
    TUYA_LOGGER,
)

ACCESS_ID = "j95tg7qeaug3rhhon40v"
ACCESS_KEY = "65fb01867e554121b14e35c1abe315be"
API_ENDPOINT = "https://openapi.tuyacn.com"
MQ_ENDPOINT = "wss://mqe.tuyacn.com:8285/"

global setvalue
# Enable debug log
TUYA_LOGGER.setLevel(logging.DEBUG)

# Init Message Queue
open_pulsar = TuyaOpenPulsar(
    ACCESS_ID, ACCESS_KEY, MQ_ENDPOINT, TuyaCloudPulsarTopic.PROD
)

# Init openapi and connect
openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
openapi.connect()

# set up device_id
DEVICE_ID ="6c9ac0eb115c46e798brja"

def pmsg(self):
    global setvalue
    print(self)
    # json类型的数据转化为python类型的数据
    xman = json.loads(self)
    # 打印转换后data类型
    print(xman)
    # 获取内容
    devid = xman.get('devId')
    print(devid)
    if devid == "6c8864f34fc9678054u6e4":
        devstatus = xman.get('status')
        devvalue = devstatus[0].get('value')
        print(devvalue)
        setvalue = devvalue

    if devid == "6cf6a24d12026f2be3yqcr":
        devstatus = xman.get('status')
        devpir = devstatus[0].get('value')
        print(devpir)
        if devpir == "pir":
            DEVICE_ID = "6c9ac0eb115c46e798brja"
            # Send commands
            commands = {'commands': [{'code': 'switch_led', 'value': True}]}
            openapi.post('/v1.0/iot-03/devices/{}/commands'.format(DEVICE_ID), commands)
        else:
            if setvalue == True:
                DEVICE_ID = "6c9ac0eb115c46e798brja"
                # Send commands
                commands = {'commands': [{'code': 'switch_led', 'value': False}]}
                openapi.post('/v1.0/iot-03/devices/{}/commands'.format(DEVICE_ID), commands)

# Add Message Queue listener
open_pulsar.add_message_listener(pmsg)

# Start Message Queue
open_pulsar.start()

class MY_GUI():
    def __init__(self,init_window_name):
        self.init_window_name = init_window_name


    #设置窗口
    def set_init_window(self):
        self.init_window_name.title("Tuya智能场景管理_v1.0")           #窗口名
        #self.init_window_name.geometry('320x160+0+10')                         #290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        self.init_window_name.geometry('480x320+380+200')
        #self.init_window_name["bg"] = "pink"                                    #窗口背景色，其他背景色见：blog.csdn.net/chl0000/article/details/7657887
        #self.init_window_name.attributes("-alpha",0.9)                          #虚化，值越小虚化程度越高
        # 按钮
        self.left_home_button = Button(self.init_window_name, text="启动离家模式", bg="lightblue", width=10,
                                              command=self.left_home)  # 调用内部方法  加()为直接调用
        self.left_home_button.place(relx=0.4 , rely=0.4)
        self.exit_button = Button(self.init_window_name, text="关闭窗口", bg="red", width=10,
                                       command=JieShu)  # 调用内部方法  加()为直接调用
        self.exit_button.place(relx=0.4, rely=0.8)

    # 功能函数
    def left_home(self):
        DEVICE_ID = "6c9ac0eb115c46e798brja"
        # Send commands
        commands = {'commands': [{'code': 'switch_led', 'value': False}]}
        openapi.post('/v1.0/iot-03/devices/{}/commands'.format(DEVICE_ID), commands)

        DEVICE_ID = "6cfc422844a7470d86mnzf"
        # Send commands
        commands = {'commands': [{'code': 'switch_1', 'value': False}]}
        openapi.post('/v1.0/iot-03/devices/{}/commands'.format(DEVICE_ID), commands)


init_window = Tk()             #实例化出一个父窗口

def JieShu():
    open_pulsar.stop()
    init_window.destroy()

def gui_start():
    ZMJ_PORTAL = MY_GUI(init_window)
    # 设置根窗口默认属性
    ZMJ_PORTAL.set_init_window()
    # 接收到关闭点击操作的语句,之后调用JieShu函数
    init_window.protocol("WM_DELETE_WINDOW", JieShu)
    init_window.mainloop()          #父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示


gui_start()