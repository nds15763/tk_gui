from tkinter import ttk      
import tkinter as tk
from tkinter import filedialog           
from tkinter.ttk import Progressbar      
from tkinter import messagebox
import time
import threading
import tiktok as tt

window = tk.Tk()
window.config(bg='black')           
frame_num = 0
frames = []
data_list = []

font = ('consolas', 12)    
text = tk.Text(window, height=10, width=85, bg='black', fg='white',           
                borderwidth=5, relief='raised', font=font)
text.pack(padx=10, pady=10)          

tab_control = ttk.Notebook(window)  
   
# 添加样式 
ttk.Style().theme_create('black', parent='alt', settings={
    'TFrame': {'background': 'black'}, 
    'TNotebook': {'background': 'black'},
    'TNotebook.Tab': {'background': 'black', 'foreground': 'white'},
})   
ttk.Style().theme_use('black')   


def add_group():
    global frame_num            
    frame_num += 1
    frame = ttk.Frame(tab1)
    frames.append(frame)     
    frame.video_desc_entry = ttk.Entry(frame)  
    frame.pub_desc_entry = ttk.Entry(frame)    
    frame.goods_entry = ttk.Entry(frame)    
    if not hasattr(frame, 'video_desc_entry'):  # 判断是否已添加输入实例变量
        frame.video_desc_entry = ttk.Entry(frame)  
        frame.pub_desc_entry = ttk.Entry(frame)    
        frame.goods_entry = ttk.Entry(frame)
    else:
        data = {  
            'video_desc': frame.video_desc_entry.get(),
            'pub_desc': frame.pub_desc_entry.get(),
            'goods': frame.goods_entry.get() 
        }
        data_list.append(data) # 已有输入实例变量,提取数据并追加到data_list

    video_desc_label = tk.Label(frame, text='视频内文案:', bg='black', fg='white', font=font) 
    video_desc_label.pack(side='left')  

    video_desc_entry = tk.Entry(frame, bg='black', fg='white', justify='center', font=font)
    video_desc_entry.pack(side='left')

    pub_desc_label = tk.Label(frame, text='发布文案:', bg='black', fg='white', font=font)  
    pub_desc_label.pack(side='left')  

    pub_desc_entry = tk.Entry(frame, bg='black', fg='white', justify='center', font=font)  
    pub_desc_entry.pack(side='left')  

    goods_label = tk.Label(frame, text='挂车商品:', bg='black', fg='white', font=font)  
    goods_label.pack(side='left')  

    goods_entry = tk.Entry(frame, bg='black', fg='white', justify='center', font=font)
    goods_entry.pack(side='left')

    frame.pack()

def execute():
    data_list = []
    for frame in frames:  
        video_desc = frame.video_desc_entry.get()  
        # 提取视频内文案、发布文案和挂车商品
        pub_desc = frame.pub_desc_entry.get()
        goods = frame.goods_entry.get()  
        
        data = {
            'video_desc': video_desc,
            'pub_desc': pub_desc,
            'goods': goods 
        }
        data_list.append(data)  
        
        print(data_list)
    
    # 调用TikTok API上传视频
    for data in data_list:
        video_desc = data['video_desc']
        pub_desc = data['pub_desc']
        goods = data['goods']
        # 上传单个视频......
        
    print('视频上传完成!')

# 批量制作视频tab       
tab1 = ttk.Frame(tab_control, style='black.TFrame')  

frame1 = ttk.Frame(tab1)  
video_desc_label = tk.Label(frame1, text='视频内文案:', bg='black', fg='white', font=font)
video_desc_label.pack(side='left')  

video_desc_entry = tk.Entry(frame1, bg='black', fg='white', justify='center', font=font)  
video_desc_entry.pack(side='left')

pub_desc_label = tk.Label(frame1, text='发布文案:', bg='black', fg='white', font=font)
pub_desc_label.pack(side='left')  

pub_desc_entry = tk.Entry(frame1, bg='black', fg='white', justify='center', font=font)  
pub_desc_entry.pack(side='left') 

goods_label = tk.Label(frame1, text='挂车商品:', bg='black', fg='white', font=font)  
goods_label.pack(side='left')  

goods_entry = tk.Entry(frame1, bg='black', fg='white', justify='center', font=font) 
goods_entry.pack(side='left')  
frames.append(frame1)      # 启动时添加第一个Frame

add_group_btn = tk.Button(tab1, text='增加组', bg='black', fg='white', command=add_group, font=font)
add_group_btn.pack(side='bottom')
execute_btn = tk.Button(tab1, text='执行', bg='black', fg='white', command=execute, font=font)  
execute_btn.pack(side='bottom')  

frame1.pack()

# 定时发送视频tab        
tab2 = ttk.Frame(tab_control, style='black.TFrame')

frame = ttk.Frame(tab2) 
delay_label = tk.Label(frame, text='请输入发送视频的时间间隔(秒):', bg='black', fg='white', font=font)
delay_label.pack(side='left')

delay_entry = tk.Entry(frame, bg='black', fg='white', justify='center', font=font)  
delay_entry.pack(side='left')  

send_video_btn = tk.Button(frame, text='开始定时发送', bg='black', fg='white',  
                           command=lambda: timed_send_video(int(delay_entry.get())),
                           font=font) 
send_video_btn.pack(side='left')

frame.pack()

tab_control.add(tab1, text='批量制作视频')      
tab_control.add(tab2, text='定时发送视频')      
tab_control.pack(expand=1, fill='both')          



def validate_num(s):
    if s.isdigit():
        return True
    else:
        return False
        
def batch_make_video(num): 
    text.delete(1.0, tk.END)
    text.insert(tk.END, '开始批量制作' + str(num) + '个视频...\n')
    for i in range(num): 
        tt.post_video('9B111FFAZ004H3')  
        text.insert(tk.END, '第' + str(i+1) + '个视频制作完成!\n')

def timed_send_video(delay):
    while True:
        tt.post_video('9B111FFAZ004H3') 
        text.insert(tk.END, '发送一条视频!\n')
        time.sleep(delay)

if __name__ == '__main__':               
    window.mainloop()   