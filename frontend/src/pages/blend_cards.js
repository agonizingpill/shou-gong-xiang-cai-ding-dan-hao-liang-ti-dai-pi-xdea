        import {workspace} from '../workspace.js';
        import {el} from '../dom.js';

        const page = {
  "title": "替料制单与称重核销",
  "module": "替料制单与核销",
  "caption": "替料制单与核销",
  "detail": "替代批必须满足同一香型和标签声明。保留克数之和等于工台称量需求。",
  "path": "/blend_cards",
  "columns": [
    {
      "name": "code",
      "label": "编号"
    },
    {
      "name": "order_ref",
      "label": "实际订单"
    },
    {
      "name": "sheet",
      "label": "耗量凭证"
    },
    {
      "name": "lots",
      "label": "批号及保留克数"
    },
    {
      "name": "grams",
      "label": "出库累计 g"
    },
    {
      "name": "labels",
      "label": "沿用的标签原文"
    },
    {
      "name": "state",
      "label": "制单状态"
    }
  ],
  "layout": "flip",
  "view": "table",
  "actions": [
    {
      "name": "allocate",
      "label": "签发替料制单",
      "path": "/blend_cards/allocate",
      "fields": [
        {
          "name": "code",
          "label": "制单号",
          "kind": "text",
          "initial": "BC-024"
        },
        {
          "name": "sheet",
          "label": "耗量评估单",
          "kind": "text",
          "initial": "LS-024"
        },
        {
          "name": "lots",
          "label": "实物批与保留克数",
          "kind": "json",
          "initial": [
            {
              "lot": "LT-A1",
              "grams": 150
            },
            {
              "lot": "LT-A2",
              "grams": 230
            }
          ]
        }
      ],
      "help": "分配成功才会保留库存；发现标签冲突时订单冻结。",
      "roles": [
        "reviewer"
      ],
      "success": "已写入"
    },
    {
      "name": "close_weighing",
      "label": "扣料核销",
      "path": "/blend_cards/close-weighing",
      "fields": [
        {
          "name": "code",
          "label": "制单号",
          "kind": "text",
          "initial": "BC-024"
        }
      ],
      "help": "核销后减实物库存和已保留克数，不能重复扣料。",
      "roles": [
        "reviewer"
      ],
      "success": "已写入"
    }
  ]
};

        export const {title} = page;
        export const key = "blend_cards";
        export async function render(root, role) {
          await workspace(root, role, page);

        }
