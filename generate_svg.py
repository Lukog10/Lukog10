import os
import xml.etree.ElementTree as ET

# Exact smooth vector contour for the typographic code brace {
BRACE_LEFT_PATH = "M 62,0 L 69,0 L 69,27 L 65,27 L 60,29 L 55,36 L 55,40 L 54,41 L 54,67 L 53,68 L 53,72 L 51,78 L 43,92 L 47,97 L 53,111 L 53,115 L 54,116 L 54,142 L 55,143 L 55,147 L 60,154 L 65,156 L 69,156 L 69,183 L 63,183 L 62,182 L 57,182 L 51,180 L 42,175 L 37,170 L 32,163 L 28,151 L 28,146 L 27,145 L 27,120 L 26,119 L 26,116 L 24,112 L 17,104 L 0,91 L 17,79 L 25,69 L 27,63 L 27,39 L 28,38 L 28,32 L 31,22 L 36,14 L 45,6 L 53,2 L 61,1 L 62,0 Z"

def make_keyboard_svg(brace_color='#FFFFFF', key_color='#8CB9CC', space_color='#BFD8E3'):
    """Generates the clean Style 4 / Style 2 vector { keyboard } emblem."""
    svg = []
    # Left curly brace
    svg.append(f'<g fill="{brace_color}"><path d="{BRACE_LEFT_PATH}"/></g>')
    # Right curly brace (symmetric mirror at w=474)
    svg.append(f'<g transform="translate(474, 0) scale(-1, 1)" fill="{brace_color}"><path d="{BRACE_LEFT_PATH}"/></g>')
    
    # Row 1 (6 square keys)
    for x in [104, 150, 196, 242, 289, 335]:
        svg.append(f'<rect x="{x}" y="26" width="35" height="35" rx="5" fill="{key_color}"/>')
    
    # Row 2 (4 square keys + 1 double-width Enter key)
    for x in [104, 150, 196, 242]:
        svg.append(f'<rect x="{x}" y="72" width="35" height="35" rx="5" fill="{key_color}"/>')
    svg.append(f'<rect x="289" y="72" width="81" height="35" rx="5" fill="{key_color}"/>')
    
    # Row 3 (1 square key + elongated Spacebar + 1 square key)
    svg.append(f'<rect x="104" y="117" width="35" height="35" rx="5" fill="{key_color}"/>')
    svg.append(f'<rect x="150" y="117" width="174" height="35" rx="5" fill="{space_color}"/>')
    svg.append(f'<rect x="335" y="117" width="35" height="35" rx="5" fill="{key_color}"/>')
    
    return ''.join(svg)

def make_svg(theme='dark'):
    is_dark = (theme == 'dark')
    bg_color = '#0e1117' if is_dark else '#ffffff'
    border_color = '#00638E' if is_dark else '#004A6B'
    key_color = '#8CB9CC' if is_dark else '#004A6B'
    val_color = '#FFFFFF' if is_dark else '#1f2328'
    dot_color = '#3d4f5d' if is_dark else '#8c959f'
    header_color = '#BFD8E3' if is_dark else '#004A6B'
    rule_color = '#2B2B2B' if is_dark else '#d0d7de'

    brace_color = '#FFFFFF' if is_dark else '#141414'
    kb_key_color = '#8CB9CC' if is_dark else '#004A6B'
    kb_space_color = '#BFD8E3' if is_dark else '#00638E'

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

    # Outer Card
    svg.append(f'<rect width="1198" height="578" x="1" y="1" fill="{bg_color}" stroke="{border_color}" stroke-width="1.5" rx="12"/>')

    # Left side: Clean Vector Emblem { keyboard }
    # Total emblem dimensions: 474w x 184h.
    # Center at x=235, y=290. Scale=0.72 -> 341.3w x 132.5h.
    kb_content = make_keyboard_svg(brace_color, kb_key_color, kb_space_color)
    svg.append(f'<g transform="translate(64.5, 223.75) scale(0.72)">{kb_content}</g>')

    # Right side: Neofetch system table
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

def generate():
    os.makedirs('assets', exist_ok=True)
    
    dark_svg = make_svg('dark')
    light_svg = make_svg('light')

    # XML validation
    ET.fromstring(dark_svg)
    ET.fromstring(light_svg)

    with open('assets/dark_mode.svg', 'w', encoding='utf-8') as f:
        f.write(dark_svg)

    with open('assets/light_mode.svg', 'w', encoding='utf-8') as f:
        f.write(light_svg)

    print('Successfully generated and validated assets/dark_mode.svg and assets/light_mode.svg')

if __name__ == '__main__':
    generate()
