import erppeek
SERVER = "https://stage.saleholding.com/"
DATABASE = "stage"
USERNAME = "admin"
PASSWORD = "Hebela@123"
client = erppeek.Client(
    SERVER,
    DATABASE,
    USERNAME,
    PASSWORD
)
for i in range(10):
    try:
        contact = client.model('res.partner').create({
            "name": f"Tuấn tạo {i}",
            "phone": "{:010d}".format(i+11),
            "customer_type": "retail",
            "customer_rank": 1,                    # record.is_customer = record.customer_rank > 0 => set > 0 để show lên giao diện
            "street2": "streat2",
            # "state": "5_resaling",                  # default - Resale nhận

            ## doi marketing
            "source_id": 1569,                           # nguon khach hang, lay id trong bang utm.source
            "contact_creator_id": 3234,          # nguoi len so, lay user_id trong bang utm.source
            "marketing_team_id": 115,            # doi ngu marketing lay marketing_team_id trong bang utm.source
            "crm_group_id": 107,                       # cty con, lay crm_group_id trong utm.source
            "crmf99_system_id": 3,               # he thong, lay crmf99_system_idtrong utm.source

            ## doi ban hang
            "crm_lead_user_id": 4616,     # nhan vien kinh doanh, lay user_id trong utm.sale.order.api.url.line
            "crm_lead_team_id": 29,     # doi ngu bang hang, lay team_id trong utm.sale.order.api.url.line
            "crm_lead_crm_group_id": 107, # cong ty con nhan vien kinh doanh, lay crm_group_id trong utm.sale.order.api.url.line
            "crm_lead_crmf99_system_id": 3,  # he thong, lay crmf99_system_id trong utm.sale.order.api.url.line

            #other
            "country_type_id": 3,             # quoc gia
            "product_category_id": 58,     # nhom san pham
        })
        contact.write({
            "state": "5_resaling",  # default - Resale nhận
            # "sale_order_api_url_id": url_id     # id cho đường dẫn tạo đơn hàng
        })
        order = client.model('sale.order').create({
            "partner_id": contact.id,                           # request.env.user.partner_id.id,
            "customer_type": 'retail',                     # from res_partner
            "receiver_name":  f"Tuấn tạo {i}",                              # from ladipage
            "phone": "{:010d}".format(i),                                     # from ladipage
            # "district_id": ladipage_data.get_attr("district_id"),                         # from ladipage # 860,
            # "state_id":  ladipage_data.get_attr("state_id"),                               # from ladipage 65,
            # "note": ladipage_data.note,
            "partner_address_details": "partner_address_details",                 # from ladipage
            "country_type_id": 3,                 # from res_partner
            "shipping_address_type": "outer",                        # default
            "summary_state": "rfq",                             # default
            "is_package_viewable": True,                        # cho xem hang (boolean)
            "pickup_type": "1",                                   #  ("1", "Thu gom tận nơi"), ("2", "Gửi hàng tại bưu cục")
            "service_name": "TMDT_EMS",                          # ("TMDT_EMS", "TMĐT - Chuyển phát nhanh",)
            # "postal_code": ladipage_data.get_attr("postal_code"), # Mã bưu điện , will be updated in the apif99_res_country_state_district table
            # "warehouse_id": "",                                 # set default
            # "sale_order_api_url_id": url_id,
            "pricelist_id": 3,
            "order_line": [(0, 0, {
                    "product_id": 207,
                    "product_uom": 1,
                    "product_uom_qty": 1,
                    "price_unit": 1,
                    "fixed_amount_discount": 0,
                    "price_subtotal": 1
                })]
        })
        order.write({
            ## thong tin doi ban hang
            "product_category_id": 64,         # nhom san pham, product_category_id trong bang res_partner
            "contact_creator_id": 3234,           # nguoi len so, contact_creator_id trong res_partner
            "marketing_team_id": 115,              # doi ngu marketing, marketing_team_id trong res_partner
            "contact_creator_crm_group_id": 107, # cong ty con (marketing), crm_group_id trong res_partner
            "source_id": 1569,                         # nguon khach hang, source_id trong res_partner
            "user_id": 4616,                       # nhan vien kinh doanh, crm_lead_user_id trong res_partner
            "team_id": 29,                    # doi ngu ban hang, crm_lead_team_id trong res_partner
            "crm_group_id": 107,          # cong ty con nhan vien kinh doanh, crm_lead_crm_group_id trong res_partner
            "opportunity_id": contact.opportunity_ids[0].id,
            "opportunity_type": "resale",
            "warehouse_id": 14,
            "town_id": 22271,
            "district_id": 1413,
            "state_id": 155,
        })
        print(f"{i} : {order}")
    except Exception as e:
        print(e)