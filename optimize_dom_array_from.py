#!/usr/bin/env python3
import re
from pathlib import Path

DOCS_ROOT = Path(__file__).parent / 'docs'

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

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

    # 2. getActiveHomeSections
    pattern2 = re.compile(
        r"([ \t]*)const visiblePanel = Array\.from\(document\.querySelectorAll\('\[data-location-panel\]'\)\)\s*"
        r"\.find\(\(panel\) => panel instanceof HTMLElement && !panel\.hidden\);",
        re.MULTILINE
    )

    def repl2(match):
        indent = match.group(1)
        return f"{indent}const visiblePanel = getVisibleLocationPanel();"

    content = pattern2.sub(repl2, content)

    # 3. scrollToSpecialRooms
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

    # 4. scrollToMoviesSection
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

    # 5. initFrontBoards
    pattern_init = re.compile(
        r"([ \t]*)const locationKeys = new Set\(\s*"
        r"Array\.from\(root\.querySelectorAll\('\[data-front-board-location\]'\)\)\s*"
        r"\.map\(\(element\) => element\.getAttribute\('data-front-board-location'\) \|\| ''\)\s*"
        r"\.filter\(Boolean\)\s*"
        r"\);", re.MULTILINE
    )

    def repl_init(match):
        indent = match.group(1)
        return (
            f"{indent}// ⚡ Bolt Optimization: Replace Array.from().map().filter() with single-pass loop\n"
            f"{indent}const _elements = root.querySelectorAll('[data-front-board-location]');\n"
            f"{indent}const locationKeys = new Set();\n"
            f"{indent}for (let i = 0; i < _elements.length; i++) {{\n"
            f"{indent}  const val = _elements[i].getAttribute('data-front-board-location');\n"
            f"{indent}  if (val) locationKeys.add(val);\n"
            f"{indent}}}"
        )

    content = pattern_init.sub(repl_init, content)

    # 6. syncActiveQuickBoardPresets
    pattern_sync = re.compile(
        r"([ \t]*)const locationKeys = new Set\(\s*"
        r"Array\.from\(root\.querySelectorAll\('form\[data-front-advanced-form=\"true\"\]'\)\)\s*"
        r"\.map\(\(form\) => form instanceof HTMLFormElement \? String\(form\.dataset\.frontLocationKey \|\| ''\)\.trim\(\) : ''\)\s*"
        r"\.filter\(Boolean\)\s*"
        r"\);", re.MULTILINE
    )

    def repl_sync(match):
        indent = match.group(1)
        return (
            f"{indent}// ⚡ Bolt Optimization: Replace Array.from().map().filter() with single-pass loop\n"
            f"{indent}const _forms = root.querySelectorAll('form[data-front-advanced-form=\"true\"]');\n"
            f"{indent}const locationKeys = new Set();\n"
            f"{indent}for (let i = 0; i < _forms.length; i++) {{\n"
            f"{indent}  const form = _forms[i];\n"
            f"{indent}  if (form instanceof HTMLFormElement) {{\n"
            f"{indent}    const val = String(form.dataset.frontLocationKey || '').trim();\n"
            f"{indent}    if (val) locationKeys.add(val);\n"
            f"{indent}  }}\n"
            f"{indent}}}"
        )

    content = pattern_sync.sub(repl_sync, content)

    # 7. Array.from().some() for HTMLSelectElement.options
    pattern_options = re.compile(r"!Array\.from\(field\.options\)\.some\(\(opt\) => opt\.value === ([a-zA-Z]+)\)")
    def repl_options(match):
        var_name = match.group(1)
        return f"!Array.prototype.some.call(field.options, (opt) => opt.value === {var_name})"
    content = pattern_options.sub(repl_options, content)

    # 8. setFrontBoard availableKeys
    pattern_available_keys = re.compile(
        r"([ \t]*)const availableKeys = new Set\(panels\.map\(\(panel\) => panel\.dataset\.frontBoardPanel \|\| ''\)\);", re.MULTILINE
    )

    def repl_available_keys(match):
        indent = match.group(1)
        return (
            f"{indent}// ⚡ Bolt Optimization: Replace Array.map() with single-pass loop for Set initialization\n"
            f"{indent}const availableKeys = new Set();\n"
            f"{indent}for (let i = 0; i < panels.length; i++) {{\n"
            f"{indent}  availableKeys.add(panels[i].dataset.frontBoardPanel || '');\n"
            f"{indent}}}"
        )

    content = pattern_available_keys.sub(repl_available_keys, content)

    # 9. setFrontBoard activeButton
    pattern_active_button = re.compile(
        r"([ \t]*)const activeButton = buttons\.find\(\(button\) => button\.getAttribute\('aria-pressed'\) === 'true'\);", re.MULTILINE
    )

    def repl_active_button(match):
        indent = match.group(1)
        return (
            f"{indent}// ⚡ Bolt Optimization: Replace Array.find() with loop to avoid NodeList to Array conversion\n"
            f"{indent}let activeButton = undefined;\n"
            f"{indent}for (let i = 0; i < buttons.length; i++) {{\n"
            f"{indent}  if (buttons[i].getAttribute('aria-pressed') === 'true') {{\n"
            f"{indent}    activeButton = buttons[i];\n"
            f"{indent}    break;\n"
            f"{indent}  }}\n"
            f"{indent}}}"
        )

    content = pattern_active_button.sub(repl_active_button, content)

    # 10. Remove Array.from around buttons and panels in setFrontBoard and setBoardPanel if no other array methods are used
    # In setFrontBoard:
    content = content.replace("const buttons = Array.from(\n          root.querySelectorAll(`[data-front-board-location=\"${locationKey}\"][data-front-board-target]`)\n        );", "const buttons = root.querySelectorAll(`[data-front-board-location=\"${locationKey}\"][data-front-board-target]`);")
    content = content.replace("const panels = Array.from(\n          root.querySelectorAll(`[data-front-board-location=\"${locationKey}\"][data-front-board-panel]`)\n        );", "const panels = root.querySelectorAll(`[data-front-board-location=\"${locationKey}\"][data-front-board-panel]`);")
    # And there are also direct root.querySelectorAll without variables sometimes:
    # Actually, setHomepageLocation does this:
    # const buttons = Array.from(root.querySelectorAll('[data-location-target]'));
    # const panels = Array.from(root.querySelectorAll('[data-location-panel]'));
    # and then iterates via `for (const button of buttons)` and `for (const panel of panels)`.
    # `for...of` works natively on NodeList, so we can remove Array.from there too!
    content = content.replace("const buttons = Array.from(root.querySelectorAll('[data-location-target]'));", "const buttons = root.querySelectorAll('[data-location-target]');")
    content = content.replace("const panels = Array.from(root.querySelectorAll('[data-location-panel]'));", "const panels = root.querySelectorAll('[data-location-panel]');")

    # In setBoardPanel:
    content = content.replace("const buttons = Array.from(\n          document.querySelectorAll(`[data-front-board-location=\"${locationKey}\"][data-front-board-target]`)\n        );", "const buttons = document.querySelectorAll(`[data-front-board-location=\"${locationKey}\"][data-front-board-target]`);")
    content = content.replace("const panels = Array.from(\n          document.querySelectorAll(`[data-front-board-location=\"${locationKey}\"][data-front-board-panel]`)\n        );", "const panels = document.querySelectorAll(`[data-front-board-location=\"${locationKey}\"][data-front-board-panel]`);")

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
