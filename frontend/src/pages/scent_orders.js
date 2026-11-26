        import {workspace} from '../workspace.js';
        import {el} from '../dom.js';

        const page = {
  "title": "香型契约",
  "module": "香型契约",
  "caption": "香型契约",
  "detail": "只按合同声明核对替代批的原文集合。订单标签、香型与数量不从估算改写。",
  "path": "/scent_orders",
  "columns": [
    {
      "name": "code",
      "label": "编号"
    },
    {
      "name": "title",
      "label": "订单名称"
    },
    {
      "name": "grams",
      "label": "目标干料 g"
    },
    {
      "name": "scent",
      "label": "香型"
    },
    {
      "name": "declaration",
      "label": "标签原文集合"
    },
    {
      "name": "dryer",
      "label": "干燥架"
    },
    {
      "name": "state",
      "label": "订单状态"
    },
    {
      "name": "hold_reason",
      "label": "冻结说明"
    }
  ],
  "layout": "flip",
  "view": "stack",
  "actions": [
    {
      "name": "receive_order",
      "label": "登记新香型订单",
      "path": "/scent_orders/receive-order",
      "fields": [
        {
          "name": "code",
          "label": "新订单编号",
          "kind": "text",
          "initial": "SO-026"
        },
        {
          "name": "title",
          "label": "订单名称",
          "kind": "text",
          "initial": "展馆 · 样品套"
        },
        {
          "name": "grams",
          "label": "目标干料克数",
          "kind": "int",
          "initial": 180
        },
        {
          "name": "scent",
          "label": "合同香型",
          "kind": "text",
          "initial": "WOOD"
        },
        {
          "name": "declaration",
          "label": "标签原文字段",
          "kind": "json",
          "initial": [
            "木粉A",
            "胶粉2"
          ]
        },
        {
          "name": "dryer",
          "label": "干燥架",
          "kind": "text",
          "initial": "rack-a"
        }
      ],
      "help": "在制单前确认原文标签，不接受自由文本解释。",
      "roles": [
        "operator",
        "reviewer"
      ],
      "success": "已写入"
    },
    {
      "name": "clear_hold",
      "label": "核对并解冻订单",
      "path": "/scent_orders/clear-hold",
      "fields": [
        {
          "name": "order_ref",
          "label": "冻结订单",
          "kind": "text",
          "initial": "SO-024"
        },
        {
          "name": "reason",
          "label": "解冻核对说明",
          "kind": "text",
          "initial": "撤回有冲突的标签声明批"
        }
      ],
      "help": "只撤回冲突替料。合同标签声明保留。",
      "roles": [
        "reviewer"
      ],
      "success": "已写入"
    }
  ]
};

        export const {title} = page;
        export const key = "scent_orders";
        export async function render(root, role) {
          await workspace(root, role, page);

        }
