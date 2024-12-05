# main.py
import tkinter as tk
from custom_widgets import CustomWindow
import xiancheng
import threading

if __name__ == "__main__":
    root = tk.Tk()
    
    th1 = threading.Thread(target=xiancheng.TCPClient_Vision)
    th1.setDaemon(1)
    th1.start()

    # 替换为你的本地JPG图片路径
    image_path = r'c:\tx.jpg'
    #x方向，25是2个字，y方向，25是一个字
    # 创建并显示自定义窗口
    custom_window = CustomWindow(root,  label_text="初始标签文本", 
                                        label_text_pos=(300, 50),      

                                        button1_text="语音识别", 
                                        button1_pos=(50, 50),   
                                        label_text_yuyixianshi="语音识别内容:", 
                                        label_text_yuyixianshi_pos=(50, 100), 

                                        label_text_shuiguomingzi="水果名字:", 
                                        label_text_shuiguomingzi_pos=(50, 350), 
                                        label_text_fangzhiweizhi="放置位置:", 
                                        label_text_fangzhiweizhi_pos=(50, 375), 
                                        label_text_shifouchengshu="是否成熟:", 
                                        label_text_shifouchengshu_pos=(50, 400), 
                                        label_text_shuiguoshuliang="数量:", 
                                        label_text_shuiguoshuliang_pos=(50, 425), 

                                button2_text="启动", 
                                button2_pos=(50, 100),
                                button3_text="停止", 
                                button3_pos=(50, 150),
                                button4_text="物资分拣", 
                                button4_pos=(50, 200),

                                button_cz_text="垂直滑槽显示", 
                                button_cz_pos=(50, 250),

                                button_qx_text="倾斜滑槽显示", 
                                button_qx_pos=(50, 300),

                                canvas_pos=(0, 0), 
                                canvas_size=(1200, 800)
                                )
    # 启动主事件循环
    root.mainloop()