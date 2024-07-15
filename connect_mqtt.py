
import json
from paho.mqtt import client as mqtt


# Import LSS library
from vendor import lss 
from vendor import lss_const as lssc

CST_LSS_Port = "COM10"				# For windows platforms
CST_LSS_Baud = lssc.LSS_DefaultBaud

# Create and open a serial port
lss.initBus(CST_LSS_Port, CST_LSS_Baud)



class LSS_MQTT:
    def on_connect(self,client, userdata, flag, rc):
        print("Connected with result code " + str(rc))  # 接続できた旨表示
        self.client.subscribe("kinova/state") #　connected -> subscribe

# ブローカーが切断したときの処理
    def on_disconnect(self,client, userdata, rc):
        if  rc != 0:
            print("Unexpected disconnection.")

    def on_message(self,client, userdata, msg):
#        print("Message",msg.payload)
        js = json.loads(msg.payload)
#        print("rot:",js)
        
        print("rot:",js['rotate'])
        rot = js['rotate']
        j1 = int(float(rot['j1'])*10)
        j2 = int(float(rot['j2'])*10)
        j3 = int(float(rot['j3'])*10)
        j4 = int(float(rot['j4'])*10)
        j5 = int(float(rot['j5'])*10)

        lss.LSS(1).move(0);
        lss.LSS(2).move(j2);
        lss.LSS(3).move(-900+j3);
        lss.LSS(4).move(0+j5);
        

    def connect_mqtt(self):
        self.client = mqtt.Client()  
# MQTTの接続設定
        self.client.on_connect = self.on_connect         # 接続時のコールバック関数を登録
        self.client.on_disconnect = self.on_disconnect   # 切断時のコールバックを登録
        self.client.on_message = self.on_message         # メッセージ到着時のコールバック
        self.client.connect("192.168.207.22", 1883, 60)
#  client.loop_start()   # 通信処理開始
        self.client.loop_forever()   # 通信処理開始




mq = LSS_MQTT()

mq.connect_mqtt()

