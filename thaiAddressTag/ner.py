# from simpletransformers.ner import NERModel
# import torch

# text = "อนงค์ลักษณ์\n9/56 ม.3\nหมู่บ้านนฤมลศิริ(ซอย2)\nซ.บุญศิริ ถ.สุขุมวิท\nต.บางเมือง\nอ.เมืองสมุทรปราการ\nจ.สมุทรปราการ\n10270\nโทร.0956029655"
# path = "models"

# model = NERModel("camembert", model_name=path,
#                  use_cuda=torch.cuda.is_available())
# predict, _ = model.predict([text])

# print(predict)


def ner_extract(predict):
    name = []
    org = []
    subdistrict = []
    district = []
    province = []
    zipcode = []
    phone = []

    current_name = None
    current_org = None
    current_subdistrict = None
    current_district = None
    current_province = None
    current_zipcode = None
    current_phone = None

    for item in predict[0]:
        for key, value in item.items():
            if value == 'B-NAME' or value == 'I-NAME':  # รองรับกรณีไม่มี B-NAME
                if value == 'B-NAME':
                    if current_name:
                        name.append(current_name)
                    current_name = key  # เริ่มต้นคำใหม่
                elif value == 'I-NAME':
                    if current_name:
                        current_name += " " + key  # เพิ่มคำต่อท้าย
                    else:
                        current_name = key  # หากไม่มี B-NAME ก่อนหน้าให้ถือว่า I-NAME เป็นการเริ่มต้น

            elif value == 'B-ORG' or value == 'I-ORG':
                if value == 'B-ORG':
                    if current_org:
                        org.append(current_org)
                    current_org = key
                elif value == 'I-ORG':
                    if current_org:
                        current_org += " " + key

            elif value == 'B-SUB' or value == 'I-SUB':
                if value == 'B-SUB':
                    if current_subdistrict:
                        subdistrict.append(current_subdistrict)
                    current_subdistrict = key
                elif value == 'I-SUB':
                    if current_subdistrict:
                        current_subdistrict += " " + key

            elif value == 'B-DIS' or value == 'I-DIS':
                if value == 'B-DIS':
                    if current_district:
                        district.append(current_district)
                    current_district = key
                elif value == 'I-DIS':
                    if current_district:
                        current_district += " " + key

            elif value == 'B-PROV' or value == 'I-PROV':
                if value == 'B-PROV':
                    if current_province:
                        province.append(current_province)
                    current_province = key
                elif value == 'I-PROV':
                    if current_province:
                        current_province += " " + key

            elif value == 'B-ZIP' or value == 'I-ZIP':
                if value == 'B-ZIP':
                    if current_zipcode:
                        zipcode.append(current_zipcode)
                    current_zipcode = key
                elif value == 'I-ZIP':
                    if current_zipcode:
                        current_zipcode += " " + key

            elif value == 'B-PHONE' or value == 'I-PHONE':
                if value == 'B-PHONE':
                    if current_phone:
                        phone.append(current_phone)
                    current_phone = key
                elif value == 'I-PHONE':
                    if current_phone:
                        current_phone += " " + key

    # เพิ่ม entity สุดท้ายลงไปใน list เมื่อจบการวนลูป
    if current_name:
        name.append(current_name)
    if current_org:
        org.append(current_org)
    if current_subdistrict:
        subdistrict.append(current_subdistrict)
    if current_district:
        district.append(current_district)
    if current_province:
        province.append(current_province)
    if current_zipcode:
        zipcode.append(current_zipcode) if len(current_zipcode) == 5 else None
    if current_phone:
        phone.append(current_phone)

    return name, org, subdistrict, district, province, zipcode, phone
