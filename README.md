# 手工香材订单耗量替代批

草木间线香作坊预测订单干燥损耗，按克保留同标签替代批并签发领料单。

## 现场工作与联系人

模拟客户为草木间线香作坊。香型契约、粉料损耗回归、等效替料验证、制单；过敏成分声明不一致则冻结工单。

- 香型契约 `scent_orders`，字段为 `title`（订单名称）、`grams`（目标干料 g）、`scent`（香型）、`declaration`（标签原文集合）、`dryer`（干燥架）、`state`（订单状态）、`hold_reason`（冻结说明）。模型约束位于 `backend/domain/scent_orders_model.py`，规则位于 `scent_orders_service.py`。
- 粉料批与耗量 `powder_lots`，字段为 `material`（供应批物料）、`scent`（香型）、`declaration`（标签原文集合）、`moisture`（含水百分比）、`batch_grams`（实物余量 g）、`reserved_grams`（已保留 g）。模型约束位于 `backend/domain/powder_lots_model.py`，规则位于 `powder_lots_service.py`。
- 耗量评估单 `loss_sheets`，字段为 `order_ref`（订单）、`primary_lot`（参考实物批）、`need_g`（计划公斤换算 g）、`loss_g`（预测干燥损耗 g）、`features`（预测与验证证据）。模型约束位于 `backend/domain/loss_sheets_model.py`，规则位于 `loss_sheets_service.py`。
- 替料制单与核销 `blend_cards`，字段为 `order_ref`（实际订单）、`sheet`（耗量凭证）、`lots`（批号及保留克数）、`grams`（出库累计 g）、`labels`（沿用的标签原文）、`state`（制单状态）。模型约束位于 `backend/domain/blend_cards_model.py`，规则位于 `blend_cards_service.py`。

团队为模拟的9 人香材作坊按香型契约安排小批制单。

订单纸条和粉料批签分开。干燥损耗受历史批次影响，替料时标签可能不匹配，已冻结订单容易被重新制单。

香型、粉料含水和损耗批史进入耗量估计，制单员检查替代品声明后领配料卡。

### 一天的业务操作

1. 08:20 登记 SO-024，订单要求 320 克清木细线，签收合同声明木粉A和胶粉2。
2. 09:00 主用批 LT-A1 只有 200 克，先以含水率 12% 的 LT-A2 作为参考批，预测出料损耗。
3. 10:15 操作员归档 LS-024，计划总克数由模型给出。
4. 10:30 尝试使用同香型的 LT-X9，却发现其标签写胶粉7，制单被冻结。
5. 11:10 复核员撤回冲突材料后解冻。选择同原文标签的 LT-A1 与 LT-A2，分别保留足量。
6. 14:00 称料后核销 BC-024，实物库存扣减，只执行一次。

## 启动

```sh
cp .env.example .env
docker compose up -d --build --wait
docker compose exec -T backend python -m scripts.seed_demo
```

打开 `http://127.0.0.1:18319`。FastAPI OpenAPI 在 `http://127.0.0.1:19319/docs`。
Compose 运行 Nginx、Python FastAPI、独立 Redis 消费进程、SQL 数据库和 Redis，SQL 与 Redis 使用命名卷。
本机开发时，在 Python 3.11 环境安装 `backend/requirements.txt` 后从 backend 目录运行 `uvicorn core.app:app`。须提供 `DATABASE_URL`、`REDIS_URL`、`JWT_SECRET`，`SEED_DEMO` 控制演示初始化。

| 演示账号 | 权限 |
|---|---|
| operator@demo.test | 提交领域记录和计算请求 |
| reviewer@demo.test | 提交记录并执行有业务约束的复核操作 |
| viewer@demo.test | 浏览业务台账 |

三个本地演示账号均使用 `DemoC0de!2026`。角色在 `backend/core/roles.py` 和 `frontend/src/store.js` 中声明。计算状态在 worker、queueing、API 和同一前端 store 中使用。

## 页面与接口

| 业务任务 | FastAPI 路由 | 页面 |
|---|---|---|
| 香型契约 | `/scent_orders` /scent_orders/receive-order，/scent_orders/clear-hold | `frontend/src/pages/scent_orders.js` |
| 粉料批与耗量 | `/powder_lots` /powder_lots/receive-lot | `frontend/src/pages/powder_lots.js` |
| 耗量评估单 | `/loss_sheets` /loss_sheets/estimate-loss，/loss_sheets/file-loss | `frontend/src/pages/loss_sheets.js` |
| 替料制单与核销 | `/blend_cards` /blend_cards/allocate，/blend_cards/close-weighing | `frontend/src/pages/blend_cards.js` |

SQL 实体与约束在 `backend/domain` 下维护。前端使用原生 ES modules。核心算子为 HistGradientBoostingRegressor。280 条训练、80 条末段留出，展示耗量 MAE、人工固定比例基线和输入哈希。以整数克向上取整为领料量。

全部是模拟采购标签、订单和历史测重。标签比较是文本集合的业务核对，不是成分检验、健康指导或使用建议。

[MIT](LICENSE)
