
import configdjj
import image_recognition
import time
import socket
import cv2
import os
import random
def TCPClient_Vision():

    # 载入预训练模型
    model = image_recognition.load_model()
    image_recognition.clear_cached_images()
    configdjj.socket_client = socket.socket()
    configdjj.socket_client.connect(('192.168.5.12',2001))
    #configdjj.socket_client.connect(('192.168.101.185',2001))
    #configdjj.socket_client.connect(('172.19.126.28',2001))
    print('djj xiancheng')
    while 1:
        print("xiancheng:wait receive")
        data = configdjj.socket_client.recv(1024).decode()
        print('djj get')
        print(data)
        time.sleep(0.1)
        configdjj.step_flag = 0
        if(data == "ok2"):
            configdjj.wlzs = configdjj.wlzs + 1
            print(configdjj.wlzs)
            print("wlzs")
        if(data == "plc_yy_hcs_1"):
            configdjj.hcls = configdjj.hcls + 1
        if(data == "plc_yy_ngs_1"):
            configdjj.ngls = configdjj.ngls + 1
        #if data == 'plc_tx_wz':
        if 'plc_tx_wz' in data:        
                file_path = r'C:\tx.jpg'  # 注意：在 Windows 路径中使用原始字符串（r'...'）可以避免转义字符的问题
 
                if os.path.isfile(file_path):
                    src_roi = cv2.imread(r'C:\tx.jpg')
                    # 对图像进行推断
                    label, pred_class,myvalue = image_recognition.model_inference(model, src_roi)
                    
                    print(label, pred_class)
                    # 在图像上显示结果
                    image_recognition.display_result(src_roi, pred_class)
                    label_map = {0: 'apple,1', 1: 'apple,2', 2: 'apple,3', 
                    3: 'banana,1',4: 'banana,2', 5: 'banana,3', 
                    6: 'mango,1',7: 'mango,2',8: 'mango,3', 
                    9: 'strawberry,1', 10: 'strawberry,2',11: 'strawberry,3'}

                    msg = 'tx_plc_wz,'+ label_map.get(label)
                    #dujiajie
                    if(myvalue<1.5):
                        print('NGNGNGNGNGNGNGGGGGGGGGGGGGGGGGGGG')
                        print(myvalue)
                        msg = "tx_plc_kb"
                    """
                    kk = random.randint(1, 12)
                    print("dujiji:",kk)
                    if(kk%12 == 0):
                        msg = 'tx_plc_wz,apple,1'
                    if(kk%12 == 1):
                        msg = 'tx_plc_wz,apple,2'
                    if(kk%12 == 11):
                        msg = 'tx_plc_wz,apple,3'
                    if(kk%12 == 2):
                        msg = 'tx_plc_wz,banana,1'
                    if(kk%12 == 3):
                        msg = 'tx_plc_wz,banana,2'
                    if(kk%12 == 10):
                        msg = 'tx_plc_wz,banana,3'
                    if(kk%12 == 4):
                        msg = 'tx_plc_wz,mango,1'
                    if(kk%12 == 5):
                        msg = 'tx_plc_wz,mango,2'
                    if(kk%12 == 9):
                        msg = 'tx_plc_wz,mango,3'
                    if(kk%12 == 6):
                        msg = 'tx_plc_wz,strawberry,1'
                    if(kk%12 == 7):
                        msg = 'tx_plc_wz,strawberry,2'
                    if(kk%12 == 8):
                        msg = 'tx_plc_wz,strawberry,3'
                    """
                    print("it is:",msg)
                    configdjj.tx_show_change = 1
                    if 'huangse' in data:
                        configdjj.tx_qxhc_show_change = 1
                        configdjj.shifouchengshu = "成熟"
                    if 'hongse' in data:
                        configdjj.tx_qxhc_show_change = 1
                        configdjj.shifouchengshu = "成熟"
                        
                    if 'lvse' in data:
                        configdjj.tx_czhc_show_change = 1
                        configdjj.shifouchengshu = "不成熟"
                    if 'apple' in msg:
                        configdjj.tx_local = 1
                        configdjj.fruit_name = "苹果"
                        configdjj.fangzhiweizhi = 1
                    if 'banana' in msg:
                        configdjj.tx_local = 2
                        configdjj.fruit_name = "香蕉"
                        configdjj.fangzhiweizhi = 2
                    if 'mango' in msg:
                        configdjj.tx_local = 3
                        configdjj.fruit_name = "芒果"
                        configdjj.fangzhiweizhi = 3
                    if 'strawberry' in msg:
                        configdjj.tx_local = 4
                        configdjj.fruit_name = "草莓"
                        configdjj.fangzhiweizhi = 4
                    if '1' in msg:
                        configdjj.shuiguo_num = 1
                    if '2' in msg:
                        configdjj.shuiguo_num = 2
                    if '3' in msg:
                        configdjj.shuiguo_num = 3
                    
                    
                    configdjj.socket_client.send(msg.encode())
                    
                    print("tx msg:",msg)
                else:
                    msg = "tx_plc_kb"
                    configdjj.socket_client.send(msg.encode())
                    print("tx_plc_wz_______ng")