from datetime import datetime
import paho.mqtt.client as mqtt

# Cau hinh broker
BROKER = "localhost"
PORT = 1883
TOPIC = "iot/lab/message"

# Tao Client
try:
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="Subscriber_Bai1")
except AttributeError:
    client = mqtt.Client(client_id="Subscriber_Bai1")

def on_connect(client, userdata, flags, rc, *args, **kwargs):
    if rc == 0:
        print(f"[*] Ket noi thanh cong toi Broker: {BROKER}:{PORT}")
        print(f"[*] Dang lang nghe tren topic: '{TOPIC}'...")
        print("[*] Nhan Ctrl+C de dung chuong trinh.\n" + "="*40)
        client.subscribe(TOPIC, qos=1)
    else:
        print(f"[!] Ket noi that bai, ma loi: {rc}")

def on_message(client, userdata, msg):
    current_time = datetime.now().strftime("%H:%M:%S")
    payload_str = msg.payload.decode("utf-8")
    
    print("\nNhan duoc message:")
    print(f"Topic  : {msg.topic}")
    print(f"Payload: {payload_str}")
    print(f"Time   : {current_time}")
    print("-" * 40)

client.on_connect = on_connect
client.on_message = on_message

print("Dang ket noi toi MQTT Broker...")
client.connect(BROKER, PORT, keepalive=60)

try:
    # Lang nghe lien tuc
    client.loop_forever()
except KeyboardInterrupt:
    print("\n[*] Nguoi dung da dung chuong trinh.")
    client.disconnect()
    print("[*] Da ngat ket noi.")
