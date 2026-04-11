#!/usr/bin/env python3
import re
from pathlib import Path

DOCS_ROOT = Path(__file__).parent / 'docs'

RE_GET_SCREENINGS_LINK = re.compile(r"([ \t]*)function getScreeningsLink\(\)\s*\{")

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    if "let _cachedTopbar = null;" not in content:
        # Define cache code inside regex sub using lambda
        def replace_with_cache(match):
            indent = match.group(1)
            formatted_cache = (
                f"{indent}let _cachedTopbar = null;\n"
                f"{indent}function _getTopbar() {{\n"
                f"{indent}  if (!_cachedTopbar) _cachedTopbar = document.querySelector('.topbar');\n"
                f"{indent}  return _cachedTopbar;\n"
                f"{indent}}}\n\n"
                f"{indent}let _cachedScreeningsLink = null;\n"
                f"{indent}function _getScreeningsLink() {{\n"
                f"{indent}  if (!_cachedScreeningsLink) _cachedScreeningsLink = document.querySelector('[data-nav-link=\"screenings\"]');\n"
                f"{indent}  return _cachedScreeningsLink;\n"
                f"{indent}}}\n\n"
                f"{indent}let _cachedCartelera = null;\n"
                f"{indent}function _getCartelera() {{\n"
                f"{indent}  if (!_cachedCartelera) _cachedCartelera = document.getElementById('cartelera');\n"
                f"{indent}  return _cachedCartelera;\n"
                f"{indent}}}\n\n"
                f"{indent}let _cachedNavLinks = null;\n"
                f"{indent}function _getNavLinks() {{\n"
                f"{indent}  if (!_cachedNavLinks) _cachedNavLinks = document.querySelectorAll('[data-nav-link]');\n"
                f"{indent}  return _cachedNavLinks;\n"
                f"{indent}}}\n\n"
                f"{indent}function getScreeningsLink() {{"
            )
            return formatted_cache

        content = RE_GET_SCREENINGS_LINK.sub(replace_with_cache, content)

    # Replace queries with our cached functions using compiled regexes
    # document.querySelector('.topbar') -> _getTopbar()
    content = re.sub(r"document\.querySelector\('\.topbar'\)", "_getTopbar()", content)

    # document.querySelector('[data-nav-link="screenings"]') -> _getScreeningsLink()
    # Ensure we don't replace the one inside _getScreeningsLink itself
    # We can use negative lookbehind but Python's re doesn't support variable length lookbehind.
    # Instead, we just replace all, and then fix the definition.
    content = content.replace("document.querySelector('[data-nav-link=\"screenings\"]')", "_getScreeningsLink()")
    content = content.replace("_cachedScreeningsLink = _getScreeningsLink();", "_cachedScreeningsLink = document.querySelector('[data-nav-link=\"screenings\"]');")

    # We also need to fix _getTopbar and _getCartelera and _getNavLinks because the generic replacements will touch them too
    content = content.replace("_cachedTopbar = _getTopbar();", "_cachedTopbar = document.querySelector('.topbar');")

    content = content.replace("document.querySelectorAll('[data-nav-link]')", "_getNavLinks()")
    content = content.replace("_cachedNavLinks = _getNavLinks();", "_cachedNavLinks = document.querySelectorAll('[data-nav-link]');")

    content = content.replace("document.getElementById('cartelera')", "_getCartelera()")
    content = content.replace("_cachedCartelera = _getCartelera();", "_cachedCartelera = document.getElementById('cartelera');")

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
            print(f"Patched: {file_path.relative_to(DOCS_ROOT)}")

    print(f"\nDone! Patched {processed_count} files out of {len(files)} total HTML files.")

if __name__ == '__main__':
    main()
