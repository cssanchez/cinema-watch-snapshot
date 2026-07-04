#!/usr/bin/env python3
import re
from pathlib import Path

DOCS_ROOT = Path(__file__).parent / 'docs'

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    pattern = re.compile(
        r"([ \t]*)function sortRowsForFront\(rows, resultPreset = null\) \{\s*"
        r"const normalizedSort = String\(resultPreset\?\.sort \|\| ''\)\.trim\(\)\.toLowerCase\(\);\s*"
        r"const nextRows = \[\.\.\.rows\];\s*"
        r"if \(normalizedSort === 'sold_desc'\) \{\s*"
        r"nextRows\.sort\(\(left, right\) => \{\s*"
        r"const leftSold = toInt\(left\.sold_percent\);\s*"
        r"const rightSold = toInt\(right\.sold_percent\);\s*"
        r"const leftRank = leftSold === null \? -1 : leftSold;\s*"
        r"const rightRank = rightSold === null \? -1 : rightSold;\s*"
        r"if \(rightRank !== leftRank\) \{\s*"
        r"return rightRank - leftRank;\s*"
        r"\}\s*"
        r"const leftKey = `\$\{left\.date_iso\}\|\$\{left\.time_label\}\|\$\{left\.movie_title\}`;\s*"
        r"const rightKey = `\$\{right\.date_iso\}\|\$\{right\.time_label\}\|\$\{right\.movie_title\}`;\s*"
        r"return leftKey\.localeCompare\(rightKey\);\s*"
        r"\}\);\s*"
        r"return nextRows;\s*"
        r"\}\s*"
        r"nextRows\.sort\(\(left, right\) => \{\s*"
        r"const leftKey = `\$\{left\.date_iso\}\|\$\{left\.time_label\}`;\s*"
        r"const rightKey = `\$\{right\.date_iso\}\|\$\{right\.time_label\}`;\s*"
        r"return leftKey\.localeCompare\(rightKey\);\s*"
        r"\}\);\s*"
        r"return nextRows;\s*"
        r"\}",
        re.MULTILINE
    )

    def repl(match):
        indent = match.group(1)
        return (
            f"{indent}function sortRowsForFront(rows, resultPreset = null) {{\n"
            f"{indent}  const normalizedSort = String(resultPreset?.sort || '').trim().toLowerCase();\n"
            f"{indent}  const nextRows = [...rows];\n"
            f"{indent}  if (normalizedSort === 'sold_desc') {{\n"
            f"{indent}    nextRows.sort((left, right) => {{\n"
            f"{indent}      const leftSold = toInt(left.sold_percent);\n"
            f"{indent}      const rightSold = toInt(right.sold_percent);\n"
            f"{indent}      const leftRank = leftSold === null ? -1 : leftSold;\n"
            f"{indent}      const rightRank = rightSold === null ? -1 : rightSold;\n"
            f"{indent}      if (rightRank !== leftRank) {{\n"
            f"{indent}        return rightRank - leftRank;\n"
            f"{indent}      }}\n"
            f"{indent}      const lDate = left.date_iso || '';\n"
            f"{indent}      const rDate = right.date_iso || '';\n"
            f"{indent}      if (lDate !== rDate) return lDate < rDate ? -1 : 1;\n"
            f"{indent}      const lTime = left.time_label || '';\n"
            f"{indent}      const rTime = right.time_label || '';\n"
            f"{indent}      if (lTime !== rTime) return lTime < rTime ? -1 : 1;\n"
            f"{indent}      const lTitle = left.movie_title || '';\n"
            f"{indent}      const rTitle = right.movie_title || '';\n"
            f"{indent}      if (lTitle !== rTitle) return lTitle < rTitle ? -1 : 1;\n"
            f"{indent}      return 0;\n"
            f"{indent}    }});\n"
            f"{indent}    return nextRows;\n"
            f"{indent}  }}\n"
            f"{indent}  nextRows.sort((left, right) => {{\n"
            f"{indent}    const lDate = left.date_iso || '';\n"
            f"{indent}    const rDate = right.date_iso || '';\n"
            f"{indent}    if (lDate !== rDate) return lDate < rDate ? -1 : 1;\n"
            f"{indent}    const lTime = left.time_label || '';\n"
            f"{indent}    const rTime = right.time_label || '';\n"
            f"{indent}    if (lTime !== rTime) return lTime < rTime ? -1 : 1;\n"
            f"{indent}    return 0;\n"
            f"{indent}  }});\n"
            f"{indent}  return nextRows;\n"
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

    print(f"Patched {processed_count} files out of {len(files)} total HTML files.")

if __name__ == '__main__':
    main()
