#!/Users/wangjunping/.openclaw/workspace-tst01/skills/ppt-agent/.venv/bin/python3
"""
生成 HTML 预览页面
"""

import json
import argparse
from pathlib import Path

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{TITLE}}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #1a1a2e;
            color: #fff;
            min-height: 100vh;
        }}
        
        .header {{
            padding: 20px 40px;
            background: rgba(0,0,0,0.3);
            display: flex;
            align-items: center;
            gap: 20px;
        }}
        
        .logo {{
            width: 50px;
            height: 50px;
            background: {{ACCENT_COLOR}};
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            font-weight: bold;
            color: #fff;
        }}
        
        .title {{
            font-size: 24px;
            font-weight: 600;
        }}
        
        .controls {{
            padding: 20px 40px;
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }}
        
        .btn {{
            padding: 10px 20px;
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            color: #fff;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
        }}
        
        .btn:hover {{
            background: {{ACCENT_COLOR}};
        }}
        
        .btn.active {{
            background: {{ACCENT_COLOR}};
        }}
        
        .gallery {{
            padding: 20px 40px;
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 20px;
        }}
        
        .slide-card {{
            background: rgba(255,255,255,0.05);
            border-radius: 12px;
            overflow: hidden;
            transition: transform 0.3s;
        }}
        
        .slide-card:hover {{
            transform: translateY(-5px);
        }}
        
        .slide-card img {{
            width: 100%;
            height: auto;
            display: block;
        }}
        
        .slide-label {{
            padding: 10px 15px;
            font-size: 14px;
            color: rgba(255,255,255,0.7);
        }}
        
        .present-mode {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: #000;
            z-index: 1000;
        }}
        
        .present-mode.active {{
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .present-slide {{
            max-width: 90vw;
            max-height: 90vh;
        }}
        
        .present-slide img {{
            width: 100%;
            height: 100%;
            object-fit: contain;
        }}
        
        .nav-btn {{
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            background: rgba(255,255,255,0.1);
            border: none;
            color: #fff;
            font-size: 30px;
            padding: 20px;
            cursor: pointer;
            opacity: 0;
            transition: opacity 0.3s;
        }}
        
        .present-mode:hover .nav-btn {{
            opacity: 1;
        }}
        
        .nav-btn:hover {{
            background: rgba(255,255,255,0.2);
        }}
        
        .nav-prev {{ left: 20px; }}
        .nav-next {{ right: 20px; }}
        
        .close-btn {{
            position: absolute;
            top: 20px;
            right: 20px;
            background: rgba(255,255,255,0.1);
            border: none;
            color: #fff;
            font-size: 24px;
            padding: 10px 15px;
            cursor: pointer;
            border-radius: 8px;
        }}
        
        .scroll-view {{
            display: none;
            padding: 40px;
            max-width: 1280px;
            margin: 0 auto;
        }}
        
        .scroll-view.active {{
            display: block;
        }}
        
        .scroll-slide {{
            margin-bottom: 40px;
            background: rgba(255,255,255,0.05);
            border-radius: 12px;
            overflow: hidden;
        }}
        
        .scroll-slide img {{
            width: 100%;
            height: auto;
            display: block;
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="logo">{{LOGO}}</div>
        <div class="title">{{TITLE}}</div>
    </div>
    
    <div class="controls">
        <button class="btn active" onclick="showGallery()">📷 Gallery</button>
        <button class="btn" onclick="showScroll()">📜 Scroll</button>
        <button class="btn" onclick="startPresent()">▶️ Present</button>
    </div>
    
    <div class="gallery" id="gallery">
        {{SLIDES_GALLERY}}
    </div>
    
    <div class="scroll-view" id="scrollView">
        {{SLIDES_SCROLL}}
    </div>
    
    <div class="present-mode" id="presentMode">
        <button class="close-btn" onclick="stopPresent()">✕</button>
        <button class="nav-btn nav-prev" onclick="prevSlide()">‹</button>
        <div class="present-slide" id="presentSlide"></div>
        <button class="nav-btn nav-next" onclick="nextSlide()">›</button>
    </div>
    
    <script>
        const slides = {{SLIDES_JSON}};
        let currentSlide = 0;
        
        function showGallery() {{
            document.getElementById('gallery').style.display = 'grid';
            document.getElementById('scrollView').classList.remove('active');
            document.querySelectorAll('.controls .btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
        }}
        
        function showScroll() {{
            document.getElementById('gallery').style.display = 'none';
            document.getElementById('scrollView').classList.add('active');
            document.querySelectorAll('.controls .btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
        }}
        
        function startPresent() {{
            currentSlide = 0;
            updatePresentSlide();
            document.getElementById('presentMode').classList.add('active');
        }}
        
        function stopPresent() {{
            document.getElementById('presentMode').classList.remove('active');
        }}
        
        function updatePresentSlide() {{
            const slide = slides[currentSlide];
            document.getElementById('presentSlide').innerHTML = 
                `<img src="${{slide.file}}" alt="${{slide.label}}">`;
        }}
        
        function nextSlide() {{
            currentSlide = (currentSlide + 1) % slides.length;
            updatePresentSlide();
        }}
        
        function prevSlide() {{
            currentSlide = (currentSlide - 1 + slides.length) % slides.length;
            updatePresentSlide();
        }}
        
        document.addEventListener('keydown', (e) => {{
            if (!document.getElementById('presentMode').classList.contains('active')) return;
            if (e.key === 'ArrowRight' || e.key === ' ') nextSlide();
            if (e.key === 'ArrowLeft') prevSlide();
            if (e.key === 'Escape') stopPresent();
        }});
    </script>
</body>
</html>
'''

def generate_preview(run_dir, output_file=None):
    """生成预览 HTML"""
    
    run_path = Path(run_dir)
    
    # 读取大纲
    outline_file = run_path / "outline.json"
    title = "PPT Preview"
    slides_data = []
    
    if outline_file.exists():
        try:
            with open(outline_file, 'r', encoding='utf-8') as f:
                outline = json.load(f)
                title = outline.get('title', title)
                for slide in outline.get('slides', []):
                    slides_data.append({
                        'file': f"slide-{slide['index']:02d}.svg",
                        'label': slide.get('title', f"Slide {slide['index']}")
                    })
        except:
            pass
    
    # 如果没有大纲，扫描 slides 目录
    if not slides_data:
        slides_dir = run_path / "slides"
        if slides_dir.exists():
            for svg_file in sorted(slides_dir.glob("*.svg")):
                idx = svg_file.stem.split('-')[-1]
                slides_data.append({
                    'file': svg_file.name,
                    'label': f"Slide {idx}"
                })
    
    # 生成画廊 HTML
    gallery_html = ""
    for slide in slides_data:
        gallery_html += f'''
        <div class="slide-card">
            <img src="slides/{slide['file']}" alt="{slide['label']}">
            <div class="slide-label">{slide['label']}</div>
        </div>
        '''
    
    # 生成滚动视图 HTML
    scroll_html = ""
    for slide in slides_data:
        scroll_html += f'''
        <div class="scroll-slide">
            <img src="slides/{slide['file']}" alt="{slide['label']}">
        </div>
        '''
    
    # 读取样式获取强调色
    accent_color = "#FF6900"
    style_file = run_path / "style.yaml"
    if style_file.exists():
        try:
            import yaml
            with open(style_file, 'r', encoding='utf-8') as f:
                style = yaml.safe_load(f)
                accent_color = style.get('accent', accent_color)
        except:
            pass
    
    # 生成 HTML
    html = HTML_TEMPLATE
    html = html.replace('{{TITLE}}', title)
    html = html.replace('{{LOGO}}', title[:2].upper())
    html = html.replace('{{ACCENT_COLOR}}', accent_color)
    html = html.replace('{{SLIDES_GALLERY}}', gallery_html)
    html = html.replace('{{SLIDES_SCROLL}}', scroll_html)
    html = html.replace('{{SLIDES_JSON}}', json.dumps(slides_data, ensure_ascii=False))
    
    # 保存
    if output_file is None:
        output_file = run_path / "output" / "index.html"
    else:
        output_file = Path(output_file)
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(html, encoding='utf-8')
    
    print(f"Preview generated: {output_file}")
    return output_file

def main():
    parser = argparse.ArgumentParser(description='Generate HTML preview')
    parser.add_argument('run_dir', help='Run directory path')
    parser.add_argument('-o', '--output', help='Output HTML file path')
    
    args = parser.parse_args()
    generate_preview(args.run_dir, args.output)

if __name__ == '__main__':
    main()
