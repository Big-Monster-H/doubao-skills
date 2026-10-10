# MiniMax H3 I2VA 单图 Keyframe Completion 六段式规范

> 适用：MiniMax H3 单图生视频（I2VA，仅 Picture 1 作为首帧）。
> 这不是 U6 多图全参考（reference generation）任务。每张上传的图是具体帧锚点，不是并列参考素材。
> 前置：先读 references/13-minimax-h3.md 完成平台判断与五模式路由。

## 输出格式（严格 JSON）

只输出一个 JSON 对象，不要 markdown 围栏、不要解释、不要多余字段：

{
  "subject_definitions": ["每行一条参考内容的定义句"],
  "summary": "一段英文，以 [keyframe completion] 开头",
  "retention_analysis": ["每行一条参考内容的保留关系"],
  "detailed_description": "正文，含风格开场句与 [Shot N] 分镜，换行分隔",
  "overall_soundscape": "全片环境音与物理音",
  "non_diegetic_music": "只有观众能听到的配乐，没有则写 N/A"
}

## 通用写作规范

- 六段全部用英文书写。只有 <d> 里的台词/歌词，以及画面中可见的文字，保留原语言。
- 主体开口的完整格式是 <Subject N> (Sx) + 动作/语气 + <d>[Language] 台词</d>，三者缺一不可。
- Language 必须用英文语言全称，与 ref-en.txt 及页面 @ 对白一致，常用：Chinese / English / Korean / Japanese。
- 正确：<Subject 1> (S1) 开口说，<d>[Chinese] 师姐我终于找到你了。</d>；<Subject 2> (S1) turns toward the woman and says, <d>[English] Last summer, I went to my grandfather's house.</d>。
- 禁止只写 <d> 不带 <Subject N> (Sx)；禁止只写主体名不带 (S1)；禁止 zh、en、ja、ko、zh-CN。

## subject_definitions（必须包含帧锚点行）

- 必须包含帧锚点行，并写清该帧画面里实际看见的内容（构图、主体位置、服装、光线、环境），不要只写 "is the first frame"：
  <Picture 1> is the first frame of the target video, showing ...
- 另写主体身份锁定行：<Subject 1> is ... in <Picture 1>。对照帧画面写真实可见、能把该主体认出来的特征，通常 5-8 项：年龄感、发型发色与盘法、五官与妆容、肤色、服装款式/颜色/面料、配饰、体态。图里没有的不要编。官方短句只是句式，不是上限。
- 从首帧锁定身份后，后续镜头沿用同一标签，不要重新定义。
- 禁止把多张图写成并列 reference generation 素材。
- 禁止 summary 以 [reference generation] 开头，除非用户明确要求额外 reference 关系且与 keyframe 并存，此时用 [keyframe completion + reference generation]。

## summary

- 必须以 [keyframe completion] 开头。
- 说明视频从 <Picture 1> 首帧延续，以及动作、运镜、光线的变化。
- 不得引入白名单外的参考标签。
- 只写成片目标：类型、核心事件、时长意向、成片要达成的效果。不要复述素材清单。
- 任务类型按素材实际角色选，不要因为用户附了视频/音频就改成 video editing 或 audio reuse。
- 仅当用户明确要求剪辑、转场、特效、字幕、画中画、变速、混音、配乐替换时，才用 video editing / audio reuse。
- 任务类型只用官方枚举：keyframe completion / reference generation / video editing / video continuation / audio reuse / audio reference。纯文生视频额外允许 [text to video]。不要自造 first-frame-to-video 这类前缀。
- 本段不得引入新的参考标签。

## retention_analysis

- 只评已定义角色是否保留，不要把新动作、新剧情、新运镜当成保真损失。
- 每个已定义标签写一行：哪些定义特征被保留、哪些被改。特征未改时关系词用 fully_preserved，并点名被保留的特征。
- 可见内容用 fully_preserved / partially_preserved / attribute_transfer / weak_reference；音频用 fully_copy / partially_copy / reference / weak_reference。
- <Subject N> 写成 <Subject 1> (appears in [Shot 1], [Shot 3]): fully_preserved - ...
- <Picture N> 写它担任的角色而不是 appears in，例如 <Picture 2> ([Shot 1] first frame): fully_preserved - ...
- 本段不出现 (Sx) 说话人编号。
- 没有参考素材时按当前模式写一致性要求，不要编造参考标签。
- 本模式固定包含：
  <Picture 1> ([Shot 1] first frame): fully_preserved - ...
  <Subject 1> (appears in ...): partially_preserved 或 fully_preserved - ...（说明从首帧到尾帧/全程哪些特征保留、哪些变化）

## detailed_description（成片正文）

- 官方要求写细，不要压成剧情梗概或参考关系清单。
- 先用一到两句确立整体风格（画质、色调、镜头语言），再按播放顺序分镜。风格开场必须写在 [Shot 1] 之前。
- 每个镜头至少写清七件事：构图/景别、主体外观与在画面中的位置、环境与光线、动作与状态、运镜（类型、幅度、速度）、当前声音、参考内容具体在哪里生效。
- 重要 <Subject N> 第一次清楚出场时，把定义段锁定的外观落到这个镜头的可见画面里（位置 + 当前动作）；之后镜头沿用同一标签，不要重新定义标签含义。
- [Shot 1] 不带时间戳；之后 [Shot N] At MM:SS.mmm, ...，切点必须小于目标时长。
- 有人开口时必须同时写出：主体标签 + 说话人编号 + 对白语言和文字。官方格式：<Subject 1> (S1) ... <d>[Chinese] 台词。</d>
- (Sx) 按成片里实际发声顺序从 (S1) 起编，同一发声源全程复用；不要在 retention_analysis 里写 (Sx)。

### 多人齐声

- 用户原文或画面明显是多人同时说、齐声、一起喊、合唱同一句时，必须用复合说话人编号 (S1,S2)，不要并排写 (S1) (S2)。
- 正确：<Subject 1> and <Subject 2> (S1,S2) shout together, <d>[Chinese] 师姐我们一起去吧！</d>
- 中文叙述同样结构：<Subject 1> 和 <Subject 2> (S1,S2) 齐声说，<d>[Chinese] 师姐我们一起去吧！</d>
- 错误：<Subject 1> (S1) <Subject 2> (S2) 一起说 <d>[Chinese] ...</d>（这会被读成两个人先后开口）。
- (S1,S2) 里的编号必须是各人第一次单独开口时已经分好的号，这次只复用，不新分配；同一句只写一个 <d>。
- 先后对白仍各自写 <Subject N> (Sx) ... <d>...</d>。
- 画外音写成 <Subject N> (Sx) off-screen。对不上已定义主体时，用稳定音色描述 + (Sx)，例如 a young male narrator (S2)。
- 只有直接复用的 BGM/完整音轨里的唱词才用 <Audio N> 当声源，不要再编一个 (Sx)。

### 本模式额外要求

- [Shot 1] 必须写明从 <Picture 1> 起幅（the shot begins from <Picture 1>）。
- 从首帧延续动作与运镜，不要引用不存在的 <Picture 2>。
- 生成类任务按 350-500 英文词的信息量来写（中文输出时保持同等细节，不要因为换语言而变短）。对白密集时优先把台词时间线写完整。

## overall_soundscape

- 只写全片环境音与现场物理声，不要写观众听到的配乐。

## non_diegetic_music

- 只写观众听到、角色听不到的配乐；有配乐时写乐器、速度、动态，不要只写「轻快」或「悲伤」。没有配乐写 N/A。

## 台词完整性

- 完整台词只写在 detailed_description 的 <d> 里，不要在声音两段重复整句台词。
