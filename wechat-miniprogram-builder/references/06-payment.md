# 微信支付接入规范（API v2，含回调验签、退款、幂等）

> 默认使用微信支付 API v2（XML + MD5 签名 + p12 证书）。文件末尾附 v3 迁移要点。所有涉及钱的操作必须符合本规范。
> 具体接口路径、参数以微信支付官方最新文档为准，构建时核验。

## 1. 前置条件

- 商户号（mchid）、API 密钥（32 位，商户平台设置）、API 证书（p12/pem）
- 证书管理：证书只存在于云函数侧。**推荐环境变量注入 Base64**，云函数运行时写入 /tmp 使用；禁止打包进前端代码，禁止提交仓库
- 回调地址：`https://<envId>.service.tcloudbase.com/<http函数路径>/payNotify`，在商户平台配置

## 2. 统一下单（云函数实现，禁止前端直调支付接口）

流程：
1. 前端提交 orderId → 云函数校验订单归属 + 状态为 pending
2. **服务端重取价**（从订单记录读取金额，禁止信任前端金额）
3. 生成微信支付参数（mchid、appid、out_trade_no、total_fee(分)、notify_url、body、spbill_create_ip、nonce_str、sign）
4. MD5 签名：参数按键名 ASCII 升序排列，`key=...&key=API密钥`，MD5 后大写
5. 调 `https://api.mch.weixin.qq.cn/pay/unifiedorder`（v2）
6. 返回 prepay_id → 前端 `wx.requestPayment`（用小程序端二次签名参数）

签名算法（必须正确）：
```js
function generateSign(params, key) {
  const sorted = Object.keys(params).sort();
  let str = '';
  for (const k of sorted) {
    const v = params[k];
    if (v !== undefined && v !== null && v !== '' && k !== 'sign') str += k + '=' + v + '&';
  }
  str += 'key=' + key;
  return crypto.createHash('md5').update(str).digest('hex').toUpperCase();
}
```

## 3. 支付回调（payNotify）——资金安全核心

- [ ] **验签**：回调 XML 的 sign 必须用 API 密钥重新计算比对，失败直接拒绝并返回 FAIL
- [ ] **幂等**：以订单当前状态判断——已处理（paid）则直接返回成功，禁止重复入账/重复通知
- [ ] 校验金额一致：回调 total_fee 必须等于订单金额（分）
- [ ] 校验商户号一致：回调 mch_id 必须等于本商户号
- [ ] 校验 out_trade_no 对应订单存在
- [ ] 处理成功返回 `<xml><return_code>SUCCESS</return_code></xml>`；处理失败返回 FAIL（微信会重试）
- [ ] 所有分支写日志

## 4. 退款（需要证书的双向认证）

流程：
1. 校验身份 + 订单归属 + 状态可退（见状态机白名单）
2. 订单标记 `pending_refund`（人工审核）或直接调退款（按产品规则）
3. 使用 p12 证书创建 https.Agent（pfx + passphrase=商户号）
4. 调 `https://api.mch.weixin.qq.cn/secapi/pay/refund`
5. 退款结果写入订单 + statusLog + 日志

证书加载（云函数）：
```js
// 优先环境变量 Base64 → /tmp 写入；兜底函数目录本地文件
const certPath = '/tmp/apiclient_cert.p12';
fs.writeFileSync(certPath, Buffer.from(process.env.WXPAY_CERT_BASE64, 'base64'));
const agent = new https.Agent({ pfx: fs.readFileSync(certPath), passphrase: process.env.WXPAY_MCH_ID || '' });
```

## 5. 幂等设计（所有涉及钱的操作）

| 操作 | 幂等策略 |
|---|---|
| 支付回调 | 状态机：仅 pending → paid 一次 |
| 退款 | 状态 pending_refund/refunded 防重复；退款单号唯一 |
| 提现打款 | 提现单状态机 + 唯一流水号 |
| 邀请奖励 | 奖励发放记录集合 + 唯一性校验（一单/一人一次） |

原则：**先查状态再变更，条件更新 + updated===1，重复请求返回当前状态而非重复执行。**

## 6. 合规要点

- 费率：微信支付费率（如 0.6%）从商户平台确认，展示给用户时如实说明
- 退款时限/规则：按产品规则定义，用户端明示
- **虚拟支付（iOS）**：iOS 端虚拟商品/服务禁止使用微信支付（微信小程序虚拟支付限制）——如项目属虚拟服务，必须在架构阶段评估并明确告知用户 iOS 端的收款方案（跳转外部/H5/仅 Android 等），禁止交付后才发现
- 结算周期：商户平台结算规则如实告知

## 7. 测试要求

- 用 1 分钱（0.01 元）真实支付跑通：下单 → 支付 → 回调 → 状态变更 → 退款全链路
- 测试重复回调、金额不符、签名错误、商户号不符四类攻击

## 8. v3 迁移要点（留作扩展，不在默认范围）

- API v3 使用 RSA 签名（商户私钥 + 微信平台证书验签），请求头 `Authorization: WECHATPAY2-SHA256-RSA2048`
- 回调用 AES-256-GCM 解密 resource 字段
- 证书用 apiclient_key.pem（私钥）而非 p12；需证书序列号
- 迁移时机：v2 停用前完成；云函数内封装支付模块，切换时只改内部实现不改进口
