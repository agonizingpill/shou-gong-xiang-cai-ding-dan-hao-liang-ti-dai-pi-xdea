from fastapi import APIRouter, Depends

from core.auth import actor, allow
from core.audit import record
from core.db import transaction
from core.records import scan
from domain import loss_sheets_service as service
from domain.loss_sheets_model import loss_sheets
from domain.loss_sheets_schemas import EstimateLoss, FileLoss

router = APIRouter()

@router.get('/loss_sheets')
def list_loss_sheets(user=Depends(actor)):
    with transaction() as conn:
        return scan(conn, loss_sheets)


@router.post('/loss_sheets/estimate-loss')
def estimate_loss(data: EstimateLoss, user=Depends(actor)):
    allow(user, ('operator', 'reviewer'))
    with transaction() as conn:
        output = service.estimate_loss(conn, user, data)
        record(conn, user, 'loss_sheets.estimate_loss')
        return output


@router.post('/loss_sheets/file-loss')
def file_loss(data: FileLoss, user=Depends(actor)):
    allow(user, ('operator', 'reviewer'))
    with transaction() as conn:
        output = service.file_loss(conn, user, data)
        record(conn, user, 'loss_sheets.file_loss')
        return output
