# BÁO CÁO THỰC HÀNH BUỔI 1: LẬP TRÌNH PYTHON VỚI GIAO THỨC MQTT

---

## 1. Cấu trúc thư mục dự án

```text
TH_IoT_Buoi1/
│
├── B1/
│   ├── publisher_bai1.py          # Publisher: Gửi thông điệp chứa Họ tên & MSV lên Broker
│   └── subscriber_bai1.py         # Subscriber: Lắng nghe topic và in thông điệp kèm timestamp
│
├── B2/
│   ├── sensor_publisher_bai2.py   # Publisher: Mô phỏng cảm biến, gửi JSON định kỳ 3 giây
│   └── monitor_subscriber_bai2.py # Subscriber: Nhận & parse JSON, cảnh báo vượt ngưỡng
│
├── B3/
│   ├── device_bai3.py             # Thiết bị đèn: nhận lệnh ON/OFF, phản hồi trạng thái JSON
│   └── controller_bai3.py         # Bộ điều khiển: nhận input từ bàn phím, gửi lệnh & xem phản hồi
│
├── README.md                      # Báo cáo tổng hợp toàn bộ bài thực hành (Markdown)
└── README.txt                     # Hướng dẫn tóm tắt tổng hợp (Plain Text)
```

---

## 2. Môi trường & Cấu hình MQTT Broker

### 2.1 Yêu cầu hệ thống
- **Ngôn ngữ:** Python 3.8 trở lên
- **Thư viện MQTT:** `paho-mqtt`

```bash
pip install paho-mqtt
```

### 2.2 Cấu hình Broker
| Thuộc tính | Giá trị |
|:---|:---|
| **Loại Broker** | Eclipse Mosquitto (local) hoặc Public Broker (`broker.emqx.io`, `broker.hivemq.com`) |
| **Host / IP** | `localhost` |
| **Port** | `1883` |
| **Giao thức** | MQTT over TCP (không mã hóa TLS) |

> **Lưu ý:** Cần khởi động Mosquitto Broker trước khi chạy bất kỳ script nào.
> ```bash
> # Khởi động Mosquitto trên Windows
> mosquitto -v
> ```

### 2.3 Công cụ hỗ trợ kiểm thử
- **MQTT Explorer** – Giao diện đồ họa giám sát topic/payload trực quan.
- **mosquitto_sub / mosquitto_pub** – Lệnh CLI để test nhanh.

---

## 3. Tổng quan các bài thực hành & MQTT Topic

| Bài | Mô hình MQTT | Mô tả ngắn | Topic(s) |
|:---:|:---:|:---|:---|
| **B1** | 1-Way (Pub → Sub) | Gửi & nhận thông điệp văn bản đơn giản | `iot/lab/message` |
| **B2** | 1-Way Periodic | Cảm biến gửi JSON định kỳ, Monitor cảnh báo ngưỡng | `iot/lab/sensor01/data` |
| **B3** | 2-Way (Pub/Sub ↔ Sub/Pub) | Điều khiển đèn thông minh, phản hồi tức thì | `iot/lab/light01/cmd` & `iot/lab/light01/status` |

---

## 4. Chi tiết từng bài thực hành

---

### 🔹 BÀI 1: Ứng dụng gửi và nhận thông điệp MQTT cơ bản

#### 4.1.1 Mô tả & Mục tiêu

Bài 1 triển khai mô hình Publish/Subscribe đơn giản nhất với 2 ứng dụng Python hoạt động độc lập:

- **Publisher (`publisher_bai1.py`):**
  - Kết nối tới MQTT Broker.
  - Đóng gói thông tin cá nhân (Họ tên, Mã sinh viên) cùng lời chào thành payload dạng chuỗi ký tự.
  - Publish payload lên topic `iot/lab/message` **một lần duy nhất**, sau đó ngắt kết nối.

- **Subscriber (`subscriber_bai1.py`):**
  - Kết nối tới MQTT Broker và đăng ký (subscribe) topic `iot/lab/message`.
  - Lắng nghe **liên tục** (vòng lặp sự kiện MQTT).
  - Mỗi khi nhận được message, in ra payload cùng **thời điểm nhận thực tế** (định dạng `HH:MM:SS`).

#### 4.1.2 Topic & Payload

- **Topic:** `iot/lab/message`
- **Payload (Plain Text):** `Xin chao tu client Python MQTT - <MSV> - <Ho ten>`

#### 4.1.3 Cách chạy

Mở **2 cửa sổ Terminal** (chạy theo thứ tự):

```bash
# Terminal 1 – Khởi động Subscriber trước (lắng nghe sẵn)
python B1/subscriber_bai1.py

# Terminal 2 – Gửi thông điệp
python B1/publisher_bai1.py
```

