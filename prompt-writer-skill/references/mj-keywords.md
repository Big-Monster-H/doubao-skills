# Midjourney 关键词速查表

> 来源：willwulfken/MidJourney-Styles-and-Keywords-Reference（GitHub ⭐12.3k）
> 用途：写 MJ 提示词时按分类查关键词，直接复制使用。

## 1. 镜头 / 相机 / 胶片

| 类别 | 关键词 |
|---|---|
| 焦段 | `12mm ultra wide angle`, `24mm wide angle`, `35mm`, `50mm standard lens`, `85mm portrait`, `135mm telephoto` |
| 镜头效果 | `bokeh`, `shallow depth of field`, `deep depth of field`, `tilt-shift`, `macro photography`, `fisheye` |
| 胶片 | `Kodak Portra 400`, `Fujifilm Pro 400H`, `Cinestill 800T`, `Ilford HP5 black and white`, `Polaroid photo`, `35mm film grain` |
| 快门 | `long exposure`, `motion blur`, `freeze motion`, `slow shutter` |

## 2. 光照

| 类别 | 关键词 |
|---|---|
| 自然光 | `golden hour sunlight`, `blue hour`, `midday sun`, `moonlight`, `starlight`, `sunrise`, `sunset`, `backlit` |
| 人工光 | `candlelight`, `lantern light`, `neon light`, `chandelier light`, `spotlight`, `rim lighting` |
| 光效 | `god rays`, `tyndall effect`, `volumetric lighting`, `lens flare`, `crepuscular rays`, `dappled light through leaves` |
| 质感 | `soft diffused light`, `harsh shadows`, `low key lighting`, `high key lighting`, `dramatic chiaroscuro` |

## 3. 色彩 / 调色板

| 类别 | 关键词 |
|---|---|
| 冷调 | `cool blue tones`, `deep indigo`, `icy cyan`, `monochrome blue` |
| 暖调 | `warm gold tones`, `amber`, `sepia`, `warm sunset orange` |
| 对比 | `complementary colors`, `vibrant red and teal`, `orange and blue contrast`, `split complementary` |
| 情绪色 | `pastel dreamy tones`, `moody dark tones`, `high saturation`, `desaturated muted tones`, `earth tones` |

## 4. 材质 / 纹理

| 类别 | 关键词 |
|---|---|
| 布料 | `silk`, `satin`, `linen`, `velvet`, `chiffon`, `brocade`, `leather`, `denim`, `wool` |
| 金属 | `polished gold`, `brushed silver`, `oxidized copper`, `bronze patina`, `chrome`, `rusted iron` |
| 石头/木 | `weathered marble`, `granite`, `rough sandstone`, `ancient oak`, `cedar wood grain`, `bamboo` |
| 透明/发光 | `translucent glass`, `frosted crystal`, `glowing aura`, `bioluminescent`, `iridescent`, `holographic` |
| 自然 | `mossy texture`, `wet stone`, `snow dust`, `sand particles`, `water droplets` |

## 5. 艺术风格 / 流派

| 类别 | 关键词 |
|---|---|
| 古典 | `oil painting, Renaissance style`, `Baroque lighting`, `Art Nouveau`, `Impressionist brushstrokes`, `Ukiyo-e woodblock print` |
| 现代 | `Art Deco`, `Bauhaus`, `pop art`, `graffiti art`, `minimalist`, `surrealism`, `Dada` |
| 数字/3D | `Unreal Engine 5 render`, `octane render`, `blender cycles`, `cinematic 3D render`, `voxel art`, `low poly` |
| 国风 | `Chinese ink wash painting`, `gongbi detailed brushwork`, `shan shui landscape`, `traditional Chinese painting` |
| 动漫 | `Studio Ghibli style`, `Makoto Shinkai sky`, `Kyoto Animation style`, `anime key visual`, `cel shading` |

## 6. 构图 / 视角

| 类别 | 关键词 |
|---|---|
| 视角 | `bird's eye view`, `worm's eye view`, `eye level`, `Dutch angle`, `over-the-shoulder`, `POV shot` |
| 构图 | `rule of thirds`, `symmetrical composition`, `leading lines`, `framing within framing`, `negative space`, `centered composition` |
| 透视 | `one-point perspective`, `two-point perspective`, `isometric view`, `forced perspective` |

## 7. 氛围 / 情绪

| 类别 | 关键词 |
|---|---|
| 静谧 | `serene and peaceful`, `quiet solitude`, `meditative atmosphere`, `calm stillness` |
| 神秘 | `mysterious and enigmatic`, `ethereal otherworldly`, `dreamlike haze`, `mystical aura` |
| 史诗 | `epic grand scale`, `awe-inspiring`, `monumental`, `sweeping vista` |
| 动感 | `dynamic action pose`, `motion energy`, `swirling movement`, `explosive energy` |
| 孤独 | `lonely figure`, `vast emptiness`, `isolation`, `melancholic mood` |

