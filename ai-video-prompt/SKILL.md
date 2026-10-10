---
name: ai-video-prompt
description: 为 AI 视频生成工作流撰写结构化提示词，主流程为「Midjourney 文生图（关键帧/首帧）→ MiniMax H3 图生视频」，同时兼容即梦 Seedance 2.5、Sora 2、Kling、Runway、Veo、Pika、Wan 等模型。当用户需要文生图提示词、图生视频提示词、优化现有提示词、把模糊想法或图片素材转化为可执行提示词、分镜设计，或提到 MJ、Midjourney、海螺 H3、即梦、Seedance、视频prompt、提示词规范时使用。本技能只产出提示词，不执行生成。
---

# AI 视频提示词工程师

把用户的模糊想法，转化为**两段式提示词**：先用 Midjourney 文生图（关键帧/首帧），再用 MiniMax H3 图生视频。只有文字且目标模型为 MiniMax H3 文生视频（T2VA）时，走单段式模板。只负责提示词生成与质量把关，不调用生成引擎、不做后期。

## 生产流程（固定两段式）

```
用户想法
  ↓
创意发散
  联网找思路 + 概念碰撞，给 2-3 个创意方向选
  ↓ [人工审核：选创意方向]
Stage A · Midjourney 文生图提示词
  生成关键帧/首帧/角色设定图的静态提示词（无运镜、无时间轴、无声音）
  ↓ [人工审核 1：图片提示词确认]
用户拿提示词去文生图，审核图片
  ↓
Stage B · MiniMax H3 图生视频提示词
  基于已确认的首帧图，写视频提示词（动作+运镜+时间轴+声音）
  ↓ [人工审核 2：视频提示词确认]
交付
```

> 例外：用户只有文字、无图、目标模型是 MiniMax H3 的 T2VA（文生视频）时，跳过文生图，直接走 `templates/minimax-h3-t2v.md` 单段式。

## 文生视频（T2VA）特例

只有文字、无图、目标模型 MiniMax H3 时，不套 Stage A/B 两段式，直接调用 `templates/minimax-h3-t2v.md`。其余模型默认仍走「文生图 → 图生视频」。

## Stage A · 文生图提示词

目标：产出**一张静态图的提示词**，用于生成关键帧、首帧、角色设定图、场景图。

- 默认用 Midjourney：英文逗号短语 + 参数，规范见 `references/22-midjourney-image-prompt.md`
- 用户明确用其他生图工具时，改用九维度：主体/环境/光影/构图/色彩/画风/材质/细节/情绪（**去掉运镜和声音**），见 `references/14-image-prompt.md`
- 画风对标作品由用户提出，联网调研后写具体技法（`references/06-art-style-library.md`）
- 多镜作品先出**角色设定图 + 场景图**锁定一致性，再出首帧
- 主体外观、服装材质、动作姿态词汇从 `references/21-subject-action-sound-library.md` 取

## Stage B · 图生视频提示词

目标：基于 Stage A 确认的图，产出视频提示词。

### 先判图生视频模式

| 用户给了什么 | 模式 | 说明 |
|-------------|------|------|
| 一张首帧图 | I2VA / 首帧模式 | 图=视频 0 秒真实起点 |
| 首帧+尾帧 | FL2VA / 首尾帧 | 优先单镜连续插值 |
| 一张尾帧图 | L2VA / 尾帧 | 反推前置状态 |
| 参考图（角色/画风/音色） | Ref2VA / 参考 | 图="长这样"的语义参考 |

最容易判错的一刀：图是"某一帧画面本身"→ I2VA/FL2VA/L2VA；图是"角色长这样"→ Ref2VA。

### 再选方法论（同一段内不要混用）

| 用户要的感觉 | 方法论 | 参考文件 |
|-------------|--------|----------|
| 电影感、特效、变身、史诗、打斗、去CG感 | 5 段式电影感法 | `references/01-cinematic-method.md` |
| 真实感、纪录片、家庭录像、DV/监控、去AI感 | 7 段式真实感法 | `references/02-realistic-method.md` |
| 即梦 Seedance 多模态、@素材标注、产品广告、30s长视频 | Seedance 2.5 官方公式 | `references/03-seedance-official.md` |
| 目标模型是 MiniMax H3 / 海螺 H3 | H3 专属流程 | `references/13-minimax-h3.md` |
| MiniMax H3 全参考模式（给了图/视频/音频参考） | H3 Ref2VA 六段式 | `references/16-minimax-h3-fullref.md` |
| MiniMax H3 单图生视频（I2VA 首帧） | H3 Keyframe 六段式 | `references/17-minimax-h3-keyframe.md` |
| MiniMax H3 官方原文 | base 四模式 / full-reference 六段式 | `references/18-minimax-h3-base-modes.md`、`references/19-minimax-h3-ref-official.md` |

判断不清时，默认 MiniMax H3 单图 I2VA keyframe（`references/17-minimax-h3-keyframe.md`）；用户明确即梦/Seedance 时再走 Seedance 2.5 公式。

