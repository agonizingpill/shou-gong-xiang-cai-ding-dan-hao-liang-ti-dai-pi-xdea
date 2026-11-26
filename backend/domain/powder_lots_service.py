from sqlalchemy import select

from core.queueing import submit, result
from core.records import get, insert, need, scan, update
from domain.scent_orders_model import scent_orders
from domain.powder_lots_model import powder_lots
from domain.loss_sheets_model import loss_sheets
from domain.blend_cards_model import blend_cards


def receive_lot(conn, user, data):
    from domain.incense_rules import label_set
    labels = label_set(data.declaration)
    need(data.scent in {'WOOD','PAPER'} and 4<=data.moisture<=20 and 1<=data.batch_grams<=20000,
         '核对粉料批香型、测试含水和实物余量')
    return insert(conn,powder_lots,**(data.model_dump() | {'declaration':sorted(labels),'reserved_grams':0}))
