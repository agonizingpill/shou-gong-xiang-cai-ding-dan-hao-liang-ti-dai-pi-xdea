from sqlalchemy import select

from core.queueing import submit, result
from core.records import get, insert, need, scan, update
from domain.scent_orders_model import scent_orders
from domain.powder_lots_model import powder_lots
from domain.loss_sheets_model import loss_sheets
from domain.blend_cards_model import blend_cards


def receive_order(conn, user, data):
    from domain.incense_rules import label_set
    need(80 <= data.grams <= 1200,'订单须在 80–1200 克')
    need(data.scent in {'WOOD','PAPER'} and data.dryer in {'rack-a','rack-b'},'香型或干燥架未登记')
    labels = label_set(data.declaration)
    return insert(conn,scent_orders,**(data.model_dump() | {'declaration':sorted(labels),'state':'待耗量','hold_reason':None}))


def clear_hold(conn, user, data):
    order = get(conn,scent_orders,data.order_ref,lock=True)
    need(order['state']=='已冻结' and len(data.reason.strip())>=5,'选择冻结订单并填写独立核对说明')
    record_exists = any(item['order_ref']==order['code'] for item in scan(conn,loss_sheets))
    return update(conn,scent_orders,order['code'],state='待配料' if record_exists else '待耗量',hold_reason=None)