## 8. 镜头运动（视频用）

| 类别 | 关键词 |
|---|---|
| 推/拉 | `slow push in`, `dolly zoom out`, `tracking shot forward` |
| 摇 | `pan left`, `pan right`, `tilt up`, `tilt down` |
| 跟 | `tracking shot following`, `steadicam walk`, `handheld shake` |
| 环绕 | `arc shot around subject`, `360-degree orbit` |

## 9. MJ 参数提示

| 参数 | 用途 |
|---|---|
| `--ar 16:9` | 横版电影感 |
| `--ar 9:16` | 竖版手机壁纸 |
| `--ar 1:1` | 方图/头像 |
| `--ar 21:9` | 超宽幅电影 |
| `--no xxx` | 排除元素 |
| `--stylize 100-1000` | 风格化强度 |
| `--chaos 10-50` | 多样性 |

## 写法顺序

MJ 提示词按这个顺序写效果最好：

```
[镜头焦段] + [主体] + [动作/姿势] + [服装/材质] + [场景/环境] + [光照] + [色彩] + [艺术风格] + [氛围]
```

示例：
`24mm wide angle, a young cultivator girl, silver-blue hair flowing, white silk robes, bamboo forest path, golden hour backlight, cool blue tones, Chinese ink wash style, serene atmosphere`

## 高分提示词写法（从实际案例提炼）

### 一句话一个信息层

不要堆成一长串，每个句子写一个信息：

```
a digital painting of a female anime character with cat ears in a dynamic, swirling pose.
she wears an elaborate, layered hanfu garment made of translucent, flowing fabrics in cream, gold, and blue.
her dark hair blows in the wind around her pale face as she looks back over her shoulder with a gentle smile.
the lighting is soft and warm, with a blurred, pastel background.
```

顺序：主体是谁 → 穿什么材质 → 头发/动作 → 表情 → 光线 → 背景。

### 主动控制焦外

| 写法 | 效果 |
|---|---|
| `face in soft focus` | 面部柔焦 |
| `some in focus and others blurred` | 部分对焦部分虚化 |
| `blurred, pastel background` | 背景模糊粉彩 |
| `shallow depth of field` | 浅景深 |

### 光的落点

不要只写“soft lighting”，要写光打在哪里：

```
soft warm light illuminates the scene, casting highlights on her face, hair, and the surrounding flowers.
```

`casting highlights on [A], [B], and [C]` —— 列出来光打在哪几个物体上。

### 动态词

| 写法 | 效果 |
|---|---|
| `dynamic, swirling pose` | 动态旋转姿势 |
| `hair blows in the wind` | 头发被风吹 |
| `ribbons trailing in the wind` | 飘带在风中拖曳 |
| `billowing fabric` | 布料翻涌 |

### 结尾锁定构图

最后一句直接锁景别和构图：

```
the composition is a close up shot focusing on the character's face and upper body.
```

### 材质叠加

| 写法 | 效果 |
|---|---|
| `translucent, flowing fabrics` | 透明流动面料 |
| `swirling metallic and glass-like textures` | 旋转金属玻璃质感 |
| `layered` | 多层叠加 |
| `subtle embroidered patterns faintly shimmering` | 隐约浮动刺绣 |

## 官方规则与最佳实践（2025）

### 官方核心规则

- **短而简单最好**：不要长列表和详细指令，会让模型混乱。一句话快照你的想法。
- **用具体同义词**：不说 big，说 huge / gigantic / enormous；不说 beautiful，说 luminous / ethereal / radiant。
- **单数优于复数**：写 `a cat` 比 `cats` 效果好。
- **不用否定句**：写 “not scary” 模型反而会 focus 在 scary 上。用正向描述。
- **语法要正确**：清晰语法比碎片化拼写效果好。

### 结构公式

```
[Subject] [Action/Pose] [Details] [Style/Mood] [Lighting] [Parameters]
```

### 三个细节上限

- 最多3个细节，多了模型处理不过来。
- 一句叙事加载多个视觉信息：`hunched over a candlelit desk` 同时给了姿势、光线、场景、比例关系。

### 引用参考

- 艺术家/电影/摄影技法直接写名字：`Rembrandt lighting`、`Japanese woodblock print`、`Wes Anderson composition`。
- 约束用参数：`--ar`、`--no`、`--stylize`。

### 常见错误

| 错误 | 修正 |
|---|---|
| 写一长串逗号 | 拆成短句，一句一个信息 |
| 写 “not blurry” | 写 “sharp focus, crisp details” |
| 写 “beautiful girl” | 写 “a young woman with luminous eyes and delicate features” |
| 写 “dark” | 写 “moody low-key lighting, deep shadows” |
| 复数名词 | 改单数 |
