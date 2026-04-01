# Auto PPT Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Compatible-blue.svg)](https://openclaw.ai)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)

> 🎨 **AI驱动的PPT幻灯片生成工作流** - 基于 OpenClaw 的自动化演示文稿生成工具

Auto PPT Skill 是一个专为 OpenClaw 设计的 PPT 生成工作流，支持从主题调研到最终交付的完整流程。基于 LLM 生成内容，输出 SVG 格式（1280×720）的高质量演示文稿。

## 🙏 致谢

本项目参考并基于 [ppt-agent](https://github.com/zengwenliang416/ppt-agent) 实现，感谢原作者的开源贡献。

## ✨ 特性

- 🤖 **智能调研** - 自动搜索和收集主题相关资料
- 📝 **大纲规划** - 基于金字塔原理结构化大纲
- 🎨 **Bento Grid 布局** - 现代化的卡片式幻灯片设计
- 📐 **SVG 输出** - 1280×720 矢量格式，可缩放不失真
- 🎭 **17种风格** - business、tech、creative、minimal 等预设风格
- 🏷️ **品牌定制** - 支持自定义品牌色彩和标识
- 🔧 **OpenClaw 原生** - 深度集成 OpenClaw 生态

## 📸 效果展示

### 新一代小米SU7发布会
专业级产品发布会PPT，包含设计、性能、智能、价格等完整内容：

| 封面 | 性能页 | 价格页 |
|:---:|:---:|:---:|
| 人车家全生态 | 2.78s破百 | 21.59万起 |

### 人工智能发展趋势
深度调研报告型PPT，包含市场数据、技术趋势、未来展望：

| 市场概览 | 技术演进 | 行动建议 |
|:---:|:---:|:---:|
| $5000亿市场 | 四大技术趋势 | 企业应对策略 |

## 🚀 快速开始

### 前置要求

- OpenClaw 已安装并配置
- Python 3.8+
- curl（用于网络搜索）

### 安装步骤

#### 1. 克隆仓库到 OpenClaw skills 目录

```bash
# 进入 OpenClaw workspace 的 skills 目录
cd ~/.openclaw/workspace/skills

# 克隆 Auto PPT Skill
git clone https://github.com/wangjunping999/auto-ppt-skill.git

# 进入项目目录
cd auto-ppt-skill
```

#### 2. 创建 Python 虚拟环境

```bash
# 创建虚拟环境
python3 -m venv .venv

# 激活虚拟环境（Linux/Mac）
source .venv/bin/activate

# 激活虚拟环境（Windows）
# .venv\Scripts\activate

# 安装依赖
pip install pyyaml
```

#### 3. 验证安装

```bash
# 确保虚拟环境已激活
source .venv/bin/activate

# 测试脚本
python3 scripts/workflow.py --help
```

输出应显示帮助信息：
```
usage: workflow.py [-h] {init,research,outline,design,status} ...
...
```

#### 4. 开始使用

在 OpenClaw 中直接使用：

```
/auto-ppt-skill:ppt 新一代小米SU7发布会
```

或调用脚本：

```bash
# 激活虚拟环境
source .venv/bin/activate

# 初始化项目
python3 scripts/workflow.py init -t "你的演示主题" --style tech

# 查看生成的 run-id
python3 scripts/workflow.py status
```

## 📖 使用指南

### 完整工作流

```
1. 初始化 → 2. 调研 → 3. 大纲 → 4. 设计 → 5. 交付
```

#### Step 1: 初始化项目

```bash
# 激活虚拟环境
source .venv/bin/activate

# 初始化
python3 scripts/workflow.py init \
  --topic "你的演示主题" \
  --style tech \
  --pages 10-15
```

参数说明：
- `--topic` / `-t`: 演示主题（必填）
- `--style` / `-s`: 风格预设，可选：business、tech、creative、minimal 等
- `--pages` / `-p`: 目标页数范围，默认 10-15
- `--brand-colors`: 品牌色彩 YAML 文件路径（可选）

#### Step 2: 调研阶段

```bash
python3 scripts/workflow.py research --run-id <run-id>
```

根据生成的提示词，使用 OpenClaw 的 `web_search` 工具收集资料，保存到 `research-context.md`。

#### Step 3: 大纲规划

```bash
python3 scripts/workflow.py outline --run-id <run-id>
```

根据提示词生成 `outline.json` 结构化大纲。

#### Step 4: 生成幻灯片

```bash
# 逐页生成
python3 scripts/workflow.py design --run-id <run-id> --slide 1
```

将生成的提示词发送给 LLM，生成 SVG 并保存到 `slides/` 目录。

#### Step 5: 生成预览

```bash
python3 scripts/generate-preview.py openspec/changes/<run-id>
```

生成 `output/index.html` 交互式预览页面。

### 查看成品

```bash
# 在浏览器中打开预览
open openspec/changes/<run-id>/output/index.html
```

支持三种查看模式：
- 📷 **Gallery** - 缩略图网格浏览
- 📜 **Scroll** - 垂直滚动查看
- ▶️ **Present** - 全屏演示（键盘 ← → 切换）

## 🎨 品牌色彩自定义

创建 `brand.yaml`：

```yaml
brand:
  primary: "#FF6900"     # 主品牌色（如小米橙）
  secondary: "#000000"   # 辅助品牌色
  logo_text: "Mi"        # 品牌标识（2-3字符）
```

使用：
```bash
python3 scripts/workflow.py init \
  --topic "小米SU7发布会" \
  --brand-colors brand.yaml
```

## 🎭 内置风格

| 风格 | 描述 | 适用场景 |
|------|------|----------|
| `business` | 商务专业风，深蓝+暖橙 | 企业汇报、投资路演 |
| `tech` | 科技现代风，暗色+靛蓝 | 技术演示、产品发布 |
| `creative` | 创意大胆风，紫+粉+琥珀 | 设计提案、营销方案 |
| `minimal` | 极简清洁风，大量留白 | keynote、学术演讲 |
| `blueprint` | 蓝图工程风，网格+制图美学 | 工程架构、系统设计 |
| `bold-editorial` | 大胆编辑风，高对比 | 品牌发布、宣言演讲 |
| `chalkboard` | 黑板教育风，手绘感 | 教学、工作坊 |
| `editorial-infographic` | 编辑信息图风 | 数据报告、研究展示 |
| `fantasy-animation` | 奇幻动画风 | 故事讲述、娱乐 |
| `intuition-machine` | 直觉机器风，AI 感 | AI 演示、未来主义 |
| `notion` | Notion 结构化风 | 团队更新、项目回顾 |
| `pixel-art` | 像素艺术风 | 游戏、复古主题 |
| `scientific` | 学术研究风 | 学术会议、论文答辩 |
| `sketch-notes` | 手绘笔记风 | 头脑风暴、非正式演讲 |
| `vector-illustration` | 矢量插画风 | 产品演示、创业路演 |
| `vintage` | 复古经典风 | 历史讲述、品牌传承 |
| `watercolor` | 水彩艺术风 | 艺术展示、生活方式 |

## 📁 项目结构

```
auto-ppt-skill/
├── SKILL.md                    # OpenClaw Skill 定义
├── README.md                   # 本文件
├── LICENSE                     # MIT 许可证
├── CONTRIBUTING.md             # 贡献指南
├── requirements.txt            # Python 依赖
├── .gitignore                  # Git 忽略文件
├── scripts/                    # 工作流脚本
│   ├── workflow.py            # 主工作流管理
│   ├── generate-preview.py    # HTML 预览生成
│   └── svg-validator.py       # SVG 验证工具
├── styles/                     # 风格配置（17种预设）
│   ├── business.yaml
│   ├── tech.yaml
│   └── ...
├── references/                 # 提示词参考
│   └── prompts/
│       ├── outline-architect.md
│       ├── bento-grid-layout.md
│       └── ...
├── assets/                     # 资源文件
│   └── preview-template.html
└── openspec/                   # 输出目录（运行时生成）
    └── changes/
        └── <run-id>/
            ├── input.md
            ├── research-context.md
            ├── outline.json
            ├── style.yaml
            ├── slides/
            │   ├── slide-01.svg
            │   └── ...
            └── output/
                └── index.html
```

## 🔧 配置说明

### OpenClaw 配置

确保以下配置正确：

1. **Python 虚拟环境已激活**
   ```bash
   source ~/.openclaw/workspace/skills/auto-ppt-skill/.venv/bin/activate
   ```

2. **脚本有执行权限**
   ```bash
   chmod +x scripts/*.py
   ```

3. **SKILL.md 路径正确**
   - 文件位于 `~/.openclaw/workspace/skills/auto-ppt-skill/SKILL.md`
   - OpenClaw 会自动识别并加载

### 环境变量（可选）

```bash
# 自定义输出目录
export PPT_AGENT_OUTPUT_DIR="/path/to/output"

# 调试模式
export PPT_AGENT_DEBUG=1
```

## 🛠️ 开发指南

### 添加新风格

1. 在 `styles/` 目录创建新的 YAML 文件：

```yaml
name: "My Style"
mood: "Description of the style"
color_scheme:
  primary: "#xxxxxx"
  secondary: "#xxxxxx"
  accent: "#xxxxxx"
  background: "#xxxxxx"
  text: "#xxxxxx"
  card_bg: "#xxxxxx"
typography:
  heading_font: "Font Name, sans-serif"
  body_font: "Font Name, sans-serif"
```

2. 更新 `README.md` 和 `SKILL.md` 中的风格列表

### 自定义提示词

编辑 `references/prompts/` 目录下的 Markdown 文件：

- `outline-architect.md` - 大纲生成提示词
- `bento-grid-layout.md` - 布局设计提示词
- `svg-generator.md` - SVG 生成提示词

## 🤝 贡献指南

欢迎提交 Issue 和 PR！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

详见 [CONTRIBUTING.md](CONTRIBUTING.md)

## 📄 许可证

本项目采用 [MIT](LICENSE) 许可证。

## 🙏 致谢

- 本项目参考并基于 [ppt-agent](https://github.com/zengwenliang416/ppt-agent) 实现
- 感谢原作者的开源贡献
- 感谢 OpenClaw 社区的支持

## 📞 联系方式

- GitHub Issues: [https://github.com/wangjunping999/auto-ppt-skill/issues](https://github.com/wangjunping999/auto-ppt-skill/issues)
- 原始项目: [https://github.com/zengwenliang416/ppt-agent](https://github.com/zengwenliang416/ppt-agent)

---

**Auto PPT Skill** - 让 AI 帮你制作专业演示文稿 🎨
