========================================================================
BÁO CÁO THỰC HÀNH BUỔI 1: LẬP TRÌNH PYTHON VỚI GIAO THỨC MQTT
========================================================================

1. CẤU TRÚC DỰ ÁN:
TH_IoT_Buoi1/
├── B1/
│   ├── publisher_bai1.py          # Publisher: Gửi thông điệp chứa Họ tên, MSV lên Broker
│   └── subscriber_bai1.py         # Subscriber: Lắng nghe và in thông điệp kèm thời gian nhận
├── B2/
│   ├── sensor_publisher_bai2.py   # Publisher: Mô phỏng cảm biến, gửi JSON định kỳ mỗi 3 giây
│   └── monitor_subscriber_bai2.py # Subscriber: Nhận dữ liệu, parse JSON, cảnh báo ngưỡng
├── B3/
│   ├── device_bai3.py             # Thiết bị đèn: Nhận lệnh ON/OFF và phản hồi trạng thái JSON
│   └── controller_bai3.py         # Bộ điều khiển: Người dùng nhập lệnh và theo dõi trạng thái
├── README.md                      # Báo cáo tổng hợp chi tiết (Markdown)
└── README.txt                     # Hướng dẫn tóm tắt tổng hợp (Plain Text)

------------------------------------------------------------------------

2. MÔI TRƯỜNG & CÔNG CỤ SỬ DỤNG:
- Ngôn ngữ:      Python 3.8 trở lên
- Thư viện MQTT: paho-mqtt
  Cài đặt bằng lệnh: pip install paho-mqtt
- MQTT Broker:   Eclipse Mosquitto (cài cục bộ) hoặc Public Broker
  + Host / IP  : localhost         (nếu dùng Mosquitto local)
  + Cổng (Port): 1883
  + Giao thức  : MQTT over TCP (không mã hóa TLS)
- Công cụ test:  MQTT Explorer, mosquitto_sub / mosquitto_pub (CLI)

------------------------------------------------------------------------

3. TỔNG QUAN CÁC BÀI THỰC HÀNH & MQTT TOPIC:

┌─────────┬─────────────────────────────────────────┬───────────────────────────────────────┐
│  Bài    │           Mô tả chức năng                │          MQTT Topic                   │
├─────────┼─────────────────────────────────────────┼───────────────────────────────────────┤
│  B1     │ Gửi / nhận thông điệp văn bản đơn giản  │ iot/lab/message                       │
│  B2     │ Mô phỏng cảm biến + giám sát ngưỡng     │ iot/lab/sensor01/data                 │
│  B3     │ Điều khiển đèn thông minh 2 chiều        │ iot/lab/light01/cmd  (lệnh điều khiển)│
│         │                                           │ iot/lab/light01/status (phản hồi)    │
└─────────┴─────────────────────────────────────────┴───────────────────────────────────────┘

------------------------------------------------------------------------

4. CHI TIẾT TỪNG BÀI & CÁCH CHẠY:
   (Yêu cầu: Mosquitto Broker phải đang chạy trước khi thực thi)
   (Mở 2 cửa sổ Terminal độc lập cho mỗi bài)

══════════════════════════════════════════
BÀI 1: Gửi & Nhận thông điệp MQTT cơ bản
══════════════════════════════════════════
Mục tiêu:
  - publisher_bai1.py kết nối Broker, đóng gói thông tin (Họ tên, MSV)
    thành payload và gửi 1 lần lên topic 'iot/lab/message'.
  - subscriber_bai1.py lắng nghe liên tục trên topic, nhận và in
    thông điệp ra màn hình kèm dấu thời gian thực tế.

Cách chạy:
  Terminal 1 (khởi động trước):  python B1/subscriber_bai1.py
  Terminal 2 (gửi thông điệp):   python B1/publisher_bai1.py

Kết quả mong đợi:
  [Publisher] Gửi payload "Xin chao tu client Python MQTT - <MSV> - <Ho ten>"
  [Subscriber] In ra payload nhận được kèm thời gian: "Time: HH:MM:SS"

══════════════════════════════════════════
BÀI 2: Mô phỏng cảm biến nhiệt độ & độ ẩm
══════════════════════════════════════════
Mục tiêu:
  - sensor_publisher_bai2.py sinh dữ liệu ngẫu nhiên (nhiệt độ 20–40°C,
    độ ẩm 30–90%), định dạng JSON, và tự động publish mỗi 3 giây.
  - monitor_subscriber_bai2.py nhận bản tin, parse JSON và đánh giá:
      + Cảnh báo nhiệt độ cao : T > 35°C
      + Cảnh báo độ ẩm thấp  : H < 40%

Định dạng Payload (JSON):
  {"device_id": "sensor01", "temperature": 36.8, "humidity": 37.4}

Cách chạy:
  Terminal 1 (Subscriber/Monitor): python B2/monitor_subscriber_bai2.py
  Terminal 2 (Publisher/Sensor):   python B2/sensor_publisher_bai2.py

Kết quả mong đợi:
  [Subscriber] In thông số nhận được; nếu vượt ngưỡng in thêm dòng cảnh báo:
               ">>> CANH BAO: Nhiet do cao <<<"
               ">>> CANH BAO: Do am thap  <<<"

══════════════════════════════════════════
BÀI 3: Điều khiển đèn thông minh (2 chiều)
══════════════════════════════════════════
Mục tiêu:
  - device_bai3.py đóng vai thiết bị đèn: subscribe topic nhận lệnh
    'iot/lab/light01/cmd', xử lý lệnh ON/OFF, cập nhật trạng thái nội
    bộ và publish phản hồi JSON về topic 'iot/lab/light01/status'.
  - controller_bai3.py đóng vai bộ điều khiển: nhận input từ bàn phím
    (ON / OFF / EXIT), publish lệnh và subscribe topic status để hiển
    thị phản hồi trực tiếp từ thiết bị.

Topics:
  - Lệnh điều khiển : iot/lab/light01/cmd
  - Phản hồi trạng thái: iot/lab/light01/status

Payload phản hồi (JSON):
  {"device_id": "light01", "status": "ON"}  hoặc  "status": "OFF"

Cách chạy:
  Terminal 1 (Khởi động thiết bị): python B3/device_bai3.py
  Terminal 2 (Giao diện điều khiển): python B3/controller_bai3.py
    >> Nhập lệnh tại Terminal 2: ON  /  OFF  /  EXIT

------------------------------------------------------------------------

5. LUỒNG HOẠT ĐỘNG TỔNG QUAN (FLOW):

  [Bài 1] publisher ──(plain text)──► Broker ──► subscriber (in + timestamp)

  [Bài 2] sensor_pub ──(JSON, 3s)──► Broker ──► monitor_sub (parse + cảnh báo)

  [Bài 3] controller ──(ON/OFF cmd)──► Broker ──► device
          controller ◄──(JSON status)──  Broker ◄── device

------------------------------------------------------------------------

6. KẾT QUẢ ĐẠT ĐƯỢC:
- Bài 1: Gửi và nhận thông điệp chứa Họ tên, MSV thành công trên
         topic 'iot/lab/message'. Thời gian nhận được hiển thị đúng.
- Bài 2: Publisher sinh và gửi JSON định kỳ 3s; Subscriber parse đúng
         trường dữ liệu và đưa ra cảnh báo chính xác khi T > 35°C
         hoặc H < 40%.
- Bài 3: Giao tiếp 2 chiều ổn định giữa Controller và Device;
         lệnh ON/OFF được phản hồi tức thì dưới dạng JSON trạng thái.
         Lệnh không hợp lệ được kiểm tra và bỏ qua.

========================================================================
