
import json
from paho.mqtt import client as mqtt
import sys
import os
from datetime import datetime

# Import LSS library
from vendor import lss 
from vendor import lss_const as lssc




CST_LSS_Port = os.environ.get("LSS_COM","COM10")				# For windows platforms
CST_LSS_Baud = lssc.LSS_DefaultBaud

# Create and open a serial port
lss.initBus(CST_LSS_Port, CST_LSS_Baud)



class LSS_MQTT:
    def __init__(self,fname):
        self.start = -1
        self.log = open(fname,"w")

    def on_connect(self,client, userdata, flag, rc):
        print("Connected with result code " + str(rc))  # 接続できた旨表示
        self.client.subscribe("lss4dof/state") #　connected -> subscribe

# ブローカーが切断したときの処理
    def on_disconnect(self,client, userdata, rc):
        if  rc != 0:
            print("Unexpected disconnection.")

    def on_message(self,client, userdata, msg):
#        print("Message",msg.payload)
        js = json.loads(msg.payload)
        if js['abutton']== True:
             self.start = 0
        if self.start < 0:
             return
        self.start +=1
        # 一定時間動作したら、abutton で停止
        if self.start > 100 and js['abutton']==True:
            self.client.disconnect()
            self.log.close()
            return
#        print("rot:",js)
        rot = [int(float(x)*10)  for x in js['rotate']]        
#        print("rot:",rot)

        # 生で送っちゃだめ！
        # まず、現在の値を所得
        real_joints = []
        for i in range(1,6):
            real_joints.append(lss.LSS(i).getPosition())

        set_joints = real_joints.copy()
        set_joints[0] = -set_joints[0]
        set_joints[2] = set_joints[2]+900 
        set_joints[5] = -set_joints[5]
        real_rot = [x/10 for x in set_joints]
        
        self.client.publish("lss4dof/real",json.dumps({"rotate":real_rot}))
        
        if abs(real_joints[0]+rot[0])>10:
                lss.LSS(1).move(-rot[0])
        if abs(real_joints[1]-rot[1])>10:
                lss.LSS(2).move(rot[1])
        if abs(real_joints[2]-rot[2]+900)>10:
                lss.LSS(3).move(rot[2]-900)
        if abs(real_joints[3]-rot[3])>10:
                lss.LSS(4).move(rot[3])
        if abs(real_joints[4]+rot[4])>10:
                lss.LSS(5).move(-rot[4])
# 時刻
        ctime = datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f")
        self.log.write(json.dumps({"time":ctime, "recv":rot, "real":real_rot})+"\n")
#        lss.LSS(1).move(-rot[0]);
#        lss.LSS(2).move(rot[1]);
#        lss.LSS(3).move(rot[2]-900);
#        lss.LSS(4).move(rot[3]);
#        lss.LSS(5).move(-rot[4]);
        

    def connect_mqtt(self):
        self.client = mqtt.Client()  
# MQTTの接続設定
        self.client.on_connect = self.on_connect         # 接続時のコールバック関数を登録
        self.client.on_disconnect = self.on_disconnect   # 切断時のコールバックを登録
        self.client.on_message = self.on_message         # メッセージ到着時のコールバック
        self.client.connect("192.168.207.22", 1883, 60)
#  client.loop_start()   # 通信処理開始
        self.client.loop_forever()   # 通信処理開始



fname = sys.argv[1]
if fname == "":
    fname = "lss4dof.log"
mq = LSS_MQTT(fname)

mq.connect_mqtt()


