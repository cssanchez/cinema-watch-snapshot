#!/usr/bin/env python3
import re
from pathlib import Path

DOCS_ROOT = Path(__file__).parent / 'docs'

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Step 1: Extract the buttons inside the nav-location-dropdown
    options_pattern = re.compile(r'<div class="nav-location-menu" hidden>(.*?)</div>', re.DOTALL)
    options_match = options_pattern.search(content)
    if not options_match:
        print(f"Skipping {file_path}: No location menu found")
        return False

    options_html = options_match.group(1).strip()

    # Step 2: Remove the nav-location-dropdown from the topbar
    dropdown_pattern = re.compile(r'\s*<div class="nav-location-dropdown" data-location-dropdown>.*?</div>(?=\s*<div class="nav-tools">)', re.DOTALL)
    content = dropdown_pattern.sub('', content)

    # Step 3: Insert the new location selector panel below the front-hero and above the cartelera
    new_panel = f"""
<div class="location-selector" style="margin-top: 1rem;">
  <p data-i18n-source>Zone</p>
  <div class="location-selector-options">
    {options_html}
  </div>
</div>
"""

    hero_pattern = re.compile(r'(</section>\s*)<div id="cartelera" aria-hidden="true"></div>')
    content = hero_pattern.sub(r'\1' + new_panel + r'\n<div id="cartelera" aria-hidden="true"></div>', content)

    # Step 4: Remove JS related to toggling the dropdown
    # We want to remove the click handler parts that reference nav-location-dropdown-toggle
    # But keep the handler that handles the location-target buttons
    js_toggle_pattern = re.compile(
        r"const toggle = event\.target\.closest\('\[data-location-dropdown-toggle\]'\);.*?return;\n\s*\}\n\n\s*if \(!event\.target\.closest\('\[data-location-dropdown\]'\)\) \{.*?\n\s*\}\n",
        re.DOTALL
    )
    content = js_toggle_pattern.sub('', content)

    js_close_pattern = re.compile(
        r"const menuToClose = document\.querySelector\('\.nav-location-menu'\);.*?toggleToClose\.setAttribute\('aria-expanded', 'false'\);\n\s*\}",
        re.DOTALL
    )
    content = js_close_pattern.sub('', content)

    # Let's fix the css in media queries where nav-location-dropdown is referenced
    css_pattern = re.compile(r'\s*\.nav-location-dropdown \{[^}]*\}', re.DOTALL)
    content = css_pattern.sub('', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return True

def main():
    files = list(DOCS_ROOT.rglob('index.html'))
    for file in files:
        if process_file(file):
            print(f"Processed {file.relative_to(DOCS_ROOT)}")

if __name__ == "__main__":
    main()
