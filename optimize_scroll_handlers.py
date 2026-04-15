#!/usr/bin/env python3
import re
from pathlib import Path

DOCS_ROOT = Path(__file__).parent / 'docs'

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # 1. Memoize getActiveHomeSections based on visiblePanel
    pattern_active_sections = re.compile(
        r"([ \t]*)function getActiveHomeSections\(\)\s*\{\s*"
        r"const visiblePanel = getVisibleLocationPanel\(\);\s*"
        r"const specials = visiblePanel\?\.querySelector\('\[data-front-specials=\"true\"\]'\)\s*"
        r"\|\| document\.querySelector\('\[data-front-specials=\"true\"\]'\);\s*"
        r"const movies = visiblePanel\?\.querySelector\('\[data-front-movies=\"true\"\]'\)\s*"
        r"\|\| document\.querySelector\('\[data-front-movies=\"true\"\]'\);\s*"
        r"return \{\s*"
        r"cartelera: _getCartelera\(\),\s*"
        r"specials: specials instanceof HTMLElement \? specials : null,\s*"
        r"movies: movies instanceof HTMLElement \? movies : null,?\s*"
        r"\};\s*"
        r"\}",
        re.MULTILINE
    )

    def repl_active_sections(match):
        indent = match.group(1)
        return (
            f"{indent}let _lastVisiblePanel = undefined;\n"
            f"{indent}let _lastActiveSections = null;\n"
            f"{indent}function getActiveHomeSections() {{\n"
            f"{indent}  const visiblePanel = getVisibleLocationPanel();\n"
            f"{indent}  if (_lastVisiblePanel === visiblePanel && _lastActiveSections) {{\n"
            f"{indent}    return _lastActiveSections;\n"
            f"{indent}  }}\n"
            f"{indent}  const specials = visiblePanel?.querySelector('[data-front-specials=\"true\"]')\n"
            f"{indent}    || document.querySelector('[data-front-specials=\"true\"]');\n"
            f"{indent}  const movies = visiblePanel?.querySelector('[data-front-movies=\"true\"]')\n"
            f"{indent}    || document.querySelector('[data-front-movies=\"true\"]');\n"
            f"{indent}  _lastVisiblePanel = visiblePanel;\n"
            f"{indent}  _lastActiveSections = {{\n"
            f"{indent}    cartelera: _getCartelera(),\n"
            f"{indent}    specials: specials instanceof HTMLElement ? specials : null,\n"
            f"{indent}    movies: movies instanceof HTMLElement ? movies : null,\n"
            f"{indent}  }};\n"
            f"{indent}  return _lastActiveSections;\n"
            f"{indent}}}"
        )

    content = pattern_active_sections.sub(repl_active_sections, content)

    # 2. Optimize URLSearchParams parsing in syncTopNavState
    pattern_sync_top_nav = re.compile(
        r"([ \t]*)function syncTopNavState\(\)\s*\{\s*"
        r"const path = window\.location\.pathname \|\| '/';\s*"
        r"const params = new URLSearchParams\(window\.location\.search \|\| ''\);\s*"
        r"const category = \(params\.get\('category'\) \|\| ''\)\.toLowerCase\(\);\s*"
        r"const focusParam = \(params\.get\('focus'\) \|\| ''\)\.toLowerCase\(\);\s*",
        re.MULTILINE
    )

    def repl_sync_top_nav(match):
        indent = match.group(1)
        return (
            f"{indent}let _lastSearch = null;\n"
            f"{indent}let _cachedCategory = '';\n"
            f"{indent}let _cachedFocusParam = '';\n"
            f"{indent}function syncTopNavState() {{\n"
            f"{indent}  const path = window.location.pathname || '/';\n"
            f"{indent}  const currentSearch = window.location.search || '';\n"
            f"{indent}  if (_lastSearch !== currentSearch) {{\n"
            f"{indent}    const params = new URLSearchParams(currentSearch);\n"
            f"{indent}    _cachedCategory = (params.get('category') || '').toLowerCase();\n"
            f"{indent}    _cachedFocusParam = (params.get('focus') || '').toLowerCase();\n"
            f"{indent}    _lastSearch = currentSearch;\n"
            f"{indent}  }}\n"
            f"{indent}  const category = _cachedCategory;\n"
            f"{indent}  const focusParam = _cachedFocusParam;\n"
        )

    content = pattern_sync_top_nav.sub(repl_sync_top_nav, content)

    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    files = list(DOCS_ROOT.rglob('*.html'))
    processed_count = 0
    for file_path in files:
        if process_file(file_path):
            processed_count += 1

    print(f"Patched {processed_count} files out of {len(files)} total HTML files.")

if __name__ == '__main__':
    main()
