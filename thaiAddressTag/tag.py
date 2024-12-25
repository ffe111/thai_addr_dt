# from simpletransformers.ner import NERModel
# import torch
from thaiAddressTag.addresses import *
from thaiAddressTag.ner import *
from thaiAddressTag.utils import *

from fuzzywuzzy import process, fuzz
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)


def check_result(results):
    """ check result from query by dataframe """
    if results:
        return results[0]
    else:
        return None  # not found result


def match_location(locations, zipcode=None):
    # make variable
    word = None
    p, d, s, z = None, None, None, None
    dup_subdist = []

    """
    ZIPCODE
    """
    # check zipcode has correct
    if zipcode != None and type(zipcode) == list and zipcode:
        for zip in zipcode:  # if zipcode >1
            print(zip)
            if zip in ZIPCODES:
                z = zip
            else:  # zipcode incorrect!
                z = None
        # get subdistrict by zipcode
        for word in locations:
            # skip case เมือง
            if word == "เมือง" and z not in ['33110', '42000']:
                print("found เมือง")
                # not district ignore
                word = None
            # SOPELLCHACK before process
            elif word not in PROVINCES and word not in DISTRICTS and word not in set(SUBDISTRICTS_ZIP_DICT.get(z, SUBDISTRICTS)):
                word = [l for l, _ in process.extract(
                    word, set(SUBDISTRICTS_ZIP_DICT.get(z, SUBDISTRICTS)), scorer=fuzz.ratio, limit=3)if _ >= 65]
                print(word)
                if word:
                    word = word[0]
            if type(word) != list and word in set(SUBDISTRICTS_ZIP_DICT.get(z, SUBDISTRICTS)):
                dup_subdist.append(word)
                # print(dup_subdist)
        # check if subdist in list_word >1
        if len(set(dup_subdist)) > 1:  # set inn't duplicate case พนัส, พนัส
            s = [word for word in dup_subdist if word not in
                 set(DISTRICTS_ZIP_DICT.get(z, DISTRICTS))]  # amphoe
            s = s[0]
        else:
            s = dup_subdist[0] if dup_subdist else None
        # ZIPCODE check subdistrict
        if s != None:
            return check_result(results=ADDR_DF[(ADDR_DF['subdistrict'] == s) & (
                ADDR_DF['zipcode'] == z)].to_dict('records'))
        else:
            # not SUBDISTRICT find district
            for word in locations:
                print(word)
                # check district "เมือง" != 33110, 42000 ตำบลเมือง
                if word == "เมือง" and z not in ['33110', '42000']:
                    # word = "เมือง" + ADDR_DF[ADDR_DF['zipcode'] == z]['province'].unique()[0]
                    # up date word in locations list
                    locations[locations.index(
                        word)] = word = "เมือง" + ADDR_DF[ADDR_DF['zipcode'] == z]['province'].unique()[0]
                # SPELLCHECK before process
                elif word not in PROVINCES and word not in set(DISTRICTS_ZIP_DICT.get(z, DISTRICTS)):
                    word = [l for l, _ in process.extract(
                        word, set(DISTRICTS_ZIP_DICT.get(z, DISTRICTS)), scorer=fuzz.ratio, limit=3) if _ >= 65]
                    if word:
                        word = word[0]
                if type(word) != list and word in set(DISTRICTS_ZIP_DICT.get(z, DISTRICTS)):
                    d = word
            # NOT found district
            # if d != None:
            d = d if d != None else None
            # return check_result(results = ADDR_DF[(ADDR_DF['district'] == d) & (
            #       ADDR_DF['zipcode'] == z)][['province', 'district']].to_dict('records'))
            # find province
            for word in locations:
                # SPELLCHCEK before process
                if word not in PROVINCES:
                    word = [l for l, _ in process.extract(word, ADDR_DF[ADDR_DF['zipcode'] == z]
                                                          ['province'].unique(), scorer=fuzz.ratio, limit=3) if _ >= 65]
                    # print(word)
                    if word:
                        word = word[0]
                if type(word) != list and word in PROVINCES:
                    p = word
            p = p if p != None else None
            return {'province': p, 'district': d, 'subdistrict': s, 'zipcode': z}
    print("skip to prvince")

    """
    Province 
    """
    # print("skip to prvince")
    # find Province
    for word in locations:
        print("first ")
        if word == "กรุงเทพ":
            word = "กรุงเทพมหานคร"
        elif word == "อยุธยา":
            word = "พระนครศรีอยุธยา"
        elif word not in PROVINCES and word not in DISTRICTS and word not in SUBDISTRICTS:
            fix_word = [l for l, _ in process.extract(
                word, PROVINCES, scorer=fuzz.ratio, limit=3) if _ >= 65]
            print(fix_word)
            # if len(word) >= 2:
            #   word = word[0:2] # case ชบุรี get ราชบุรี 90 and ชลบุรี
            # elif len(word) == 1:
            #   word = word[0]
            if fix_word:
                locations.remove(word)
                word = fix_word[0]
                fix_word = None
        print("p", p, "word", word)
        if type(word) != list and word in PROVINCES:
            print("found p")
            p = word
            print(p)
            break

    # Check found PROVINCE
    if p != None:
        # get district by province
        for word in locations:
            print("check word ", word)
            if word == "เมือง" and z not in ['33110', '42000']:
                # word = "เมือง" + ADDR_DF[ADDR_DF['zipcode'] == z]['province'].unique()[0]
                # up date word in locations list
                locations[locations.index(word)] = word = "เมือง" + p
                # SPELLCHECK before process
            print("check word ", word)
            if word not in PROVINCES and word not in DISTRICTS and word not in set(SUBDISTRICTS_DICT.get(p, SUBDISTRICTS)):
                print("spell dist", process.extract(
                    word, set(SUBDISTRICTS_DICT.get(p, SUBDISTRICTS)), scorer=fuzz.ratio, limit=3))
                word = [l for l, _ in process.extract(
                    word, set(SUBDISTRICTS_DICT.get(p, SUBDISTRICTS)), scorer=fuzz.ratio, limit=3)if _ >= 65]
                print(word)
                if word:
                    word = word[0]
            if type(word) != list and word in set(SUBDISTRICTS_DICT.get(p, SUBDISTRICTS)):
                dup_subdist.append(word)
                print(dup_subdist)
            # check if subdist in list_word >1
            if len(set(dup_subdist)) > 1:  # set inn't duplicate case พนัส, พนัส
                s = [word for word in dup_subdist if word not in
                     set(DISTRICTS_DICT.get(p, DISTRICTS))]  # amphoe
                s = s[0]
            else:
                s = dup_subdist[0] if dup_subdist else None
            # PROVINCE check subdistrict
            if s != None:
                return check_result(results=ADDR_DF[(ADDR_DF['subdistrict'] == s) & (
                    ADDR_DF['province'] == p)][['province', 'district', 'subdistrict', 'zipcode']].to_dict('records'))


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

    location = province + district + subdistrict
    location = match_location(location, zipcode)
    location = {'province': province, 'district': district,
                'subdistrict': subdistrict, 'zipcode': zipcode} if location == None else location
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
