# MiniMax H3 / 海螺 H3 专属提示词规范

> H3 的提示词和 Seedance/Sora 很不一样：**平台决定格式，五模式决定结构**。写错格式是「台词乱语/角色漂移/音效错位」的直接病因。

## 先判断平台（最重要，决定输出格式）

H3 是三段式系统：`H3-Context-IR（理解改写）→ H3-Base 768p（音视频生成）→ H3-Regenerate-2K（重生成）`。

| 用户在哪跑 | 输出格式 |
|-----------|---------|
| 海螺官网 / MiniMax API（Context-IR 在跑） | **中文自然语言**，只做决策补齐，不要手工结构化（会跟 Context-IR 打架） |
| 本地 ComfyUI / SGLang（无 Context-IR） | **完整英文结构化格式**，字段逐字精确（你就是 Context-IR） |
| 用户没说 | 必须问；有信号（ComfyUI/SGLang/显卡/工作流json → 本地；海螺官网/API/duration 参数 → API）则直接判定并声明 |

## 五模式判断

| 用户给了什么 | 模式 | 判断关键 |
|-------------|------|---------|
| 只有文字 | T2VA | — |
| 一张图，是画面第一帧 | I2VA | 图=视频真实起点 |
| 两张图，首+尾 | FL2VA | 优先单镜头连续插值 |
| 一张图，是画面最后一帧 | L2VA | 反推前置状态 |
| 参考图/视频/音频（角色/画风/音色/动作迁移） | Ref2VA | 图="长这样的角色"的语义参考 |

**最容易判错的一刀**：图是"某一帧画面本身"→ I2VA/FL2VA/L2VA；图是"角色长这样"→ Ref2VA。需要音色参考或角色开口对口型 → 只能 Ref2VA。

## 官方硬上限

官方原始指南已纳入本地：`references/18-minimax-h3-base-modes.md`（T2VA/I2VA/FL2VA/L2VA 与官方案例）、`references/19-minimax-h3-ref-official.md`（full-reference 标签、保留关系与完整示例）。

- 输出时长 4-15s，24 FPS，短边默认 768p（2K 需 Regenerate-2K）
- Ref2VA：图 ≤9、视频 ≤3 段（合计 ≤15s）、音频 ≤3 段（合计 ≤15s，**必须搭配图或视频，不能单独**）
- 混合输入 ≤12 个文件

## API 端：中文自然语言 + 决策补齐

职责不是给原话套电影术语，而是**替用户做掉没做的决策**：时长、模式、前 2 秒放什么、三层声音、参考素材分工。写清「镜头意图 + 声音层次 + 素材分工」，不要 `[Shot N]` 字段。

## 本地端：英文结构化格式

### 三核心字段（T2VA/I2VA/FL2VA/L2VA）

```
integrated_multimodal_description: [Shot 1] ...
overall_soundscape: ...
non_diegetic_music: ...
```

- `integrated_multimodal_description`：视觉/动作/镜头/说话人/对白/歌声/剧内音效
- `overall_soundscape`：环境音 + 动作音 + 非语言人声
- `non_diegetic_music`：观众才听到的配乐，写乐器/速度/力度变化，**禁写情绪词**，没有填 N/A

### 首帧/尾帧对齐指令（第一行）

I2VA 单图生视频的完整六段式逐字规范见 `references/17-minimax-h3-keyframe.md`；Ref2VA 全参考见 `references/16-minimax-h3-fullref.md`。

- I2VA：`For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.`
- FL2VA：`How the reference pictures align with the target video — Picture 1 (from Shot 1) aligns with the 0.00-second mark...; Picture 2 (from Shot N) aligns with the S.SS-second mark...`
- L2VA：`<Picture 1> (from [Shot N]) aligns with the S.SS-second mark of the target video.`

### 镜头写法

- 首镜 `[Shot 1]` 无时间戳，后续严格递增且 ≤ 片长
- `[Shot 2] At 00:03.500, the camera cuts to...`
- 风格锚定写 `[Shot 1]` 开头：`Live-action` / `2D-animated` / `3D CG` / `claymation` / `watercolor` / `vintage film`（Ref2VA 写在 Shot 1 之前独立成句）

### 运镜词表（只用官方词，不自造）

`Zoom In / Zoom Out`（变焦）、`Push In / Pull Out`（机位推拉）、`Pan Left/Right`、`Truck`、`Tilt`、`Pedestal`、`Arc Shot`、`Tracking Shot`、`Static Shot`、`Roll`、`Shake`、`POV`。可挂 `with small/large amplitude`、`at slow/fast speed`；中等幅度和常速省略。

## Ref2VA 六段结构（本地端逐字精确）

完整逐字写作规范（subject_definitions 写法、retention_analysis 保留关系、多人齐声编号、详细分镜七要素等）见 `references/16-minimax-h3-fullref.md`。

```
subject_definitions → summary → retention_analysis → detailed_description
→ overall_soundscape → non_diegetic_music
```

### 标签纪律

- `<Subject N>`：可复用的可见内容（人/物/场景/服装/风格/动作）
- `<Picture N>`：具体首帧/尾帧/分镜锚点
- `<Video N>`：整段视频关系（剪辑/续接/运镜节奏）
- `<Audio N>`：独立音频或音轨（音色/对白/BGM 风格）

`retention_analysis` 每标签一行，关系标记固定枚举：
- 视觉：`fully_preserved / partially_preserved / attribute_transfer / weak_reference`
- 音频：`fully_copy / partially_copy / reference / weak_reference`

`detailed_description` 生成类任务 **350-500 英文词**（台词密集时以装完台词时间线为准，不硬凑词数）。

### 声景三分家（不重复）

1. 环境音/动作音/非语言人声 → `overall_soundscape`
2. 台词/歌声/剧内音乐 → 主描述字段（`<d>[语言]</d>` 包台词，说话人 ID 稳定）
3. 观众才听得到的配乐 → `non_diegetic_music`

## 「我替你做了哪些决策」不能省

输出末尾必须列：时长定 Xs 因为什么、前 2 秒放什么、为什么没给配乐、其余默认项。用户下次才能给到更好的输入。

## 自检清单

- [ ] 平台确认，API 走人话 / 本地走结构化，没有混用
- [ ] 模式判断正确（图是"某一帧"还是"长这样"）
- [ ] 时长 ≤15s，素材未超官方上限
- [ ] 台词是用户逐字原文，没有编造
- [ ] 前 2 秒不是"缓缓推进"开场
- [ ] 三层声音各司其职、无重复
- [ ] 本地端字段名逐字正确，Ref2VA 六段顺序没错
- [ ] 运镜词全部来自官方词表
- [ ] 「我替你做了哪些决策」已写

## 来源

- [MiniMax-AI/MiniMax-H3 官方技能库](https://github.com/MiniMax-AI/MiniMax-H3/tree/main/skills/h3-prompt-writing)
- [HF MiniMaxAI/MiniMax-H3 模型卡](https://huggingface.co/MiniMaxAI/MiniMax-H3)
- 社区改写器：[ye4wzp/minimax-h3-prompt-skill](https://github.com/ye4wzp/minimax-h3-prompt-skill)
