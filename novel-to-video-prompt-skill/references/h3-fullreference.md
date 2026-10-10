# MiniMax H3 全参考模式（Full-Reference）六段式 JSON 规范

> 适用：用户上传了角色/场景/道具参考图，要生成对齐参考图的视频。
> 输出：一个 JSON 对象，六个字段，全英文（台词和画面文字保留原语言）。

## 输出结构（严格 JSON）

```json
{
  "subject_definitions": ["每行一条参考内容的定义句"],
  "summary": "一段英文，以方括号任务类型前缀开头",
  "retention_analysis": ["每行一条参考内容的保留关系"],
  "detailed_description": "正文，含风格开场句与 [Shot N] 分镜，换行分隔",
  "overall_soundscape": "全片环境音与物理音",
  "non_diegetic_music": "只有观众能听到的配乐，没有则写 N/A"
}
```

## 写作规范

- 六段全部用英文书写。只有 `<d>` 里的台词/歌词，以及画面中可见的文字，保留原语言。
- 主体发声的完整格式：`<Subject N> (Sx) + 思维配音句式 + <d>[Language] 台词</d>`，三者缺一不可。
- Language 必须用英文语言全称：Chinese / English / Korean / Japanese。禁止 zh、en、ja、ko、zh-CN。
- 正确示例：
  - `<Subject 1> (S1) says in an off-screen voiceover, while their lips remain completely closed, <d>[Chinese] 师姐我终于找到你了。</d>`
  - `<Subject 2> (S1) looks toward the woman and says in an off-screen voiceover, while his lips remain completely closed, <d>[English] Last summer, I went to my grandfather's house.</d>`
- 禁止只写 `<d>` 不带 `<Subject N> (Sx)`；禁止只写主体名不带 `(S1)`；禁止只写 says 却不写 lips remain completely closed。

## 字段详解

### subject_definitions（身份锁定段）

标签含义 + 参考角色 + 需要跟随的主要特征。每行一句。

人物/生物写真实可见、能把该主体认出来的特征，5–8 项：年龄感、发型发色与盘法、五官与妆容、肤色、服装款式/颜色/面料、配饰、体态与标志性姿态。图里没有的不要编。

场景写空间结构、关键陈设与材质、主色、标志物、光线与天气，不要只写「雪景」「房间」。

人物定义示例：
`<Subject 1> is the young woman in <Picture 1>, with long dark hair falling over one shoulder, a pale complexion, a blue knit cardigan over a white blouse, and a thin silver necklace.`

场景定义示例：
`<Subject 1> is the coffee-shop environment in <Picture 1>, featuring an exposed brick wall, an orange tufted sofa with patterned pillows, a neon sign, and a wooden coffee table.`

服装、道具、风格若被单独跟踪，各自成行；仅用于定义人物的图不要单独立 `<Picture N>`。多素材定义同一主体时合并成一句，说明各素材分别提供外观、动作还是音色。

### summary

一段英文，以方括号任务类型前缀开头。只写成片目标：类型、核心事件、时长意向、成片要达成的效果。不要复述素材清单。

任务类型枚举（按素材实际角色选）：
- `keyframe completion`：首帧完成
- `reference generation`：参考生成
- `video editing`：剪辑（仅用户明确要求剪辑/转场/特效/字幕/画中画/变速/混音/配乐替换时用）
- `video continuation`：视频续写
- `audio reuse`：音频复用
- `audio reference`：音频参考
- 纯文生视频额外允许 `[text to video]`

不要自造前缀（如 first-frame-to-video）。

### retention_analysis

每行一条已定义标签的保留关系。特征未改时用 `fully_preserved`，并点名被保留的特征。

可见内容枚举：`fully_preserved` / `partially_preserved` / `attribute_transfer` / `weak_reference`。
音频枚举：`fully_copy` / `partially_copy` / `reference` / `weak_reference`。

`<Subject N>` 写法：`<Subject 1> (appears in [Shot 1], [Shot 3]): fully_preserved - ...`
`<Picture N>` 写法：`<Picture 2> ([Shot 1] first frame): fully_preserved - ...`

本段不出现 `(Sx)` 说话人编号。不把新动作、新剧情、新运镜当成保真损失。

### detailed_description（成片正文）

先用一到两句确立整体风格（画质、色调、镜头语言），再按播放顺序分镜。风格开场必须写在 `[Shot 1]` 之前。

每个镜头至少写清七件事：
1. 构图/景别
2. 主体外观与在画面中的位置
3. 环境与光线
4. 动作与状态
5. 运镜（类型、幅度、速度）
6. 当前声音
7. 参考内容具体在哪里生效

重要 `<Subject N>` 第一次清楚出场时，把定义段锁定的外观落到这个镜头的可见画面里。之后沿用同一标签，不要重新定义。

时间戳：`[Shot 1]` 不带时间戳；之后 `[Shot N] At MM:SS.mmm, ...`，切点必须小于目标时长。

### 镜数规则

H3 每镜需要 2.5–4.0 秒呼吸空间。按时长卡镜头数（含 Shot 1）：
- 4.0–6.0 秒：最多 1–2 镜
- 7.0–10.0 秒：最多 2–3 镜
- 11.0–15.0 秒：最多 3–5 镜

禁止 1 秒碎切，禁止一参考一镜的孤立幻灯片。多主体必须同框调度（前景/中景/后景）。

### 思维配音（默认）

有人说话时默认用思维配音法——声音是角色脑海中的思维声，观众听得见，画面里的嘴保持完全闭合。

完整格式：
`<Subject N> (Sx) says in an off-screen voiceover, while their lips remain completely closed, <d>[Language] 台词。</d>`

中文叙述同样结构：
`<Subject 1> (S1) 以画外思维配音说出，嘴唇始终完全闭合，<d>[Chinese] 台词。</d>`

只有用户明确要求对口型、开口说话、唇形同步时，才改回 `<Subject N> (Sx) says, <d>…</d>` 的开口句式。

`(Sx)` 按成片里实际发声顺序从 `(S1)` 起编，同一发声源全程复用。

多人齐声用 `(S1,S2)` 复合编号。对不上已定义主体的旁白，用稳定音色描述 + `(Sx)`。

### overall_soundscape

全片环境音与现场物理声。不写配乐，不重复整句台词。

### non_diegetic_music

只有观众能听到的配乐。写乐器、速度、动态。没有写 `N/A`。

## 输出模板

```
[reference generation] …（一句话说明目标视频和参考关系，英文）

retention_analysis:
<Subject 1> (appears in [Shot 1]): fully_preserved - …（保留了哪些特征）
<Subject 2> (appears in [Shot 1]): fully_preserved - …（保留了哪些特征）
<Subject 3> (appears in [Shot 1]): fully_preserved - …（保留了哪些特征）
<Subject 4> (appears in [Shot 1]): fully_preserved - …（保留了哪些特征）

detailed_description:
The target video is in a … style.（一到两句风格开场）
[Shot 1] …（构图、主体外观与位置、环境光线、动作、运镜、当前声音）
[Shot 2] At 00:01.500, …（切到什么画面，发生了什么）
[Shot 3] At 00:03.000, …（切到什么画面，发生了什么）

overall_soundscape:
…（全片的环境音与物理音）

non_diegetic_music:
N/A
```
