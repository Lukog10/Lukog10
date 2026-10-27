import base64
import os
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image
from scipy.ndimage import label

def prepare_recolored_assets():
    source_path = r'C:\Users\Administrator\.gemini\antigravity-ide\brain\a9c1daa9-d848-4653-a853-842cb3a976a8\.user_uploaded\media_1793085724101.png'
    im = Image.open(source_path).convert('RGBA')
    arr = np.array(im, dtype=float)

    # 1. External background
    is_bg_candidate = np.all(arr[:, :, :3] > 240, axis=2)
    lbl, _ = label(is_bg_candidate)
    bg_mask = (lbl == lbl[0, 0])
    
    # Bottom right cast shadow & sliver cleanup
    y_coords, x_coords = np.indices(arr.shape[:2])
    shadow_mask = (y_coords > 800) & (x_coords > 820)
    bg_mask = bg_mask | shadow_mask

    r = arr[:, :, 0]
    g = arr[:, :, 1]
    b = arr[:, :, 2]
    lum = (r * 0.299 + g * 0.587 + b * 0.114)

    # Region segmentation masks
    outline_mask = (~bg_mask) & (lum < 75)
    lavender_mask = (~bg_mask) & (~outline_mask) & (b > 170) & (b > r + 20) & (lum > 110)
    beige_mask = (~bg_mask) & (~outline_mask) & (r > 170) & (g > 140) & (r > b + 15) & (lum > 140)
    screen_mask = (~bg_mask) & (~outline_mask) & (x_coords > 260) & (x_coords < 800) & (y_coords > 120) & (y_coords < 630) & (b > r + 5) & (lum < 160)
    face_mask = (~bg_mask) & (x_coords > 380) & (x_coords < 700) & (y_coords > 330) & (y_coords < 490) & (lum > 220)
    note_mask = (~bg_mask) & (x_coords >= 265) & (x_coords <= 410) & (y_coords >= 145) & (y_coords <= 315) & (lum > 200) & (~face_mask)
    tape_mask = (~bg_mask) & (x_coords >= 320) & (x_coords <= 355) & (y_coords >= 110) & (y_coords <= 195) & (r > 180) & (b < 120)
    classified = lavender_mask | beige_mask | screen_mask | face_mask | note_mask | tape_mask | outline_mask | bg_mask
    other_accents = (~classified)

    def render_img(chassis_col, bezel_col, screen_col, face_col, outline_col, note_col, tape_col, accent_col):
        out = np.zeros_like(arr)
        out[:, :, 3] = 255
        out[bg_mask, 3] = 0

        def apply_tint(mask, target_col):
            if np.sum(mask) == 0: return
            target = np.array(target_col, dtype=float)
            region_lum = lum[mask]
            mean_lum = np.mean(region_lum) if np.mean(region_lum) > 0 else 1.0
            scale = np.clip(region_lum / mean_lum, 0.75, 1.25)[:, None]
            out[mask, :3] = np.clip(target * scale, 0, 255)

        apply_tint(lavender_mask, chassis_col)
        apply_tint(beige_mask, bezel_col)
        apply_tint(screen_mask, screen_col)
        apply_tint(face_mask, face_col)
        apply_tint(note_mask, note_col)
        apply_tint(tape_mask, tape_col)
        apply_tint(other_accents, accent_col)
        out[outline_mask, :3] = outline_col

        ys, xs = np.where(~bg_mask)
        ymin, ymax = ys.min(), ys.max()
        xmin, xmax = xs.min(), xs.max()
        cropped = out[ymin:ymax+1, xmin:xmax+1]
        
        # Clean bottom right edge
        h, w = cropped.shape[:2]
        cropped[int(h*0.95):, int(w*0.95):, 3] = 0

        return Image.fromarray(cropped.astype(np.uint8))

    os.makedirs('assets', exist_ok=True)

    # 1. Azure Developer Theme (Dark Mode)
    # Chassis: Dark Azure Slate (#182230), Bezel: Steel Navy (#243244), Screen: CRT Black (#080c12)
    # Face: Light Azure (#8CB9CC), Tape/Accents: Dark Azure (#00638E), Note: Document White (#e2e8f0)
    img_dark = render_img(
        chassis_col=[24, 34, 48],
        bezel_col=[36, 50, 68],
        screen_col=[8, 12, 18],
        face_col=[140, 185, 204],
        outline_col=[14, 17, 23],
        note_col=[226, 232, 240],
        tape_col=[0, 99, 142],
        accent_col=[0, 99, 142]
    )
    img_dark.save('assets/computer_dark.png')

    # 2. Slate Developer Theme (Light Mode)
    # Chassis: Cool Slate Gray (#e1e8f0), Bezel: Clean Titanium (#f0f4f8), Screen: Deep Navy CRT (#0f172a)
    # Face: Sky Cyan (#38bdf8), Tape/Accents: Deep Azure (#0284c7), Note: Yellow Note (#fef08a)
    img_light = render_img(
        chassis_col=[225, 232, 240],
        bezel_col=[240, 244, 248],
        screen_col=[15, 23, 42],
        face_col=[56, 189, 248],
        outline_col=[30, 41, 59],
        note_col=[254, 240, 138],
        tape_col=[2, 132, 199],
        accent_col=[2, 132, 199]
    )
    img_light.save('assets/computer_light.png')

def make_svg(theme='dark'):
    is_dark = (theme == 'dark')
    bg_color = '#0e1117' if is_dark else '#ffffff'
    border_color = '#00638E' if is_dark else '#004A6B'
    key_color = '#8CB9CC' if is_dark else '#004A6B'
    val_color = '#FFFFFF' if is_dark else '#1f2328'
    dot_color = '#3d4f5d' if is_dark else '#8c959f'
    header_color = '#BFD8E3' if is_dark else '#004A6B'
    rule_color = '#2B2B2B' if is_dark else '#d0d7de'

    img_file = 'assets/computer_dark.png' if is_dark else 'assets/computer_light.png'
    with open(img_file, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode('utf-8')
    data_uri = f'data:image/png;base64,{b64}'

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
        ('field', 'LinkedIn', 'https://www.linkedin.com/in/gokulrlukog/', 68),
        ('field', 'Portfolio', 'https://gokul-portfolio-sepia.vercel.app/', 68),
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

    # Left side: Developer Computer Illustration
    # Fit into width ~ 380, height ~ 340, centered in left half (x from 20 to 450, y from 0 to 580)
    svg.append(f'<image href="{data_uri}" x="45" y="115" width="380" height="340" preserveAspectRatio="xMidYMid meet"/>')

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
    prepare_recolored_assets()
    
    dark_svg = make_svg('dark')
    light_svg = make_svg('light')

    # XML Validation
    ET.fromstring(dark_svg)
    ET.fromstring(light_svg)

    with open('assets/dark_mode.svg', 'w', encoding='utf-8') as f:
        f.write(dark_svg)

    with open('assets/light_mode.svg', 'w', encoding='utf-8') as f:
        f.write(light_svg)

    print('Successfully generated and validated assets/dark_mode.svg and assets/light_mode.svg with Developer Computer')

if __name__ == '__main__':
    generate()
