import uiautomator2 as u2
import os,time
import threading
import json

device_account = {'9A261FFAZ008UN':['kimiaf_shoper','kimiac_shoper','kimiad_shoper','kimiae_shoper']}
account_list = {'kimiaf_shoper':0,'kimiac_shoper':0,'kimiad_shoper':0,'kimiae_shoper':0}


def get_device_name():
    #读取本地的tmp.json文件
    with open('device.json', encoding='utf-8') as f:
        data = json.load(f)
         
        return  data
    
global_device_name = get_device_name()

def dev_print(device,msg):

    print(global_device_name[device]+":"+msg)

def get_input_data(device):
    #读取本地的tmp.json文件
    with open('data.json', encoding='utf-8') as f:
        data = json.load(f)
        print(data)
        return data[device]


def get_device_account_data(device):
    #读取本地的设备账号对应文件
    with open('account.json', encoding='utf-8') as f:
        data = json.load(f)
        print(data)
        return data[device]
    
def get_account_post_data(account_list):
    #读取本地的账号发布数量文件
    with open('schedule.json', encoding='utf-8') as f:
        data = json.load(f)
        total = 0
        redata = {}
        #循环该机器的所有账号，从所有排期表中找出对应的账号，并添加到返回列表里
        for account in account_list:
          if data.__contains__(account):
            redata[account] = data[account]
            total = total + data[account]
        return redata,total


def get_devices_serials():
    devices_list = []
    fd = os.popen("adb devices")
    devices_list_src = fd.readlines()
    fd.close()
    for device in devices_list_src:
        if "device\n" in device:
            device = device.replace("\tdevice\n","")
            devices_list.append(device)
    return devices_list

def wake_up(device):
    d = u2.connect(device)
    dev_print(device,"唤醒设备")
    print(d.info)
    #d.app_start("com.zhiliaoapp.musically")

def post_drafts(device):
    d = u2.connect(device)
    dev_print(device,"唤醒设备")

    #提取该设备中所有的账号
    account_list = get_device_account_data(device)

    account_schedule,total = get_account_post_data(account_list)


    #循环数量为所有需要发布的视频数量
    for j in range(total):
        #判断是否有privacy setting文字
        if d(text="Privacy settings").exists():
            #点击返回个人主页
            d.click(100,150)

        #点击profile
        dev_print(device,"点击profile")
        d.click(960,2150)
        time.sleep(5)
        username = ""
        #获取当前用户名
        if d(textStartsWith="@"):
            username = d(textStartsWith="@").get_text()
            #账号名去掉@符号
            username = username.replace("@","")
            #输出用户名
            dev_print(device,"获取当前用户名:"+username)
        else:
            dev_print(device,"**获取不到用户名**")

        #如果已经为0,则继续下一个账号
        if account_schedule[username] == 0:
            switch_account(d,account_list[j% len(account_list)])
            continue
        
        #判断是否存在未发布的视频
        dy = 0
        tsp = d(text="TikTok Shop")
        if tsp.exists():
            loc = tsp[0].center()
            d.click(loc[0]-400,loc[1]-150)
            time.sleep(5)

        #判断 如果存在草稿，点击草稿
        if d(textStartsWith="Drafts").exists():
            d(textStartsWith="Drafts").click()
            time.sleep(5)
            dy = 1

        if dy == 0:#就如果现在已经没有草稿了

            #那应该给这个账号剩下需要排期发布的数据清零
            account_schedule[username] = 0

            #判断是否填写的排期表比实际数量还要多，比如要发6个，实际之存了俩视频，怎么办
            tt = 0
            for k in account_schedule:
                tt += account_schedule[k]
            if tt == 0:
                return
        
        if dy == 1:
            #点击第一个视频
            d.click(0.141, 0.29)
            time.sleep(5)
            #点击Next文字
            d(text="Next").click()
            time.sleep(5)
            #点击Post文字
            d.click(770,2130)
            dev_print(device,'点击发送视频，休眠:'+str(3600/60)+"分钟")
            #dev_print(device,'点击Post文字')
            #然后等半个小时,换号
            time.sleep(1800)
            #切换账号
            #账号对应数量加一
            account_schedule[username] = account_schedule[username] - 1
            cancelPopup(d)
        
        #查询一下account_schedule，如果要切换的下一个账号已经为0了，就继续下一个
        if account_schedule[username] == 0:
            j+=1
            #在数组里删除该账号
            del account_schedule[username]
            #在account_list里也删除该账号
            account_list.remove(username)
        
        #如果删完了以后没有该发的帐号了，就退出
        if len(account_schedule) == 0:
            return
        
        #如果account_schedule里面的只有一个账号，则不切换账号
        if len(account_schedule) == 1:
            continue
        
        nextuser = account_list[j% len(account_list)]
        if nextuser == username:
            nextuser = account_list[j+1% len(account_list)]
        #切换账号
        switch_account(d,nextuser,device)

