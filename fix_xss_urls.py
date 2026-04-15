import os
import re
from pathlib import Path

def process_file(filepath):
    content = filepath.read_text(encoding="utf-8")
    original_content = content

    # Inject sanitizeUrl right before mapStaticRows
    if "function sanitizeUrl(" not in content:
        sanitize_fn = (
            "      function sanitizeUrl(url) {\n"
            "        const str = String(url || '').trim();\n"
            "        const lower = str.toLowerCase();\n"
            "        if (lower.startsWith('javascript:') || lower.startsWith('data:') || lower.startsWith('vbscript:')) {\n"
            "          return '#';\n"
            "        }\n"
            "        return str;\n"
            "      }\n\n"
            "      function mapStaticRows(rows) {"
        )
        content = content.replace("      function mapStaticRows(rows) {", sanitize_fn)

    # Update mapStaticRows to use sanitizeUrl
    content = re.sub(
        r"movie_href:\s*String\(row\.movie_href\s*\|\|\s*''\),",
        r"movie_href: sanitizeUrl(row.movie_href),",
        content
    )
    content = re.sub(
        r"venue_href:\s*String\(row\.venue_href\s*\|\|\s*''\),",
        r"venue_href: sanitizeUrl(row.venue_href),",
        content
    )

    # Update mapApiRows to use sanitizeUrl (if it exists)
    content = re.sub(
        r"venue_href:\s*String\(row\.venue_href\s*\|\|\s*\(row\.provider\s*&&\s*row\.venue_key\s*\?\s*`/venues/\$\{row\.provider\}/\$\{row\.venue_key\}`\s*:\s*''\)\),",
        r"venue_href: sanitizeUrl(row.venue_href || (row.provider && row.venue_key ? `/venues/${row.provider}/${row.venue_key}` : '')),",
        content
    )

    if content != original_content:
        filepath.write_text(content, encoding="utf-8")
        return True
    return False

def main():
    docs_dir = Path("docs")
    changed = 0
    for html_file in docs_dir.rglob("*.html"):
        if process_file(html_file):
            changed += 1
    print(f"Patched {changed} files out of {len(list(docs_dir.rglob('*.html')))} total HTML files.")

if __name__ == '__main__':
    main()
