# MiniMax H3 文生视频模板（T2VA）

> 适用：只有文字、无图片，直接从文字生成视频。
> 前置：先读 `references/13-minimax-h3.md`。有图不要走 T2VA，改走 I2VA / FL2VA / L2VA / Ref2VA。

## 路由速判

| 输入 | 模式 |
|------|------|
| 只有文字 | T2VA（本模板） |
| 一张首帧图 | I2VA |
| 首帧+尾帧 | FL2VA |
| 一张尾帧图 | L2VA |
| 参考图/视频/音频 | Ref2VA |

## 平台先判，否则整段重写

| 用户在哪跑 | 输出格式 |
|-----------|---------|
| 海螺官网 / MiniMax API（有 Context-IR 理解改写） | **中文自然语言**，只做决策补齐，不手工结构化 |
| 本地 ComfyUI / SGLang（无 Context-IR） | **英文结构化三字段**，你就是 Context-IR |
| 用户没说 | 必须问；有 `ComfyUI/SGLang/工作流json/显卡` 信号 → 本地，有 `duration/API` 信号 → API |

## 官方硬上限

- 时长 4-15s，24 FPS，短边 768p；2K 需 Regenerate-2K
- T2VA 无参考图，禁止写 `@图片N`
- 台词必须是用户逐字原文，不代写、不改写

## 决策补齐（T2VA 必须替用户定四件事）

1. 时长：默认 10s，动作/台词多则 12-15s
2. 前 2 秒放什么：不要写「缓缓推进/温柔微笑」开场，写一个立即发生的事件
3. 声音三层：环境音 / 动作音 / 配乐，各司其职、不重复
4. 风格锚定：`Live-action` / `2D-animated` / `3D CG` / `claymation` / `watercolor` / `vintage film`，写进 Shot 1 开头

## API 端输出模板（中文自然语言）

```
{一句话总概念}。

时长：{10}s，{24}FPS。

前2秒：{立即发生的事件，不是空镜}。
视觉：{主体+动作+环境+光影+画风，按时间顺序写}。
镜头：{只用官方运镜词，1-2 个镜头即可，不用自造词}。
声音：环境音{具体环境声}；动作音{具体动作声}；{无配乐 / 配乐{乐器+速度+力度变化，不写情绪词}}。
```

## 本地端输出模板（英文结构化）

```
[Shot 1] Live-action. {风格锚定 + 场景 + 主体 + 动作}。

integrated_multimodal_description: [Shot 1] {视觉/动作/镜头/说话人/对白/剧内音效}。 [Shot 2] At 00:SS.SSS, the camera cuts to {下一镜内容}。

overall_soundscape: {环境音 + 动作音 + 非语言人声}。

non_diegetic_music: {乐器/速度/力度变化；没有填 N/A}。
```

说明：
- T2VA 无首帧/尾帧，**不写** `<Picture N>` 对齐行。
- 首镜 `[Shot 1]` 无时间戳；后续时间戳严格递增且 ≤ 片长。
- 多镜最多写清楚 2-3 个关键镜头，不要堆 8 镜导致每镜失控。

## 台词 / 歌声格式

- 台词用 `<d>[语言]</d>` 包裹，说话人 ID 稳定，例如 `<d>[Chinese] 你来了。</d>`
- 歌声同样进入 `integrated_multimodal_description`，不放进 `non_diegetic_music`
- 音色参考必须走 Ref2VA，T2VA 只能描述声音类型，不能锁具体音色

## 官方运镜词表（只用这些）

`Zoom In / Zoom Out`、`Push In / Pull Out`、`Pan Left / Pan Right`、`Truck`、`Tilt`、`Pedestal`、`Arc Shot`、`Tracking Shot`、`Static Shot`、`Roll`、`Shake`、`POV`

可挂幅度/速度：`with small/large amplitude`、`at slow/fast speed`；中等幅度和常速省略。

## 声景三分家（不重复）

1. 环境音 / 动作音 / 非语言人声 → `overall_soundscape`
2. 台词 / 歌声 / 剧内音乐 → `integrated_multimodal_description`
3. 观众才听得到的配乐 → `non_diegetic_music`

## 快速示例

### API 端中文版（10s 橘猫）

```
一只橘猫在窗台伸懒腰的治愈片段。

时长：10s，24FPS。

前2秒：橘猫前爪按在木窗台上，身体向后拉长，尾巴翘起。
视觉：午后暖光斜照进厨房，橘猫伸完懒腰后收回身体坐好，眯眼看窗外的树叶晃动。写实摄影质感，浅景深，木窗台与白色纱帘清晰。
镜头：Static Shot，末尾缓慢 Push In 到猫脸。
声音：环境音有远处鸟叫和轻微风声；动作音有猫爪摩擦木头的轻响；无配乐。
```

### 本地端英文版（10s 橘猫）

```
[Shot 1] Live-action. A warm kitchen windowsill in late afternoon sunlight; an orange tabby cat stretches its front paws on the wooden sill, tail raised.

integrated_multimodal_description: [Shot 1] The orange tabby presses its front paws onto the wooden windowsill and stretches its body backward, tail curling upward. After the stretch it sits back down, narrows its eyes, and watches leaves moving outside the window. [Shot 2] At 00:06.500, the camera slowly pushes in toward the cat's face.

overall_soundscape: distant birdsong and light wind; faint sound of cat paws rubbing against the wooden sill.

non_diegetic_music: N/A
```

## 交付清单

- [ ] 平台已判定：API 中文人话 / 本地英文结构化，没有混用
- [ ] 模式确认是 T2VA，无图，未写 `@图片N`
- [ ] 时长 4-15s、24FPS，已明确写在前 2 秒决策
- [ ] Shot 1 开头有风格锚定词
- [ ] 台词逐字原文，`<d>[语言]</d>` 包裹，未编造
- [ ] 三层声音各司其职、无重复，`non_diegetic_music` 没有情绪词
- [ ] 运镜词全部来自官方词表
- [ ] 末尾已列「我替你做了哪些决策」
