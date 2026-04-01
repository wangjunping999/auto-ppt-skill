---
name: auto-ppt-skill
description: "PPT 幻灯片生成工作流。使用 LLM 生成内容，输出 SVG 格式（1280×720）的 Bento Grid 布局演示文稿。支持 17 种风格预设和品牌色彩自定义。基于 ppt-agent 适配 OpenClaw。开源地址：https://github.com/wangjunping999/auto-ppt-skill"
metadata:
  {
    "openclaw":
      {
        "emoji": "📊",
        "requires": { "bins": ["curl", "python3"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "curl",
              "bins": ["curl"],
              "label": "Install curl (brew)",
            },
          ],
      },
  }
---

# Auto PPT Skill - 幻灯片生成

[![GitHub](https://img.shields.io/badge/GitHub-auto--ppt--skill-blue.svg)](https://github.com/wangjunping999/auto-ppt-skill)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> 本项目参考并基于 [ppt-agent](https://github.com/zengwenliang416/ppt-agent) 实现

多智能体 PPT 幻灯片生成工作流，支持跨平台运行。

## 功能特性

- **智能调研**：自动搜索和收集主题相关资料
- **大纲规划**：基于金字塔原理结构化大纲
- **Bento Grid 布局**：现代化的卡片式幻灯片设计
- **SVG 输出**：1280×720 矢量格式，可缩放不失真
- **17 种风格**：business、tech、creative、minimal 等
- **品牌定制**：支持自定义品牌色彩和标识

## 使用方法

### 基本用法

```
/ppt-agent:ppt <主题或需求描述>
```

### 高级用法

```
/ppt-agent:ppt [--style=<style>] [--brand-colors=<path>] [--pages=10-15] <主题>
```

### 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--style` | business | 风格预设：business、tech、creative、minimal、blueprint、bold-editorial、chalkboard、editorial-infographic、fantasy-animation、intuition-machine、notion、pixel-art、scientific、sketch-notes、vector-illustration、vintage、watercolor |
| `--brand-colors` | 无 | 品牌色彩 YAML 文件路径 |
| `--pages` | 10-15 | 目标页数范围 |
| `--run-id` | 自动生成 | 恢复已有运行目录 |

### 品牌色彩自定义

创建 `brand.yaml`：

```yaml
brand:
  primary: "#FF6900"     # 主品牌色
  secondary: "#000000"   # 辅助品牌色
  logo_text: "Mi"        # 品牌标识（2-3字符）
```

使用：
```
/ppt-agent:ppt --brand-colors=brand.yaml 小米SU7发布会
```

## 工作流程

1. **初始化** — 解析参数，创建运行目录
2. **需求调研** — 背景搜索 + 用户确认需求
3. **素材收集** — 按章节并行深度搜索
4. **大纲规划** — 金字塔原理结构化大纲 + 用户审批
5. **规划草稿** — 每页生成简版 SVG 草稿
6. **设计稿** — Bento Grid SVG 生成
7. **交付** — 最终 SVG 文件 + 交互式 HTML 预览页

## 输出目录

```
openspec/changes/<run_id>/
├── input.md                 # 输入参数
├── proposal.md              # 变更提案
├── tasks.md                 # 任务清单
├── research-context.md      # 调研上下文
├── requirements.md          # 需求文档
├── materials.md             # 素材汇总
├── style.yaml               # 样式配置
├── outline.json             # 结构化大纲
├── outline-preview.md       # 大纲预览
├── drafts/slide-{nn}.svg    # 规划草稿
├── slides/slide-{nn}.svg    # 设计稿
├── output/
│   ├── slide-{nn}.svg       # 最终 SVG
│   ├── index.html           # 交互式预览页
│   └── speaker-notes.md     # 演讲者备注
```

## 风格列表

| 风格 | 描述 | 适用场景 |
|------|------|----------|
| business | 商务专业风，深蓝+暖橙 | 企业汇报、投资路演 |
| tech | 科技现代风，暗色+靛蓝 | 技术演示、产品发布 |
| creative | 创意大胆风，紫+粉+琥珀 | 设计提案、营销方案 |
| minimal | 极简清洁风，大量留白 |  keynote、学术演讲 |
| blueprint | 蓝图工程风，网格+制图美学 | 工程架构、系统设计 |
| bold-editorial | 大胆编辑风，高对比 | 品牌发布、宣言演讲 |
| chalkboard | 黑板教育风，手绘感 | 教学、工作坊 |
| editorial-infographic | 编辑信息图风 | 数据报告、研究展示 |
| fantasy-animation | 奇幻动画风 | 故事讲述、娱乐 |
| intuition-machine | 直觉机器风，AI 感 | AI 演示、未来主义 |
| notion | Notion 结构化风 | 团队更新、项目回顾 |
| pixel-art | 像素艺术风 | 游戏、复古主题 |
| scientific | 学术研究风 | 学术会议、论文答辩 |
| sketch-notes | 手绘笔记风 | 头脑风暴、非正式演讲 |
| vector-illustration | 矢量插画风 | 产品演示、创业路演 |
| vintage | 复古经典风 | 历史讲述、品牌传承 |
| watercolor | 水彩艺术风 | 艺术展示、生活方式 |

## 质量标准

- 布局评分 ≥ 6/10
- 可读性 ≥ 6/10
- 有效 SVG 输出（1280×720 viewBox）
- 字体大小下限（正文 ≥ 14px，标签 ≥ 12px）
- 安全边距（≥ 60px）

## 依赖工具

- `curl` — 网页读取、API 调用
- `python3` — JSON 处理、YAML 解析
- `web_search` — 网络搜索（OpenClaw 内置）
- `web_fetch` — 网页内容提取（OpenClaw 内置）

## 注意事项

1. 生成过程需要多次用户确认（调研结果、大纲规划）
2. 每页幻灯片独立生成，支持断点续传
3. 最终输出为 SVG 格式，可用浏览器直接打开
4. HTML 预览页支持 Gallery/Scroll/Present 三种模式

## 🚀 OpenClaw 快速安装

### 方式一：Git 克隆（推荐）

```bash
# 1. 进入 OpenClaw skills 目录
cd ~/.openclaw/workspace/skills

# 2. 克隆仓库
git clone https://github.com/zengwenliang416/ppt-agent.git

# 3. 进入项目目录
cd ppt-agent

# 4. 创建虚拟环境
python3 -m venv .venv

# 5. 激活虚拟环境并安装依赖
source .venv/bin/activate
pip install pyyaml

# 6. 验证安装
python3 scripts/workflow.py --help
```

### 方式二：手动下载

1. 从 GitHub 下载最新 Release 压缩包
2. 解压到 `~/.openclaw/workspace/skills/ppt-agent/`
3. 按照上述步骤 4-6 完成安装

### 方式三：使用 OpenClaw 内置命令

在 OpenClaw 中直接执行：

```
# 安装 skill
exec: cd ~/.openclaw/workspace/skills && git clone https://github.com/zengwenliang416/ppt-agent.git

# 设置权限
exec: chmod +x ~/.openclaw/workspace/skills/ppt-agent/scripts/*.py
```

## 环境设置

本 skill 使用独立的 Python 虚拟环境：

```bash
# 虚拟环境位置
~/.openclaw/workspace/skills/ppt-agent/.venv

# 激活虚拟环境
source ~/.openclaw/workspace/skills/ppt-agent/.venv/bin/activate

# 已安装的依赖
pip list  # 查看已安装包
```

### 添加新的依赖

```bash
# 激活虚拟环境后
source ~/.openclaw/workspace/skills/ppt-agent/.venv/bin/activate
pip install <package-name>
```

## OpenClaw 适配说明

由于原 skill 是为 Claude Code/OpenCode 设计的，在 OpenClaw 中使用时采用**简化工作流**：

### 与原版的区别

| 功能 | 原版 (Claude Code) | OpenClaw 适配版 |
|------|-------------------|----------------|
| 子代理调用 | `Task(subagent_type=...)` | 顺序执行，使用文件状态跟踪 |
| 用户交互 | `AskUserQuestion` | 使用 message 工具或分步确认 |
| Gemini 审查 | 自动调用 Gemini API | 可选，使用 LLM 自检 |
| 并行生成 | 多 slide 并行 | 顺序生成 |

### 使用步骤

#### Step 0: 激活虚拟环境（重要）

```bash
source /Users/wangjunping/.openclaw/workspace-tst01/skills/ppt-agent/.venv/bin/activate
```

#### Step 1: 初始化项目

```bash
# 使用工作流脚本初始化（确保虚拟环境已激活）
python3 skills/ppt-agent/scripts/workflow.py init --topic "你的演示主题" --style business

# 或使用默认参数
python3 skills/ppt-agent/scripts/workflow.py init -t "小米SU7发布会"
```

#### Step 2: 调研阶段

```bash
# 生成调研提示词
python3 skills/ppt-agent/scripts/workflow.py research --run-id <run-id>

# 然后使用 web_search 工具搜索相关信息
# 将搜索结果整理后保存到 openspec/changes/<run-id>/research-context.md
```

#### Step 3: 大纲规划

```bash
# 生成大纲提示词
python3 skills/ppt-agent/scripts/workflow.py outline --run-id <run-id>

# 根据提示词生成大纲，保存为 openspec/changes/<run-id>/outline.json
```

#### Step 4: 生成幻灯片

```bash
# 逐页生成幻灯片（示例：生成第 1 页）
python3 skills/ppt-agent/scripts/workflow.py design --run-id <run-id> --slide 1

# 将生成的提示词发送给 LLM，要求生成 SVG
# 将 SVG 保存到 openspec/changes/<run-id>/slides/slide-01.svg
```

#### Step 5: 生成预览

```bash
# 生成 HTML 预览页面
python3 skills/ppt-agent/scripts/generate-preview.py openspec/changes/<run-id>
```

### 快捷命令

在 OpenClaw 中，可以直接使用：

```
# 初始化并生成调研提示词
/ppt-agent:ppt 小米SU7发布会

# 指定风格
/ppt-agent:ppt --style=tech 人工智能发展趋势

# 恢复已有项目
/ppt-agent:ppt --run-id=ppt-xiaomi-su7-20260401
```

### 文件结构

```
skills/ppt-agent/
├── SKILL.md                    # 本文件
├── scripts/
│   ├── workflow.py            # 工作流管理脚本
│   ├── svg-validator.py       # SVG 验证工具
│   └── generate-preview.py    # HTML 预览生成器
├── styles/                     # 风格配置（从原项目复制）
│   ├── business.yaml
│   ├── tech.yaml
│   └── ...
├── references/                 # 提示词参考（从原项目复制）
│   └── prompts/
└── assets/                     # 资源文件（从原项目复制）
```

### 手动复制样式文件

```bash
# 执行以下命令复制原项目的样式文件
cp -r /Users/wangjunping/Downloads/ppt-agent/skills/_shared/styles/* \
  ~/.openclaw/workspace-tst01/skills/ppt-agent/styles/

cp -r /Users/wangjunping/Downloads/ppt-agent/skills/_shared/references/* \
  ~/.openclaw/workspace-tst01/skills/ppt-agent/references/

cp -r /Users/wangjunping/Downloads/ppt-agent/skills/_shared/assets/* \
  ~/.openclaw/workspace-tst01/skills/ppt-agent/assets/
```

## License

MIT
