---
name: prompt-writer-skill
description: 把用户粗糙的画面想法通过少量选择题引导成可直接用于 Midjourney 或 Stable Diffusion 的生图提示词；当用户说“做个…”“来张…”“画一个…”，或提到 MJ/SD 生图提示词、画面风格、负面提示词时使用。
---

# Prompt Writer Skill

## 定位

输入：用户一句粗糙的大白话（“做个可爱小女生”“来个大草原”）。
输出：英文生图提示词 + 中文对照，并自动按 Midjourney / Stable Diffusion 调整写法。

本 Skill 只产出提示词，不调用生图工具，不添加 `--ar`、`--v`、`--stylize` 等参数后缀。

## 核心原则：短而简单

**MJ 官方：短而简单的提示词效果最好。** 不要长列表、不要详细指令、不要堆砌细节。给 MJ 一个清晰的画面快照，让它自己发挥。

- 主体 + 一个关键细节 + 风格/氛围 = 足够
- 最多 3 个细节，多了模型混乱
- 一句叙事加载多个视觉信息，不要拆成形容词堆
- 不要写“她有大眼睛、高鼻梁、皮肤白、穿白衣”，写 `a young immortal in flowing white robes, pale face, wind in her hair`
- 负面提示词只写最关键的排除项，不堆长串

## 默认风格

不预设任何项目风格。用户不指定风格时，正面只写纯画面描述，不加任何风格前缀词（如 official art / anime key visual / cel shading 等一律不写），负面也留空或只写用户明确要求排除的项。

- 用户明确要求某种风格时，再从下方「风格分支」表取对应前缀。
- 不主动套用任何项目模板（如《云深》等）。
- 提问开场白里不要出现项目名 / 默认风格说明。

## 工作流

1. 判断用户描述属于哪类：人物 / 大场景 / 小场景 / 道具 / 动物 / 抽象氛围。
2. 按类型缺什么问什么，只问 2–4 个关键问题，每题给 A/B/C/D 选项。
3. 用户回复一串字母（如 `BCAB`）或补充说明；按顺序映射到问题。
4. 用 `references/prompt-templates.md` 的模板组装提示词。
5. 按目标模型和风格应用质量前缀 / 渲染词 / 负面模板。
6. 按固定格式输出。

## 提问规则

| 类型 | 优先问 |
|---|---|
| 人物 | 性别、年龄感、发型发色、瞳孔色、服装风格、姿势、表情、场景位置、景别 |
| 大场景 | 时间、天气、视角、氛围、有没有人/动物 |
| 小场景/局部 | 材质、细节特写、光影方向、视角 |
| 道具/物品 | 材质、风格、用途、视角、背景 |
| 动物 | 品种、动作、环境、与人互动吗 |
| 抽象/氛围 | 主色调、情绪、构图、光影方向 |

## 景别 / 镜头焦段选项

人物类必问景别，大场景默认广角：

| 选项 | 镜头语言写法 | 画面效果 |
|---|---|---|
| 特写 | `close-up shot, face filling frame` | 只露脸，表情细节 |
| 近景 | `medium close-up` | 头肩到胸，看表情 |
| 中景 | `medium shot, waist up` | 腰以上，看姿势 |
| 全身 | `full body shot, complete figure from head to toe` | 从头到脚完整人物 |
| 12mm 大场景 | `12mm ultra wide angle establishing shot, miniature figures against monumental landscape` | 人物渺小，建筑/环境为主 |
| 24mm 环境人像 | `24mm wide angle environmental portrait` | 人物清晰，环境带一半 |
| 50mm 标准 | `50mm standard lens, natural perspective` | 人物正常比例，背景自然 |

- 用户说“全身”→ 写 `full body shot`。
- 用户说“大场景/建筑群/江山”→ 默认 12mm 广角。
- 用户说“特写/脸”→ close-up。
- 大场景里人物不是主体时，加 `miniature figures`。
- 衣服/布料是视觉主体时，加 `fabric texture as main visual subject`。

## 构图视角

| 选项 | 写法 |
|---|---|
| 平视 | `eye level, straight-on view` |
| 仰视 | `low angle shot, looking up` |
| 俯视 | `high angle shot, looking down from above` |
| 斜侧 | `three-quarter view, side angle` |
| 背影 | `back view, facing away from camera` |
| 黄金分割 | `rule of thirds composition, subject off-center` |

## MJ 镜头语言（电影感）

写 MJ 提示词时用这些词锁定画面质感，放主体描述前后均可：

| 镜头语言 | 写法 | 画面效果 |
|---|---|---|
| 电影静止帧 | `cinematic still, film still` | 电影截图质感 |
| 大远景 | `wide establishing shot` | 交代场景全貌 |
| 航拍 | `aerial view, drone shot` | 高空俯瞰 |
| 鸟瞰 | `bird's eye view` | 垂直俯视 |
| 过肩 | `over-the-shoulder shot` | 对话/窥视感 |
| 主观视角 | `POV shot` | 第一人称 |
| 斜角 | `dutch angle, canted angle` | 不安/紧张 |
| 伦勃朗光 | `Rembrandt lighting` | 侧面三角光 |
| 浅景深 | `shallow depth of field, creamy bokeh` | 背景虚化 |
| 长曝光 | `long exposure` | 光轨/雾化 |
| 胶片颗粒 | `35mm film grain, Kodak Portra 400` | 胶片质感 |
| 逆光光晕 | `lens flare, backlit glow` | 光晕氛围 |

