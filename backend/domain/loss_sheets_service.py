from sqlalchemy import select

from core.queueing import submit, result
from core.records import get, insert, need, scan, update
from domain.scent_orders_model import scent_orders
from domain.powder_lots_model import powder_lots
from domain.loss_sheets_model import loss_sheets
from domain.blend_cards_model import blend_cards


def estimate_loss(conn, user, data):
    from domain.incense_rules import compatible
    order = get(conn,scent_orders,data.order_ref,lock=True)
    lot = get(conn,powder_lots,data.lot)
    need(order['state'] in {'待耗量','待配料'},'冻结或已制单订单无法重估')
    need(compatible(order,lot),'参考批香型或标签说明不同')
    return submit(user,{'order_ref':order['code'],'target':order['grams'],'scent':order['scent'],
                        'dryer':order['dryer'],'lot':lot['code'],'moisture':lot['moisture']})


def file_loss(conn, user, data):
    run = result(user,data.token)
    calc,model = run['input'],run['result']
    order = get(conn,scent_orders,calc['order_ref'],lock=True)
    need(order['state'] in {'待耗量','待配料'},'订单状态不允许归档耗量')
    entry = insert(conn,loss_sheets,code=data.code,order_ref=order['code'],primary_lot=calc['lot'],
                   need_g=model['need_g'],loss_g=model['loss_g'],features=model)
    update(conn,scent_orders,order['code'],state='待配料')
    return entry
