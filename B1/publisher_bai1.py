import time
# pyrefly: ignore [missing-import] // Khi chạy bỏ dòng này
import paho.mqtt.client as mqtt

# Cau hinh Broker
BROKER = "localhost"   # Su dung Local Mosquitto Broker tren may
PORT = 1883
TOPIC = "iot/lab/message"

# Message
STUDENT_NAME = "Nguyen Dinh Quang Huy"
STUDENT_ID = "B23DCCN393"
GREETING = "Xin chao tu client Python MQTT"

# Tao Client
try:
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="Publisher_Bai1")
except AttributeError:
    client = mqtt.Client(client_id="Publisher_Bai1")

def on_connect(client, userdata, flags, rc, *args, **kwargs):
    if rc == 0:
        print(f"[*] Ket noi thanh cong toi Broker: {BROKER}:{PORT}")
    else:
        print(f"[!] Ket noi that bai, ma loi (RC): {rc}")

client.on_connect = on_connect

print("Dang ket noi toi MQTT Broker...")
client.connect(BROKER, PORT, keepalive=60)
client.loop_start()  # Chay loop o background

time.sleep(1) # Cho ket noi on dinh

# Noi dung thong diep
payload = f"{GREETING} - {STUDENT_ID} - {STUDENT_NAME}"

print(f"\n--- DANG GUI MESSAGE ---")
print(f"Topic  : {TOPIC}")
print(f"Payload: {payload}")

# Publish thong diep len topic
result = client.publish(TOPIC, payload, qos=1)
result.wait_for_publish()

if result.is_published():
    print("[+] Da gui message thanh cong!")
else:
    print("[-] Gui message that bai.")

time.sleep(1)
client.loop_stop()
client.disconnect()
print("[*] Da ngat ket noi.")
