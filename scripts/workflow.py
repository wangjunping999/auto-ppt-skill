#!/Users/wangjunping/.openclaw/workspace-tst01/skills/ppt-agent/.venv/bin/python3
"""
PPT Agent Workflow - OpenClaw 适配版
简化版工作流，使用顺序执行替代并行子代理
"""

import os
import sys
import json
import re
import argparse
from datetime import datetime
from pathlib import Path

# 配置
RUN_DIR_BASE = "openspec/changes"
STYLES_DIR = Path(__file__).parent.parent / "styles"
REFERENCES_DIR = Path(__file__).parent.parent / "references"

# 风格列表
STYLES = [
    "business", "tech", "creative", "minimal", "blueprint",
    "bold-editorial", "chalkboard", "editorial-infographic",
    "fantasy-animation", "intuition-machine", "notion",
    "pixel-art", "scientific", "sketch-notes",
    "vector-illustration", "vintage", "watercolor"
]

def slugify(text):
    """将文本转换为 kebab-case"""
    text = re.sub(r'[^\w\s-]', '', text.lower())
    text = re.sub(r'[-\s]+', '-', text).strip('-')
    return text

def init_run(topic, style="business", pages="10-15", run_id=None, brand_colors=None):
    """初始化运行目录"""
    
    # 生成 run_id
    if run_id:
        change_id = run_id
    else:
        slug = slugify(topic)[:30]
        change_id = f"ppt-{slug}-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    
    run_dir = Path(RUN_DIR_BASE) / change_id
    run_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建子目录
    (run_dir / "drafts").mkdir(exist_ok=True)
    (run_dir / "slides").mkdir(exist_ok=True)
    (run_dir / "output").mkdir(exist_ok=True)
    
    # 写入 input.md
    input_content = f"""# Input

## Topic
{topic}

## Style
{style}

## Pages
{pages}

## Brand Colors
{brand_colors if brand_colors else "None"}

## Created
{datetime.now().isoformat()}
"""
    (run_dir / "input.md").write_text(input_content, encoding="utf-8")
    
    # 写入 proposal.md
    proposal_content = f"""# Change: {topic}

## Why
生成关于"{topic}"的专业演示文稿

## What Changes
- 结构化大纲
- {pages} 页 SVG 幻灯片
- 交互式 HTML 预览
- 演讲者备注

## Impact
提供可直接使用的演示文稿素材
"""
    (run_dir / "proposal.md").write_text(proposal_content, encoding="utf-8")
    
    # 写入 tasks.md
    tasks_content = """# Tasks

- [x] Phase 1: Init
- [ ] Phase 2: Requirement Research
- [ ] Phase 3: Material Collection
- [ ] Phase 4: Outline Planning
- [ ] Phase 5: Planning Draft
- [ ] Phase 6: Design Draft
- [ ] Phase 7: Delivery
"""
    (run_dir / "tasks.md").write_text(tasks_content, encoding="utf-8")
    
    # 复制或生成 style.yaml
    style_file = STYLES_DIR / f"{style}.yaml"
    if style_file.exists():
        import shutil
        shutil.copy(style_file, run_dir / "style.yaml")
    
    print(f"Run directory created: {run_dir}")
    print(f"Run ID: {change_id}")
    
    return run_dir, change_id

