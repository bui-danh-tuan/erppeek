from _odoo_config import product
p = product()
c = p.get_client()

arr = [
718555,
718665,
725481,
721377,
717361,
725384,
725416,
725460,
725414,
725420,
725422,
719805,
718503,
723528,
724171,
]
for a in arr:
    c.model('crm.lead').browse(a).is_inprogress = False