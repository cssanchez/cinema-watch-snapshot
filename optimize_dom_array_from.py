#!/usr/bin/env python3
import re
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor

DOCS_ROOT = Path(__file__).parent / 'docs'

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # We want to replace `Array.from(document.querySelectorAll(...)).find(...)` with a for-loop over NodeList.
    # The functions currentHomeSectionFocus and other functions rely on these panel searches frequently.

    # 1. getVisibleLocationPanel
    pattern1 = re.compile(
        r"([ \t]*)function getVisibleLocationPanel\(\)\s*\{\s*"
        r"return Array\.from\(document\.querySelectorAll\('\[data-location-panel\]'\)\)\s*"
        r"\.find\(\(panel\) => panel instanceof HTMLElement && !panel\.hidden\) \|\| null;\s*"
        r"\}",
        re.MULTILINE
    )

    def repl1(match):
        indent = match.group(1)
        return (
            f"{indent}function getVisibleLocationPanel() {{\n"
            f"{indent}  const panels = document.querySelectorAll('[data-location-panel]');\n"
            f"{indent}  for (let i = 0; i < panels.length; i++) {{\n"
            f"{indent}    const panel = panels[i];\n"
            f"{indent}    if (panel instanceof HTMLElement && !panel.hidden) return panel;\n"
            f"{indent}  }}\n"
            f"{indent}  return null;\n"
            f"{indent}}}"
        )
    content = pattern1.sub(repl1, content)

    # 2. getActiveHomeSections - replacing Array.from with getVisibleLocationPanel
    pattern2 = re.compile(
        r"([ \t]*)const visiblePanel = Array\.from\(document\.querySelectorAll\('\[data-location-panel\]'\)\)\s*"
        r"\.find\(\(panel\) => panel instanceof HTMLElement && !panel\.hidden\);",
        re.MULTILINE
    )

    def repl2(match):
        indent = match.group(1)
        return f"{indent}const visiblePanel = getVisibleLocationPanel();"

    content = pattern2.sub(repl2, content)

    # 3. scrollToSpecialRooms - fix target lookup (second Array.from)
    pattern3 = re.compile(
        r"([ \t]*)target = Array\.from\(document\.querySelectorAll\('\[data-front-specials=\"true\"\]'\)\)\s*"
        r"\.find\(\(section\) => \{\s*"
        r"if \(!\(section instanceof HTMLElement\)\) \{\s*"
        r"return false;\s*"
        r"\}\s*"
        r"const panel = section\.closest\('\[data-location-panel\]'\);\s*"
        r"return !\(panel instanceof HTMLElement\) \|\| !panel\.hidden;\s*"
        r"\}\);",
        re.MULTILINE
    )

    def repl3(match):
        indent = match.group(1)
        return (
            f"{indent}const specials = document.querySelectorAll('[data-front-specials=\"true\"]');\n"
            f"{indent}target = undefined;\n"
            f"{indent}for (let i = 0; i < specials.length; i++) {{\n"
            f"{indent}  const section = specials[i];\n"
            f"{indent}  if (section instanceof HTMLElement) {{\n"
            f"{indent}    const panel = section.closest('[data-location-panel]');\n"
            f"{indent}    if (!(panel instanceof HTMLElement) || !panel.hidden) {{\n"
            f"{indent}      target = section;\n"
            f"{indent}      break;\n"
            f"{indent}    }}\n"
            f"{indent}  }}\n"
            f"{indent}}}"
        )

    content = pattern3.sub(repl3, content)

    # 4. scrollToMoviesSection - fix target lookup (second Array.from)
    pattern4 = re.compile(
        r"([ \t]*)target = Array\.from\(document\.querySelectorAll\('\[data-front-movies=\"true\"\]'\)\)\s*"
        r"\.find\(\(section\) => \{\s*"
        r"if \(!\(section instanceof HTMLElement\)\) \{\s*"
        r"return false;\s*"
        r"\}\s*"
        r"const panel = section\.closest\('\[data-location-panel\]'\);\s*"
        r"return !\(panel instanceof HTMLElement\) \|\| !panel\.hidden;\s*"
        r"\}\);",
        re.MULTILINE
    )

    def repl4(match):
        indent = match.group(1)
        return (
            f"{indent}const movies = document.querySelectorAll('[data-front-movies=\"true\"]');\n"
            f"{indent}target = undefined;\n"
            f"{indent}for (let i = 0; i < movies.length; i++) {{\n"
            f"{indent}  const section = movies[i];\n"
            f"{indent}  if (section instanceof HTMLElement) {{\n"
            f"{indent}    const panel = section.closest('[data-location-panel]');\n"
            f"{indent}    if (!(panel instanceof HTMLElement) || !panel.hidden) {{\n"
            f"{indent}      target = section;\n"
            f"{indent}      break;\n"
            f"{indent}    }}\n"
            f"{indent}  }}\n"
            f"{indent}}}"
        )

    content = pattern4.sub(repl4, content)

    # 5. _getNavLinks replacement
    # We should also replace Array.from on document.querySelectorAll generally where find is used.
    # We found `Array.from(document.querySelectorAll('[data-location-panel]')).find` inside:
    # - getVisibleLocationPanel
    # - getActiveHomeSections
    # - scrollToCartelera
    # - scrollToSpecialRooms
    # - scrollToMoviesSection
    # Since `pattern2` replaces the exact code `const visiblePanel = Array.from(document.querySelectorAll('[data-location-panel]')).find(...)` with `const visiblePanel = getVisibleLocationPanel();`, and since that exact code is used inside `getActiveHomeSections`, `scrollToCartelera`, `scrollToSpecialRooms`, and `scrollToMoviesSection`, it actually covers all of them!

    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    files = list(DOCS_ROOT.rglob('*.html'))

    with ProcessPoolExecutor() as executor:
        results = list(executor.map(process_file, files))

    processed_count = sum(1 for r in results if r)
    print(f"Patched {processed_count} files out of {len(files)} total HTML files.")

if __name__ == '__main__':
    main()
