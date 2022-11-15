from matplotlib.style import use
from _odoo_config import product


p = product()
c = p.get_client()
user = c.model('res.users').browse(2687).login_token = 'auto'