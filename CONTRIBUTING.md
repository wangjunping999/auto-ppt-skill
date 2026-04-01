# Contributing to Auto PPT Skill

感谢您对 Auto PPT Skill 的兴趣！我们欢迎各种形式的贡献。

## 项目背景

本项目参考并基于 [ppt-agent](https://github.com/zengwenliang416/ppt-agent) 实现，感谢原作者的开源贡献。我们在原始项目的基础上进行了针对 OpenClaw 的适配和优化。

## 如何贡献

### 报告问题

如果您发现了 bug 或有功能建议，请通过 GitHub Issues 提交：

1. 检查是否已有类似 issue
2. 创建新 issue，详细描述问题
3. 提供复现步骤（如适用）
4. 添加相关标签

### 提交代码

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/your-feature`
3. 提交更改：`git commit -m 'Add some feature'`
4. 推送分支：`git push origin feature/your-feature`
5. 创建 Pull Request

### 代码规范

- 遵循 PEP 8 Python 代码风格
- 添加必要的注释和文档
- 确保代码通过基本测试
- 如果修改了核心逻辑，请同时更新原始项目的相关部分（如适用）

### 添加新风格

1. 在 `styles/` 目录创建 YAML 文件
2. 参考现有风格格式
3. 更新 README.md 风格列表
4. 提交 PR 时附上示例截图

## 开发环境设置

```bash
# 克隆仓库
git clone https://github.com/wangjunping999/auto-ppt-skill.git
cd auto-ppt-skill

# 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 运行测试
python3 scripts/workflow.py --help
```

## 与上游项目同步

如果你从 [ppt-agent](https://github.com/zengwenliang416/ppt-agent) 同步更新：

```bash
# 添加原始项目作为上游
git remote add upstream https://github.com/zengwenliang416/ppt-agent.git

# 获取上游更新
git fetch upstream

# 合并到本地分支
git merge upstream/main
```

## 行为准则

- 尊重他人，保持友善
- 接受建设性批评
- 关注社区最佳利益
- 尊重原始项目的贡献者

## 联系方式

- GitHub Issues: https://github.com/wangjunping999/auto-ppt-skill/issues
- 原始项目: https://github.com/zengwenliang416/ppt-agent

再次感谢您的贡献！
