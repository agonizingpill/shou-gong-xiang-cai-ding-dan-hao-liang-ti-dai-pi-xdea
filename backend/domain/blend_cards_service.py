from sqlalchemy import select

from core.queueing import submit, result
from core.records import get, insert, need, scan, update
from domain.scent_orders_model import scent_orders
from domain.powder_lots_model import powder_lots
from domain.loss_sheets_model import loss_sheets
from domain.blend_cards_model import blend_cards


def allocate(conn, user, data):
    from domain.incense_rules import allocate
    return allocate(conn,data)


def close_weighing(conn, user, data):
    from domain.incense_rules import finish
    return finish(conn,data.code)
