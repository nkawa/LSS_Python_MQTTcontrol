
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

    def on_connect(self,client, userdata, flag, rc):
        print("Connected with result code " + str(rc))  # 接続できた旨表示

# ブローカーが切断したときの処理
    def on_disconnect(self,client, userdata, rc):
        if  rc != 0:
            print("Unexpected disconnection.")

    def connect_mqtt(self):
        self.client = mqtt.Client()  
# MQTTの接続設定
        self.client.on_connect = self.on_connect         # 接続時のコールバック関数を登録
        self.client.on_disconnect = self.on_disconnect   # 切断時のコールバックを登録
        self.client.connect("192.168.207.22", 1883, 60)
        self.client.loop_start()   # 通信処理開始
#        self.client.loop_forever()   # 通信処理開始

mq = LSS_MQTT()
mq.connect_mqtt()

while True:
    real_joints = []
    for i in range(1,6):
        real_joints.append(int(lss.LSS(i).getPosition()))
    real_joints[0] = -real_joints[0]
    real_joints[2] = real_joints[2]+900 
    real_joints[4] = -real_joints[4]
    real_rot = [x/10 for x in real_joints]
    print("Rot:",real_rot)

    mq.client.publish("lss4dof/real",json.dumps({"rotate":real_rot}))
