import os
import re

def create_sanitize_url_function():
    return (
        "const _sanitizeUrlCache = new Map();\n"
        "      function sanitizeUrl(url) {\n"
        "        const strUrl = String(url ?? '').trim();\n"
        "        if (_sanitizeUrlCache.has(strUrl)) return _sanitizeUrlCache.get(strUrl);\n"
        "        let result = strUrl;\n"
        "        const lowerUrl = strUrl.toLowerCase();\n"
        "        if (lowerUrl.startsWith('javascript:') || \n"
        "            lowerUrl.startsWith('data:') || \n"
        "            lowerUrl.startsWith('vbscript:')) {\n"
        "          result = '#';\n"
        "        }\n"
        "        if (_sanitizeUrlCache.size > 2000) _sanitizeUrlCache.clear();\n"
        "        _sanitizeUrlCache.set(strUrl, result);\n"
        "        return result;\n"
        "      }\n"
        "\n"
        "const _escapeHtmlCache ="
    )

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Avoid processing if already processed
    if "function sanitizeUrl" in content:
        return False

    modified = False

    # 1. Update usages: escapeHtml(item.movie_href) -> escapeHtml(sanitizeUrl(item.movie_href))
    # Do this first to avoid self-mutating the newly injected code if it contained the matched strings
    if 'escapeHtml(item.movie_href)' in content:
        content = content.replace(
            'escapeHtml(item.movie_href)',
            'escapeHtml(sanitizeUrl(item.movie_href))'
        )
        modified = True

    if 'escapeHtml(item.venue_href)' in content:
        content = content.replace(
            'escapeHtml(item.venue_href)',
            'escapeHtml(sanitizeUrl(item.venue_href))'
        )
        modified = True

    # 2. Inject the sanitizeUrl function before escapeHtml function
    if "const _escapeHtmlCache =" in content:
        content = content.replace(
            "const _escapeHtmlCache =",
            create_sanitize_url_function()
        )
        modified = True

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    docs_dir = "docs"
    count = 0
    for root, _, files in os.walk(docs_dir):
        for file in files:
            if file.endswith(".html"):
                filepath = os.path.join(root, file)
                if process_file(filepath):
                    count += 1

    print(f"Patched {count} files")

if __name__ == "__main__":
    main()