#切换账号
def switch_account(d,account,device):
    dev_print(device,"切换账号:"+account)
    #先执行退出
    d.app_stop('com.zhiliaoapp.musically')
    #等待10秒
    time.sleep(10)
    #再唤醒app
    d.app_start('com.zhiliaoapp.musically')
    #等待10秒
    time.sleep(10)
    #点击profile
    d.click(960,2150)
    time.sleep(2)
    #点击右上角三个点
    d.click(1000,150)
    time.sleep(2)
    #点击Settings
    d(textStartsWith="Settings").click()
    time.sleep(2)
    #拉到最下面
    d.swipe(500, 2100, 500, 0)
    time.sleep(2)
    #点击switch account
    d(textStartsWith="Switch").click()
    #获取所有kimi开头的账号
    time.sleep(3)
    kimi_list = d(text=account)
    #按顺序点击，比如第一次点的是kim1，第二次点的是kim2，测试这种排序行不行，后期肯定还要关联db
    kimi_list.click()
    #等十秒钟加载信息
    time.sleep(10)

#监测发布视频后和切换账号后是否有奇怪弹窗
def cancelPopup(d):
    fbMsgBox = d(text="Don't allow")
    if fbMsgBox.exists():
        fbMsgBox.click()
        time.sleep(1)

#发布视频
def post_video(device):
    d = u2.connect(device)
    dev_print(device,"唤醒设备")
    print(d.info)
    #d.app_start("com.zhiliaoapp.musically")
    data = get_input_data(device)

    for i in range(len(data)):
        tmpdata = data[i]
        #选择视频
        SelectVideo(d,i,device)
        if tmpdata["video_text"] != "":
            #添加文案
            AddVideotext(d,tmpdata["video_text"],device)
        #添加音乐
        AddMusic(d,device)
        #如果需要静音
        mute = False
        try: 
            mute = tmpdata["mute_bgm"]
        except Exception as e:
            dev_print(device,"通知:没有mute_bgm字段")

        if mute:
            #编辑音量
            EditVolume(d)

        #点击下一步
        d(text="Next").click()
        #填写post文案
        EditPostContent(d,tmpdata,device)
        
        for j in range(len(tmpdata['product'])):
            #添加产品
            AddProduct(d,tmpdata['product'][j],device)


        #判断是否是仅自己可见
        if d(textStartsWith="Only you can").exists():
            dev_print(device,"出现仅自己可见")
            d(textStartsWith="Only you can").click()
            time.sleep(2)
            dev_print(device,"设置所有人可见")
            d(text="Everyone").click()
            time.sleep(2)
            dev_print(device,"落下弹窗")
            #点击空白处落下键盘
            d.click(1024,650)

        #点击存入草稿箱
        dev_print(device,"结束--点击存入草稿箱")

        d(text="Drafts").click()
        time.sleep(5)

