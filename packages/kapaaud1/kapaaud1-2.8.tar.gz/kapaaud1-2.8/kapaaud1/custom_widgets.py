# custom_widgets.py
import tkinter as tk
from PIL import Image, ImageTk
import baiduasr
import configdjj
from threading import Timer
import threading

class CustomWindow:
    def __init__(self, root, label_text=None, 
                             label_text_pos=None,

                             label_text_yuyixianshi=None,
                             label_text_yuyixianshi_pos=None,
                button1_text=None, 
                button1_pos=None,
                button2_text=None,
                button2_pos=None,

                button3_text=None,
                button3_pos=None,
                button4_text=None,
                button4_pos=None,
                                 
                button_cz_text=None,
                button_cz_pos=None,
        
                button_qx_text=None,
                button_qx_pos=None,

                label_text_shuiguomingzi=None,
                label_text_shuiguomingzi_pos=None, 
                label_text_fangzhiweizhi=None,
                label_text_fangzhiweizhi_pos=None,
                label_text_shifouchengshu=None,
                label_text_shifouchengshu_pos=None,
                label_text_shuiguoshuliang=None,
                label_text_shuiguoshuliang_pos=None,

                image_path=None,  canvas_pos=(20, 20), canvas_size=(300, 200)):
        self.root = root
        self.root.title("自定义窗口")
        self.root.geometry("1200x800")  # 设置窗口大小

        self.czhc_start_x=200
        self.czhc_start_y=500
        self.qxhc_start_x=600
        self.qxhc_start_y=500
        #滑槽间隔
        self.hc_jg=40
        self.image_list = []

        # 创建Canvas控件
        self.canvas = tk.Canvas(root, width=canvas_size[0], height=canvas_size[1])
        self.canvas.place(x=canvas_pos[0], y=canvas_pos[1])
        #self.canvas.pack()

        #常规打包，=0不管画布，=1与画布互斥
        changgui_dabao = 0
        # 创建Label控件
        self.label = tk.Label(root, text=label_text)
        self.label.place(x=label_text_pos[0], y=label_text_pos[1])  # 使用place方法指定位置
        if changgui_dabao==1:
            self.label.pack(pady=10)
        #语音显示
        self.label_yyxs = tk.Label(root, text=label_text_yuyixianshi)
        self.label_yyxs.place(x=label_text_yuyixianshi_pos[0], y=label_text_yuyixianshi_pos[1])  # 使用place方法指定位置
        if changgui_dabao==1:
            self.label_yyxs.pack(pady=10)
        #水果名字
        self.label_sgmz = tk.Label(root, text=label_text_shuiguomingzi)
        self.label_sgmz.place(x=label_text_shuiguomingzi_pos[0], y=label_text_shuiguomingzi_pos[1])  # 使用place方法指定位置
        if changgui_dabao==1:
            self.label_sgmz.pack(pady=10)
        #放置物资
        self.label_fzwz = tk.Label(root, text=label_text_fangzhiweizhi)
        self.label_fzwz.place(x=label_text_fangzhiweizhi_pos[0], y=label_text_fangzhiweizhi_pos[1])  # 使用place方法指定位置
        if changgui_dabao==1:
            self.label_fzwz.pack(pady=10)
        #是否成熟
        self.label_sfcs = tk.Label(root, text=label_text_shifouchengshu)
        self.label_sfcs.place(x=label_text_shifouchengshu_pos[0], y=label_text_shifouchengshu_pos[1])  # 使用place方法指定位置
        if changgui_dabao==1:
            self.label_sfcs.pack(pady=10)
        #水果数量        

        self.label_sgsl = tk.Label(root, text=label_text_shuiguoshuliang)
        self.label_sgsl.place(x=label_text_shuiguoshuliang_pos[0], y=label_text_shuiguoshuliang_pos[1])  # 使用place方法指定位置
        if changgui_dabao==1:
            self.label_sgsl.pack(pady=10)


        # 用于存储图片对象的变量（初始化为None）
        self.image_on_canvas = None

        # 创建第一个Button控件
        self.button1 = tk.Button(root, text=button1_text, command=self.on_button1_click_1)
        self.button1.place(x=button1_pos[0], y=button1_pos[1])

        # 创建第二个Button控件（可选）
        self.button2 = tk.Button(root, text=button2_text, command=self.ts_qd)
        self.button2.place(x=button2_pos[0], y=button2_pos[1])
        self.button2.pack()
        #self.button2.pack_forget()
        ############################

        self.button3 = tk.Button(root, text=button3_text, command=self.ts_tz)
        self.button3.place(x=button3_pos[0], y=button3_pos[1])
        self.button3.pack()
        #self.button3.pack_forget()
        ############################

        self.button4 = tk.Button(root, text=button4_text, command=self.ts_fj)
        self.button4.place(x=button4_pos[0], y=button4_pos[1])
        self.button4.pack()
        #self.button4.pack_forget()
        ############################

        self.button_cz = tk.Button(root, text=button_cz_text, command=self.btn_cz_cliked)
        self.button_cz.place(x=button_cz_pos[0], y=button_cz_pos[1])
        self.button_cz.pack_forget()

        self.button_qx = tk.Button(root, text=button_qx_text, command=self.btn_qx_cliked)
        self.button_qx.place(x=button_qx_pos[0], y=button_qx_pos[1])
        self.button_qx.pack_forget()
        
        # 存储图片路径
        self.image_path = image_path
        self.djj_huahua(r'c:\mic.jpg',configdjj.mkf_wz[0],configdjj.mkf_wz[1])

        self.canvas.create_text(self.czhc_start_x+self.hc_jg+70,self.czhc_start_y+25,text="垂直滑槽")
        self.canvas.create_text(self.qxhc_start_x+self.hc_jg+70,self.qxhc_start_y+25,text="倾斜滑槽")
        #self.canvas.create_text(self.czhc_start_x+self.hc_jg+40,self.czhc_start_y,text="滑槽1       滑槽2         滑槽3       滑槽4     ")
        #self.canvas.create_text(self.qxhc_start_x+self.hc_jg+40,self.qxhc_start_y,text="滑槽1       滑槽2         滑槽3       滑槽4     ")
       
        self.canvas.create_line(self.czhc_start_x +1.5*self.hc_jg,        self.czhc_start_y-self.hc_jg,
                                self.czhc_start_x +1.5*self.hc_jg,        self.czhc_start_y-self.hc_jg*8,
                                )
        self.canvas.create_line(self.czhc_start_x +3.5*self.hc_jg,        self.czhc_start_y-self.hc_jg,
                                self.czhc_start_x +3.5*self.hc_jg,        self.czhc_start_y-self.hc_jg*8,
                                )
        self.canvas.create_line(self.czhc_start_x +5.5*self.hc_jg,        self.czhc_start_y-self.hc_jg,
                                self.czhc_start_x +5.5*self.hc_jg,        self.czhc_start_y-self.hc_jg*8,
                                )
        self.canvas.create_line(self.czhc_start_x +7.5*self.hc_jg,        self.czhc_start_y-self.hc_jg,
                                self.czhc_start_x +7.5*self.hc_jg,        self.czhc_start_y-self.hc_jg*8,
                                )
        self.canvas.create_line(self.czhc_start_x +9.5*self.hc_jg,        self.czhc_start_y-self.hc_jg,
                                self.czhc_start_x +9.5*self.hc_jg,        self.czhc_start_y-self.hc_jg*8,
                                )
        self.canvas.create_line(self.czhc_start_x +1.5*self.hc_jg,        self.czhc_start_y-self.hc_jg,
                                self.czhc_start_x +9.5*self.hc_jg,        self.czhc_start_y-self.hc_jg,
                                )
        self.canvas.create_line(self.czhc_start_x +1.5*self.hc_jg,        self.czhc_start_y-self.hc_jg*8,
                                self.czhc_start_x +9.5*self.hc_jg,        self.czhc_start_y-self.hc_jg*8,
                                )
        
        self.canvas.create_line(self.qxhc_start_x +1.5*self.hc_jg,        self.qxhc_start_y-self.hc_jg,
                                self.qxhc_start_x +1.5*self.hc_jg,        self.qxhc_start_y-self.hc_jg*8,
                                )
        self.canvas.create_line(self.qxhc_start_x +3.5*self.hc_jg,        self.qxhc_start_y-self.hc_jg,
                                self.qxhc_start_x +3.5*self.hc_jg,        self.qxhc_start_y-self.hc_jg*8,
                                )
        self.canvas.create_line(self.qxhc_start_x +5.5*self.hc_jg,        self.qxhc_start_y-self.hc_jg,
                                self.qxhc_start_x +5.5*self.hc_jg,        self.qxhc_start_y-self.hc_jg*8,
                                )
        self.canvas.create_line(self.qxhc_start_x +7.5*self.hc_jg,        self.qxhc_start_y-self.hc_jg,
                                self.qxhc_start_x +7.5*self.hc_jg,        self.qxhc_start_y-self.hc_jg*8,
                                )
        self.canvas.create_line(self.qxhc_start_x +9.5*self.hc_jg,        self.qxhc_start_y-self.hc_jg,
                                self.qxhc_start_x +9.5*self.hc_jg,        self.qxhc_start_y-self.hc_jg*8,
                                )
        self.canvas.create_line(self.qxhc_start_x +1.5*self.hc_jg,        self.qxhc_start_y-self.hc_jg,
                                self.qxhc_start_x +9.5*self.hc_jg,        self.qxhc_start_y-self.hc_jg,
                                )
        self.canvas.create_line(self.qxhc_start_x +1.5*self.hc_jg,        self.qxhc_start_y-self.hc_jg*8,
                                self.qxhc_start_x +9.5*self.hc_jg,        self.qxhc_start_y-self.hc_jg*8,
                                )

        self.canvas.create_text(self.czhc_start_x +2*self.hc_jg, self.czhc_start_y+self.hc_jg*0,text="滑槽1")
        self.canvas.create_text(self.czhc_start_x +4*self.hc_jg, self.czhc_start_y+self.hc_jg*0,text="滑槽2")
        self.canvas.create_text(self.czhc_start_x +6*self.hc_jg, self.czhc_start_y+self.hc_jg*0,text="滑槽3")
        self.canvas.create_text(self.czhc_start_x +8*self.hc_jg, self.czhc_start_y+self.hc_jg*0,text="滑槽4")
                                
        self.canvas.create_text(self.qxhc_start_x +2*self.hc_jg, self.qxhc_start_y+self.hc_jg*0,text="滑槽1")
        self.canvas.create_text(self.qxhc_start_x +4*self.hc_jg, self.qxhc_start_y+self.hc_jg*0,text="滑槽2")
        self.canvas.create_text(self.qxhc_start_x +6*self.hc_jg, self.qxhc_start_y+self.hc_jg*0,text="滑槽3")
        self.canvas.create_text(self.qxhc_start_x +8*self.hc_jg, self.qxhc_start_y+self.hc_jg*0,text="滑槽4")
                
        
        self.btn_cz_cliked()
        #dujiajie
        self.t = Timer(1,self.my_tim)
        self.t.start()
    def qx_delete(self):
        self.canvas.delete(self.cover_qx)
        self.cover_qx = self.canvas.create_rectangle(self.qxhc_start_x,             self.qxhc_start_y+100,
                                                     self.qxhc_start_x+self.hc_jg*10,self.qxhc_start_y-self.hc_jg*10, 
                                                     fill=self.canvas["bg"], outline="")
    def cz_delete(self):
        self.canvas.delete(self.cover_cz)
        self.cover_cz = self.canvas.create_rectangle(self.czhc_start_x,             self.czhc_start_y+100,
                                                     self.czhc_start_x+self.hc_jg*10,self.czhc_start_y-self.hc_jg*10, 
                                                     fill=self.canvas["bg"], outline="")
    def my_tim(self):
        #print("11")
        self.t.cancel()
        self.t = Timer(1,self.my_tim)
        self.t.start()
        
        if(configdjj.tx_show_change == 1):

            self.label_sgsl.config(text = "数量:"+str(configdjj.shuiguo_num))
            self.label_sgmz.config(text = "水果名字:"+str(configdjj.fruit_name))
            self.label_fzwz.config(text = "放置位置:"+str(configdjj.fangzhiweizhi))
            self.label_sfcs.config(text = "是否成熟:"+str(configdjj.shifouchengshu))
            
            if configdjj.tx_czhc_show_change ==1:
                configdjj.czhc_index[configdjj.tx_local-1] = configdjj.czhc_index[configdjj.tx_local-1] + 1
                heng = configdjj.tx_local+1
                shu = configdjj.czhc_index[configdjj.tx_local-1]
                self.djj_huacaoshow(r'c:\tx.jpg',self.czhc_start_x +(heng*2)*self.hc_jg, self.czhc_start_y-self.hc_jg * (configdjj.czhc_index[configdjj.tx_local-1]+1))
                if configdjj.pingbi_shuaxin == 'cz':
                    self.cz_delete()
            if configdjj.tx_qxhc_show_change ==1:
                configdjj.qxhc_index[configdjj.tx_local-1] = configdjj.qxhc_index[configdjj.tx_local-1] + 1
                heng = configdjj.tx_local+1
                shu = configdjj.qxhc_index[configdjj.tx_local-1]
                self.djj_huacaoshow(r'c:\tx.jpg',self.qxhc_start_x +(heng*2)*self.hc_jg, self.qxhc_start_y-self.hc_jg * (configdjj.qxhc_index[configdjj.tx_local-1]+1))
                
                if configdjj.pingbi_shuaxin == 'qx':
                    self.qx_delete()
            configdjj.tx_show_change = 0
            configdjj.tx_czhc_show_change = 0
            configdjj.tx_qxhc_show_change = 0
            


    def on_button1_click_2(self):
        print("hi 2")
        baiduasr.record()
        data = "语音识别内容:" + baiduasr.asr_updata()
        #data = '123'
        self.label_yyxs.config(text = data)

        t = data.split(',')
        print(t)
        for i in range(len(t)):
            if '启动' in t[i]:
                msg='yy_plc_qd'
                print(msg)
                configdjj.socket_client.send(msg.encode())
            if '分' in t[i]:
                msg='an_plc_ksfj'
                print(msg)
                configdjj.socket_client.send(msg.encode())
            if '停止' in t[i]:
                msg='yy_plc_tz'
                print(msg)
                configdjj.socket_client.send(msg.encode())
            if '上' in t[i]:
                msg='an_plc_z+'
                print(msg)
                configdjj.socket_client.send(msg.encode())
            if '下' in t[i]:
                msg='an_plc_z-'
                print(msg)
                configdjj.socket_client.send(msg.encode())
            if '左' in t[i]:
                msg='an_plc_x-'
                print(msg)
                configdjj.socket_client.send(msg.encode())
            if '右' in t[i]:
                msg='an_plc_x+'
                print(msg)
                configdjj.socket_client.send(msg.encode())
            if '前' in t[i]:
                msg='an_plc_y+'
                print(msg)
                configdjj.socket_client.send(msg.encode())
            if '后' in t[i]:
                msg='an_plc_y-'
                print(msg)
                configdjj.socket_client.send(msg.encode())
            
        self.djj_huahua(r'c:\mic.jpg',configdjj.mkf_wz[0],configdjj.mkf_wz[1])

    def djj_huahua(self,image_path,x,y):
        image = Image.open(image_path)
        new_size = (40, 40)
        image = image.resize(new_size,Image.ANTIALIAS)
        self.image_on_canvas = ImageTk.PhotoImage(image)
        self.image_list.append(self.image_on_canvas)  # 保持引用
        self.canvas.create_image(x,y, image=self.image_on_canvas)

    def djj_huacaoshow(self,image_path,x,y):
        image = Image.open(image_path)
        new_size = (40, 40)
        image = image.resize(new_size)
        self.image_on_canvas = ImageTk.PhotoImage(image)
        self.image_list.append(self.image_on_canvas)  # 保持引用
        self.canvas.create_image(x,y, image=self.image_on_canvas)
    
    def on_button1_click_1(self):
        self.djj_huahua(r'c:\mic1.jpg',configdjj.mkf_wz[0],configdjj.mkf_wz[1])
        print("hi 1")
        self.root.after(100, self.on_button1_click_2)    

    def ts_qd(self):
        msg = 'yy_plc_qd'
        configdjj.socket_client.send(msg.encode())
        configdjj.ceshi_num = configdjj.ceshi_num + 1
        
    def ts_tz(self):
        msg = 'yy_plc_tz'
        configdjj.socket_client.send(msg.encode())
        

    def ts_fj(self):
        msg = 'yy_plc_ksfj'
        configdjj.socket_client.send(msg.encode())
        #self.canvas.create_line(40,40,500,500)
        #self.canvas.create_text(444,444,text="你好！！！！！！！！！")
    def btn_cz_cliked(self):
        if configdjj.pingbi_shuaxin=='cz':
            #self.canvas.move(self.cover_cz, 600, 0)
            self.cover_qx = self.canvas.create_rectangle(self.qxhc_start_x,              self.qxhc_start_y+100,
                                                        self.qxhc_start_x+self.hc_jg*10,self.qxhc_start_y-self.hc_jg*10, 
                                                        fill=self.canvas["bg"], outline="")
            if configdjj.xianshi_flag == 1:
                self.canvas.delete(self.cover_cz)
            configdjj.xianshi_flag = 1
            configdjj.pingbi_shuaxin = 'qx'
    def btn_qx_cliked(self):
        #当前为倾斜（qx）屏蔽的时候，按下倾斜显示
        if configdjj.pingbi_shuaxin=='qx':
            self.cover_cz = self.canvas.create_rectangle(self.czhc_start_x,              self.czhc_start_y+100,
                                                        self.czhc_start_x+self.hc_jg*10,self.czhc_start_y-self.hc_jg*10, 
                                                        fill=self.canvas["bg"], outline="")
            self.canvas.delete(self.cover_qx)
            configdjj.pingbi_shuaxin =1
            configdjj.pingbi_shuaxin = 'cz'

        

# 注意：这里没有直接启动mainloop，因为mainloop应该在主程序中启动。