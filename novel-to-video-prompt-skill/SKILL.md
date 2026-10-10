---
name: novel-to-video-prompt-skill
description: 把用户粘贴的小说片段直接转成 MiniMax H3 或即梦 Seedance 2.5 视频提示词；豆包自己当导演分镜、标注台词/旁白/内心独白、@角色与场景并写音效，不需要用户填 API Key。当用户提到“小说转视频”“文字转视频提示词”“H3”“Seedance”时使用。
---

# Novel to Video Prompt Skill

## 定位

输入：用户自己分好段的一段小说文字（几十字到几千字）。
输出：可直接复制到 H3 或 Seedance 2.5 平台跑视频的提示词。

核心原则：豆包当导演，不做文本扩写，不改台词，不自动拆长文本。

## 使用方式

1. 用户直接在对话里粘贴一段小说原文，并说明目标模型（H3 或 Seedance 2.5；没说时默认问一句，或按上下文判断）。
2. 豆包按 `references/llm-system-prompt.md` 里的导演指令直接分镜。
3. 按 `references/model-formats.md` 里对应模型的官方格式输出提示词。
4. 用户复制输出，去对应平台跑视频。

> 可选：`web/index.html` 是一个纯前端工具，适合用户想在浏览器里自己接第三方 LLM API 时使用。**默认不走这条路**，直接由豆包执行即可。

## 官方格式结论

| 目标模型 | 默认输出 |
|---|---|
| MiniMax H3（有参考图，中文自然语言） | 开头 `@角色 @场景` 语义占位 + 总概念 + 时长/24FPS + 前2秒 + 视觉（只写动作）+ 镜头 + 声音；**不写 `[Shot N]` 字段** |
| MiniMax H3（全参考模式，上传角色/场景参考图） | 六段式 JSON：`subject_definitions / summary / retention_analysis / detailed_description / overall_soundscape / non_diegetic_music`，见 `references/h3-fullreference.md` |
| 即梦 Seedance 2.5 | 官方四段式：`@角色 @场景` + 一句话概括 + 时间戳情节 + 全局补充 + 音效 + 时长 |

H3 若在本地 ComfyUI / SGLang 跑，则改用英文三字段 `integrated_multimodal_description / overall_soundscape / non_diegetic_music`，见 `references/model-formats.md`。

## 时长基准

- H3：**4–15 秒**，24FPS。默认按内容密度取 5–10 秒。
- Seedance 2.5：标准 **4–30 秒**；Long Video 模式 30–180 秒。默认按短片段 5–12 秒处理，对话多可到 15–20 秒。
- 一段文字明显超过单条视频可承载的信息量时，不要硬拆，提示用户再分短一点。

## 输出必须包含

每个镜头必须写清：

- 画面描述（场景、人物动作）
- 景别（远/全/中/近/特）
- 运镜
- 时间点（Seedance 用 `0-3s` 区间；H3 API 用“前2秒/视觉/镜头/声音”自然叙述）
- 台词（有则嵌在对应镜头里）
- 音效

文本类型标注：

| 类型 | 标注 |
|---|---|
| 对话台词 | 直接嵌在镜头里，保持原文 |
| 旁白 | `旁白：xxx` |
| 内心独白 | `（内心）xxx` |
| 纯环境空镜 | 不标台词，直接写画面 |

参考图：

- 默认假设用户会上传参考图。开头写语义占位 `@云溪`、`@云城街道`，用户上传素材后替换成平台实际的 `@图片1` / `@图片2`。
- 因为有参考图，视觉部分**只写动作和事件**，不重复描述角色外貌、服装、场景细节——那些参考图里已有。

声音：只写音效，不写音乐。

## 不可破坏的约束

- 台词是原文，不改写。
- 用户自己分段，豆包不自动拆长文本；文本明显太长时提示用户先分段。
- 音效要写，音乐不要。
- 不写风格描述（画风/色调），全靠参考图。
- 默认有参考图：开头写 `@角色 @场景` 语义占位；视觉只写动作和事件，不重复外貌/场景细节。
- H3 海螺 API 不手工结构化，Seedance 按官方四段式输出。
- 多人对话时豆包自行分镜，不行的用户自己改。
- 角色动作连续性豆包不负责，由视频模型处理。

## 文件结构

```text
novel-to-video-prompt-skill/
├── SKILL.md
├── references/
│   ├── llm-system-prompt.md   # 导演核心指令（豆包直接执行）
│   ├── model-formats.md       # H3 / Seedance 2.5 格式差异
│   └── h3-fullreference.md    # H3 全参考模式六段式 JSON 规范
└── web/
    └── index.html             # 可选纯前端工具（用户自接 API 时用）
```

## 模型格式维护

格式有平台更新时，只改 `references/model-formats.md`。更深入的 H3/Seedance 官方规则可参考本机 `ai-video-prompt` skill，但本 skill 保持可直接使用的最小格式。
