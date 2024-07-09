# Address Detection API

## Detail

Detect Address from Text
program find province, amphoe, district, zipcode, name, phone

**Request**

```
 {
   "text": "อนงค์ลักษณ์\n9/56 ม.3\nหมู่บ้านนฤมลศิริ(ซอย2)\nซ.บุญศิริ ถ.สุขุมวิท\nต.บางเมือง\nอ.เมืองสมุทรปราการ\nจ.สมุทรปนาการ\n10270\nโทร.0956029655"
 }
```

**Response**

```
 {
   "address": {
     "province": "สมุทรปราการ",
     "amphoe": "เมืองสมุทรปราการ",
     "district": "บางเมือง",
     "zipcode": "10270",
     "name": "",
     "phone": "0956029655"
   }
 }
```

## Install

1.  create virtual environment for this project
    ```
      python -m venv venv
    ```
2.  activate virtual environment
    ```
      venv\Script\activate  # for window
      source venv\Bin\activate     # for mac or linux
    ```
3.  install useful package for this project
    ```
      pip install -r requirments.txt
    ```
4.  run this program python main.py

## Build Docker

```
docker build -t address-api:v1 .
docker run -p 8000:8000 --name address-service address-api:v1
```

or

```
docker compose up
```

## How to use

1.  before run program
2.  go to 127.0.0.1:8000/docs
3.  POST box /address-check
    sent Request body format
    { "text": "Enter address text" }
4.  Execute btn
