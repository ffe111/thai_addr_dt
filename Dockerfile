# FROM python:3.11-slim

# RUN apt-get update && apt-get install -y wget unzip && pip install gdown

# EXPOSE 8080
# ENV PORT 8080

# WORKDIR /app

# COPY requirements.txt requirements.txt


# RUN pip install -r requirements.txt

# # torch==2.0.1 image size has 3GB++
# RUN pip install torch==2.0.1+cpu -f https://download.pytorch.org/whl/torch_stable.html

# # fix torch==2.0.1+cpu error numpy version 
# RUN pip install --upgrade pip && pip install "numpy<2"

# # torch==2.4.1 image size has 10GB++
# # RUN pip install torch==2.4.1 -f https://download.pytorch.org/whl/cpu

# # torch==2.4.1+cpu image size has 6GB++
# # RUN pip3 --no-cache-dir install torch \
# #         --index-url https://download.pytorch.org/whl/cu118

# COPY . .

# # สร้างโฟลเดอร์ /app/thaiAddressTag/models ถ้ายังไม่มี
# # WORKDIR /app/thaiAddressTag

# # ใช้ gdown เพื่อดาวน์โหลดไฟล์จาก Google Drive
# # RUN gdown https://drive.google.com/uc?id=14ADJrypJasKrIxc8KbwBaVwui7S4we0Z -O model_ner.zip && \
# #     unzip model_ner.zip -d models && \
# #     rm model_ner.zip

# # WORKDIR /app/

# CMD python main.py

FROM python:3.11-slim

EXPOSE 8080
ENV PORT 8080

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

# RUN pip install .

WORKDIR /app

CMD python main.py