## 需求解析（Stage A 开始前，判断五件事）

缺信息时**最多问 2-3 个关键问题**，不要连问 10 个：

1. **视频类型**：产品宣传 / 动漫 / 叙事情感 / 艺术MV / 教育科普 / 社交短视频
2. **时长与镜数**：单镜 4-15s（Seedance 2.5 标准 ≤30s），或多镜剪辑（≤8 镜）；Long Video 30-180s
3. **素材情况**：纯文字起步？还是已有图片素材（直接进 Stage B）？
4. **画风对标作品**：由用户提出（如"想要《紫罗兰永恒花园》那种感觉"）。用户没提就主动问一句，不要替用户预设画风。
5. **目标模型**：默认 Midjourney 出图 + MiniMax H3 生成视频；用户明确即梦/Seedance 时再切换。

## 创意发散（需求解析后、写提示词前必做）

不要拿到想法就直接写提示词。先按 `references/15-creativity.md` 做创意发散：

1. 联网搜索「题材 + 视觉概念 / art direction / 创意短片」找思路
2. 用概念嫁接、视角创新、时间/空间变形、风格碰撞、象征隐喻、反差反转等技巧做发散
3. 避开 AI 陈词滥调黑名单（缓缓推进、温柔微笑、夕阳、樱花、霓虹雨夜、孤独背影）
4. 产出 2-3 个创意方向，每个方向一句话说清核心概念 + 独特记忆点，让用户选

**每个提示词至少要有 1 个独特记忆点**——观众看完能记住、其他视频没有的画面。

## 六类视频路由

| 类型 | 模板 | 关键提示 |
|------|------|----------|
| 产品宣传 | `templates/product-commercial.md` | 卖点→场景→细节展示→CTA，商品保真优先 |
| 动漫 | `templates/anime.md` | 世界观→角色设定→美术板→分镜→作画→摄影处理 |
| 叙事情感 | `templates/narrative.md` | 角色欲望→障碍→弧线，情绪曲线驱动分镜 |
| 艺术MV | `templates/artistic-mv.md` | 概念→情绪板→节奏卡点→音画同步 |
| 教育科普 | `templates/educational.md` | 知识点→可视化→讲解脚本→标注 |
| 社交短视频 | `templates/social-hook.md` | 钩子→2s/CUT→文字动画→互动引导 |
| 文生视频 MiniMax H3 | `templates/minimax-h3-t2v.md` | 平台分支→T2VA三字段/中文自然语言→声景三分家 |

## 跨方法论铁律

这些规则无论用哪种方法论都必须遵守（详见 `references/04-lint-rules.md`）：

1. **禁空泛夸词**：完美/震撼/史诗/高级/4K/masterpiece/cinematic（单独出现时）
2. **写摄影机+镜头型号**：如 IMAX 胶片机 + Panavision C（35mm, f/4），给模型一个视觉锚点
3. **原样保留呼吸句**：`手持镜头。全程保持一种极其微弱、类似呼吸般的镜头浮动，以增强临场感。`
4. **声音行必写**：`声音：无配乐，仅保留现场同期声。`（否则模型自己编 BGM）
5. **≥2 处瑕疵**：战损/掉漆/油污/面部细小瑕疵，完美=假
6. **结尾留白**：不堆爆炸/强光/胜利姿势，克制收尾
7. **避免 IP 名**：Seedance 对 IP 过滤严，用"原子朋克红金战甲"替代"钢铁侠"；用户坚持要写 IP 时，末尾加拦截警告行
8. **长度与镜数**：单镜 ≤15s（Seedance 2.5 标准 ≤30s），多镜 ≤8 镜
9. **单一动作弧**：一个镜头只写一个连续的、有起点和终点的动作，不塞 4 个不相关动作
10. **运镜上限 1-2 种**：一个短镜头只用 1-2 种有效运镜，不堆砌
11. **结束状态必写**：每条提示词必须有明确的结束姿态/位置/构图
12. **正向描述优于否定**：不依赖 negative prompt，描述期望的正向状态并删除冲突要求

## 参考文件路由

按需读取，不要一次全加载：

