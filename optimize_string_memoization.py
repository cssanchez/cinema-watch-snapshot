#!/usr/bin/env python3
import re
from pathlib import Path

DOCS_ROOT = Path(__file__).parent / 'docs'

RE_NORMALIZE_SOURCE = re.compile(
    r"function normalizeSource\(value\)\s*\{\s*return String\(value \?\? ''\)\.replace\(/\\s\+/g, ' '\)\.trim\(\);\s*\}",
    re.MULTILINE
)
RE_NORMALIZE_SOURCE_REPLACEMENT = """const _normalizeSourceCache = new Map();
      function normalizeSource(value) {
        const strValue = String(value ?? '');
        if (_normalizeSourceCache.has(strValue)) return _normalizeSourceCache.get(strValue);
        const result = strValue.replace(/\\\\s+/g, ' ').trim();
        if (_normalizeSourceCache.size > 2000) _normalizeSourceCache.clear();
        _normalizeSourceCache.set(strValue, result);
        return result;
      }"""

RE_FOLD_TEXT = re.compile(
    r"function foldText\(value\)\s*\{\s*return String\(value \?\? ''\)\s*\.normalize\('NFD'\)\s*\.replace\(/\[\\u0300-\\u036f\]/g, ''\)\s*\.toLowerCase\(\)\s*\.trim\(\);\s*\}",
    re.MULTILINE
)
RE_FOLD_TEXT_REPLACEMENT = """const _foldTextCache = new Map();
      function foldText(value) {
        const strValue = String(value ?? '');
        if (_foldTextCache.has(strValue)) return _foldTextCache.get(strValue);
        const result = strValue
          .normalize('NFD')
          .replace(/[\\\\u0300-\\\\u036f]/g, '')
          .toLowerCase()
          .trim();
        if (_foldTextCache.size > 2000) _foldTextCache.clear();
        _foldTextCache.set(strValue, result);
        return result;
      }"""

RE_CANONICAL_LANGUAGE = re.compile(
    r"function canonicalLanguage\(value\)\s*\{\s*const text = foldText\(value\);\s*if \(\!text\) return '';\s*if \(text\.includes\('subti'\)\) return 'subtitulado';\s*if \(\['espanol', 'español', 'castellano', 'doblada'\]\.includes\(text\)\) return 'espanol';\s*return text;\s*\}",
    re.MULTILINE
)
RE_CANONICAL_LANGUAGE_REPLACEMENT = """const _canonicalLanguageCache = new Map();
      function canonicalLanguage(value) {
        const strValue = String(value ?? '');
        if (_canonicalLanguageCache.has(strValue)) return _canonicalLanguageCache.get(strValue);
        const text = foldText(strValue);
        let result = text;
        if (!text) {
          result = '';
        } else if (text.includes('subti')) {
          result = 'subtitulado';
        } else if (['espanol', 'español', 'castellano', 'doblada'].includes(text)) {
          result = 'espanol';
        }
        if (_canonicalLanguageCache.size > 2000) _canonicalLanguageCache.clear();
        _canonicalLanguageCache.set(strValue, result);
        return result;
      }"""

RE_CANONICAL_FORMAT = re.compile(
    r"function canonicalFormat\(value\)\s*\{\s*return foldText\(value\)\.replace\(/\\s\+/g, ''\);\s*\}",
    re.MULTILINE
)
RE_CANONICAL_FORMAT_REPLACEMENT = """const _canonicalFormatCache = new Map();
      function canonicalFormat(value) {
        const strValue = String(value ?? '');
        if (_canonicalFormatCache.has(strValue)) return _canonicalFormatCache.get(strValue);
        const result = foldText(strValue).replace(/\\\\s+/g, '');
        if (_canonicalFormatCache.size > 2000) _canonicalFormatCache.clear();
        _canonicalFormatCache.set(strValue, result);
        return result;
      }"""

RE_TRANSLATE_SOURCE = re.compile(
    r"function translateSource\(value, language = currentLanguage\)\s*\{\s*const key = normalizeSource\(value\);\s*if \(language === 'en'\) \{\s*return key;\s*\}\s*return sourceTranslations\[language\]\?\.\[key\] \|\| key;\s*\}",
    re.MULTILINE
)
RE_TRANSLATE_SOURCE_REPLACEMENT = """const _translateSourceCache = new Map();
      function translateSource(value, language = currentLanguage) {
        const cacheKey = String(value ?? '') + '|' + language;
        if (_translateSourceCache.has(cacheKey)) return _translateSourceCache.get(cacheKey);
        const key = normalizeSource(value);
        let result = key;
        if (language !== 'en') {
          result = sourceTranslations[language]?.[key] || key;
        }
        if (_translateSourceCache.size > 2000) _translateSourceCache.clear();
        _translateSourceCache.set(cacheKey, result);
        return result;
      }"""

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    content = RE_NORMALIZE_SOURCE.sub(lambda m: RE_NORMALIZE_SOURCE_REPLACEMENT.replace('\\\\', '\\'), content)
    content = RE_FOLD_TEXT.sub(lambda m: RE_FOLD_TEXT_REPLACEMENT.replace('\\\\', '\\'), content)
    content = RE_CANONICAL_LANGUAGE.sub(lambda m: RE_CANONICAL_LANGUAGE_REPLACEMENT.replace('\\\\', '\\'), content)
    content = RE_CANONICAL_FORMAT.sub(lambda m: RE_CANONICAL_FORMAT_REPLACEMENT.replace('\\\\', '\\'), content)
    content = RE_TRANSLATE_SOURCE.sub(lambda m: RE_TRANSLATE_SOURCE_REPLACEMENT.replace('\\\\', '\\'), content)

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
