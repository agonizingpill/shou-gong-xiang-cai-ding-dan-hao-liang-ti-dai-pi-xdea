from domain.scent_orders_api import router as scent_orders
from domain.powder_lots_api import router as powder_lots
from domain.loss_sheets_api import router as loss_sheets
from domain.blend_cards_api import router as blend_cards

routers = (scent_orders, powder_lots, loss_sheets, blend_cards,)
