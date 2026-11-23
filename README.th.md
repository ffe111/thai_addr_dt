# Thai Address Tagging API

[English](README.md) | ภาษาไทย

สกัดองค์ประกอบของที่อยู่ภาษาไทยด้วยโมเดล Transformer สำหรับระบุเอนทิตี (NER) แล้วจับคู่จังหวัด อำเภอ ตำบล และรหัสไปรษณีย์กับข้อมูลอ้างอิง บริการ FastAPI ยังพยายามสกัดชื่อ องค์กร และเบอร์โทรศัพท์เมื่อพบในข้อความ

## เริ่มต้นใช้งาน

สร้างและรันคอนเทนเนอร์จากไดเรกทอรีหลักของ repo:

```bash
docker build -t thai-address-tagging .
docker run --rm -p 127.0.0.1:8080:8080 thai-address-tagging
```

หากพัฒนาบนเครื่อง ให้ใช้ Python 3.11 (ตาม [Dockerfile](Dockerfile)) ติดตั้ง [`requirements.txt`](requirements.txt) ใน virtual environment แล้วรัน `python main.py` บริการโหลดโมเดล [`F311/addrthner`](https://huggingface.co/F311/addrthner) ด้วย CPU ตอนเริ่มทำงาน หากยังไม่มีโมเดลในแคชจะต้องเชื่อมต่ออินเทอร์เน็ต ไฟล์ Compose ใน repo ผูกพอร์ต 8000 แต่แอปฟังที่ **8080** จึงควรใช้คำสั่ง Docker ด้านบนหากยังไม่ได้ปรับการแมปพอร์ต

## ทดลองเรียก API

เปิด [Swagger UI](http://localhost:8080/docs) แล้วเรียก `POST /addr-detect/address-check` ด้วยข้อความตัวอย่างที่สร้างขึ้น:

```json
{"text":"ต.สุเทพ อ.เมืองเชียงใหม่ จ.เชียงใหม่ 50200"}
```

ผลลัพธ์มี `text` ที่ส่งเข้ามาและออบเจ็กต์ `address` ฟิลด์อาจไม่ครบหากโมเดลหรือข้อมูลอ้างอิงระบุไม่ได้ ต้นแบบนี้อาจพิมพ์ข้อมูลที่สกัดได้ออกทาง stdout จึงไม่ควรใช้ข้อมูลส่วนบุคคลจริงในเดโม ล็อกที่แชร์ หรือรายงานปัญหา

เริ่มอ่านจาก [จุดรับคำขอ API](main.py) และ [ขั้นตอนสกัดและจับคู่ข้อมูล](thaiAddressTag/tag.py) หรือเปรียบเทียบกับ [API แบบพจนานุกรม](https://github.com/ffe111/address_detection_api)