#添加文案
def AddVideotext(d,text,device):
    dev_print(device,"文案---添加文案:"+text)
    #点击添加文案
    d(text="Text").click()
    time.sleep(2)
    tts = d(text="Done")
    if not tts.exists():
        #再次点击Text文案
        dev_print(device,"文案---再次点击Text文案")
        d(text="Text").click()
        time.sleep(2)
    
    if not tts.exists():
        #长按text文案1秒
        dev_print(device,"文案---长按text文案1秒")
        d(text="Text").long_click(1)
        time.sleep(2)

    if not tts.exists():
        #报错
        dev_print(device,"错误:文案---找不到文字输入框")
        return
    
    time.sleep(2)
    #把内容存入剪贴板
    dev_print(device,"文案---把内容存入剪贴板")
    d.set_clipboard(text)
    time.sleep(2)
    #长按输入框2秒
    dev_print(device,"文案---长按输入框2秒")
    d.long_click(560, 678, 2)
    time.sleep(1)
    #点击Paste
    dev_print(device,"文案---点击Paste")
    d(text="Paste").click()
    time.sleep(1)
    d.click(82,1124)
    time.sleep(2)
    #点击Done
    dev_print(device,"文案---点击Done")
    d(text="Done").click()
    time.sleep(1)
    #长按正中间，向上拖动500像素
    dev_print(device,"文案---长按正中间，向上拖动500像素")
    d.swipe(0.5, 0.5, 0.5, 0.5-400/1920, 0.5)
    time.sleep(1)


#选择视频
def SelectVideo(d,i,device):
    dev_print(device,"视频---点击发布视频")
    #点击发布视频
    d.click(550,2150)
    time.sleep(2)
    dev_print(device,"视频---点击Upload")
    d(text="Upload").click()
    time.sleep(2)
    dev_print(device,"视频---点击Videos")
    d(text="Videos").click()
    time.sleep(2)
    dev_print(device,"视频---点击第"+str(i)+"个视频")
    video_list = d(textStartsWith="00")
    video_list[i].click()
    time.sleep(2)
    #判断是否有select按钮
    dev_print(device,"视频---判断是否有select按钮")
    isselect = d(text="Select")
    if isselect.exists():
        #点击Next按钮
        d.click(990,2108)
        dev_print(device,"视频---点击Next按钮位置坐标")
        time.sleep(2)

#添加音乐
def AddMusic(d,device):
    #点击音乐
    dev_print(device,"点击音乐")
    sound = d(text="Add sound")
    if sound.exists():
        sound.click()
    elif d(text="Sounds"):
        d(text="Sounds").click()
    else:
        dev_print(device,"错误!音乐---找不到添加音乐按钮")
        return
    
    time.sleep(2)
    #这一步是如果添加音乐拉起的是半屏，就点击访问全屏界面
    dev_print(device,"音乐---点击访问全屏界面")
    d.click(1000,1148)
    time.sleep(5)
    fav_button =  d(text="Favorites")
    dev_print(device,"音乐---点击Favorites")
    fav_button.click()
    time.sleep(2)
    re_center = fav_button.center()
    #选择下面的一首曲子
    dev_print(device,"音乐---选择下面的一首曲子")
    d.click(re_center[0],re_center[1]+200)
    time.sleep(1)
    #点击对勾
    dev_print(device,"音乐---点击对勾")
    d.click(900,re_center[1]+200)
    time.sleep(2)
    #去掉半窗
    dev_print(device,"音乐---去掉半窗")
    d.click(30,300)
    time.sleep(2)

#编辑音量
def EditVolume(d,device):
    #点击编辑音频音量
    dev_print(device,"音量---点击编辑音频音量")
    edit = d(text="Edit")
    if edit:
        edit.click()
    elif d(text="Adjust clips"):
        d(text="Adjust clips").click()
    else:
        dev_print(device,"错误!音量---找不到编辑视频按钮")
        return
    
    time.sleep(2)

    #编辑音频音量
    dev_print(device,"音量---编辑音频音量")
    d.click(600,1710)
    time.sleep(2)
    #点击volume
    dev_print(device,"音量---点击volume")
    d(text="Volume").click()
    time.sleep(2)
    #拖动音量按钮到200%
    dev_print(device,"音量---拖动音量按钮到200%")
    d.swipe(0.5, 0.86, 0.05, 0.86, 0.5)
    time.sleep(2)
    #点击Save
    dev_print(device,"音量---点击Save")
    d(text="Save").click()
    time.sleep(2)

    #编辑视频音量
    dev_print(device,"音量---编辑视频音量")
    d.click(600,1570)
    time.sleep(2)
    #点击volume
    dev_print(device,"音量---点击volume")
    d(text="Volume").click()
    time.sleep(2)
    #拖动音量按钮到200%
    dev_print(device,"音量---拖动音量按钮到200%")
    d.swipe(0.5, 0.86, 0.95, 0.86, 0.5)
    time.sleep(2)
    #点击Save
    dev_print(device,"音量---点击Save")
    d(text="Save").click()
    time.sleep(2)
    #点击Save
    dev_print(device,"音量---点击Save")
    d(text="Save").click()
    time.sleep(2)

