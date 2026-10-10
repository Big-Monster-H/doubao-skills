# Negative Prompts

负面提示词按“通用 + 人物 + 风格”叠加。输出英文，附中文对照。

## 通用负面

所有模型/风格都加：

```text
low quality, worst quality, blurry, deformed, watermark, text, signature
```

中文：低质量、最差质量、模糊、畸形、水印、文字、签名。

## 人物额外负面

```text
bad anatomy, bad hands, missing fingers, extra digits
```

中文：解剖结构错误、手部错误、缺手指、多余手指。

## 按风格追加

### 动漫赛璐璐风

```text
realistic, 3d, photo, mature, sexy
```

中文：写实、3D、照片、成熟、性感。

### 写实 CG / 摄影风

```text
illustration, cartoon, anime, CGI look
```

中文：插画、卡通、动漫、CG 感。

### 水墨风

```text
photo, 3d, realistic, bright colors
```

中文：照片、3D、写实、鲜艳色彩。

## SD 完整负面示例（动漫人物）

```text
low quality, worst quality, blurry, deformed, watermark, text, signature, bad anatomy, bad hands, missing fingers, extra digits, realistic, 3d, photo, mature, sexy
```

中文对照：低质量、最差质量、模糊、畸形、水印、文字、签名、解剖结构错误、手部错误、缺手指、多余手指、写实、3D、照片、成熟、性感。

## MJ 使用说明

Midjourney 不直接使用“负面提示词”字段。可将词条转为 `--no` 参数，例如：

```text
--no text, watermark, signature, blurry
```

用户自行决定是否加，Skill 只负责给出可转换的词表。