#### 4.1.4 Kết quả thực thi thực tế

**Terminal Publisher:**
```text
Dang ket noi toi MQTT Broker...
[*] Ket noi thanh cong toi Broker: localhost:1883

--- DANG GUI MESSAGE ---
Topic  : iot/lab/message
Payload: Xin chao tu client Python MQTT - B23DCCN393 - Nguyen Dinh Quang Huy
[+] Da gui message thanh cong!
[*] Da ngat ket noi.
```

**Terminal Subscriber:**
```text
Dang ket noi toi MQTT Broker...
[*] Ket noi thanh cong toi Broker: localhost:1883
[*] Dang lang nghe tren topic: 'iot/lab/message'...
[*] Nhan Ctrl+C de dung chuong trinh.
========================================

Nhan duoc message:
Topic  : iot/lab/message
Payload: Xin chao tu client Python MQTT - B23DCCN393 - Nguyen Dinh Quang Huy
Time   : 10:15:20
----------------------------------------
```

---

### 🔹 BÀI 2: Mô phỏng hệ thống giám sát cảm biến môi trường

#### 4.2.1 Mô tả & Mục tiêu

Bài 2 mô phỏng một hệ thống IoT thu thập và giám sát dữ liệu môi trường thời gian thực:

- **Sensor Publisher (`sensor_publisher_bai2.py`):**
  - Mô phỏng thiết bị cảm biến thực địa.
  - Sinh ngẫu nhiên giá trị **nhiệt độ** (20°C – 40°C) và **độ ẩm** (30% – 90%).
  - Đóng gói dữ liệu thành chuỗi **JSON** có cấu trúc rõ ràng.
  - Tự động publish lên Broker **mỗi 3 giây** (vòng lặp liên tục cho đến khi nhấn Ctrl+C).

- **Monitoring Subscriber (`monitor_subscriber_bai2.py`):**
  - Subscribe topic dữ liệu cảm biến.
  - Parse chuỗi JSON nhận được, trích xuất các trường giá trị.
  - In bảng thông số rõ ràng và **tự động cảnh báo** khi:
    - Nhiệt độ vượt ngưỡng: **T > 35°C** → `>>> CANH BAO: Nhiet do cao <<<`
    - Độ ẩm dưới ngưỡng:   **H < 40%**  → `>>> CANH BAO: Do am thap  <<<`

#### 4.2.2 Topic & Định dạng Payload (JSON)

- **Topic:** `iot/lab/sensor01/data`
- **Payload mẫu:**
  ```json
  {
    "device_id": "sensor01",
    "temperature": 36.8,
    "humidity": 37.4
  }
  ```

#### 4.2.3 Cách chạy

```bash
# Terminal 1 – Khởi động Monitor (lắng nghe sẵn)
python B2/monitor_subscriber_bai2.py

# Terminal 2 – Khởi động Sensor Publisher
python B2/sensor_publisher_bai2.py
```

#### 4.2.4 Kết quả thực thi thực tế

**Terminal Sensor Publisher:**
```text
Dang ket noi toi MQTT Broker...
[*] Ket noi thanh cong toi Broker: localhost:1883
[*] Bat dau gui du lieu cam bien dinh ky moi 3s len topic 'iot/lab/sensor01/data'...
[*] Nhan Ctrl+C de dung chuong trinh.
========================================
[1] Gui du lieu: {"device_id": "sensor01", "temperature": 28.5, "humidity": 65.2}
[2] Gui du lieu: {"device_id": "sensor01", "temperature": 36.8, "humidity": 37.4}
```

**Terminal Monitoring Subscriber:**
```text
-----------------------------------
Device     : sensor01
Temperature: 28.5 C
Humidity   : 65.2 %
-----------------------------------

-----------------------------------
Device     : sensor01
Temperature: 36.8 C
Humidity   : 37.4 %
>>> CANH BAO: Nhiet do cao <<<
>>> CANH BAO: Do am thap   <<<
-----------------------------------
```

---

### 🔹 BÀI 3: Mô phỏng hệ thống điều khiển đèn thông minh (Giao tiếp 2 chiều)

#### 4.3.1 Mô tả & Mục tiêu

Bài 3 triển khai mô hình **giao tiếp 2 chiều** (bidirectional) giữa thiết bị IoT và bộ điều khiển thông qua MQTT Broker, mô phỏng kịch bản điều khiển thiết bị thực tế từ xa:

- **Thiết bị đèn (`device_bai3.py`):**
  - Subscribe topic nhận lệnh `iot/lab/light01/cmd`.
  - Khi nhận lệnh `ON` hoặc `OFF`:
    - Cập nhật trạng thái nội bộ của đèn.
    - Publish ngay trạng thái mới dưới dạng JSON về topic `iot/lab/light01/status`.
  - Bỏ qua các lệnh không hợp lệ (không phải `ON`/`OFF`).