#填写post文案
def EditPostContent(d,data,device):
    #把内容存入剪贴板
    dev_print(device,"填写post文案---把内容存入剪贴板")
    d.set_clipboard(data['post_text']+" ")
    time.sleep(2)
    #长按输入框2秒
    dev_print(device,"填写post文案---长按输入框2秒")
    d.long_click(0.07, 0.13, 2)
    time.sleep(1)
    #点击Paste
    dev_print(device,"填写post文案---点击Paste")
    d(text="Paste").click()
    time.sleep(3)
    #点击空白区域落下键盘
    dev_print(device,"填写post文案---点击空白区域落下键盘")
    d.click(968,668)
    time.sleep(2)

#添加产品
def AddProduct(d,p,device):
    #点击add link按钮
    dev_print(device,"产品--添加产品:"+p)
    d(text="Add link").click()
    time.sleep(2)
    #点击add product按钮
    dev_print(device,"产品--点击add product按钮") 
    d(text="Product").click()
    time.sleep(5)
    #把产品信息依次粘贴至剪贴板
    dev_print(device,"产品--把产品信息依次粘贴至剪贴板")
    d.set_clipboard(p)
    time.sleep(1)
    #点击输入框，长按2秒后
    dev_print(device,"产品--点击输入框，长按2秒后")
    d.long_click(0.157, 0.127, 2)
    time.sleep(1)
    #点击Paste
    dev_print(device,"产品--点击Paste")
    d(text="Paste").click()
    time.sleep(2)
    #点击右下角搜索
    dev_print(device,"产品--点击右下角搜索")
    d.click(0.9, 0.9)
    time.sleep(5)
    #点击第一个add按钮
    dev_print(device,"产品--点击第一个add按钮")
    addlist = d(text="Add")
    addlist[0].click()
    time.sleep(2)
    #如果弹窗了点击一个add按钮
    dev_print(device,"产品--如果弹窗了点击一个add按钮")
    d.click(0.5, 0.5)
    time.sleep(5)
    try:
        #添加产品之后返回页面
        d(text="Add").click()
    except Exception as e:
        dev_print(device,"错误!产品--添加产品失败")
        return
    
    time.sleep(5)
    #这里判断，如果是没挂上车要给报警
    #判断是否还存在 Add a product的文案
    #点击左下角落下键盘
    dev_print(device,"产品--点击左下角落下键盘")
    d.click(0.152, 0.974)
    time.sleep(2)

def test(device):
    d = u2.connect(device)
    #先执行退出
    dev_print(device,"退出app")
    try:
        d.app_stop('com.zhiliaoapp.musically')
        d.app_stop('com.ss.android.ugc.trill') 
    except Exception as e:
        dev_print(device,e)

    #等待10秒
    dev_print(device,"等待10秒")
    time.sleep(10)

    #再唤醒app
    try:
        d.app_start('com.zhiliaoapp.musically')
    except Exception as e:
        print(e)
    
    try:
        d.app_start('com.ss.android.ugc.trill') 
    except Exception as e:
        print(e)

    dev_print(device,"唤醒app")
    #等待10秒
    dev_print(device,"等待10秒")
    time.sleep(10)


def multitask(devices_list,task):
    threads = []
    t = threading.Thread()
    get_device_name()
    for device in devices_list:
        #唤醒
        if task == 'connect':
            1==1
        elif task == 'get_data':
            t = threading.Thread(target=get_input_data, args=(device,))
        #发送草稿
        elif task == 'wake_up':
            t = threading.Thread(target=wake_up, args=(device,))
        #发送草稿
        elif task == 'post_drafts':
            t = threading.Thread(target=post_drafts, args=(device,))
        #上传视频
        elif task == 'swtich_account':
            t = threading.Thread(target=switch_account, args=(device,))
        #下载制作好的视频
        elif task == 'post_video':
            t = threading.Thread(target=post_video, args=(device,))
        elif task == 'test':
            t=test(device)
        else:
            print('无效命令,请重新输入!')
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()