def load_style(run_dir):
    """加载样式配置"""
    style_file = run_dir / "style.yaml"
    if style_file.exists():
        try:
            import yaml
            with open(style_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except:
            pass
    return {}

def generate_research_prompt(topic, run_dir):
    """生成调研提示词"""
    return f"""请对以下主题进行背景调研：

主题：{topic}

请提供：
1. 主题概述和背景
2. 关键概念和术语
3. 相关数据和趋势
4. 目标受众分析建议
5. 可能的章节结构建议

将结果保存到：{run_dir}/research-context.md
"""

def generate_outline_prompt(run_dir):
    """生成大纲提示词"""
    research_file = run_dir / "research-context.md"
    requirements_file = run_dir / "requirements.md"
    
    context = ""
    if research_file.exists():
        context += f"\n\n调研背景：\n{research_file.read_text(encoding='utf-8')[:2000]}"
    if requirements_file.exists():
        context += f"\n\n需求文档：\n{requirements_file.read_text(encoding='utf-8')[:1000]}"
    
    return f"""基于以下信息，生成 PPT 大纲：

{context}

要求：
1. 使用金字塔原理组织内容
2. 包含 10-15 页幻灯片
3. 每页有明确的标题和要点
4. 输出 JSON 格式到：{run_dir}/outline.json

JSON 格式示例：
{{
  "title": "演示标题",
  "slides": [
    {{"index": 1, "type": "cover", "title": "封面", "points": []}},
    {{"index": 2, "type": "content", "title": "章节标题", "points": ["要点1", "要点2"]}}
  ]
}}
"""

def generate_slide_prompt(run_dir, slide_index, style):
    """生成单页幻灯片提示词"""
    outline_file = run_dir / "outline.json"
    style_file = run_dir / "style.yaml"
    
    outline = {}
    if outline_file.exists():
        try:
            outline = json.loads(outline_file.read_text(encoding='utf-8'))
        except:
            pass
    
    slide_info = {}
    if 'slides' in outline:
        for s in outline['slides']:
            if s.get('index') == slide_index:
                slide_info = s
                break
    
    style_content = ""
    if style_file.exists():
        style_content = style_file.read_text(encoding='utf-8')[:500]
    
    return f"""生成第 {slide_index} 页幻灯片的 SVG：

幻灯片信息：
- 标题：{slide_info.get('title', '标题')}
- 要点：{slide_info.get('points', [])}
- 类型：{slide_info.get('type', 'content')}

样式配置：
{style_content}

要求：
1. 使用 Bento Grid 布局
2. 尺寸：1280×720 (viewBox="0 0 1280 720")
3. 符合样式配置的颜色和字体
4. 输出到：{run_dir}/slides/slide-{slide_index:02d}.svg

SVG 要求：
- 有效的 XML 格式
- 包含 viewBox="0 0 1280 720"
- 字体大小：正文 ≥ 14px，标签 ≥ 12px
- 安全边距：≥ 60px
"""

def main():
    parser = argparse.ArgumentParser(description='PPT Agent Workflow')
    parser.add_argument('command', choices=['init', 'research', 'outline', 'design', 'status'])
    parser.add_argument('--topic', '-t', help='演示主题')
    parser.add_argument('--style', '-s', default='business', choices=STYLES, help='风格')
    parser.add_argument('--pages', '-p', default='10-15', help='页数范围')
    parser.add_argument('--run-id', '-r', help='运行 ID')
    parser.add_argument('--brand-colors', '-b', help='品牌色彩文件路径')
    parser.add_argument('--slide', type=int, help='幻灯片索引（用于 design 命令）')
    
    args = parser.parse_args()
    
    if args.command == 'init':
        if not args.topic:
            print("Error: --topic is required for init")
            sys.exit(1)
        run_dir, run_id = init_run(
            topic=args.topic,
            style=args.style,
            pages=args.pages,
            run_id=args.run_id,
            brand_colors=args.brand_colors
        )
        print(f"\nNext step: Run research phase")
        print(f"  python3 {sys.argv[0]} research --run-id {run_id}")
        
    elif args.command == 'research':
        if not args.run_id:
            print("Error: --run-id is required")
            sys.exit(1)
        run_dir = Path(RUN_DIR_BASE) / args.run_id
        if not run_dir.exists():
            print(f"Error: Run directory not found: {run_dir}")
            sys.exit(1)
        
        # 读取主题
        input_file = run_dir / "input.md"
        topic = "Unknown"
        if input_file.exists():
            content = input_file.read_text(encoding='utf-8')
            match = re.search(r'## Topic\n(.+)', content)
            if match:
                topic = match.group(1).strip()
        
        prompt = generate_research_prompt(topic, run_dir)
        print("=== Research Prompt ===")
        print(prompt)
        print("\n=== Next Step ===")
        print(f"Use web_search and web_fetch to gather research, then save to:")
        print(f"  {run_dir}/research-context.md")
        
    elif args.command == 'outline':
        if not args.run_id:
            print("Error: --run-id is required")
            sys.exit(1)
        run_dir = Path(RUN_DIR_BASE) / args.run_id
        
        prompt = generate_outline_prompt(run_dir)
        print("=== Outline Prompt ===")
        print(prompt)
        
    elif args.command == 'design':
        if not args.run_id or not args.slide:
            print("Error: --run-id and --slide are required")
            sys.exit(1)
        run_dir = Path(RUN_DIR_BASE) / args.run_id
        
        # 读取样式
        input_file = run_dir / "input.md"
        style = "business"
        if input_file.exists():
            content = input_file.read_text(encoding='utf-8')
            match = re.search(r'## Style\n(.+)', content)
            if match:
                style = match.group(1).strip()
        
        prompt = generate_slide_prompt(run_dir, args.slide, style)
        print("=== Slide Design Prompt ===")
        print(prompt)
        
    elif args.command == 'status':
        if not args.run_id:
            # 列出所有运行
            base_dir = Path(RUN_DIR_BASE)
            if base_dir.exists():
                runs = sorted([d.name for d in base_dir.iterdir() if d.is_dir()])
                print("Available runs:")
                for run in runs[-10:]:  # 最近 10 个
                    print(f"  - {run}")
        else:
            run_dir = Path(RUN_DIR_BASE) / args.run_id
            if run_dir.exists():
                print(f"Run: {args.run_id}")
                print(f"Directory: {run_dir}")
                
                # 检查文件
                files = ['input.md', 'research-context.md', 'requirements.md', 
                        'outline.json', 'style.yaml']
                for f in files:
                    path = run_dir / f
                    status = "✓" if path.exists() else "✗"
                    print(f"  {status} {f}")
                
                # 统计幻灯片
                slides_dir = run_dir / "slides"
                if slides_dir.exists():
                    svg_files = list(slides_dir.glob("*.svg"))
                    print(f"  Slides: {len(svg_files)} generated")

if __name__ == '__main__':
    main()
