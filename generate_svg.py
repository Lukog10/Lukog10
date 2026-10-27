import os
from PIL import Image

def generate():
    # 1. Process avatar to ASCII
    img = Image.open('assets/avatar.png').convert('L')
    thresholded = img.point(lambda p: 255 if p > 30 else 0)
    bbox = thresholded.getbbox()
    cropped = img.crop(bbox)

    width = 38
    height = 24
    resized = cropped.resize((width, height), Image.Resampling.LANCZOS)

    ascii_lines = []
    for y in range(height):
        line = ''
        for x in range(width):
            p = resized.getpixel((x, y))
            if p < 50:
                line += ' '
            elif p < 85:
                line += '.'
            elif p < 125:
                line += '-'
            elif p < 165:
                line += '+'
            elif p < 205:
                line += '*'
            else:
                line += '#'
        ascii_lines.append(line)

    def make_svg(theme='dark'):
        is_dark = (theme == 'dark')
        bg_color = '#0e1117' if is_dark else '#ffffff'
        border_color = '#00638E' if is_dark else '#004A6B'
        key_color = '#8CB9CC' if is_dark else '#004A6B'
        val_color = '#FFFFFF' if is_dark else '#1f2328'
        dot_color = '#3d4f5d' if is_dark else '#8c959f'
        ascii_color = '#BFD8E3' if is_dark else '#00638E'
        header_color = '#BFD8E3' if is_dark else '#004A6B'
        rule_color = '#2B2B2B' if is_dark else '#d0d7de'

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
        svg.append(f'.ascii {{ fill: {ascii_color}; white-space: pre; font-size: 13.5px; }}')
        svg.append('text, tspan { white-space: pre; }')
        svg.append('</style>')

        svg.append(f'<rect width="1198" height="578" x="1" y="1" fill="{bg_color}" stroke="{border_color}" stroke-width="1.5" rx="12"/>')

        svg.append('<text x="35" y="70" class="ascii">')
        for idx, line in enumerate(ascii_lines):
            y = 70 + (idx * 20)
            svg.append(f'  <tspan x="35" y="{y}">{line}</tspan>')
        svg.append('</text>')

        svg.append('<text x="475" y="45">')
        y_pos = 45
        for item in items:
            itype = item[0]
            max_w = item[3]
            if itype == 'header':
                label = item[1].replace('&', '&amp;')
                dashes = '-' * max(2, max_w - len(item[1]) - 1)
                svg.append(f'  <tspan x="475" y="{y_pos}" class="hdr">{label}</tspan><tspan class="rule"> {dashes}</tspan>')
            elif itype == 'rule':
                dashes = '-' * max_w
                svg.append(f'  <tspan x="475" y="{y_pos}" class="rule">{dashes}</tspan>')
            elif itype == 'field':
                label = item[1].replace('&', '&amp;')
                val = item[2].replace('&', '&amp;')
                prefix = f'. {item[1]}: '
                occupied = len(prefix) + len(item[2])
                dot_count = max(2, max_w - occupied)
                dots = ' ' + ('.' * (dot_count - 2)) + ' ' if dot_count >= 2 else ' '
                svg.append(f'  <tspan x="475" y="{y_pos}"><tspan class="dots">. </tspan><tspan class="key">{label}</tspan><tspan class="dots">:</tspan><tspan class="dots">{dots}</tspan><tspan class="val">{val}</tspan></tspan>')
            elif itype == 'empty':
                pass
            y_pos += 21

        svg.append('</text>')
        svg.append('</svg>')
        return '\n'.join(svg)

    with open('assets/dark_mode.svg', 'w', encoding='utf-8') as f:
        f.write(make_svg('dark'))

    with open('assets/light_mode.svg', 'w', encoding='utf-8') as f:
        f.write(make_svg('light'))

    print('Successfully generated assets/dark_mode.svg and assets/light_mode.svg')

if __name__ == '__main__':
    generate()
