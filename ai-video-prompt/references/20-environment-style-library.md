# 环境与风格提示词库

> 用途：写 Stage A 的「环境 / 画风 / 材质 / 光影」段，或 Stage B 的场景延续与风格锚定。具体组织仍按方法论文体，本库只提供可执行的视觉词汇，避免空泛风格词。

## 一、环境提示词库

### 自然景观

- 山岳：锯齿状山脊、云海翻涌、裸露岩层、风化纹理、背阴面冷光
- 森林：苔藓覆盖的树根、蕨类、交错的树冠、移动光斑、晨雾、腐叶
- 水体：湖面倒影、细碎涟漪、波光、浪花泡沫、水下光柱、水面油膜
- 沙漠：沙丘波纹、风沙低掠、孤立巨石、热浪扭曲、干裂大地
- 雪原：积雪高光、冰晶闪烁、呼气白雾、压雪松林、雪崩残迹
- 天空：积雨云、丁达尔光、晚霞色阶、星轨、极光、云层裂缝光

### 城市与建筑

- 都市街道：湿沥青反光、霓虹招牌、车流灯轨、玻璃幕墙反射、斑马线
- 老城巷弄：石板路、红砖墙、架空电线、旧招牌、窄巷纵深、墙皮剥落
- 工业区：金属管道、蒸汽喷口、厂房天窗、锈蚀钢架、水泥粉尘
- 废墟：断壁残垣、杂草、剥落墙皮、积水倒影、半掩的门窗

### 室内空间

- 咖啡馆：暖木台面、皮革沙发、黄铜灯具、咖啡蒸汽、玻璃杯反光
- 工作室：画架、工具墙、木屑、台灯光锥、散落纸张
- 卧室：柔软织物、落地灯、窗帘透光、床边杂物、暖色夜灯
- 实验室：冷白灯带、屏幕反光、玻璃器皿、金属台面、无菌感

### 天气与时间

- 雨天：细密雨丝、水洼倒影、雾面玻璃、湿润反光、雨滴击打叶片
- 雾天：低能见度、轮廓柔化、体积光、远处景物隐没
- 暴风：飞散树叶、旗帜急摆、扬尘、低压云、电线晃动
- 清晨：低角度长影、青蓝冷调、露水、薄雾
- 黄昏：金色斜阳、拉长影子、暖橙与冷紫过渡
- 午夜：月光、冷蓝调、窗内暖光对比、霓虹倒影

### 光线条件

- 逆光 / 侧逆光：勾勒轮廓、发丝边缘光
- 顶光 / 底光：戏剧化阴影、惊悚感
- 体积光：丁达尔光柱、尘雾中的光路
- 硬光：锐利阴影、高对比
- 柔光：漫反射、低对比、皮肤柔化
- 霓虹光：品红/青蓝双色污染、湿润表面反射

## 二、风格提示词库

### 写实电影

`film still, shallow depth of field, anamorphic lens, natural skin texture, practical lighting, subtle film grain`

### 动漫 / 二次元

- 赛璐璐：`cel-shaded, clean line art, flat colors, screen tones`
- 细腻电影感动画：`detailed background art, soft rim light, volumetric lighting, hair strands`
- 手绘感：`hand-drawn, pencil sketch, watercolor wash, visible brush strokes`

### 3D 动画

`3D CG, subsurface scattering, ray-traced reflections, stylized proportions, soft ambient occlusion`

### 纸艺 / 定格

- 纸拼贴：`paper collage, layered paper texture, torn edges, stop-motion feel`
- 定格动画：`claymation, felt puppets, miniature set, tactile texture`

### 极简产品广告

`white-tech studio, clean negative space, softbox lighting, dark rim light, brand color field`

### 赛博朋克

`cyberpunk, neon signs, wet streets, holographic UI, high contrast, rain reflections`

### 古风 / 水墨

`ink wash painting, rice paper texture, brush strokes, negative space, muted color`

### 油画 / 绘本插画

`oil painting, impasto, canvas texture, storybook illustration, hand-painted texture`

### 纪录片 / 真实感

`documentary, handheld, natural light, amateur DV look, imperfect focus`

### 音乐 MV

`music video, rhythmic cuts, color grading, lens flare, lip-sync`

## 三、使用方法

1. 先选主体画风，再选背景渲染，再选光影与特效，避免只写一个笼统风格词。
2. 环境提示词优先写具体可拍摄现象，不写「美丽」「震撼」。
3. 同一提示词中避免冲突风格（如「水墨 + 赛博朋克」除非用户明确要碰撞）。
4. 用户没提风格时先问对标作品，不替用户预设画风（见 `references/06-art-style-library.md`）。
