from fastapi import APIRouter, Depends

from core.auth import actor, allow
from core.audit import record
from core.db import transaction
from core.records import scan
from domain import powder_lots_service as service
from domain.powder_lots_model import powder_lots
from domain.powder_lots_schemas import ReceiveLot

router = APIRouter()

@router.get('/powder_lots')
def list_powder_lots(user=Depends(actor)):
    with transaction() as conn:
        return scan(conn, powder_lots)


@router.post('/powder_lots/receive-lot')
def receive_lot(data: ReceiveLot, user=Depends(actor)):
    allow(user, ('operator', 'reviewer'))
    with transaction() as conn:
        output = service.receive_lot(conn, user, data)
        record(conn, user, 'powder_lots.receive_lot')
        return output
