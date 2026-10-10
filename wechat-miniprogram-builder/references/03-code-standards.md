# 阶段 2/3：代码规范（必须/禁止清单）

> 本文件是代码层的硬性规范。AI 生成的每一行代码都必须符合以下规则。用规则不用原则——以下条款直接可执行。

## 1. 通用结构

- 所有云函数返回统一结构：`{ code: 0, data, ok: true }` / `{ code: 400, msg, ok: false }`
- 公共逻辑（db 实例、配置缓存、管理员校验、分页、错误格式、内容安全）必须进 common 模块，禁止各函数重复实现
- 常量集中定义：状态枚举、佣金率、超时时间等，禁止散落各处裸值
- 命名规范：云函数/集合/目录小驼峰；常量全大写；前端页面文件小驼峰

## 2. 必须清单（云函数侧）

- [ ] 所有 `await` 必须 try/catch；catch 内必须 `console.error` + 返回结构化错误，禁止空 catch
- [ ] 网络请求（支付类）必须设超时（10~15s）+ 明确错误处理
- [ ] 所有“抢/领/改状态”用 `where({ _id, status: 当前状态 }).update()` 条件更新，并校验 `stats.updated === 1`，不满足即返回“状态已变更”
- [ ] 订单状态用常量 + 状态转换白名单（allowedTransitions），状态变更写 statusLog
- [ ] 金额计算用整数分：`Math.round(x * 100) / 100` 或全程分存储
- [ ] 所有列表查询带 limit + 分页（parsePage）
- [ ] 所有云函数入口做权限校验（openid 归属校验 / checkAdmin）
- [ ] 金额/价格在任何写库前重新从数据库读取校验（服务端重取价）
- [ ] 核心纯函数（金额计算、签名、状态转换）从业务代码中抽出，可独立测试

## 3. 必须清单（前端侧）

- [ ] 页面三态完整：加载态（skeleton）、空态（有引导文案）、异常态（错误 + 重试）
- [ ] setData 最小化：只更新变化的字段，禁止整页对象塞 setData
- [ ] 请求统一封装（api.js）：loading、错误 toast、统一处理，页面禁止裸调云函数
- [ ] 列表分页 + 下拉刷新 + 上拉加载
- [ ] 表单即时校验 + 提交中按钮防重复点击（disabled + loading）
- [ ] onUnload 清理定时器、数据库 watch、订阅
- [ ] 全局组件统一（Vant），禁止页面内混搭自绘样式
- [ ] 图片使用懒加载（lazy-load）

## 4. 禁止清单（AI 高频翻车点，直接禁止）

| 禁止行为 | 原因 |
|---|---|
| 前端传价格参与计算 | 金额必须服务端重取 |
| openid 来自前端参数 | 必须 `cloud.getWXContext().OPENID` |
| 硬编码 appid/envId/密钥/商户号/证书 | 统一 `YOUR_XX` 占位 + 部署脚本替换 |
| 空 catch / 吞异常 | 错误必须可见可查 |
| 裸字符串状态散落 | 状态必须走常量 + 白名单 |
| TODO/FIXME/console.log 残留交付 | 交付前必须清扫 |
| 无 limit 的全量查询 | 数据库条数上限是硬约束 |
| 前端直接操作敏感集合（orders 等） | 必须云函数中转 |
| 用浮点直接算金额 | 必须整数分 |
| 回调/奖励等涉及钱的操作无幂等 | 重复触发 = 资金事故 |
| 同时 watch 多个集合 | 客户端 watch 有数量上限 |
| 一次性查询超过数据库条数限制 | 见 08-platform-knowledge.md |

## 5. 错误处理规范

1. 云函数错误统一：`fail(msg, code)`，code 语义化（400 参数错 / 404 不存在 / 403 无权限 / 500 服务错）
2. 前端错误提示要“人话”：“网络开小差了，请重试”，禁止裸抛技术错误
3. 日志分级：console.error 必须带上下文（openid、函数名、订单号）
4. 支付/退款等关键操作，所有分支（成功/失败/超时/回调重复）都要有日志

## 6. 状态机规范（订单等）

```js
const ORDER_STATUS = {
  PENDING: 'pending',         // 待支付
  PAID: 'paid',               // 已支付
  CLAIMED: 'claimed',         // 已接单
  PROCESSING: 'processing',   // 进行中
  PENDING_CONFIRM: 'pending_confirm', // 待确认
  DONE: 'done',               // 已完成
  CANCELLED: 'cancelled',     // 已取消
  PENDING_REFUND: 'pending_refund',   // 退款申请中
  REFUNDED: 'refunded',       // 已退款
  EXPIRED: 'expired'          // 超时未支付
};

const ALLOWED_TRANSITIONS = {
  pending: ['paid', 'cancelled', 'expired'],
  paid: ['claimed', 'pending_refund'],
  claimed: ['processing', 'pending_refund'],
  // ...
};
```

- 状态变更统一函数：`transition(order, from, to, operator, note)`，内部校验白名单 + 写 statusLog
- 条件更新 + `updated === 1` 校验兜底并发

## 7. 代码组织示例（云函数目录）

```
cloudfunctions/
├── common/          # 公共模块（被其他函数引用时复制或共享）
├── auth/            # 登录/用户
├── orders/          # 订单（index.js 超限时拆 order-core / refund / query 子模块）
├── pay/             # 支付
├── earnings/        # 提现
├── services/        # 服务/分类/Banner
├── admin/           # 管理后台（禁止巨石：按域拆文件）
└── cron/            # 定时任务
```

## 8. 交付前代码自查（Phase 4 执行）

逐项 grep / 人工检查：

- [ ] `grep -r "YOUR_\|REPLACE_" .` 确认无未替换占位符（或已明确是交付占位）
- [ ] `grep -r "console.log" .` 业务代码中清理（保留 console.error 日志）
- [ ] `grep -r "TODO\|FIXME\|HACK" .` 清零
- [ ] 无明文密钥/证书/商户号（apiclient_key、api key 等）
- [ ] 所有集合权限按 02-architecture.md 最小化配置
- [ ] 核心逻辑有测试且通过
