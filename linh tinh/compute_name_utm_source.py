import erppeek
SERVER = "http://localhost:8069/"
DATABASE = "odoo_trading"
USERNAME = "admin"
PASSWORD = "admin"
client = erppeek.Client(
    SERVER,
    DATABASE,
    USERNAME,
    PASSWORD
)
all_utm_source = client.model('utm.source').browse(8).cron_compute_name()