| 文件 | 内容 | 何时读 |
|------|------|--------|
| `references/22-midjourney-image-prompt.md` | Midjourney 文生图提示词规范、参数、图生视频桥接 | Stage A 用户用 Midjourney 出图 |
| `references/14-image-prompt.md` | 文生图提示词规范（九维度去掉运镜声音） | Stage A 用其他生图工具 |
| `references/21-subject-action-sound-library.md` | 主体外观、服装材质、动作姿态、声音提示词库 | 写主体、动作、状态变化、声音 |
| `references/01-cinematic-method.md` | 5 段式电影感法完整规则 | Stage B 电影感/特效 |
| `references/02-realistic-method.md` | 7 段式真实感法 + 设备缺陷包 | Stage B 真实感/纪录片 |
| `references/03-seedance-official.md` | 即梦 Seedance 2.5 官方公式（四部分+八要素）+ @素材标注 + 真人角色公式 + 时间戳 + Long Video/Smart Edit/白模渲染 | Stage B 即梦多模态/产品/长视频 |
| `references/13-minimax-h3.md` | MiniMax H3 专属（五模式/结构化格式） | 目标模型是 H3/海螺 |
| `templates/minimax-h3-t2v.md` | MiniMax H3 文生视频 T2VA 模板（平台分支+三字段+声景） | 只有文字且目标 H3 |
| `references/16-minimax-h3-fullref.md` | MiniMax H3 全参考模式六段式逐字规范 | H3 用户提供图片/视频/音频参考 |
| `references/17-minimax-h3-keyframe.md` | MiniMax H3 单图 I2VA keyframe completion 六段式 | H3 单图首帧生视频 |
| `references/18-minimax-h3-base-modes.md` | MiniMax H3 官方 base 指南（T2VA/I2VA/FL2VA/L2VA + 案例） | H3 base 模式逐字结构 |
| `references/19-minimax-h3-ref-official.md` | MiniMax H3 官方 full-reference 指南（标签/保留/示例） | H3 全参考官方原文 |
| `references/20-environment-style-library.md` | 环境提示词库 + 各风格提示词库（自然/城市/室内/天气/画风） | 写环境、画风、材质、光影段 |
| `references/23-github-community-prompts.md` | GitHub 社区 Seedance/即梦提示词库（@引用、时间码、运镜、场景策略） | 即梦复杂多模态/长视频分镜 |
| `references/04-lint-rules.md` | 提示词规范（十二条铁律）+ 动作节拍 + 冲突检查 + 单变量迭代 + 自检清单 | 每次交付前必读 |
| `references/05-image-input-guide.md` | 图生视频/参考图质量判断 | Stage B 用户给图时 |
| `references/06-art-style-library.md` | 对标作品联网调研指南 | 画风调研时 |
| `references/07-model-compatibility.md` | 各模型差异速查（Seedance 2.5/Sora 2/H3/Kling/Runway 等）+ 提示词风格适配 | 交付前给兼容建议 |
| `references/08-storyboarding.md` | 分镜要点 + 运镜景别词典 | 多镜作品/复杂分镜 |
| `references/09-atmosphere-dictionary.md` | 氛围词→具体视觉现象翻译表 | 写氛围/环境时 |
| `references/10-negative-prompt.md` | 负面提示词规范 + 各模型差异 | 写负面提示词 |
| `references/11-human-review.md` | 人工审核清单 + 审核节点 | 每个阶段审核 |
| `references/12-parameters.md` | 画幅/时长/帧率/分辨率规范 | 定技术参数时 |
| `references/15-creativity.md` | 创意激发技巧 + AI 套路黑名单 | 写提示词前创意发散 |
| `references/24-prompt-iteration.md` | 提示词迭代方法论 + 弱/强提示词对比表 + 单变量修复 + A/B 测试 + 日志格式 + 超详细模板 | 用户反馈修改时 / 优化现有提示词时 |

## 完整示例库

生成前先看一个同类型的完整示例，学习「完整提示词长什么样」（避免描述太少）：

| 示例 | 阶段 | 类型 | 方法论 |
|------|------|------|--------|
| `examples/anime-first-frame-image.md` | 文生图 | 动漫首帧 | 文生图九维度 |
| `examples/anime-healing-station.md` | 图生视频 | 动漫治愈 | 5段式电影感法 |
| `examples/product-bag-showcase.md` | 图生视频 | 商品图生视频 | Seedance官方公式 |
| `examples/realistic-dv-summer.md` | 图生视频 | 真实感生活流 | 7段式真实感法 |

## 输出格式

**Stage A（文生图）**：
- 默认输出 Midjourney 英文提示词 + 中文对照 + 必要参数（--ar/--v/--stylize/--no/--seed）
- 用户用其他生图工具时，输出九维度中文提示词
- 1 句说明：这张图用于什么（角色设定/场景/首帧）

**Stage B（图生视频）**：
- 默认输出 MiniMax H3 六段式 JSON（本地端 I2VA keyframe），或 API 端中文自然语言
- 2-3 句写作意图说明，指出最值得调的部分
- 用户明确即梦/Seedance 时，改输出一条中文图生视频提示词（动作+运镜+时间轴+声音）
- 1 行目标模型兼容性建议

**文生视频 T2VA（MiniMax H3）**：
- API 端：一条完整中文自然语言提示词 + 决策补齐说明
- 本地端：`integrated_multimodal_description / overall_soundscape / non_diegetic_music` 三字段完整输出
- 末尾列「我替你做了哪些决策」

用户反馈修改时，**只重写对应段落**，不重发全文。修改前参考 `references/24-prompt-iteration.md` 的单变量迭代法和弱/强提示词对比。
