from _odoo_config import product
from datetime import datetime
import requests

p = product()
c = p.get_client()
p_r = "PROD"

def tracking(orders_code):
    DHL_BASE = "https://api.dhlecommerce.dhl.com"
    DHL_PICKUP_ACCOUNT_ID = "5375635"
    DHL_SOLD_TO_ACCOUNT_ID = "5248831379"
    token = "a7ce275ba0c0432e8267ef62db46603f"

    data_request = {
        "trackItemRequest": {
            "hdr": {
                "messageType": "TRACKITEM",
                "accessToken": token,
                "messageDateTime": "2022-07-15T06:30:27+00:00",
                "messageVersion": "1.0",
                "messageLanguage": "en"
            },
            "bd": {
                "pickupAccountId": DHL_PICKUP_ACCOUNT_ID,
                "soldToAccountId": DHL_SOLD_TO_ACCOUNT_ID,
                "ePODRequired": "Y",
                "trackingReferenceNumber": [
                    f"MYANK-{p_r}{code}" for code in orders_code
                ]
            }
        }
    }
    response = requests.post("{}/rest/v3/Tracking/".format(DHL_BASE), headers={
        "Content-Type": "application/json"
    }, json=data_request)
    if response and response.status_code == 200:
        try:
            res = response.json().get('trackItemResponse')
            message = res.get("bd").get("responseStatus").get("message")
            if message == "SUCCESS":
                data_tracking = res.get("bd").get("shipmentItems")
                return data_tracking
        except:
            return False

def tracking_shipping_state(orders_code):
    data = tracking(orders_code)
    if not data:
        print(f"Không tìm thấy đơn {orders_code}")
        return
    data = sorted(data, key=lambda d: d['shipmentID'], reverse=True)
    len_data = len(data)
    count = 0
    for d in data:
        event = d.get("events")
        event = sorted(event, key=lambda d: d['dateTime'])
        if True:
            order_name = d.get("shipmentID").replace(f"MYANK-{p_r}", "")
            order_id = c.model('sale.order').search([('name', '=', order_name)], limit=1)
            order_id = c.model('sale.order').browse(order_id)
            if order_id.summary_state == 'completed':
                print(f"{order_id.name} đã hoàn thành trước đó")
                continue
            tracking_id = d.get("trackingID")
            latest_delivery_order_id = order_id.latest_delivery_order_id
            if tracking_id != order_id.latest_delivery_order_id.name[0]:
                latest_delivery_order_id = c.model('apif99.delivery.order').create({
                    'name': tracking_id,
                    'sale_id': type(order_id.id) == type(1) and order_id.id or order_id.id[0] ,
                    "third_party_shipping_state": "71005",
                    "cpn_created_datetime": '2022-09-05 10:47:41',
                    "third_party_shipping_type": 'DHL',
                })
            location_vals = [{
                    "soo_id": latest_delivery_order_id.id,
                    "pos_code": location.get("address").get("postCode"),
                    "pos_address": f"{location.get('address').get('city')}, {location.get('address').get('state')}, {location.get('address').get('country')}",
                    "location": f"{location.get('address').get('city')}, {location.get('address').get('state')}, {location.get('address').get('country')}",
                    "trace_date": location.get('dateTime') and str(location.get('dateTime')),
                    "state_display": location.get("description", False),
                    "state": location.get("status", False),
                    "third_party_shipping_type": 'DHL',

            } for location in event]
            order_location = c.model("apif99.delivery.order.location").search([('soo_id', '=', latest_delivery_order_id.id)])
            for o in order_location:
                c.model("apif99.delivery.order.location").browse(o).unlink()
            if len(location_vals) > 0:
                if latest_delivery_order_id.third_party_shipping_state[0] == location_vals[-1].get('state'):
                    # print(f"Đã Tracking {count}/{len_data}: {order_id.id} - {order_id.name} - {location_vals[-1].get('state')}")
                    count += 1
                    continue
                for vals in location_vals:
                    soo_id =  type(vals.get('soo_id')) == type(1) and vals.get('soo_id')  or vals.get('soo_id')[0]
                    vals['soo_id'] = soo_id
                    c.model("apif99.delivery.order.location").create(vals)
                    apif99_delivery_state = c.model('apif99.delivery.state').browse(1)
                    state_display = apif99_delivery_state.convert_third_party_shipping_state(location_vals[-1].get('state'), 'DHL')
                    third_party_shipping_state_display = state_display[0]
                    third_party_shipping_state_decoration = state_display[1]
                    latest_delivery_order_id.write({
                        'third_party_shipping_state':  location_vals[-1].get('state'),
                        'third_party_shipping_state_display': third_party_shipping_state_display,
                        'third_party_shipping_state_decoration': third_party_shipping_state_decoration
                    })
                    order_id.write({
                        'latest_delivery_order_state':  location_vals[-1].get('state'),
                        'latest_delivery_order_state_display': third_party_shipping_state_display,
                        'latest_delivery_order_state_decoration': third_party_shipping_state_decoration
                    })
                if event[-1].get("status") in ['77093', '77223', '77222']:
                    print(f"Hoàn Thành: {count}/{len_data}: {order_id.id} - {order_id.name}")
                else:
                    pass
                    # print(f"Tracking  : {count}/{len_data}: {order_id.id} - {order_id.name} - {location_vals[-1].get('state')}")
                count += 1
                        
f = open("D:\\Code\\Other\\erp_peek\\linh tinh\\test.txt", "r")
arr = []
# arr = ['BSO039297','BSO043626']
if len(arr) == 0:
    for x in f:
        y = x
        if '\n' in x:
            y = x.replace('\n',"")
        arr.append(y)
arr.sort(reverse=True)
for i in range(0, len(arr), 100):
    print(f"------------------------------------------{i}------------------------------------------")
    tracking_shipping_state(arr[i: i + 100])