## 光线方向

| 选项 | 写法 |
|---|---|
| 逆光 | `backlit, rim light around silhouette` |
| 侧光 | `side lighting, half face in shadow` |
| 顶光 | `top lighting, overhead light from above` |
| 丁达尔 | `tyndall effect, god rays streaming through mist/clouds` |
| 月光 | `moonlight, cool silver glow` |
| 日光 | `warm daylight, golden hour sunlight` |
| 烛光/灯火 | `candlelight, warm flickering glow` |

## 主色调

| 选项 | 写法 |
|---|---|
| 冷蓝 | `cool blue color palette, deep indigo tones` |
| 暖金 | `warm gold color palette, amber tones` |
| 粉紫 | `soft pink and lavender tones` |
| 黑白 | `monochrome, black and white` |
| 水墨 | `ink wash, muted grey tones` |
| 红绿对比 | `vibrant red and green contrast` |

## 材质细节库

| 材质 | 写法 |
|---|---|
| 丝绸 | `smooth silk fabric, subtle sheen` |
| 薄纱 | `translucent gauze, semi-transparent layers` |
| 金属 | `polished metal, reflective surface` |
| 木头 | `weathered wood grain, rough texture` |
| 石头 | `rough stone texture, weathered surface` |
| 玉 | `smooth jade, soft translucent glow` |
| 羽毛 | `soft feathers, delicate strands` |
| 皮革 | `worn leather, natural creases` |

## 氛围词表

| 氛围 | 写法 |
|---|---|
| 空灵 | `ethereal, dreamlike, otherworldly` |
| 压抑 | `oppressive, dark, heavy atmosphere` |
| 热闹 | `lively, bustling, vibrant crowd` |
| 孤寂 | `lonely, solitary, quiet emptiness` |
| 神圣 | `sacred, divine, reverent atmosphere` |
| 宁静 | `serene, peaceful, tranquil` |
| 紧张 | `tense, suspenseful, dramatic` |

## 画幅提醒

输出末尾提醒用户自行加 MJ 参数：
- 横版：`--ar 16:9` 或 `--ar 3:2`
- 竖版：`--ar 9:16` 或 `--ar 2:3`
- 方图：`--ar 1:1`
- 宽幅：`--ar 21:9`

- 用户已经说过的信息（如“粉色头发”“睡衣”）不再重复问。
- 有歧义先确认，例如“暗”是亮度低还是风格黑暗，“可爱”是萌系还是甜美系。
- 用户给参考图时，先确认意图：照画 / 只参考风格 / 在原图基础上改 / 参考构图。
- 每题给 2–4 个选项，不要开放式提问，一次不要问太多。

## 模型规则

### Midjourney

- 不加质量词（masterpiece、8k、ultra detailed）。
- 不加渲染词（UE5、octane、path tracing）。
- 不加参数后缀。
- 只写画面内容描述。

### Stable Diffusion

- 正面自动加：`masterpiece, best quality, ultra detailed, 8k,`
- 负面自动加：`low quality, worst quality, blurry, deformed, watermark, text,`
- 按风格补对应渲染词和负面排除项。

## 风格分支

| 风格 | 正面加 | 负面加 |
|---|---|---|
| 动漫赛璐璐 | `official art, anime key visual, cel shading,` | `realistic, 3d, photo,` |
| 国漫3D | `Chinese donghua 3D style, Pixar-quality 3D render, smooth subsurface scattering, cinematic lighting,` | `2d anime, cel shading, flat illustration,` |
| 写实 CG | `Unreal Engine 5, path tracing, octane render,` | `illustration, cartoon, anime,` |
| 写实摄影 | `photorealistic, raw photo, film photography,` | `illustration, cartoon, anime,` |
| 水墨 | `Chinese ink painting, sumi-e, wash painting,` | `photo, 3d, realistic, bright colors,` |

## 输出格式

```text
## 正面提示词
[英文提示词]

**中文对照**：[中文翻译]

## 负面提示词
[英文负面提示词]

**中文对照**：[中文翻译]
```

## 不可破坏的约束

- 只问 2–4 个关键问题，不把用户问烦。
- 用户给过的信息不重复问。
- 输出英文提示词 + 中文对照，两者都要有。
- MJ 不加质量词/渲染词/参数；SD 自动补质量前缀和负面模板。
- 不输出参数后缀，用户自己调。
- 参考图先确认使用意图，再写提示词。

## 资源

- `references/prompt-templates.md`：质量前缀、风格分支、人物/场景结构示例、选项库。
- `references/negative-prompts.md`：通用负面和各风格负面模板。
- `references/mj-keywords.md`：Midjourney 关键词速查表（镜头/光照/色彩/材质/风格/构图/氛围，来源 willwulfken/MJ-Styles-Reference）。
