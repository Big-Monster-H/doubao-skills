# 阶段 1：架构设计

## 1. 技术选型（默认锁定，变更需用户同意）

| 项 | 默认选择 | 理由 |
|---|---|---|
| 前端框架 | 微信小程序原生框架 | 云开发原生支持、包体积可控、无编译链风险 |
| UI 组件 | Vant Weapp（锁定版本） | 成熟、风格统一、小程序兼容性好 |
| 后端 | 微信云开发（CloudBase） | 免服务器、免备案、与小程序无缝集成 |
| 数据库 | 云数据库（文档型） | 原生、有权限体系 |
| 静态托管 | 云开发静态托管 | 管理后台页面部署 |

禁止在未获用户同意时引入 Taro/uni-app 等跨端框架（除非用户明确要求多端发布）。

## 2. 数据模型设计（通用实体模式）

### 通用实体模式（不绑定具体业务，按需实例化）

| 实体 | 关键字段 | 说明 |
|---|---|---|
| users | `_id`(openid)、nickname、avatar、role、phone、createdAt | 主键即 openid |
| categories | name、sort、icon、status | 分类 |
| items | categoryId、title、cover、images、specs、price、status、sales | 商品/服务/内容 |
| orders | orderId、userId、itemId、spec、amount(分)、status、statusLog、paidAt、cancelledAt | 订单状态机 |
| reviews | orderId、userId、itemId、rating、content、images、status | 评价（需内容安全） |
| withdrawals | providerId、amount、status、payeeInfo、reviewedAt | 提现 |
| inviteCodes | code、creatorId、status、usedBy、usedAt | 邀请码 |
| platformConfig | `_id`='config'、commissionRate、settings | 单例配置文档 |
| banners | title、image、link、sort、status | Banner |

### 设计铁律

1. **金额一律以“分”（整数）存储**，杜绝浮点误差；展示时再转元
2. **订单必须含金额快照**（下单时的价格），后续改价不影响已订单
3. **状态字段必须配合 statusLog 数组**（审计留痕：`{status, time, operator, note}`）
4. **集合命名统一小驼峰**（orders、providers、inviteCodes）
5. **平台配置用单例文档**（`_id` 固定 'config'），配合缓存读取

### 索引设计（架构阶段就要规划）

按查询模式建索引，常见的：
- orders：`userId + createdAt`（用户查自己的订单列表）
- orders：`status + createdAt`（接单大厅按状态查）
- items：`categoryId + status`（分类列表）
- 所有列表查询必须有对应索引，禁止全表扫描

## 3. 集合权限模型（关键！默认安全最小化）

| 集合类型 | 推荐权限 | 说明 |
|---|---|---|
| 用户可直读 | services、categories、banners 等展示数据 | “所有用户可读，仅创建者可写” |
| **敏感集合** | **仅管理端可读写**（云函数中转） | orders、withdrawals、users、inviteCodes、reviews 等——**禁止客户端直读他人订单** |
| 配置类 | 仅管理端可读写 | platformConfig |

**判定原则**：凡涉及钱、隐私、他人数据、状态变更的集合，一律走云函数中转，客户端只调用云函数。

## 4. 云函数拆分原则

1. **按业务域拆分**，一个函数一个职责域：auth、orders、pay、provider、earnings、services、invite、admin、cron
2. **体积纪律**：单个云函数 index.js 超过 300~500 行必须拆（抽公共文件、拆业务子模块）；超过 1000 行强制拆
3. **公共逻辑必须抽 common 模块**：响应格式、数据库实例、配置缓存、管理员校验、分页解析、错误处理、内容安全
4. **管理后台接口**：禁止堆成单文件巨石（如 2000+ 行单文件），必须按业务域拆文件
5. **HTTP 云函数与事件云函数分开**：管理后台用 HTTP 云函数（路径如 /webAdmin），业务事件用事件云函数
6. **cron 定时云函数单独**：超时订单自动退回等定时任务独立成函数，配定时触发器

### 公共模块（common.js）必须包含

- 统一响应：`ok(data)` → `{code:0, data, ok:true}`；`fail(msg, code)` → `{code, msg, ok:false}`
- 配置读取：platformConfig 缓存（30s 过期），佣金率归一化（0~1 范围校验，防配置错值）
- 管理员校验：checkAdmin(openid)
- 分页解析：parsePage（默认 20，上限 100）
- 内容安全：msgSecCheck（UGC 审核）
- 安全取集合：safeGet（集合不存在返回空，不抛错）

## 5. 切片计划（垂直切片，前端+云函数+数据库一起做）

**禁止“前端先行”或“后端先行”**——云开发的前后端是强契约，分开做必返工。按业务闭环垂直切片：

| 顺序 | 切片 | 完成标志 |
|---|---|---|
| 0 | 架构骨架 | 目录/配置/公共模块/设计系统就绪，空壳可编译 |
| 1 | 登录/用户体系 | 登录页 + auth 云函数 + users 集合权限，最小可跑 |
| 2 | 核心业务最小闭环（含支付） | 列表→详情→下单→校验→支付，第一个可演示版本 |
| 3 | 状态流转 + 回调幂等 + 用户订单列表 | 资金链路闭合 |
| 4 | 管理后台第一批（闭环必需） | 订单确认/退款/审核——必须和 1.0 一起交付 |
| 5 | 扩展业务切片 | 接单/提现/评价/邀请等（按需求） |
| 6 | 管理后台第二批（运营功能） | Banner/内容/看板，上线后按需 |

**管理后台判定标准**：只做“当前业务闭环离了它转不动”的功能，不做完整后台。第一批约占总工作量 20~30%。

## 6. 决策记录

每个架构取舍必须输出决策记录：

```
决策：___
选项：A（代价） / B（代价） / C（代价）
AI 建议：___
用户选择：___
理由：___
```
