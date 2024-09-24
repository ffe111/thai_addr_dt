import pandas as pd

# Read data from csv file
ADDR_DF = pd.read_csv(
    "thaiAddressTag/data/parsed_addresses.csv", dtype={"zipcode": str})

# Create hashmap store provinces, districts, subdistricts
PROVINCES = ADDR_DF['province'].unique().tolist()
DISTRICTS = ADDR_DF.district.unique().tolist()
SUBDISTRICTS = ADDR_DF.subdistrict.unique().tolist()

# Create list of district, subdistrict for each province
DISTRICTS_DICT = ADDR_DF.groupby("province")["district"].apply(list)
SUBDISTRICTS_DICT = ADDR_DF.groupby("province")["subdistrict"].apply(list)

# Create list of district, subdistrict for each zipcode
DISTRICTS_ZIP_DICT = ADDR_DF.groupby("zipcode")["district"].apply(list)
SUBDISTRICTS_ZIP_DICT = ADDR_DF.groupby("zipcode")["subdistrict"].apply(list)

# print(PROVINCES)
# print(set(DISTRICTS_DICT.get("ชลบุรี", DISTRICTS)))
# print(ADDR_DF[(ADDR_DF['subdistrict'] == 'แสนสุข')
#       & (ADDR_DF['zipcode'] == "20130")])
# print(ADDR_DF[(ADDR_DF['subdistrict'] == 'แสนสุข')
#       & (ADDR_DF['province'] == "ชลบุรี")])
