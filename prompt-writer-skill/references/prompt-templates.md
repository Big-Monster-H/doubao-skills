# Prompt Templates

## 模型适配总表

| 项目 | Midjourney | Stable Diffusion |
|---|---|---|
| 质量前缀 | 不加 | `masterpiece, best quality, ultra detailed, 8k,` |
| 渲染词 | 不加 | 按风格加 |
| 负面提示词 | 可给，用户自行转 `--no` | 直接输出英文负面词 |
| 参数后缀 | 不加 | 不加 |
| 输出语言 | 英文提示词 + 中文对照 | 英文提示词 + 中文对照 |

## 风格分支正/负面词

### 动漫赛璐璐风

- 正面：`official art, anime key visual, cel shading,`
- 负面：`realistic, 3d, photo,`

### 写实 CG 风

- 正面：`Unreal Engine 5, path tracing, octane render,`
- 负面：`illustration, cartoon, anime,`

### 写实摄影风

- 正面：`photorealistic, raw photo, film photography,`
- 负面：`illustration, cartoon, anime,`

### 水墨风

- 正面：`Chinese ink painting, sumi-e, wash painting,`
- 负面：`photo, 3d, realistic, bright colors,`

## 人物提示词结构

顺序：

1. 质量前缀（仅 SD）
2. 画风/渲染
3. 景别（upper body / full body / close-up）
4. 人数（1girl / 1boy / solo）
5. 外貌（发型、发色、眼睛、肤色）
6. 服装
7. 姿势/动作
8. 表情
9. 场景背景
10. 光影
11. 风格标签（moe / realistic / cinematic）

### 示例：动漫风可爱小女生

英文：

```text
masterpiece, best quality, ultra detailed, 8k,
official art, anime key visual, cel shading,
upper body, 1girl, solo,
pink twin tails, violet eyes, fair skin,
white lace pajamas,
sitting by a window, one hand holding a plush rabbit,
gentle smile,
cozy bedroom, soft morning light through curtains,
warm rim light, dreamy atmosphere,
moe
```

中文对照：高质量杰作、最佳质量、超细节、8k；官方立绘、动漫关键帧、赛璐璐上色；半身景、一名女孩、单人；粉色双马尾、紫瞳、白皙皮肤；白色蕾丝睡衣；坐在窗边、一手抱着兔子玩偶；温柔微笑；温馨卧室、晨光透过窗帘；暖色轮廓光、梦幻氛围；萌系。

## 场景提示词结构

顺序：

1. 质量前缀（仅 SD）
2. 画风/渲染
3. 构图（wide shot / aerial view / close-up）
4. 环境描述
5. 天气/时间
6. 光影
7. 调色/色调
8. 氛围词

### 示例：大草原黄昏

英文：

```text
masterpiece, best quality, ultra detailed, 8k,
photorealistic, raw photo, film photography,
wide shot,
endless grassland with a winding dirt road and distant lone tree,
dusk, clear sky with warm sunset glow,
low golden sunlight, long soft shadows,
warm amber and orange color grading,
serene, vast, cinematic
```

中文对照：高质量杰作、最佳质量、超细节、8k；照片级真实、原片质感、胶片摄影；全景；一望无际的草原、蜿蜒土路、远处孤树；黄昏、晴空与温暖落日余晖；低角度金色阳光、柔和长影；暖琥珀与橙色调色；宁静、辽阔、电影感。

## 引导提问选项库

### 时间
- A 白天
- B 黄昏
- C 夜晚
- D 阴天

### 天气
- A 晴
- B 雨
- C 雪
- D 雾

### 视角
- A 俯瞰
- B 平视
- C 仰视
- D 斜俯视

### 景别
- A 特写 close-up
- B 近景 upper body
- C 中景 medium shot
- D 全身 full body

### 发型
- A 短发
- B 双马尾
- C 长直发
- D 丸子头

### 发色
- A 黑
- B 金
- C 粉
- D 白/银

### 瞳孔色
- A 蓝
- B 紫
- C 金
- D 红

### 服装风格
- A 休闲
- B 制服
- C 古风
- D 礼服

### 姿势
- A 站姿
- B 坐姿
- C 动态动作
- D 背影

### 表情
- A 微笑
- B 冷淡
- C 惊讶
- D 悲伤

### 材质
- A 金属
- B 木质
- C 玻璃
- D 布料

### 光影方向
- A 正面光
- B 侧光
- C 逆光
- D 顶光

### 氛围
- A 温暖治愈
- B 冷清孤独
- C 神秘压抑
- D 明亮欢快

### 色调
- A 暖色调
- B 冷色调
- C 黑白
- D 高饱和

## 参考图意图确认

用户上传参考图时先确认，再写提示词：

- A 照着画一样的
- B 只参考风格
- C 在这张图基础上改
- D 参考构图
