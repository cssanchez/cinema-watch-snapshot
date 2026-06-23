#!/usr/bin/env python3
import re
from pathlib import Path

DOCS_ROOT = Path(__file__).parent / 'docs'

RE_SORT = re.compile(
    r"(\s*)function sortRowsForFront\(rows, resultPreset = null\) \{\s*const normalizedSort = String\(resultPreset\?\.sort \|\| ''\)\.trim\(\)\.toLowerCase\(\);\s*const nextRows = \[\.\.\.rows\];\s*if \(normalizedSort === 'sold_desc'\) \{\s*nextRows\.sort\(\(left, right\) => \{\s*const leftSold = toInt\(left\.sold_percent\);\s*const rightSold = toInt\(right\.sold_percent\);\s*const leftRank = leftSold === null \? -1 : leftSold;\s*const rightRank = rightSold === null \? -1 : rightSold;\s*if \(rightRank !== leftRank\) \{\s*return rightRank - leftRank;\s*\}\s*const leftKey = `\$\{left\.date_iso\}\|\$\{left\.time_label\}\|\$\{left\.movie_title\}`;\s*const rightKey = `\$\{right\.date_iso\}\|\$\{right\.time_label\}\|\$\{right\.movie_title\}`;\s*return leftKey\.localeCompare\(rightKey\);\s*\}\);\s*return nextRows;\s*\}\s*nextRows\.sort\(\(left, right\) => \{\s*const leftKey = `\$\{left\.date_iso\}\|\$\{left\.time_label\}`;\s*const rightKey = `\$\{right\.date_iso\}\|\$\{right\.time_label\}`;\s*return leftKey\.localeCompare\(rightKey\);\s*\}\);\s*return nextRows;\s*\}",
    re.MULTILINE
)

def process_file(filepath: Path) -> None:
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading {filepath.relative_to(DOCS_ROOT.parent)}: {e}")
        return

    # Check for idempotency
    if 'const _sortTitleKeyCache = new WeakMap();' in content:
        print(f"Skipping already patched file: {filepath.relative_to(DOCS_ROOT.parent)}")
        return

    original_content = content

    def replacer(match):
        indent = match.group(1)
        replacement = f"""{indent}// ⚡ Bolt Optimization: Memoize identity string concatenation in sort comparators to prevent excessive O(N log N) memory allocations and reduce GC pressure.
{indent}const _sortTitleKeyCache = new WeakMap();
{indent}const _sortTimeKeyCache = new WeakMap();
{indent}function sortRowsForFront(rows, resultPreset = null) {{
{indent}  const normalizedSort = String(resultPreset?.sort || '').trim().toLowerCase();
{indent}  const nextRows = [...rows];
{indent}  if (normalizedSort === 'sold_desc') {{
{indent}    nextRows.sort((left, right) => {{
{indent}      const leftSold = toInt(left.sold_percent);
{indent}      const rightSold = toInt(right.sold_percent);
{indent}      const leftRank = leftSold === null ? -1 : leftSold;
{indent}      const rightRank = rightSold === null ? -1 : rightSold;
{indent}      if (rightRank !== leftRank) {{
{indent}        return rightRank - leftRank;
{indent}      }}
{indent}      let leftKey = _sortTitleKeyCache.get(left);
{indent}      if (leftKey === undefined) {{
{indent}        leftKey = `${{left.date_iso}}|${{left.time_label}}|${{left.movie_title}}`;
{indent}        _sortTitleKeyCache.set(left, leftKey);
{indent}      }}
{indent}      let rightKey = _sortTitleKeyCache.get(right);
{indent}      if (rightKey === undefined) {{
{indent}        rightKey = `${{right.date_iso}}|${{right.time_label}}|${{right.movie_title}}`;
{indent}        _sortTitleKeyCache.set(right, rightKey);
{indent}      }}
{indent}      return leftKey.localeCompare(rightKey);
{indent}    }});
{indent}    return nextRows;
{indent}  }}
{indent}  nextRows.sort((left, right) => {{
{indent}    let leftKey = _sortTimeKeyCache.get(left);
{indent}    if (leftKey === undefined) {{
{indent}      leftKey = `${{left.date_iso}}|${{left.time_label}}`;
{indent}      _sortTimeKeyCache.set(left, leftKey);
{indent}    }}
{indent}    let rightKey = _sortTimeKeyCache.get(right);
{indent}    if (rightKey === undefined) {{
{indent}      rightKey = `${{right.date_iso}}|${{right.time_label}}`;
{indent}      _sortTimeKeyCache.set(right, rightKey);
{indent}    }}
{indent}    return leftKey.localeCompare(rightKey);
{indent}  }});
{indent}  return nextRows;
{indent}}}"""
        # Ensure that no double newlines exist
        lines = [line for line in replacement.split('\n') if line.strip() != '']
        return '\n'.join(lines)

    content = RE_SORT.sub(replacer, content)

    if content != original_content:
        try:
            filepath.write_text(content, encoding='utf-8')
            print(f"Patched {filepath.relative_to(DOCS_ROOT.parent)}")
        except Exception as e:
            print(f"Error writing {filepath.relative_to(DOCS_ROOT.parent)}: {e}")
    else:
        print(f"No match found in {filepath.relative_to(DOCS_ROOT.parent)}")

def main() -> None:
    print(f"Scanning for HTML files in {DOCS_ROOT}...")
    html_files = list(DOCS_ROOT.rglob("*.html"))
    print(f"Found {len(html_files)} HTML files.")

    for filepath in html_files:
        process_file(filepath)

    print("Done applying optimizations.")

if __name__ == "__main__":
    main()
