import uiautomator2 as u2
import os,time
import tiktok as tt
import threading



def __main__():
    devices_list = tt.get_devices_serials()
    print("准备连接所有设备:")
    print(devices_list)
    #连接设备
    #try:
    for device in devices_list:
        tt.wake_up(device)
    
    while True:
        input_val = input('启动成功, 请输入命令:')
        #唤醒
        if input_val != '':
            tt.multitask(devices_list,input_val)
        else:
            print('无效命令,请重新输入!')

__main__()