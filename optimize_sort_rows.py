import re
from pathlib import Path

DOCS_ROOT = Path('docs')

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    pattern_sold_desc = re.compile(
        r"([ \t]*)const leftKey = `\$\{left\.date_iso\}\|\$\{left\.time_label\}\|\$\{left\.movie_title\}`;?\s*"
        r"const rightKey = `\$\{right\.date_iso\}\|\$\{right\.time_label\}\|\$\{right\.movie_title\}`;?\s*"
        r"return leftKey\.localeCompare\(rightKey\);?",
        re.MULTILINE
    )

    def repl_sold_desc(match):
        indent = match.group(1)
        return (
            f"{indent}const ld = left.date_iso || '';\n"
            f"{indent}const rd = right.date_iso || '';\n"
            f"{indent}if (ld !== rd) return ld < rd ? -1 : 1;\n"
            f"{indent}const lt = left.time_label || '';\n"
            f"{indent}const rt = right.time_label || '';\n"
            f"{indent}if (lt !== rt) return lt < rt ? -1 : 1;\n"
            f"{indent}const lm = left.movie_title || '';\n"
            f"{indent}const rm = right.movie_title || '';\n"
            f"{indent}if (lm !== rm) return lm < rm ? -1 : 1;\n"
            f"{indent}return 0;"
        )

    content = pattern_sold_desc.sub(repl_sold_desc, content)

    pattern_default = re.compile(
        r"([ \t]*)const leftKey = `\$\{left\.date_iso\}\|\$\{left\.time_label\}`;?\s*"
        r"const rightKey = `\$\{right\.date_iso\}\|\$\{right\.time_label\}`;?\s*"
        r"return leftKey\.localeCompare\(rightKey\);?",
        re.MULTILINE
    )

    def repl_default(match):
        indent = match.group(1)
        return (
            f"{indent}const ld = left.date_iso || '';\n"
            f"{indent}const rd = right.date_iso || '';\n"
            f"{indent}if (ld !== rd) return ld < rd ? -1 : 1;\n"
            f"{indent}const lt = left.time_label || '';\n"
            f"{indent}const rt = right.time_label || '';\n"
            f"{indent}if (lt !== rt) return lt < rt ? -1 : 1;\n"
            f"{indent}return 0;"
        )

    content = pattern_default.sub(repl_default, content)

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
