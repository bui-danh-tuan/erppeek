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
all_pick = client.model('stock.picking').search([('is_pick', '=', True), ('sale_id.latest_delivery_order_id', '=', False), ('sale_id.country_type_id', '=', 3)])
for p in all_pick:
    a = client.model('stock.picking').browse(p)
    a.action_gen_delivery_order_pdf()
    print(p)