import xlrd
import unidecode

loc = ("D:\Code\Other\erp_peek\linh tinh\FILE-TỈNH-THÁNH-PHỐ-CHECK.xlsx")
 
wb = xlrd.open_workbook(loc)

sheet_state = wb.sheet_by_index(0)
sheet_district = wb.sheet_by_index(1)
sheet_town = wb.sheet_by_index(2)

n_state = sheet_state.nrows
n_district = sheet_district.nrows
n_town = sheet_town.nrows

state = ""
district = ""
town = ""

for i in range(n_state):
    s = f"""
        INSERT INTO apif99_res_country_state (name, code, country_type_id, active, shipping_unit_id) 
        VALUES ('{sheet_state.cell_value(i, 0).replace("'","''")}', 'VIETTEL_POST_{unidecode.unidecode(sheet_state.cell_value(i, 0)).strip().replace(" ","").replace("'","''")}', 1, TRUE,
        (SELECT id from shipping_unit WHERE name = 'VIETTEL_POST' LIMIT 1));
    """
    state += s
    print(f"state{i}: {s}")


for i in range(n_district):
    d = f"""
        INSERT INTO apif99_res_country_state_district (name, code, country_type_id, active, shipping_unit_id, state_id) 
        VALUES (
        '{sheet_district.cell_value(i, 0).replace("'","''")}', 'VIETTEL_POST_{unidecode.unidecode(sheet_district.cell_value(i, 0)).strip().replace(" ","").replace("'","''")}', 1, TRUE,
        (SELECT id from shipping_unit WHERE name = 'VIETTEL_POST' LIMIT 1),
        (SELECT id from apif99_res_country_state WHERE code = 'VIETTEL_POST_{unidecode.unidecode(sheet_district.cell_value(i, 1)).strip().replace(" ","").replace("'","''")}' and country_type_id = 1 LIMIT 1));
    """
    district += d
    print(f"district{i}: {d}")


for i in range(n_town):
    t = f"""
        INSERT INTO apif99_res_country_state_district_town (name, code, country_type_id, active, shipping_unit_id, state_id, district_id) 
        VALUES (
        '{sheet_town.cell_value(i, 0).replace("'","''")}', 'VIETTEL_POST_{unidecode.unidecode(sheet_town.cell_value(i, 0)).strip().replace(" ","").replace("'","''")}', 1, TRUE,
        (SELECT id from shipping_unit WHERE name = 'VIETTEL_POST' LIMIT 1),
        (SELECT id from apif99_res_country_state WHERE code = 'VIETTEL_POST_{unidecode.unidecode(sheet_town.cell_value(i, 2)).strip().replace(" ","").replace("'","''")}' and country_type_id = 1 LIMIT 1),
        (SELECT id from apif99_res_country_state_district WHERE code = 'VIETTEL_POST_{unidecode.unidecode(sheet_town.cell_value(i, 1)).strip().replace(" ","").replace("'","''")}' and country_type_id = 1 and state_id = (
            (SELECT id from apif99_res_country_state WHERE code = 'VIETTEL_POST_{unidecode.unidecode(sheet_town.cell_value(i, 2)).strip().replace(" ","").replace("'","''")}' and country_type_id = 1 LIMIT 1)
        ) LIMIT 1));
    """
    town += t
    print(f"town{i}: {t}")

f = open("D:\Code\Other\erp_peek\linh tinh\sql.txt", "w", encoding="utf8")
f.write(state)
f.write(district)
f.write(town)
f.close()
