# from simpletransformers.ner import NERModel
# import torch
from thaiAddressTag.addresses import *
from thaiAddressTag.ner import *
from thaiAddressTag.utils import *

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)


def match_location(location, zipcode=None):
    """
    Match location from location list
    find address by zipcode or province

    """
    p = ''
    d = ''
    s = ''
    z = ''
    # find by zipcode
    if zipcode:
        # check zipcode
        for zip in zipcode:
            z = zip
            for word in location:
                if word in set(SUBDISTRICTS_ZIP_DICT.get(zip, DISTRICTS)):
                    s = word
                    # print(s)
                    # break
        results = ADDR_DF[(ADDR_DF['subdistrict'] == s) & (
            ADDR_DF['zipcode'] == z)].to_dict('records')
        # print(results)
        if results:
            return results[0]
        else:
            return None  # not found result
    # find by province
    for word in location:
        if word == 'กรุงเทพมหานคร':
            location.remove(word)
            p = 'กรุงเทพ'
            # print(p)
            break
        if word in PROVINCES:
            p = word
            # drop p in location list
            location.remove(p)
            # print(p)
            break
    # check province
    if p:
        for word in location:
            if word in set(SUBDISTRICTS_DICT.get(p, DISTRICTS)):
                s = word
                # print(s)
                # break
        results = ADDR_DF[(ADDR_DF['subdistrict'] == s) & (
            ADDR_DF['province'] == p)].to_dict('records')[0]
        # print(results)
        if results:
            return results
        else:
            return None  # not found result


def extract_address(text, model):
    """
    extract address

    """
    text, phone_number = extract_phone_(text)

    predict, _ = model.predict([clean_location_text(preprocess(text))])
    print(predict)

    name, org, subdistrict, district, province, zipcode, phone = ner_extract(
        predict)

    print(name, org, subdistrict, district, province, zipcode, phone)

    location = subdistrict + district + province
    location = match_location(location, zipcode)
    location = {'province': province, 'district': district, 'subdistrict': subdistrict, 'zipcode': '1'} if location == None else location
    location.update({'name': name})
    location.update({'phone': phone_number})
    print(location)

    return location


# ---- Test:function ----
# name, phone_number = '', ''                            
# province, district, subdistrict, zipcode = ['กรุงเทพมหานคร'], ['ฉิมพลี'], ['ตลิ่งชัน'], ''
# location = subdistrict + district + province
# location = match_location(location, zipcode)
# location = {'province': province, 'district': district, 'subdistrict': subdistrict, 'zipcode': '1'} if location == None else location
# location.update({'name': name})
# location.update({'phone': phone_number})
# print(location)

# text = "อนงค์ลักษณ์\n9/56 ม.3\nหมู่บ้านนฤมลศิริ(ซอย2)\nซ.บุญศิริ ถ.สุขุมวิท\nต.บางเมือง\nอ.เมืองสมุทรปราการ\nจ.สมุทรปราการ\n10270\nโทร.0956029655"
# path = "models"

# model = NERModel("camembert", model_name=path,
#                  use_cuda=torch.cuda.is_available())

# extract_address(text, model)
