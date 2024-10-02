import re
from pythainlp.util import normalize


def preprocess(text: str) -> str:
    """
    Generalized function to preprocess an input
    """
    text = normalize(text).strip()
    text = text.replace("ส่ง ", "")
    text = text.replace("จัดส่ง", "")
    text = text.replace("ชือ.", "")
    text = text.replace("ชื่อ ", "")
    text = text.replace("ผู้รับ", "")
    text = text.replace("ส่งที่ ", " ")
    text = text.replace("ที่อยู่ ", " ")
    text = text.replace("ที้อยุ่ ", " ")
    text = text.replace("ที่อยู่จ้า ", " ")
    text = text.replace("ส่งของที่ ", " ")
    text = text.replace("ส่งมาที่", " ")
    text = text.replace("โทรศัพท์", " ")
    text = text.replace("โทร.", " ")
    text = text.replace("โทร", " ")
    text = text.replace("ติดต่อ", " ")
    text = text.replace("\n-", " ")
    text = text.replace("\n", " ")
    text = text.replace(": ", " ")
    text = text.replace(":", "")
    text = text.replace("-", "")
    text = text.replace("(", "")
    text = text.replace(")", "")
    text = text.replace('"', "")
    text = text.replace(',', "")

    # text = remove_emoji(text)
    text = " ".join([t for t in text.strip().split(" ") if t.strip() != ""])
    print(text)
    return text


def clean_location_text(text: str) -> str:
    """
    Clean location before using fuzzy string match
    """
    # text = text.replace("หมู่บ้าน", " ")
    # text = text.replace("ซอย", " ")
    text = text.replace("แขวง", " ")
    text = text.replace("เขต", " ")
    text = text.replace("จังหวัด", " ")
    text = text.replace("อำเภอ", " ")
    text = text.replace("ตำบล", " ")
    # text = text.replace("ถ.", " ")
    # text = text.replace("ซ.", " ")
    text = text.replace("ตฺ", "ต.")
    text = text.replace("ต.", " ")
    text = text.replace("อ.", " ")
    text = text.replace("จ.", " ")
    text = text.replace("คอหงส์", "คอหงษ์")
    text = text.replace("กทม.", "กรุงเทพมหานคร")
    text = text.replace("กทม", "กรุงเทพมหานคร")
    text = text.replace("กรุงเทพฯ", "กรุงเทพมหานคร")
    text = text.replace("กรุงเทพมหานคร", "กรุงเทพมหานคร")
    text = text.replace("รหัสไปรษณีย์", "")
    # text = text.replace(".", "")
    return text


def extract_phone_(text: str) -> (str, list):
    """
    Extracts phone number from the text and standardizes it.
    1. Replace country code like +XX with 0.
    2. Remove dash (-) and spaces within phone numbers only.
    3. Remove the phone number from the text.
    Returns the cleaned text and a list of extracted phone numbers.
    """
    # Remove parentheses around phone numbers
    text = text.replace('(', '').replace(')', '').replace('-', ' ')

    # Replace country code like +XX with 0
    text = re.sub(r'\+\d{2}', '0', text)

    # List to store extracted phone numbers
    phone_numbers = []

    # Function to clean and store phone numbers
    def clean_phone(match):
        phone_number = match.group(0)
        # Remove dash (-) and spaces within the phone number
        phone_number = re.sub(r'[\s-]', '', phone_number)
        phone_numbers.append(phone_number)
        return ''  # Remove the phone number from the text

    # Improved regex to capture different phone number formats
    cleaned_text = re.sub(r'\b(0[\d\s-]{7,12})\b', clean_phone, text)

    return cleaned_text, phone_numbers