- **Bộ điều khiển (`controller_bai3.py`):**
  - Subscribe topic `iot/lab/light01/status` để nhận phản hồi từ thiết bị.
  - Đồng thời cho phép người dùng nhập lệnh từ bàn phím (`ON`, `OFF`, `EXIT`).
  - Publish lệnh lên topic `iot/lab/light01/cmd` và hiển thị trạng thái phản hồi tức thì.

#### 4.3.2 Topics & Payload

| Chiều | Topic | Nội dung |
|:---:|:---|:---|
| Controller → Device | `iot/lab/light01/cmd` | Chuỗi lệnh: `ON` hoặc `OFF` |
| Device → Controller | `iot/lab/light01/status` | JSON: `{"device_id": "light01", "status": "ON"}` |

#### 4.3.3 Cách chạy

```bash
# Terminal 1 – Khởi động thiết bị đèn (chạy trước)
python B3/device_bai3.py

# Terminal 2 – Giao diện điều khiển (nhập lệnh ON / OFF / EXIT)
python B3/controller_bai3.py
```

#### 4.3.4 Kết quả thực thi thực tế

**Terminal Controller:**
```text
--- HE THONG DIEU KHIEN DEN THONG MINH ---
Cac lenh hop le: ON, OFF, EXIT

Nhap lenh: ON
[>] Da gui lenh ON toi light01
[<] Trang thai nhan duoc tu [iot/lab/light01/status]:
    {"device_id": "light01", "status": "ON"}
-----------------------------------

Nhap lenh: OFF
[>] Da gui lenh OFF toi light01
[<] Trang thai nhan duoc tu [iot/lab/light01/status]:
    {"device_id": "light01", "status": "OFF"}
-----------------------------------

Nhap lenh: EXIT
[*] Dang thoat chuong trinh...
```

**Terminal Device:**
```text
[*] Thiet bi 'light01' da ket noi toi Broker: localhost:1883
[*] Dang lang nghe lenh tren topic: 'iot/lab/light01/cmd'
=============================================
[+] Da phan hoi trang thai: {"device_id": "light01", "status": "OFF"}

[!] Nhan duoc lenh: 'ON' tu topic 'iot/lab/light01/cmd'
[*] Chuyen trang thai den thanh: [ON]
[+] Da phan hoi trang thai: {"device_id": "light01", "status": "ON"}

[!] Nhan duoc lenh: 'OFF' tu topic 'iot/lab/light01/cmd'
[*] Chuyen trang thai den thanh: [OFF]
[+] Da phan hoi trang thai: {"device_id": "light01", "status": "OFF"}
```

---

## 5. Luồng hoạt động tổng quan (System Flow)

```
[Bài 1]
publisher_bai1 ──(plain text payload)──► MQTT Broker ──► subscriber_bai1
                                                          └─ In payload + timestamp

[Bài 2]
sensor_publisher ──(JSON, mỗi 3s)──► MQTT Broker ──► monitor_subscriber
                                                       ├─ Parse JSON
                                                       ├─ In thông số
                                                       └─ Cảnh báo nếu vượt ngưỡng

[Bài 3]
controller ──(lệnh: ON/OFF)──► MQTT Broker ──► device
                                                ├─ Cập nhật trạng thái
                                                └─ Publish JSON status
controller ◄──(JSON: status)────────────────── MQTT Broker ◄── device
```

---

## 6. Tổng kết & Đánh giá

| Tiêu chí | Bài 1 | Bài 2 | Bài 3 |
| :--- | :--- | :--- | :--- |
| **Mô hình MQTT** | 1-Way (Pub → Sub) | 1-Way Periodic (Pub → Sub) | 2-Way (Pub/Sub ↔ Sub/Pub) |
| **Định dạng dữ liệu** | Chuỗi ký tự (Plain Text) | JSON (`device_id`, `temperature`, `humidity`) | Lệnh Text (`ON`/`OFF`) & JSON trạng thái |
| **Tần suất / Kích hoạt** | Gửi 1 lần khi kích hoạt | Tự động lặp mỗi 3 giây | Theo sự kiện người dùng nhập lệnh |
| **Tính năng đặc biệt** | Hiển thị thời gian nhận thực tế | Cảnh báo ngưỡng nhiệt độ & độ ẩm | Điều khiển 2 chiều, kiểm tra lệnh hợp lệ |
| **Kết quả kiểm thử** | ✅ Đạt 100% yêu cầu | ✅ Đạt 100% yêu cầu | ✅ Đạt 100% yêu cầu |
