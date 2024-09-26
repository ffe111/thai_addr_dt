FROM python:3.11-slim

RUN apt-get update && apt-get install -y wget unzip && pip install gdown

EXPOSE 8080
ENV PORT 8080

WORKDIR /app

COPY requirements.txt requirements.txt

# RUN pip install torch==2.4.1 -f https://download.pytorch.org/whl/cpu

RUN pip install -r requirements.txt

COPY . .

# สร้างโฟลเดอร์ /app/thaiAddressTag/models ถ้ายังไม่มี
# WORKDIR /app/thaiAddressTag

# ใช้ gdown เพื่อดาวน์โหลดไฟล์จาก Google Drive
# RUN gdown https://drive.google.com/uc?id=14ADJrypJasKrIxc8KbwBaVwui7S4we0Z -O model_ner.zip && \
#     unzip model_ner.zip -d models && \
#     rm model_ner.zip

# WORKDIR /app/

CMD python main.py