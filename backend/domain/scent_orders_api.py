from fastapi import APIRouter, Depends

from core.auth import actor, allow
from core.audit import record
from core.db import transaction
from core.records import scan
from domain import scent_orders_service as service
from domain.scent_orders_model import scent_orders
from domain.scent_orders_schemas import ReceiveOrder, ClearHold

router = APIRouter()

@router.get('/scent_orders')
def list_scent_orders(user=Depends(actor)):
    with transaction() as conn:
        return scan(conn, scent_orders)


@router.post('/scent_orders/receive-order')
def receive_order(data: ReceiveOrder, user=Depends(actor)):
    allow(user, ('operator', 'reviewer'))
    with transaction() as conn:
        output = service.receive_order(conn, user, data)
        record(conn, user, 'scent_orders.receive_order')
        return output


@router.post('/scent_orders/clear-hold')
def clear_hold(data: ClearHold, user=Depends(actor)):
    allow(user, ('reviewer',))
    with transaction() as conn:
        output = service.clear_hold(conn, user, data)
        record(conn, user, 'scent_orders.clear_hold')
        return output
