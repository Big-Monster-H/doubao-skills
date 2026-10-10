# 豆包 Skills 合集（doubao-skills）

由 [Big-Monster-H](https://github.com/Big-Monster-H) 自研的 **7 个豆包/通用 Agent Skills**，公开分享，可直接下载安装使用。

## 安装方法

把对应的 skill 目录（如 `voice-timbre-designer/`）整体放进宿主 Agent 的 skills 目录（豆包通用约定 `~/.agents/skills/`，其它宿主按自己的 skills 目录约定即可），目录名即 skill 名。

## Skill 列表

| Skill | 作用 |
|---|---|
| [voice-timbre-designer](voice-timbre-designer/) | 音色设计：多轮选择题引导成专业音色提示词，批量产出候选音色 |
| [prompt-writer-skill](prompt-writer-skill/) | 生图提示词：引导式选择题生成可直接用于 MJ / Stable Diffusion 的提示词 |
| [scene-builder-skill](scene-builder-skill/) | 大场景生成：蓝图 → 分区生成 → 合成，输出透视统一的大场景鸟瞰图 |
| [novel-to-video-prompt-skill](novel-to-video-prompt-skill/) | 小说转视频：粘贴小说片段，直接生成视频提示词（含分镜/台词/音效） |
| [wechat-miniprogram-builder](wechat-miniprogram-builder/) | 微信小程序开发：从零构建或修改小程序（原生框架 + Vant Weapp + 云开发） |
| [ai-video-prompt](ai-video-prompt/) | AI 视频提示词：MJ 文生图关键帧 → MiniMax H3 图生视频的完整提示词工作流 |
| [ruic-card-skill](ruic-card-skill/) | 3D 全息镭射卡：一句话/参考图生成可交互 3D 闪卡网页 + 可编辑 Blender 工程 |

## 下载

- 网页端：点击仓库页右上角 **Code → Download ZIP** 即可打包下载全部内容
- 命令行：`git clone https://github.com/Big-Monster-H/doubao-skills.git`

## 许可

各 skill 目录内自带 LICENSE（MIT），详见对应文件。
