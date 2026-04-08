#!/usr/bin/env python3
import re
from pathlib import Path

DOCS_ROOT = Path(__file__).parent / 'docs'

# Define regex patterns globally, precompiled to prevent recompiling overhead in loops
RE_NORMALIZE_SOURCE = re.compile(
    r"function normalizeSource\(value\)\s*\{\s*return String\(value \?\? ''\)\.replace\(/\\s\+/g, ' '\)\.trim\(\);\s*\}",
    re.MULTILINE
)
RE_NORMALIZE_SOURCE_REPLACEMENT = """const _normalizeSourceCache = new Map();
      function normalizeSource(value) {
        const strValue = String(value ?? '');
        if (_normalizeSourceCache.has(strValue)) return _normalizeSourceCache.get(strValue);
        const result = strValue.replace(/\\\\s+/g, ' ').trim();
        _normalizeSourceCache.set(strValue, result);
        return result;
      }"""

RE_CANONICAL_LANGUAGE = re.compile(
    r"function canonicalLanguage\(language\)\s*\{\s*return normalizeSource\(language\)\.toLowerCase\(\);\s*\}",
    re.MULTILINE
)
RE_CANONICAL_LANGUAGE_REPLACEMENT = """const _canonicalLanguageCache = new Map();
      function canonicalLanguage(language) {
        const strLanguage = String(language ?? '');
        if (_canonicalLanguageCache.has(strLanguage)) return _canonicalLanguageCache.get(strLanguage);
        const result = normalizeSource(strLanguage).toLowerCase();
        _canonicalLanguageCache.set(strLanguage, result);
        return result;
      }"""

RE_CANONICAL_FORMAT = re.compile(
    r"function canonicalFormat\(format\)\s*\{\s*const normalized = normalizeSource\(format\)\.toLowerCase\(\);\s*return\s*normalized === '2d' \|\| normalized === '3d'\s*\? normalized\s*: '2d';\s*\}",
    re.MULTILINE
)
RE_CANONICAL_FORMAT_REPLACEMENT = """const _canonicalFormatCache = new Map();
      function canonicalFormat(format) {
        const strFormat = String(format ?? '');
        if (_canonicalFormatCache.has(strFormat)) return _canonicalFormatCache.get(strFormat);
        const normalized = normalizeSource(strFormat).toLowerCase();
        const result = normalized === '2d' || normalized === '3d' ? normalized : '2d';
        _canonicalFormatCache.set(strFormat, result);
        return result;
      }"""

RE_FOLD_TEXT = re.compile(
    r"function foldText\(text\)\s*\{\s*return normalizeSource\(text\)\s*\.toLowerCase\(\)\s*\.normalize\('NFD'\)\s*\.replace\(/\[\\u0300-\\u036f\]/g, ''\);\s*\}",
    re.MULTILINE
)
RE_FOLD_TEXT_REPLACEMENT = """const _foldTextCache = new Map();
      function foldText(text) {
        const strText = String(text ?? '');
        if (_foldTextCache.has(strText)) return _foldTextCache.get(strText);
        const result = normalizeSource(strText)
          .toLowerCase()
          .normalize('NFD')
          .replace(/[\\\\u0300-\\\\u036f]/g, '');
        _foldTextCache.set(strText, result);
        return result;
      }"""

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Lambda replacement is used to avoid issues with escaped backslashes in sub's replacement string processing
    content = RE_NORMALIZE_SOURCE.sub(lambda m: RE_NORMALIZE_SOURCE_REPLACEMENT.replace('\\\\', '\\'), content)
    content = RE_CANONICAL_LANGUAGE.sub(lambda m: RE_CANONICAL_LANGUAGE_REPLACEMENT, content)
    content = RE_CANONICAL_FORMAT.sub(lambda m: RE_CANONICAL_FORMAT_REPLACEMENT, content)
    content = RE_FOLD_TEXT.sub(lambda m: RE_FOLD_TEXT_REPLACEMENT.replace('\\\\', '\\'), content)

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
