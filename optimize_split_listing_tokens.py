#!/usr/bin/env python3
import re
from pathlib import Path

DOCS_ROOT = Path(__file__).parent / 'docs'

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    pattern = re.compile(
        r"([ \t]*)function splitListingTokens\(value\) \{\s*"
        r"const text = String\(value \|\| ''\)\.trim\(\);\s*"
        r"if \(!text\) return \[\];\s*"
        r"const normalized = text\s*"
        r"\.replaceAll\('•', '\|'\)\s*"
        r"\.replaceAll\('·', '\|'\)\s*"
        r"\.replaceAll\('/', '\|'\)\s*"
        r"\.replaceAll\(' - ', '\|'\);\s*"
        r"return normalized\s*"
        r"\.split\('\|'\)\s*"
        r"\.map\(\(part\) => part\.trim\(\)\.replace\(/\\s\+/g, ' '\)\)\s*"
        r"\.filter\(Boolean\);\s*"
        r"\}",
        re.MULTILINE
    )

    def repl(match):
        indent = match.group(1)
        return (
            f"{indent}const _splitListingTokensCache = new Map();\n"
            f"{indent}function splitListingTokens(value) {{\n"
            f"{indent}  const text = String(value || '').trim();\n"
            f"{indent}  if (!text) return [];\n"
            f"{indent}  if (_splitListingTokensCache.has(text)) return [..._splitListingTokensCache.get(text)];\n"
            f"{indent}  const normalized = text\n"
            f"{indent}    .replaceAll('•', '|')\n"
            f"{indent}    .replaceAll('·', '|')\n"
            f"{indent}    .replaceAll('/', '|')\n"
            f"{indent}    .replaceAll(' - ', '|');\n"
            f"{indent}  const result = normalized\n"
            f"{indent}    .split('|')\n"
            f"{indent}    .map((part) => part.trim().replace(/\\s+/g, ' '))\n"
            f"{indent}    .filter(Boolean);\n"
            f"{indent}  if (_splitListingTokensCache.size > 2000) _splitListingTokensCache.clear();\n"
            f"{indent}  _splitListingTokensCache.set(text, result);\n"
            f"{indent}  return [...result];\n"
            f"{indent}}}"
        )
    content = pattern.sub(repl, content)

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
