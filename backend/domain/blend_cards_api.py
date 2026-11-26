from fastapi import APIRouter, Depends

from core.auth import actor, allow
from core.audit import record
from core.db import transaction
from core.records import scan
from domain import blend_cards_service as service
from domain.blend_cards_model import blend_cards
from domain.blend_cards_schemas import Allocate, CloseWeighing

router = APIRouter()

@router.get('/blend_cards')
def list_blend_cards(user=Depends(actor)):
    with transaction() as conn:
        return scan(conn, blend_cards)


@router.post('/blend_cards/allocate')
def allocate(data: Allocate, user=Depends(actor)):
    allow(user, ('reviewer',))
    with transaction() as conn:
        output = service.allocate(conn, user, data)
        record(conn, user, 'blend_cards.allocate')
        return output


@router.post('/blend_cards/close-weighing')
def close_weighing(data: CloseWeighing, user=Depends(actor)):
    allow(user, ('reviewer',))
    with transaction() as conn:
        output = service.close_weighing(conn, user, data)
        record(conn, user, 'blend_cards.close_weighing')
        return output
