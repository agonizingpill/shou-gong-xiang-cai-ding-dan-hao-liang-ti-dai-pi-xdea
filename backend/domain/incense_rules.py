from sqlalchemy import select

from core.records import get, insert, need, update
from domain.blend_cards_model import blend_cards
from domain.loss_sheets_model import loss_sheets
from domain.powder_lots_model import powder_lots
from domain.scent_orders_model import scent_orders


def label_set(raw):
    need(isinstance(raw,list) and 1<=len(raw)<=8 and
         all(isinstance(label,str) and label.strip()==label and 1<=len(label)<=24 for label in raw),
         '标签声明必须为 1–8 条逐字原文')
    entries = set(raw)
    need(len(entries)==len(raw),'标签原文不能重复')
    return entries


def compatible(order,lot):
    return order['scent']==lot['scent'] and label_set(order['declaration'])==label_set(lot['declaration'])


def material_lines(raw):
    need(isinstance(raw,list) and 1<=len(raw)<=6,'选择 1 至 6 个可称量实物批')
    lines = {}
    for row in raw:
        need(isinstance(row,dict) and set(row)=={'lot','grams'} and isinstance(row['lot'],str)
             and type(row['grams']) is int and row['grams']>0,'每行需批号与正整数克数')
        need(row['lot'] not in lines,'每个实物批只能出现一次')
        lines[row['lot']] = row['grams']
    return lines


def allocate(conn,data):
    sheet = get(conn,loss_sheets,data.sheet)
    order = get(conn,scent_orders,sheet['order_ref'],lock=True)
    need(order['state']=='待配料','订单状态不允许签发替料制单')
    # Stable lock order prevents concurrent orders sharing multiple powder lots from deadlocking.
    lines = material_lines(data.lots)
    locked = {ref:get(conn,powder_lots,ref,lock=True) for ref in sorted(lines)}
    mismatch = [ref for ref,lot in locked.items() if not compatible(order,lot)]
    if mismatch:
        reason = '香型或标签声明冲突：'+'、'.join(mismatch)
        update(conn,scent_orders,order['code'],state='已冻结',hold_reason=reason)
        return {'state':'已冻结','order_ref':order['code'],'reason':reason}
    reference = get(conn,powder_lots,sheet['primary_lot'])
    need(all(abs(lot['moisture']-reference['moisture'])<=1 for lot in locked.values()),
         '替代实物批含水超出参考批 1 个百分点，须按新批耗量重新估算')
    need(sum(lines.values())==sheet['need_g'],'保留克数之和必须等于工台称量需求')
    for ref,grams in lines.items():
        lot = locked[ref]
        need(grams<=lot['batch_grams']-lot['reserved_grams'],f'{ref} 超过实际可用库存')
    for ref,grams in lines.items():
        update(conn,powder_lots,ref,reserved_grams=locked[ref]['reserved_grams']+grams)
    card = insert(conn,blend_cards,code=data.code,sheet=sheet['code'],order_ref=order['code'],lots=data.lots,
                  grams=sum(lines.values()),labels=order['declaration'],state='已保留')
    update(conn,scent_orders,order['code'],state='已制单')
    return card


def finish(conn,code):
    card = get(conn,blend_cards,code,lock=True)
    need(card['state']=='已保留','每张保留制单仅能核销一次')
    order = get(conn,scent_orders,card['order_ref'],lock=True)
    need(order['state']=='已制单','订单已变更，请核对制单凭证')
    lines = material_lines(card['lots'])
    locked = {ref:get(conn,powder_lots,ref,lock=True) for ref in sorted(lines)}
    for ref,grams in lines.items():
        lot = locked[ref]
        need(lot['reserved_grams']>=grams and lot['batch_grams']>=grams,'库存保留凭证损坏')
    for ref,grams in lines.items():
        lot = locked[ref]
        update(conn,powder_lots,ref,batch_grams=lot['batch_grams']-grams,reserved_grams=lot['reserved_grams']-grams)
    update(conn,scent_orders,order['code'],state='已核销')
    return update(conn,blend_cards,code,state='已核销')
