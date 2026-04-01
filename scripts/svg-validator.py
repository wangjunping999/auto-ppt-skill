#!/Users/wangjunping/.openclaw/workspace-tst01/skills/ppt-agent/.venv/bin/python3
"""
SVG 验证工具
检查 SVG 文件是否符合 PPT Agent 的质量标准
"""

import sys
import re
import xml.etree.ElementTree as ET
from pathlib import Path

def validate_svg(svg_path):
    """验证 SVG 文件"""
    
    issues = []
    
    try:
        content = Path(svg_path).read_text(encoding='utf-8')
    except Exception as e:
        return {"valid": False, "issues": [f"无法读取文件: {e}"]}
    
    # 1. 检查 XML 有效性
    try:
        root = ET.fromstring(content)
    except ET.ParseError as e:
        return {"valid": False, "issues": [f"XML 解析错误: {e}"]}
    
    # 2. 检查 viewBox
    viewbox = root.get('viewBox', '')
    if not viewbox:
        issues.append("缺少 viewBox 属性")
    elif '1280' not in viewbox or '720' not in viewbox:
        issues.append(f"viewBox 尺寸不正确: {viewbox} (应为 1280x720)")
    
    # 3. 检查字体大小
    font_sizes = re.findall(r'font-size=["\'](\d+)', content)
    small_fonts = [fs for fs in font_sizes if int(fs) < 12]
    if small_fonts:
        issues.append(f"发现过小字体: {set(small_fonts)}px (最小应为 12px)")
    
    # 4. 检查安全边距（简单检查是否有元素太靠近边缘）
    # 这里简化处理，实际应该解析坐标
    
    # 5. 检查必要的 SVG 元素
    if root.tag.endswith('svg'):
        pass  # 正常
    elif root.tag != 'svg':
        issues.append(f"根元素不是 svg: {root.tag}")
    
    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "viewBox": viewbox,
        "font_sizes": sorted(set(font_sizes), key=int) if font_sizes else []
    }

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 svg-validator.py <svg-file>")
        sys.exit(1)
    
    svg_path = sys.argv[1]
    result = validate_svg(svg_path)
    
    print(f"File: {svg_path}")
    print(f"Valid: {'✓' if result['valid'] else '✗'}")
    print(f"ViewBox: {result.get('viewBox', 'N/A')}")
    print(f"Font sizes: {', '.join(result.get('font_sizes', []))}px")
    
    if result['issues']:
        print("\nIssues:")
        for issue in result['issues']:
            print(f"  - {issue}")
    
    sys.exit(0 if result['valid'] else 1)

if __name__ == '__main__':
    main()
