import os
import base64
from PIL import Image

def generate():
    # 1. Process retro computer image to transparent cutout if needed
    src_path = 'assets/retro_computer_clean.png'
    out_path = 'assets/computer_transparent.png'
    
    if os.path.exists(src_path):
        img = Image.open(src_path).convert('RGBA')
        datas = img.getdata()
        newData = []
        for item in datas:
            if item[0] > 245 and item[1] > 245 and item[2] > 245:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)
        img.putdata(newData)
        bbox = img.getbbox()
        cropped = img.crop(bbox)
        cropped.save(out_path, 'PNG')

    with open(out_path, 'rb') as f:
        b64_data = base64.b64encode(f.read()).decode('ascii')

    def make_svg(theme='dark'):
        is_dark = (theme == 'dark')
        bg_color = '#0e1117' if is_dark else '#ffffff'
        border_color = '#00638E' if is_dark else '#004A6B'
        key_color = '#8CB9CC' if is_dark else '#004A6B'
        val_color = '#FFFFFF' if is_dark else '#1f2328'
        dot_color = '#3d4f5d' if is_dark else '#8c959f'
        header_color = '#BFD8E3' if is_dark else '#004A6B'
        rule_color = '#2B2B2B' if is_dark else '#d0d7de'
        star_color = '#8CB9CC' if is_dark else '#00638E'

        items = [
            ('header', 'Gokul', '', 68),
            ('field', 'Role', 'Developer & Freelancer', 68),
            ('field', 'Focus', 'Data Analytics, ML & AI, Web Development', 68),
            ('field', 'Languages.Core', 'Python, SQL', 68),
            ('field', 'ML.Libraries', 'PyTorch, TensorFlow, Pandas, NumPy, Scikit', 68),
            ('field', 'Analytics.BI', 'Power BI, Tableau', 68),
            ('field', 'Web.Frontend', 'React, TypeScript, Tailwind CSS, HTML, CSS', 68),
            ('field', 'Design', 'Figma, UI/UX Prototyping', 68),
            ('empty', '', '', 68),
            ('header', '- Open Source', '', 68),
            ('field', 'Orbix', 'Windows notch & dock with dynamic island & widgets', 68),
            ('field', 'WizDesk', 'Desktop utility suite for developer workflows', 68),
            ('field', 'Contributions', 'New software releases, community tools, bug fixes', 68),
            ('empty', '', '', 68),
            ('header', '- Tooling & AI Environment', '', 68),
            ('field', 'Environment', 'Git, GitHub, Docker, Linux, Bash', 68),
            ('field', 'Editors', 'VS Code, Zed', 68),
            ('field', 'AI.Ecosystem', 'Claude Code, Open Code, Ollama, LM Studio', 68),
            ('empty', '', '', 68),
            ('header', '- Contact & Socials', '', 68),
            ('field', 'Email.Personal', 'gokulr.1105@gmail.com', 68),
            ('field', 'GitHub', 'github.com/Lukog10', 68),
            ('field', 'Status', 'Available for projects & open source collaborations', 68),
            ('rule', '', '', 68)
        ]

        svg = ['<?xml version="1.0" encoding="UTF-8"?>']
        svg.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 580" width="100%" height="auto" font-family="Consolas, \'Cascadia Code\', monospace" font-size="13px">')
        svg.append('<style>')
        svg.append(f'.key {{ fill: {key_color}; font-weight: 600; }}')
        svg.append(f'.val {{ fill: {val_color}; }}')
        svg.append(f'.dots {{ fill: {dot_color}; }}')
        svg.append(f'.hdr {{ fill: {header_color}; font-weight: bold; }}')
        svg.append(f'.rule {{ fill: {rule_color}; }}')
        svg.append('text, tspan { white-space: pre; }')
        svg.append('</style>')

        # Card container
        svg.append(f'<rect width="1198" height="578" x="1" y="1" fill="{bg_color}" stroke="{border_color}" stroke-width="1.5" rx="12"/>')

        # Ambient cosmic stars in space around the computer
        svg.append(f'''  <!-- Cosmic stars around the computer -->
  <g fill="{star_color}" opacity="0.6">
    <circle cx="85" cy="80" r="1.5" />
    <circle cx="210" cy="65" r="2" />
    <circle cx="370" cy="95" r="1.2" />
    <circle cx="65" cy="240" r="1" />
    <circle cx="410" cy="130" r="1.8" />
    <circle cx="95" cy="470" r="2" />
    <circle cx="230" cy="505" r="1.5" />
    <circle cx="390" cy="460" r="1.2" />
    <circle cx="50" cy="380" r="1.5" />
    <!-- 4-point stars -->
    <path d="M 160 110 Q 160 120 170 120 Q 160 120 160 130 Q 160 120 150 120 Q 160 120 160 110 Z" opacity="0.75"/>
    <path d="M 340 430 Q 340 438 348 438 Q 340 438 340 446 Q 340 438 332 438 Q 340 438 340 430 Z" opacity="0.75"/>
    <path d="M 120 330 Q 120 336 126 336 Q 120 336 120 342 Q 120 336 114 336 Q 120 336 120 330 Z" opacity="0.5"/>
  </g>''')

        # Left side: Embedded transparent retro computer illustration
        # Dimensions: 410 wide x 247 high, centered vertically in 580 card: y = (580 - 247) / 2 = 166.5
        svg.append(f'  <image href="data:image/png;base64,{b64_data}" x="35" y="166" width="410" height="247" />')

        # Right side: Neofetch system table
        svg.append('  <text x="475" y="45">')
        y_pos = 45
        for item in items:
            itype = item[0]
            max_w = item[3]
            if itype == 'header':
                label = item[1].replace('&', '&amp;')
                dashes = '-' * max(2, max_w - len(item[1]) - 1)
                svg.append(f'    <tspan x="475" y="{y_pos}" class="hdr">{label}</tspan><tspan class="rule"> {dashes}</tspan>')
            elif itype == 'rule':
                dashes = '-' * max_w
                svg.append(f'    <tspan x="475" y="{y_pos}" class="rule">{dashes}</tspan>')
            elif itype == 'field':
                label = item[1].replace('&', '&amp;')
                val = item[2].replace('&', '&amp;')
                prefix = f'. {item[1]}: '
                occupied = len(prefix) + len(item[2])
                dot_count = max(2, max_w - occupied)
                dots = ' ' + ('.' * (dot_count - 2)) + ' ' if dot_count >= 2 else ' '
                svg.append(f'    <tspan x="475" y="{y_pos}"><tspan class="dots">. </tspan><tspan class="key">{label}</tspan><tspan class="dots">:</tspan><tspan class="dots">{dots}</tspan><tspan class="val">{val}</tspan></tspan>')
            elif itype == 'empty':
                pass
            y_pos += 21

        svg.append('  </text>')
        svg.append('</svg>')
        return '\n'.join(svg)

    with open('assets/dark_mode.svg', 'w', encoding='utf-8') as f:
        f.write(make_svg('dark'))

    with open('assets/light_mode.svg', 'w', encoding='utf-8') as f:
        f.write(make_svg('light'))

    print('Successfully generated assets/dark_mode.svg and assets/light_mode.svg with embedded transparent retro computer')

if __name__ == '__main__':
    generate()
