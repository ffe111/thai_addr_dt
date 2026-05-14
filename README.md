# Thai Address Tagging API 🇹🇭

A robust REST API for detecting and extracting structured Thai address information from unstructured text. This project uses Natural Language Processing (NLP) to identify names, phone numbers, and geographical entities like provinces, districts, and zip codes.

## 🚀 Features

- **Entity Extraction**: Automatically extracts Name, Phone, Province, District (Amphoe), Sub-district (Tambon), and Zipcode.
- **NLP Powered**: Built with `simpletransformers` and `pythainlp` for high accuracy.
- **Fast & Reliable**: Powered by FastAPI with asynchronous support.
- **Containerized**: Fully Dockerized for easy deployment.
- **Interactive API Docs**: Built-in Swagger UI and Redoc.

## 🛠 Tech Stack

- **Framework**: FastAPI (Python 3.9+)
- **NLP Libraries**: SimpleTransformers (BERT-based), PyThaiNLP
- **Server**: Uvicorn
- **Container**: Docker & Docker Compose

## 📋 API Specification

### Check Address
**Endpoint**: `POST /address-check`

**Request Body**:
```json
{
  "text": "อนงค์ลักษณ์\n9/56 ม.3\nหมู่บ้านนฤมลศิริ(ซอย2)\nซ.บุญศิริ ถ.สุขุมวิท\nต.บางเมือง\nอ.เมืองสมุทรปราการ\nจ.สมุทรปนาการ\n10270\nโทร.0956029655"
}
```

**Response Body**:
```json
{
  "address": {
    "province": "สมุทรปราการ",
    "amphoe": "เมืองสมุทรปราการ",
    "district": "บางเมือง",
    "zipcode": "10270",
    "name": "อนงค์ลักษณ์",
    "phone": "0956029655"
  }
}
```

## ⚙️ Installation

### Prerequisites
- Python 3.9 or higher
- `pip` (Python package manager)

### Local Setup
1. **Clone the repository**:
   ```bash
   git clone <your-repository-url>
   cd thai-address-tag
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the environment**:
   - **Windows**: `venv\Scripts\activate`
   - **Mac/Linux**: `source venv/bin/activate`

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**:
   ```bash
   python main.py
   ```

## 🐳 Docker Deployment

### Using Docker
```bash
docker build -t address-api:v1 .
docker run -p 8000:8000 --name address-service address-api:v1
```

### Using Docker Compose
```bash
docker compose up -d
```

## 📖 Usage Guide
1. Once the server is running, navigate to `http://127.0.0.1:8000/docs` in your browser.
2. You will find the **Swagger UI** where you can test the `/address-check` endpoint interactively.
3. Click **"Try it out"**, enter your address text, and click **"Execute"**.

---
Developed by **ffe111**
