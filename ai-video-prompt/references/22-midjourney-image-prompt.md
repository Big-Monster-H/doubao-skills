# Midjourney 文生图提示词规范

> 用途：Stage A 生成关键帧/首帧/角色设定图时，如果用户用 Midjourney 出图，按本文件写提示词。生成的图再作为 Stage B 的图生视频首帧。

## 一句话原则

Midjourney 用「英文逗号短语 + 参数」描述画面，不用完整句子。结构：**主体 → 环境 → 构图 → 光影 → 风格 → 参数**。

## 基础公式

```
{主体：人物/角色/物体}, {环境与场景}, {构图与镜头}, {光影与色彩}, {风格}, {材质与细节} --ar {比例} --v {版本} --stylize {数值} --no {负面}
```

示例：
```
a young woman with long black hair in a high ponytail, dark gray fitted dance top and black wide-leg pants,
minimalist dance studio with light wooden floor and floor-to-ceiling mirror,
medium-full shot, low camera angle,
soft side backlight with gentle fill light,
cinematic realism, shallow depth of field, clean composition,
natural skin texture, visible fabric folds --ar 16:9 --v 6.1 --stylize 180 --no cartoon, 3d render, text, watermark
```

## 六要素拆解

| 要素 | 写法 |
|------|------|
| 主体 | 年龄、发型发色、五官、服装颜色与版型、配饰、体态 |
| 环境 | 空间结构、关键陈设、材质、主色、标志物、天气 |
| 构图 | 景别、角度、主体位置、负空间、对称/三分法 |
| 光影 | 光位、光质、色调、阴影、体积光 |
| 色彩 | 主色、辅助色、饱和度、对比度 |
| 风格 | 摄影/电影/动漫/3D/油画/水彩/极简等 |

主体与环境词汇优先从 `references/21-subject-action-sound-library.md` 和 `references/20-environment-style-library.md` 取，不空堆形容词。

## 常用参数

| 参数 | 说明 |
|------|------|
| `--ar 16:9` | 横屏；9:16 竖屏；1:1 方形 |
| `--v 6.1` / `--v 7` | 模型版本，按用户实际可用版本 |
| `--style raw` | 更接近真实摄影，减少默认美化 |
| `--stylize 0-1000` | 艺术化程度，写实人物建议 100-250 |
| `--chaos 0-100` | 出图多样性，首帧锁定建议 0-10 |
| `--no` | 负面：畸形手指、卡通、文字、水印等 |
| `--seed` | 固定种子，保持同角色多图一致性 |

## 人物一致性做法

多图保持同一角色时，固定角色描述短语 + `--seed`，只改动作/环境：
```
same character: a young woman with long black hair, a dark gray dance top, black wide-leg pants, white sneakers
--seed 123456 --ar 9:16
```

## 负面提示词（--no）

```
extra fingers, deformed hands, bad anatomy, cartoon, 3d render, plastic skin, over-smoothing, low resolution, text, watermark, signature
```

## 图生视频桥接

Midjourney 生成的图进入 Stage B 后：
1. 图作为首帧走 I2VA，不要重复整段 MJ 文生图提示词。
2. Stage B 只写从这张图开始的动作、运镜、时间轴、声音。
3. 人物外观沿用 Stage A 已锁定的描述，不新增、不改色、不改服装。
4. 目标模型是即梦/H3 时，图生视频提示词按对应方法论写，MJ 参数不进入视频提示词。

## 交付清单

- [ ] 主体、环境、构图、光影、风格五要素齐全
- [ ] 使用逗号短语，不是长句叙述
- [ ] 参数只写必要项：--ar 必写，--no 写具体伪影
- [ ] 人物一致性用了固定角色短语 + --seed
- [ ] 图中人物和环境可见细节足够，不写空泛词
- [ ] 进入图生视频时没有把 MJ 参数带进视频提示词
