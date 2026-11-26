        import {workspace} from '../workspace.js';
        import {el} from '../dom.js';

        const page = {
  "title": "粉料批签收",
  "module": "粉料批与耗量",
  "caption": "粉料批与耗量",
  "detail": "标签、含水率、可用克数保留到批次。相同香型也必须逐个核对声明。",
  "path": "/powder_lots",
  "columns": [
    {
      "name": "code",
      "label": "编号"
    },
    {
      "name": "material",
      "label": "供应批物料"
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
      "name": "moisture",
      "label": "含水百分比"
    },
    {
      "name": "batch_grams",
      "label": "实物余量 g"
    },
    {
      "name": "reserved_grams",
      "label": "已保留 g"
    }
  ],
  "layout": "split",
  "view": "grid",
  "actions": [
    {
      "name": "receive_lot",
      "label": "封存入料批标签",
      "path": "/powder_lots/receive-lot",
      "fields": [
        {
          "name": "code",
          "label": "批号",
          "kind": "text",
          "initial": "LT-C3"
        },
        {
          "name": "material",
          "label": "批次名称",
          "kind": "text",
          "initial": "木香粉 · 补料"
        },
        {
          "name": "scent",
          "label": "香型",
          "kind": "text",
          "initial": "WOOD"
        },
        {
          "name": "declaration",
          "label": "标签声明文字",
          "kind": "json",
          "initial": [
            "木粉A",
            "胶粉2"
          ]
        },
        {
          "name": "moisture",
          "label": "含水百分比",
          "kind": "float",
          "initial": 12
        },
        {
          "name": "batch_grams",
          "label": "实物余量 g",
          "kind": "int",
          "initial": 490
        }
      ],
      "help": "余量按整数克计，保留克数不允许直接手改。",
      "roles": [
        "operator",
        "reviewer"
      ],
      "success": "已写入"
    }
  ]
};

        export const {title} = page;
        export const key = "powder_lots";
        export async function render(root, role) {
          await workspace(root, role, page);

        }
