        import {workspace} from '../workspace.js';
        import {el} from '../dom.js';

        const page = {
  "title": "干燥损耗估算",
  "module": "耗量评估单",
  "caption": "耗量评估单",
  "detail": "模型以目标克数、粉料水分和干燥架为特征，预测需增配的原料克数。",
  "path": "/loss_sheets",
  "columns": [
    {
      "name": "code",
      "label": "编号"
    },
    {
      "name": "order_ref",
      "label": "订单"
    },
    {
      "name": "primary_lot",
      "label": "参考实物批"
    },
    {
      "name": "need_g",
      "label": "计划公斤换算 g"
    },
    {
      "name": "loss_g",
      "label": "预测干燥损耗 g"
    },
    {
      "name": "features",
      "label": "预测与验证证据"
    }
  ],
  "layout": "stack",
  "view": "table",
  "actions": [
    {
      "name": "estimate_loss",
      "label": "按当前批次估算",
      "path": "/loss_sheets/estimate-loss",
      "fields": [
        {
          "name": "order_ref",
          "label": "订单号",
          "kind": "text",
          "initial": "SO-024"
        },
        {
          "name": "lot",
          "label": "参考粉料批",
          "kind": "text",
          "initial": "LT-A2"
        }
      ],
      "help": "估算使用供料批检测值，不会保留库存。",
      "roles": [
        "operator",
        "reviewer"
      ],
      "success": "已写入"
    },
    {
      "name": "file_loss",
      "label": "盖章保存耗量凭证",
      "path": "/loss_sheets/file-loss",
      "fields": [
        {
          "name": "code",
          "label": "估算号",
          "kind": "text",
          "initial": "LS-024"
        },
        {
          "name": "token",
          "label": "后台模型任务号",
          "kind": "token",
          "initial": ""
        }
      ],
      "help": "耗量凭证可绑定替料制单并带留出结果。",
      "roles": [
        "operator",
        "reviewer"
      ],
      "success": "已写入"
    }
  ]
};

        export const {title} = page;
        export const key = "loss_sheets";
        export async function render(root, role) {
          await workspace(root, role, page);

        }
